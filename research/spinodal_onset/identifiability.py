# SPDX-License-Identifier: Apache-2.0
"""Construct a binodal-preserving counterexample to inferred spinodal uniqueness.

This is an identifiability experiment, not a recommended material model.
The added nonnegative C2 bump is zero with zero first/second derivatives
at both binodal endpoints, and zero everywhere outside the gap. Its amplitude
is tied to the baseline barrier at the gap midpoint, vanishing at criticality.
It preserves all equilibrium free energies/compositions and all homogeneous
states outside the gap, while changing the interior homogeneous curvature.
"""

import hashlib
import json
from pathlib import Path

import equinox as eqx
import jax
import jax.numpy as jnp
import numpy as np
import pandas as pd
from scipy.optimize import brentq

from atmodeller import SubregularSolution
from research.spinodal_onset.run_study import OUT, onset_zero_pressure, to_x

MODEL = SubregularSolution(75000, 424000, temperature_scale=4400, pressure_scale=-350000)


@eqx.filter_jit
def shape(temperature, pressure, z):
    """Return fit-basis homogeneous energy, curvature and bump coefficients."""
    c = MODEL.coexistence(temperature, pressure)
    a, b = c.lower, c.upper
    width = jnp.where(c.has_gap, b - a, 1.0)
    mid = (a + b) / 2
    barrier = MODEL.gibbs_energy(temperature, pressure, mid) - MODEL.equilibrium_gibbs_energy(
        temperature, pressure, mid
    )
    u = jnp.clip((z - a) / width, 0.0, 1.0)
    active = c.contains(z)
    bump = jnp.where(active, barrier * 64 * u**3 * (1 - u) ** 3, 0.0)
    second = 384 * u * (1 - u) * (1 - 5 * u + 5 * u**2) / width**2
    curvature_bump = jnp.where(active, barrier * second, 0.0)
    return (
        MODEL.gibbs_energy(temperature, pressure, z),
        MODEL.curvature(temperature, pressure, z),
        bump,
        curvature_bump,
        barrier,
    )


def main():
    native = SubregularSolution.hydrogen_silicate_gilmore26()
    rows = []
    for weight in (0.01, 0.02, 0.03, 0.05):
        x = float(to_x(weight))
        z = float(native.mixing_composition(x))
        tb = float(onset_zero_pressure(native, jnp.array([x]))[0]) * (1 - 2 / 35)
        temperatures = np.linspace(tb - 1e-5, 2000, 1001)
        _, curv, _, extra, _ = shape(temperatures, 20000.0, z)
        for amplitude in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0):
            values = np.asarray(curv + amplitude * extra)
            crossings = np.flatnonzero((values[:-1] >= 0) & (values[1:] < 0))
            ts, h = np.nan, np.nan
            if len(crossings):
                i = crossings[0]

                def objective(t):
                    _, base, _, delta, _ = shape(t, 20000.0, z)
                    return float(base + amplitude * delta)

                ts = brentq(objective, temperatures[i + 1], temperatures[i], xtol=1e-7)
                c = native.coexistence(ts, 20000.0)
                h = float(c.upper_fraction(x) * c.upper / x)
            rows.append(
                dict(
                    hydrogen_wt_percent=weight * 100,
                    bump_amplitude=amplitude,
                    pressure_GPa=2.0,
                    binodal_temperature_K=tb,
                    spinodal_temperature_K=ts,
                    metastable_interval_K=tb - ts,
                    H_in_rich_phase_at_spinodal=h,
                    positive_to_negative_crossings_in_2000K_window=len(crossings),
                )
            )
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "identifiability.csv", index=False)

    # A deliberately off-binodal grid checks global supporting-tangent margins.
    # Positivity of the added term proves preservation everywhere, not only here.
    margins, endpoint_changes = [], []
    plot_rows = []
    for t in (2500.0, 3000.0, 3400.0, 4000.0):
        z = np.linspace(0, 1, 1001)
        g, curvature, bump, _, _ = shape(t, 20000.0, z)
        equilibrium = np.asarray(MODEL.equilibrium_gibbs_energy(t, 20000.0, z))
        assert np.min(bump) >= 0
        for amplitude in (0.0, 1.0, 4.0, 8.0):
            margins.append(float(np.min(g + amplitude * bump - equilibrium)))
            for i, zi in enumerate(z):
                plot_rows.append(
                    dict(
                        temperature_K=t,
                        fit_z=zi,
                        bump_amplitude=amplitude,
                        energy_above_equilibrium_J_per_fit_mol=float(
                            g[i] + amplitude * bump[i] - equilibrium[i]
                        ),
                    )
                )
        c = MODEL.coexistence(t, 20000.0)
        if c.has_gap:
            _, _, endpoint_bump, endpoint_second, _ = shape(
                t, 20000.0, jnp.array([c.lower, c.upper])
            )
            endpoint_changes.extend(np.asarray(endpoint_bump).tolist())
            endpoint_changes.extend(np.asarray(endpoint_second).tolist())
    assert min(margins) > -1e-7
    assert max(np.abs(endpoint_changes)) < 1e-8
    assert np.asarray(shape(4000.0, 50000.0, np.linspace(0, 1, 51))[2] == 0).all()
    derivative_errors = []
    for t, z in ((2500.0, 0.4), (3000.0, 0.6), (3400.0, 0.7), (4000.0, 0.5)):

        def perturbed_energy(composition):
            energy, _, bump, _, _ = shape(t, 20000.0, composition)
            return energy + 4 * bump

        autodiff = float(jax.grad(jax.grad(perturbed_energy))(z))
        _, base_second, _, bump_second, _ = shape(t, 20000.0, z)
        analytic = float(base_second + 4 * bump_second)
        derivative_errors.append(abs(autodiff - analytic) / max(abs(analytic), 1.0))
    assert max(derivative_errors) < 1e-10
    baseline = df.loc[(df.hydrogen_wt_percent == 3) & (df.bump_amplitude == 0)].iloc[0]
    np.testing.assert_allclose(
        baseline.spinodal_temperature_K,
        native.spinodal_temperature(20000.0, to_x(0.03)),
        atol=1e-6,
    )
    pd.DataFrame(plot_rows).to_csv(OUT / "identifiability_energy.csv", index=False)
    Path(OUT / "identifiability_checks.json").write_text(
        json.dumps(
            dict(
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                minimum_sampled_support_margin_J_per_fit_mol=min(margins),
                maximum_endpoint_energy_or_curvature_change=max(np.abs(endpoint_changes)),
                homogeneous_EDTable2_states_unchanged=True,
                maximum_relative_curvature_error_against_autodiff=max(derivative_errors),
                scope="Constructed thermodynamic counterexample; amplitudes are not calibrated material uncertainties.",
            ),
            indent=2,
        )
        + "\n"
    )
    print(df.loc[df.hydrogen_wt_percent == 3].to_string(index=False))


if __name__ == "__main__":
    main()
