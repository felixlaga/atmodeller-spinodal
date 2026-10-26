# How insightful are these results?

The study is useful as a controlled feasibility experiment and as a guide to the next research question. It does not yet establish an observable planetary signature of spinodal decomposition. The current evidence supports a numerically tested equilibrium implementation, with atmospheric effects conditional on an imposed transfer prescription.

## The strongest insights

**Equilibrium separation and local spinodal instability need different physical explanations.** In the adopted binary model, the 1 wt% H₂ case can separate at equilibrium while retaining positive homogeneous curvature. The 3 wt% case at 3500 K and 1 GPa is locally unstable, and about 83% of its hydrogen enters the hydrogen-rich phase at equilibrium. These provide useful contrasting cases for studying nucleation, growth and transport. Merely selecting the API's `spinodal` mode does not calculate any of those rates.

The approximately 1.006 wt% lower bound for possible negative curvature is a property of this free-energy parameterization when its excess-energy factor is nonnegative. It refers to the composition of the modeled H₂–MgSiO₃ mixture. A planet with 1 wt% total hydrogen can have individual layers with much higher hydrogen concentrations. The bound therefore cannot rule out spinodal instability throughout such a planet, and cannot be compared directly with a whole-planet hydrogen budget without specifying its interior distribution and other components.

**A large initial composition difference can disappear while the amount of gas still changes.** In the 1 wt% source example, upper-phase-only transfer reduces hot-parcel H₂O and SiO mole fractions by factors of 24.5 and 39.1. With 10% lower-phase entrainment and condensation enabled, their mole fractions recover the reference values, but gas mass per unit original bulk remains about 52% of the reference. This makes the survival of a chemical signal a better research target than the mere existence of a demixing-induced inventory change. The mass result concerns the selected fixed-pressure parcel; a planetary envelope mass still requires structural and transport closure.

**Trace-species enhancement factors can mislead.** The example's SiH₄ enhancement changes from roughly seven million-fold in the gas-only control to 1.081-fold when condensates are permitted. The apparent enormous increase starts from an extremely small reference abundance. Absolute abundances and phase stability must accompany any ratio proposed as an observational diagnostic.

Numerical values and assumptions are given in the [full report](README.md), [summary](outputs/summary.json) and [validation record](validation.json).

## What is established already, and what might be new

The mixing free energy and hydrogen–silicate coexistence mechanism are adopted from [Rogers, Young & Schlichting, equation 7](https://arxiv.org/html/2509.13320v1#S2.SS1.SSS1). Reproducing that phase diagram is implementation validation, not a new discovery of immiscibility. [Hakim et al., section 3.3](https://arxiv.org/html/2508.19235v2#S3.SS3) already establish that condensation strongly affects silicon-bearing atmospheric gases. A claim that this general buffering mechanism is new would also be unjustified.

The potentially useful contribution is a consistent connection between phase-separated inventories, reacting atmospheric chemistry and the conditions under which material from the different phases mixes again. The current study illustrates that connection with an imposed entrainment fraction; it has not yet supplied a physical transport law or established literature-level novelty for the combined result.

## What would strengthen the thesis

1. **Close the thermodynamics of exchange.** Establish compatible endmember chemical potentials for the nonideal deep mixture and reacting gas network. The closed-binary calculation's H₂ reference term cannot be treated as a calibrated high-pressure fluid chemical potential without that work. Avoid counting the same hydrogen in both a binary fluid and an independent atmospheric reservoir.
2. **Test the physical robustness of the phase diagram.** Bound uncertainty in the adopted free energy and include major additional components as defensible data become available. Distinguish local layer composition from bulk planetary composition.
3. **Constrain transfer and timescales.** Compare separation or nucleation, mixing, settling and cooling timescales, replacing freely selected entrainment fractions with justified ranges. Assess which equilibrium endpoints can actually be reached.
4. **Carry the chemistry to observable conditions.** The current atmospheric calculations are hot, at 2300–3000 K. They do not reproduce Hakim's 920 K atmospheric calculation, its complete elemental network, or an observable spectrum. Appropriate cold condensates, quenching and any rainout prescription are needed before connecting the result to measurements.

The most promising question is: **under which physically plausible conditions does hydrogen–silicate separation leave a chemical signal after mixing and condensation?** A robust finding that the chemical signature is erased, while interior hydrogen storage or envelope evolution changes, could also be scientifically valuable. Thousands of successful equilibrium solves establish numerical consistency of the chosen equations; they do not by themselves establish calibration, novelty or observability.
