# SPDX-License-Identifier: Apache-2.0
"""Build the manuscript-style research report from computed data and figures.

Reproduce with: uv run --with reportlab python research/spinodal_onset/build_report.py
ReportLab is an artifact dependency, not an Atmodeller runtime dependency.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

HERE = Path(__file__).resolve().parent
DEST = HERE / "output/pdf/delayed_hydrogen_exsolution.pdf"
INK = colors.HexColor("#203b49")
TEAL = colors.HexColor("#166b79")
MUTED = colors.HexColor("#546974")
PALE = colors.HexColor("#edf4f4")
WIDTH = 487


def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    key = json.loads((HERE / "outputs/key_results.json").read_text())
    summary = json.loads((HERE / "outputs/summary.json").read_text())
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleLocal",
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=29,
            textColor=INK,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Deck",
            fontName="Helvetica",
            fontSize=12,
            leading=17,
            textColor=MUTED,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=TEAL,
            spaceBefore=5,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subsection",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyLocal",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=INK,
            spaceAfter=9,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CaptionLocal",
            fontName="Helvetica",
            fontSize=8.6,
            leading=12,
            textColor=MUTED,
            spaceBefore=4,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallLocal",
            fontName="Helvetica",
            fontSize=8.7,
            leading=12,
            textColor=INK,
            spaceAfter=7,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Equation",
            fontName="Courier",
            fontSize=9.2,
            leading=14,
            textColor=TEAL,
            backColor=PALE,
            borderPadding=8,
            spaceBefore=5,
            spaceAfter=13,
        )
    )
    story = []

    def p(text, style="BodyLocal"):
        story.append(Paragraph(text, styles[style]))

    def title(text):
        p(text, "Section")

    def sub(text):
        p(text, "Subsection")

    def figure(name, caption, width=WIDTH):
        path = HERE / "figures" / (name + ".png")
        w, h = ImageReader(str(path)).getSize()
        story.append(
            KeepTogether(
                [
                    Image(str(path), width=width, height=width * h / w),
                    Paragraph(caption, styles["CaptionLocal"]),
                ]
            )
        )

    def table(rows, widths):
        formatted = [
            [Paragraph(escape(str(c)), styles["SmallLocal"]) for c in row] for row in rows
        ]
        t = Table(formatted, colWidths=widths, hAlign="LEFT", repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), PALE),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.6, TEAL),
                    ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#d7e1e4")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.extend([t, Spacer(1, 9)])

    def page():
        story.append(PageBreak())

    p("ATMODELLER / RESEARCH DRAFT / 29 OCTOBER 2026", "SmallLocal")
    story.append(HRFlowable(width="100%", color=TEAL, thickness=1.4, spaceAfter=18))
    p("When does hydrogen<br/>actually separate?", "TitleLocal")
    p(
        "Composition-consistent bounds on delayed hydrogen-silicate exsolution, and what equilibrium data cannot determine",
        "Deck",
    )
    p(
        "<b>Status:</b> completed numerical study and paper candidate. Not a submission-ready physical prediction. No authorship or venue assignment is implied.",
        "SmallLocal",
    )
    sub("Abstract")
    p(
        "Hydrogen exsolution may supply evolving sub-Neptune envelopes, but an equilibrium miscibility boundary does not specify the onset of separation in an initially homogeneous parcel. We extend Atmodeller with the final 2026 hydrogen-silicate free-energy fit, preserving the published composition basis in extensive energies, chemical potentials and phase inventories. We compare instantaneous equilibrium with an imposed limit that suppresses nucleation until local instability. For a closed parcel at 2 GPa and 3 wt% hydrogen, the model gives binodal and spinodal temperatures of 3356 and 2942 K. At the latter temperature, equilibrium would place 65.5% of the parcel hydrogen in a distinct H-rich phase. This inventory bound is insensitive to several fit parameters because of the model's separable structure. However, reproduction of the tabulated simulations reveals material endpoint and volume discrepancies. A constructed free-energy perturbation also preserves every binodal while changing the spinodal. The result motivates direct constraints on metastable curvature and kinetics before equilibrium exsolution is converted into atmospheric evolution."
    )
    table(
        [
            ["At 2 GPa, 3 wt% local H", "Result", "Meaning"],
            [
                "Binodal-to-spinodal interval",
                "414 K",
                "Cooling interval available for metastability",
            ],
            [
                "Equilibrium H in rich phase at spinodal",
                "65.5%",
                "Inventory bound if nucleation is entirely suppressed",
            ],
            [
                "Full package tests",
                "288 passed",
                "Numerical/software validation, not material calibration",
            ],
        ],
        [220, 67, 200],
    )
    p(
        "The calculation conserves hydrogen. A delayed parcel still contains all its hydrogen, mixed with silicate. Neither limiting curve gives the mass or composition of an observable atmosphere.",
        "CaptionLocal",
    )

    page()
    title("1. Question, prior work and scope")
    p(
        "The focused question is whether the equilibrium assumption hides a material interval of delayed hydrogen separation during isobaric cooling. The unit of analysis is one closed, stoichiometric H2-MgSiO3 parcel. Local hydrogen mass fractions are not whole-planet envelope fractions."
    )
    table(
        [
            ["Literature", "What is already established", "Role in this study"],
            [
                "Gilmore & Stixrude 2026 [1,2]",
                "First-principles coexistence and homogeneous properties; asymmetric solution fit",
                "Final coefficients, composition convention and source-data audit",
            ],
            [
                "Rogers et al. 2025 [3]",
                "Hydrogen storage and exsolution using a historical fit",
                "Reproducible historical control",
            ],
            [
                "Rogers & Schlichting 2026 v2 [4]",
                "Evolving envelopes supplied by interior hydrogen",
                "Motivation to test the instantaneous-equilibrium assumption",
            ],
            [
                "Tejada Arevalo et al. 2026 v2 [5]",
                "Coupled thermal/compositional evolution and silicate rain",
                "Rainout and evolutionary memory are existing work",
            ],
            [
                "Young et al. 2025; Young & Werlen 2026 v2 [6,7]",
                "Binary spinodals and multicomponent miscibility",
                "A spinodal diagram alone is not a new contribution",
            ],
            [
                "Hakim et al. 2026 [8]",
                "Atmospheric chemistry and condensation",
                "Downstream chemistry requires an additional physical coupling",
            ],
        ],
        [137, 186, 164],
    )
    sub("Two limiting histories")
    p(
        "<b>Equilibrium limit:</b> use the common tangent throughout the miscibility gap, including its metastable portion. <b>Delayed limit:</b> maintain a homogeneous parcel until its curvature first becomes negative, then impose immediate equilibration. The delayed limit is an extreme sensitivity experiment: heterogeneous nucleation on an existing interface can erase the delay, and finite growth can delay separation further. No time-dependent kinetic law is solved."
    )
    sub("Design and novelty boundary")
    p(
        "The main grid contains 20,664 onset rows across three parameterizations, 10,827 cooling states and 375 deterministic parameter-stress cases. Pressures span 2-10 GPa and local H fractions 0.1-20 wt%. Cooling histories use 2000-4000 K. Regions below 2500 K extrapolate below the lowest tabulated two-phase simulation temperature; there is no crystallization model. The candidate contribution is the audited exsolution bound plus an explicit identifiability test, not a claim to discover miscibility or spinodal decomposition."
    )
    p(
        "Literature was checked to 29 October 2026, including the October 14 revision of [4]. Searches identified close prior work but do not establish exhaustive novelty.",
        "CaptionLocal",
    )

    page()
    title("2. Thermodynamics and implementation")
    p(
        "Let y be the native H2 formula-unit mole fraction and z the published oxide-basis fraction. One MgSiO3 formula unit contributes two oxide units. Converting only composition would give inconsistent extensive energies and chemical potentials."
    )
    p(
        "z = y/(2-y);  y = 2z/(1+z)<br/>G = (2 n_sil + n_H2) g_fit(z)<br/>g_native(y) = (2-y) g_fit(z)<br/>mu_sil,native = 2 mu_0,fit;  mu_H2,native = mu_1,fit",
        "Equation",
    )
    p(
        "The final fit is g<sub>fit</sub> = RT[(1-z)ln(1-z)+z ln z] + F h(z), with h(z)=z(1-z)[A(1-z)+Bz], F=1-T/C+P/D, A=75 kJ/mol, B=424 kJ/mol, C=4400 K and D=-35 GPa [1]. All public API compositions and inventories remain in native (MgSiO3,H2) units. Pressure passed to Atmodeller is in bar."
    )
    sub("Analytical spinodal and an invariance result")
    p(
        "h''(z) = 2B - 4A + 6(A-B)z<br/>T_s(P,z) = -h''(z)(1+P/D) / [R/(z(1-z))-h''(z)/C]",
        "Equation",
    )
    p(
        "A valid positive root locates a curvature zero, not a nucleation rate. In the studied regime it marks loss of stability on cooling. At fixed z, the spinodal fixes F/(RT)=-1/[z(1-z)h''(z)]. Hence the equilibrium endpoints at this temperature depend on the shape of h, not on P or C. All boundary temperatures scale as (1+P/D). The hydrogen inventory at the spinodal is therefore pressure-independent within this model. Its numerical invariance is checked on the full resolved grid."
    )
    sub("Conservation and software interface")
    p(
        "For native endpoints y<sub>a</sub>, y<sub>b</sub>, the upper-phase mole fraction is f=(y-y<sub>a</sub>)/(y<sub>b</sub>-y<sub>a</sub>). The fraction of total hydrogen in that phase is f y<sub>b</sub>/y. This is a hydrogen inventory fraction, not a phase mass fraction. The implemented model uses the existing Equinox/JAX mixing and activity interfaces; the old constructor remains unchanged."
    )
    p(
        'mixing = SubregularSolution.hydrogen_silicate_gilmore26()<br/>T_s = mixing.spinodal_temperature(pressure_bar, y)<br/>model = EquilibriumModel.from_species(<br/>    ..., mixing_models={"silicate_melt": mixing},<br/>    phase_equilibrium="spinodal")',
        "Equation",
    )
    p(
        'The API name "spinodal" still selects common-tangent equilibrium over the whole binodal. The imposed delayed history is implemented in the study script, not silently added to this equilibrium solver. Tests cover extensive derivatives, Gibbs-Duhem, trace activities, JAX derivatives, common-tangent support, independent roots and legacy regression.',
        "SmallLocal",
    )

    page()
    title("3. Quantitative exsolution bounds")
    figure(
        "01_onset_comparison",
        "Figure 1. Final 2026 fit, historical 2025 fit and a deliberately incorrect direct-import control at 2 GPa. All plotted H mass fractions use the same native molecular masses. Missing spinodals have no positive root or lie below the 2000 K plotting window. The incorrect-basis control is not recommended for use.",
    )
    table(
        [
            [
                "3 wt% local H",
                "Binodal (K)",
                "Spinodal (K)",
                "Interval (K)",
                "H fraction at spinodal",
            ],
            ["Final 2026 / 2 GPa", "3355.9", "2942.2", "413.7", "65.5%"],
            ["Final 2026 / 5 GPa", "3050.8", "2674.7", "376.1", "65.5%"],
            ["Final 2026 / 10 GPa", "2542.4", "2228.9*", "313.4*", "65.5%*"],
            ["Historical 2025 / 2 GPa", "3961.6", "3908.4", "53.2", "39.0%"],
            ["Incorrect 2026 basis / 2 GPa", "3467.7", "3421.8", "45.9", "36.1%"],
        ],
        [149, 76, 77, 72, 113],
    )
    p(
        "* Below the lowest tabulated two-phase DFT temperature. These values are model extrapolations. The 2025 comparison is a historical implementation control; it does not allege that current evolution papers use the wrong basis or coefficients.",
        "CaptionLocal",
    )
    sub("A directly interpretable inventory discrepancy")
    p(
        f"At 3000 K, 2 GPa and 3 wt% H, instantaneous equilibrium puts {100 * key['at_3000K_2GPa_3wt']['H_equilibrium_fraction']:.1f}% of the hydrogen in the rich phase, while the delayed limit has not separated. For a 1 kg parcel this is 18.4 g of hydrogen assigned to different phase inventories, with total hydrogen fixed at 30 g. The free-energy reduction is {key['at_3000K_2GPa_3wt']['equilibrium_energy_lowering_J_per_native_mol'] / 1000:.2f} kJ per native mole. That is a Gibbs-energy difference, not a calculated heat release."
    )
    p(
        "The final fit has no positive-temperature spinodal for a 1 wt% local parcel in the positive-F regime, despite equilibrium demixing on cooling. Its formal lower spinodal-composition threshold is 1.404 wt%, versus 1.006 wt% in the historical fit and 0.707 wt% under the incorrect basis import. These asymptotic thresholds are model-dependent and need not be reached before freezing."
    )

    page()
    title("4. Cooling histories and stopping conditions")
    figure(
        "02_cooling_bounds",
        "Figure 2. Hydrogen phase inventory for a 3 wt% parcel. The shaded green interval lies between binodal and spinodal; tan shading marks temperatures below 2500 K. The dashed curve imposes an abrupt jump to equilibrium at the spinodal. It is not an integrated nucleation or growth solution.",
    )
    p(
        "At 2 and 5 GPa the nominal 3 wt% spinodals lie within the tabulated two-phase temperature range. At 10 GPa the formal spinodal is 2229 K. A parcel that freezes or ceases to follow the fluid model above this temperature cannot be assumed to reach it. Lower hydrogen contents make that issue more pronounced."
    )
    figure(
        "05_cooling_endpoint",
        "Figure 3. Remaining hydrogen-inventory difference if cooling stops at 3000, 2500 or 2000 K. The zero values after instability reflect the imposed instantaneous post-spinodal equilibration. Sharp jumps are properties of the limiting-history construction, not predictions of real planetary evolution.",
    )
    p(
        "No unique atmospheric composition follows from these curves. Transport must connect the separated inventory to a gas reservoir; water, helium and other components can alter the phase diagram; condensation changes the eventual gas composition. The earlier atmospheric-feed study in this repository already demonstrates sensitivity to transfer and entrainment. It is not repeated with a second arbitrary coupling prescription here."
    )

    page()
    title("5. Reproduction audit of published data")
    figure(
        "03_source_audit",
        "Figure 4. (A) All four two-phase pairs from Extended Data Table 1, evaluated at each reported P and T. Error bars are the quoted +/-0.05 in published z. (B) Reconstructed Table 2 excess properties compared with the thermodynamically implied fit. Standardized residuals propagate reported table errors; they omit an EOS correction and share endmember covariance, so they are not a formal independent chi-square test. Original tables: Gilmore & Stixrude, CC-BY-4.0 [1,2].",
    )
    p(
        "The final fit classifies all ten tabulated single-phase states consistently, but only one of four coexistence pairs has both endpoints within +/-0.05 at nominal pressure. Scanning 101 pressures across each quoted pressure interval still gives one of four joint matches. The largest nominal endpoint discrepancy is 0.252 in z. This is a reproduction audit of data used in developing the fit, not independent out-of-sample validation."
    )
    p(
        "For example, the 3500 K, 1.65 GPa pair is tabulated as (0.458, 0.576), while the implemented final fit gives approximately (0.595, 0.828). At 3000 K and 5.14 GPa the table gives (0.587, 0.706), compared with (0.398, 0.941). The numerical common tangents satisfy both chemical-potential equalities; changing numerical tolerances does not resolve a material-model mismatch."
    )
    sub("Independent energetic bookkeeping")
    p(
        "Table 2 properties in per-atom units are converted using n<sub>fit</sub>=N<sub>H</sub>/2+2N<sub>MgSiO3</sub>. Pure-endmember contributions are subtracted before division by n<sub>fit</sub>; ideal mixing entropy is also subtracted for excess entropy. The implied model is H<sub>mix</sub>=h(1+P/D), S<sub>ex</sub>=h/C and V<sub>ex</sub>=h/D. The volume discrepancies are especially large relative to the quoted propagated errors (up to about 9.1). Pure reference runs are at 5.00 GPa, mixtures at 5.06-5.08 GPa; that pressure offset and shared errors must be addressed before statistical fitting."
    )
    p(
        "These discrepancies do not establish that the published simulations are incorrect. They show that this approximate analytic fit does not reproduce all tabulated quantities to their stated error bars under the explicit conventions above. No point was discarded and no parameter was silently refitted.",
        "CaptionLocal",
    )

    page()
    title("6. Robustness is conditional on model structure")
    figure(
        "04_sensitivity_and_identifiability",
        "Figure 5. (A) Deterministic +/-10% stress tests of A, B, C and |D| at 2 GPa, 3 wt% H. These are not confidence intervals. (B) A different structural test: a nonnegative interior free-energy bump preserves all equilibrium boundaries but shifts the spinodal. The 2 wt% crossings lie below 2500 K and are extrapolations; the 3 and 5 wt% examples do not.",
    )
    p(
        "For the 3 wt% case, parameter stress tests give intervals of 329-504 K and hydrogen inventory bounds of 64.4-66.3%. The narrow inventory range partly reflects the separable functional form: changing C, D or pressure leaves that fraction exactly invariant. It should not be read as empirical precision."
    )
    sub("A constructive identifiability test")
    p(
        "Let a(T,P) and b(T,P) be the fit-basis binodal, u=(z-a)/(b-a), and B(T,P) the baseline free-energy height above the common tangent at the midpoint. Add the following term only inside the gap:"
    )
    p(
        "delta_g(z,T,P) = lambda B(T,P) 64 u^3(1-u)^3<br/>delta_g = 0 outside [a,b];  lambda &gt;= 0",
        "Equation",
    )
    p(
        "The term is nonnegative and its value, first derivative and second derivative vanish at both endpoints. Therefore it cannot lower any state below the original supporting tangent; every binodal and equilibrium free energy remains unchanged. It is also zero at the 4000 K homogeneous Table 2 states. But its interior second derivative changes local stability. At 3 wt%, lambda=8 shifts onset from 2942 to 2978 K without changing equilibrium data; at 5 wt%, it shifts 3365 to 3351 K. These amplitudes are constructed counterexamples, not a calibrated uncertainty distribution or a proposed replacement material model."
    )
    p(
        "The missing information is therefore not merely a tighter fit to binodal points. A binodal constrains the convex envelope; a spinodal requires the curvature of the homogeneous free energy above that envelope. Metastable homogeneous simulations or appropriate fluctuation/response measurements would test that curvature directly."
    )

    page()
    title("7. Publication assessment and decisive next work")
    p(
        "<b>Assessment:</b> the inventory effect is large enough to investigate, and the composition-basis and identifiability analysis make a defensible research direction. The current artifact is a reproducible pilot study, not yet a strong submission claiming revised atmospheric abundances or planetary evolution."
    )
    table(
        [
            ["Next test", "Concrete design", "What would change the conclusion"],
            [
                "Reconcile the source fit",
                "Check basis, endpoint extraction and pressure conventions against the complete source data; jointly fit thermodynamic derivatives with correlated errors.",
                "A reconciled fit could materially shift the 414 K interval; publish the discrepancy if it persists.",
            ],
            [
                "Constrain metastable curvature",
                "At 2 GPa, bracket 3000-3400 K and z about 0.35-0.55 with constrained homogeneous simulations; measure free-energy derivatives or composition response.",
                "Curvature inconsistent with the assumed polynomial invalidates its spinodal forecast even if the binodal fits.",
            ],
            [
                "Determine whether delay survives",
                "Obtain interfacial free energy and diffusivity/mobility; compare homogeneous and interface-assisted nucleation with an explicit cooling history.",
                "Efficient heterogeneous nucleation can remove most of the proposed delay.",
            ],
            [
                "Connect to a planet",
                "Couple calibrated source inventories to mass/energy-conserving transport, evolving structure, multicomponent chemistry and condensation.",
                "Only then test atmospheric composition, radius/age evolution or spectra against observations.",
            ],
        ],
        [115, 215, 157],
    )
    sub("Validation and reproducibility")
    p(
        f"All {summary['native_solver']['number_solves']} native EquilibriumModel checks were accepted. Maximum relative elemental error and lever-rule reconstruction error are both about 2.2e-16. The full non-performance package suite passed 288 tests, with three performance cases deselected. These establish correctness of the implemented numerical model; they do not validate the kinetic limiting assumptions or the material calibration."
    )
    p(
        "The pressure-invariance check shows an absolute H-fraction spread below 1e-9 away from criticality. One grid point 0.0213 wt% from the critical composition has a 7.3e-6 spread as the two endpoints merge and the lever rule becomes ill-conditioned. This numerical limitation is retained in the outputs and does not affect the 3 wt% case.",
        "SmallLocal",
    )
    p(
        "Study commands, original licensed tables, CSV data, editable SVG figures, the protocol, and validation logs are stored under research/spinodal_onset/. Analysis-source hashes and package versions are in outputs/provenance.json; the counterexample has its own checked script hash. A final artifact manifest verifies all delivered study files. The working branch is feat/spinodal-metastability-study."
    )
    p(
        "The post-result additions (pressure-uncertainty audit, homogeneous-property audit and constructive identifiability test) are explicitly recorded in the protocol. No authors were contacted, no new ab initio calculation was performed, and no physical nucleation timescale was inferred.",
        "CaptionLocal",
    )

    page()
    title("References and data provenance")
    refs = [
        (
            "1",
            "Gilmore & Stixrude (2026). Nature 650, 60-64. Final hydrogen-silicate phase-equilibrium paper; equations 1 and 8-11.",
            "https://doi.org/10.1038/s41586-025-09970-4",
        ),
        (
            "2",
            "Gilmore & Stixrude. Source data: Extended Data Tables 1 and 2. Zenodo record 17716049; CC-BY-4.0. Original XLSX files preserved with SHA-256 hashes.",
            "https://doi.org/10.5281/zenodo.17716049",
        ),
        (
            "3",
            "Rogers, Young & Schlichting (2025). MNRAS. Historical hydrogen-silicate parameterization, equation 7.",
            "https://doi.org/10.1093/mnras/staf1940",
        ),
        (
            "4",
            "Rogers & Schlichting (2026). arXiv:2606.30644v2, revised 14 October 2026. Current interior-exsolution/evolving-envelope study.",
            "https://arxiv.org/abs/2606.30644v2",
        ),
        (
            "5",
            "Tejada Arevalo et al. (2026). arXiv:2601.00059v2, revised 18 March 2026. Coupled thermal and compositional evolution.",
            "https://arxiv.org/abs/2601.00059v2",
        ),
        (
            "6",
            "Young et al. (2025). Planetary Science Journal 6, 251. Published binary spinodal/binodal and multicomponent miscibility work.",
            "https://doi.org/10.3847/PSJ/ae1012",
        ),
        (
            "7",
            "Young & Werlen (2026). arXiv:2604.28135v2, revised 28 June 2026. H-silicate-iron miscibility and planetary inference.",
            "https://arxiv.org/abs/2604.28135v2",
        ),
        (
            "8",
            "Hakim et al. (2026). MNRAS. Atmospheric thermochemistry including silicon-bearing species and condensation.",
            "https://doi.org/10.1093/mnras/stag133",
        ),
        (
            "9",
            "Bower et al. (2025). Astrophysical Journal 995, 59. Atmodeller reference. The present extension preserves the native phase/activity architecture.",
            "https://doi.org/10.3847/1538-4357/ae1479",
        ),
    ]
    for number, text, url in refs:
        p(
            f'<b>[{number}]</b> {escape(text)}<br/><a href="{url}" color="#166b79">{escape(url)}</a>',
            "SmallLocal",
        )
    sub("Code and data index")
    table(
        [
            ["Path within research/spinodal_onset", "Contents"],
            [
                "run_study.py / identifiability.py",
                "Numerical analysis and structural counterexample",
            ],
            ["outputs/*.csv, *.json, *.npy", "Raw computed data, solver checks and source hashes"],
            ["sources/", "Original CC-BY tables with attribution and download URLs"],
            ["figures/", "Five standalone figures in PNG and editable SVG"],
            [
                "validation/ / artifact_manifest.json",
                "Focused type/docs/lint results, full test log and file hashes",
            ],
        ],
        [259, 228],
    )
    p(
        "Repository: <a href="
        + '"https://github.com/felixlaga/atmodeller-spinodal/tree/feat/spinodal-metastability-study" color="#166b79">felixlaga/atmodeller-spinodal</a>. Direct fork of ExPlanetology/atmodeller. Earlier studies and their provenance remain archived unchanged.',
        "SmallLocal",
    )

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#d7e1e4"))
        canvas.line(54, 42, 541, 42)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(54, 29, "ATMODELLER  |  Delayed hydrogen separation  |  Research draft")
        canvas.drawRightString(541, 29, str(doc.page))
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(DEST),
        pagesize=(595, 842),
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=58,
        title="Delayed hydrogen separation: thermodynamic bounds and identifiability",
        author="Atmodeller spinodal research",
        subject="Reproducible research draft, 29 October 2026",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(DEST)


if __name__ == "__main__":
    main()
