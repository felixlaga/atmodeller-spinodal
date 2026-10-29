# Delayed hydrogen exsolution: what the source data allow

**Answer:** the published 2026 fit predicts a 414 K delay between equilibrium separation and instability for a 3 wt% hydrogen parcel at 2 GPa. **Refits of the same source data give median delays of 42 to 220 K.** The delay cannot be fixed from coexistence data. A direct curvature measurement could fix it to about 25 K.

The full draft, in the layout of the bachelor thesis, is [paper/main.pdf](paper/main.pdf). It has 28 pages, 9 figures and 6 tables. Most numbers in its text are generated from `outputs/` by `paper/make_numbers.py`, and an independent fact-check compared the rest with the outputs.

## The question

A homogeneous H2–MgSiO3 parcel that cools enters the miscibility gap at the **binodal**. It becomes unstable only at the **spinodal**. In between it is metastable: separation needs nucleation. If nucleation is suppressed, hydrogen release is delayed until the spinodal.

The study bounds that delay, and asks how well the existing simulations constrain it.

## Results

| Model, 3 wt% H at 2 GPa | Binodal (K) | Spinodal (K) | Delay (K), 68% range | H withheld at spinodal |
|---|---:|---:|---:|---:|
| Published 2026 fit | 3356 | 2942 | 414 | 65.5% |
| Refit M1, all data | 3194 | 3104 | 90 (68–115) | 48% |
| Refit M2, independent H, S, V | 3201 | 3162 | 42 (24–68) | 41% |
| Refit M4, most flexible | 3194 | 3101 | 144 (92–248) | 47% |
| Historical 2025 fit | 3962 | 3908 | 53 | 39.0% |

Binodal and spinodal of the refits are best-fit values. Delay and withheld hydrogen are posterior medians. The 95% range of M4 reaches 479 K, so the most flexible class does not exclude the published value. The [recalibration table](paper/tables/recalibration.tex) lists all nine refits.

### How the audit mismatch was resolved

The earlier audit found that the published fit matches only one of four two-phase compositions. That mismatch is in the source, not in Atmodeller:

- **Our implementation reproduces the published Figure 2a curves** to 2.3 K RMS (largest deviation 15 K). An independent solver agrees with Atmodeller to 10⁻⁶ K, except within 0.02 of the critical composition (0.11 K).
- **The source table and figure disagree** for the two runs closest to the critical curve, by up to 0.07 in composition. For the two wide-gap runs they agree to 0.0006.
- **The published fit also misses its own excess volumes**: −1.94 cm³/mol predicted against −1.00 ± 0.17 simulated at x = 0.588. The fitted pressure scale follows the critical curve instead.

The source data disagree with each other. Without the homogeneous data, the M1 refit returns to the published asymmetry (B/A ≈ 6) but with a larger excess entropy, and gives 132 K. With them, M1 is nearly symmetric (B/A ≈ 1.4–1.5), and the delay is 65 to 92 K. Wider errors (σx = 0.15) on the near-critical compositions give B/A = 2.4 and 220 K. The delay depends on the asymmetry, the excess entropy and the interaction strength together.

### Why equilibrium data cannot settle it

A perturbation that leaves every equilibrium observable unchanged still moves the spinodal by 14 to 250 K. So any spinodal inferred from coexistence data is a property of the chosen model form.

### What would settle it

- One more homogeneous simulation of excess H, S and V helps little: it lowers the spinodal uncertainty from 83 to 75 K.
- **A 10% measurement of the composition curvature** ∂²g/∂x² at 3 wt%, 2 GPa and 3200 K lowers it to 25 K. The concentration structure factor S_cc(0) = RT/(∂²g/∂x²) gives this curvature without a free-energy model.

## Scope

These are thermodynamic limits for a closed binary parcel. The study does not compute nucleation rates, planetary radii or spectra. The published fit stays the baseline model of Atmodeller. The refits are uncertainty estimates, not replacements: none fits all source data within the quoted errors.

All post-audit analyses are listed in the [protocol amendment](PROTOCOL_AMENDMENT.md). The source data of Gilmore & Stixrude (2026) are used under CC-BY-4.0 and stored unmodified in `sources/`.

## Reproduce

From the repository root:

```sh
uv sync --locked --all-extras --dev
PYTHONPATH=. uv run python research/spinodal_onset/run_study.py
PYTHONPATH=. uv run python research/spinodal_onset/identifiability.py
PYTHONPATH=. uv run python research/spinodal_onset/digitize_source_figure.py
PYTHONPATH=. uv run python research/spinodal_onset/calibration.py   # about 40 min with 8 worker processes
PYTHONPATH=. uv run python research/spinodal_onset/design.py
PYTHONPATH=. uv run python research/spinodal_onset/make_paper_figures.py
PYTHONPATH=. uv run python research/spinodal_onset/paper/make_numbers.py
cd research/spinodal_onset/paper && tectonic -X compile main.tex
```

`tectonic` fetches the Palatino fonts the thesis layout needs. With a full TeX Live, `latexmk -pdf main.tex` works too.

Check the delivered artifacts with:

```sh
PYTHONPATH=. uv run python research/spinodal_onset/verify_artifacts.py
```

| Files | Purpose |
|---|---|
| `paper/` | Draft: LaTeX sources, thesis style, generated numbers and tables, figures, PDF |
| `mixing_models.py` | Independent scalar solver for T-linear Redlich–Kister models |
| `digitize_source_figure.py`, `outputs/source_figure_digitized.json` | Published Figure 2a against our implementation |
| `calibration.py`, `outputs/calibration_*` | Nine recalibrations, posterior samples and diagnostics |
| `design.py`, `outputs/design_*` | Which new simulation constrains the spinodal |
| `run_study.py`, `identifiability.py` | Onset grid, cooling paths, audit and the identifiability test |
| `sources/` | ED Tables 1–2 and Figure 2 of the source paper, with hashes |
| `explorer.html` | Interactive cooling paths of the published model |

## Primary references (checked 29 October 2026)

- [Gilmore & Stixrude 2026, Nature 650, 60–64](https://doi.org/10.1038/s41586-025-09970-4), equations 1 and 8–19; [source data](https://doi.org/10.5281/zenodo.17716049).
- [Rogers, Young & Schlichting 2025, MNRAS 544, 3496](https://doi.org/10.1093/mnras/staf1940); [Rogers & Schlichting 2026](https://arxiv.org/abs/2606.30644v2).
- [Young et al. 2025, PSJ 6, 251](https://doi.org/10.3847/PSJ/ae1012); [Young & Werlen 2026](https://arxiv.org/abs/2604.28135v2); [Tejada Arevalo et al. 2026](https://arxiv.org/abs/2601.00059v2).
- [Hakim et al. 2026, MNRAS 546, stag133](https://doi.org/10.1093/mnras/stag133); [Bower et al. 2025, ApJ 995, 59](https://doi.org/10.3847/1538-4357/ae1479).
