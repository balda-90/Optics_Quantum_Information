"""
Quantum electronics — course recap (original notes + numerical demos).

A public map of the Sapienza "Elettronica quantistica" course: light as wave
and photon, two-level atoms, laser rate equations, semiconductor lasers,
fiber lasers, photonic crystals, surface plasmons, and quantum dots — and
how they connect to qubits.

This file contains *my* reconstruction and code. Course PDFs / lectures in
local `data/` stay unpublished (copyright).

Run from the repo root:

    python "quantum/04_quantum_electronics/03_course_recap.py"

Companion notebooks:
    01_rabi_oscillations.ipynb
    02_semiconductor_states_and_dos.ipynb
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_HERE = Path(__file__).resolve().parent
_QUANTUM = _HERE.parent
if str(_QUANTUM) not in sys.path:
    sys.path.insert(0, str(_QUANTUM))

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import PAULI_X, PAULI_Z, ket0, savefig

# ---------------------------------------------------------------------------
# Printing helpers (keep this folder independent from tesi/_lib)
# ---------------------------------------------------------------------------


def _fill(text: str, indent: str = "  ") -> None:
    print(textwrap.fill(text, width=78, initial_indent=indent, subsequent_indent=indent))


def heading(title: str, subtitle: str = "") -> None:
    line = "=" * 78
    print(f"\n{line}\n  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print(line)


def section(number: int, title: str) -> None:
    print(f"\n{'-' * 78}")
    print(f"  {number}. {title}")
    print(f"{'-' * 78}")


def bullets(items: list[str]) -> None:
    for item in items:
        print(f"    - {item}")


# ---------------------------------------------------------------------------
# 1. Two-level Rabi (analytic + one numerical check)
# ---------------------------------------------------------------------------


def rabi_population(omega: float, delta: float, t: np.ndarray) -> np.ndarray:
    """Excited-state population starting from |0>, H = (Delta/2) Z + (Omega/2) X."""
    omega_eff = np.sqrt(omega**2 + delta**2)
    # Avoid 0/0 at the isolated point omega = delta = 0.
    amp = 0.0 if omega_eff == 0 else (omega / omega_eff) ** 2
    return amp * np.sin(0.5 * omega_eff * t) ** 2


def demo_rabi() -> Path:
    omega = 2 * np.pi
    t = np.linspace(0.0, 2.0, 800)
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    for delta, label in [(0.0, r"on resonance $\Delta=0$"), (omega, r"off resonance $\Delta=\Omega$")]:
        pop = rabi_population(omega, delta, t)
        ax.plot(t, pop, lw=2, label=f"{label}  (max = {pop.max():.3f})")
        # Numerical check of the exact unitary on a few points.
        H = 0.5 * delta * PAULI_Z + 0.5 * omega * PAULI_X
        evals, evecs = np.linalg.eigh(H)
        psi0 = ket0.reshape(2)
        t_check = np.array([0.25, 0.5, 1.0])
        analytic = rabi_population(omega, delta, t_check)
        numeric = []
        for ti in t_check:
            u = evecs @ np.diag(np.exp(-1j * evals * ti)) @ evecs.conj().T
            psi = u @ psi0
            numeric.append(abs(psi[1]) ** 2)
        ok = np.allclose(analytic, numeric, atol=1e-10)
        print(f"    Rabi check  {label:28s}  analytic=numeric? {ok}")

    ax.set_xlabel("time (arb. units)")
    ax.set_ylabel(r"excited population  $P_e(t)$")
    ax.set_title("Two-level atom: Rabi oscillations")
    ax.set_ylim(-0.05, 1.08)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = savefig(fig, __file__, "qe_recap_rabi.png")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# 2. Four-level laser rate equations (switch-on + relaxation oscillations)
# ---------------------------------------------------------------------------


def laser_rate_rhs(y, pump, tau_sp, tau_ph, beta):
    """
    Dimensionless 4-level model.

    n : inversion (carriers / threshold inversion)
    q : photon number in the cavity (in units of the saturation photon number)

    dn/dt = pump - n/tau_sp - n q
    dq/dt = (n - 1) q / tau_ph + beta n / tau_sp
    """
    n, q = y
    dn = pump - n / tau_sp - n * q
    dq = (n - 1.0) * q / tau_ph + beta * n / tau_sp
    return np.array([dn, dq])


def rk4(fun, y0: np.ndarray, t: np.ndarray, **kwargs) -> np.ndarray:
    """Fixed-step RK4; avoids a scipy dependency (numpy-only like the rest of this folder)."""
    y = np.empty((len(t), y0.size), dtype=float)
    y[0] = y0
    for i in range(len(t) - 1):
        dt = t[i + 1] - t[i]
        k1 = fun(y[i], **kwargs)
        k2 = fun(y[i] + 0.5 * dt * k1, **kwargs)
        k3 = fun(y[i] + 0.5 * dt * k2, **kwargs)
        k4 = fun(y[i] + dt * k3, **kwargs)
        y[i + 1] = y[i] + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


def demo_rate_equations() -> Path:
    tau_sp, tau_ph, beta = 1.0, 0.02, 1e-4
    t = np.linspace(0.0, 40.0, 4000)
    y0 = np.array([0.05, 1e-6])

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.2), sharex=True)
    for pump, color in [(0.7, "#C44E52"), (1.6, "#4C72B0")]:
        traj = rk4(
            laser_rate_rhs,
            y0,
            t,
            pump=pump,
            tau_sp=tau_sp,
            tau_ph=tau_ph,
            beta=beta,
        )
        n, q = traj[:, 0], traj[:, 1]
        label = f"pump = {pump:.1f} x threshold"
        axes[0].plot(t, n, color=color, lw=2, label=label)
        axes[1].plot(t, q, color=color, lw=2, label=label)
        print(
            f"    pump={pump:.1f}:  n(inf)={n[-1]:.3f}   q(inf)={q[-1]:.3f}   "
            f"lasing={'yes' if q[-1] > 0.05 else 'no (below threshold)'}"
        )

    axes[0].axhline(1.0, color="k", ls="--", lw=1, alpha=0.5, label="threshold inversion")
    axes[0].set_ylabel("inversion  n / n_th")
    axes[0].set_title("Population inversion")
    axes[1].set_ylabel("cavity photons  q")
    axes[1].set_title("Photon number (switch-on)")
    for ax in axes:
        ax.set_xlabel("time / τ_sp")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    path = savefig(fig, __file__, "qe_recap_rate_equations.png")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# 3. Semiconductor laser: 3D DOS x Fermi occupation  →  inversion
# ---------------------------------------------------------------------------


def fermi_dirac(E: np.ndarray, mu: float, kT: float) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(np.clip((E - mu) / kT, -60.0, 60.0)))


def demo_semiconductor_inversion() -> Path:
    """
    Qualitative gain condition: stimulated emission needs inversion,
    f_c(E_c) > f_v(E_v), i.e. a quasi-Fermi separation larger than the gap.
    """
    Eg = 1.42  # eV, GaAs-like
    kT = 0.026  # ~300 K
    E = np.linspace(0.0, 2.4, 600)
    dos_v = np.sqrt(np.clip(Eg / 2 - E, 0, None))  # schematic valence DOS
    dos_c = np.sqrt(np.clip(E - Eg, 0, None))  # schematic conduction DOS

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.3))
    for ax, (mu_c, mu_v, title) in [
        (axes[0], (0.95, 0.55, "thermal equilibrium (no inversion)")),
        (axes[1], (1.70, 0.20, "pumped: quasi-Fermi inversion")),
    ]:
        fc = fermi_dirac(E, mu_c, kT)
        fv = fermi_dirac(E, mu_v, kT)
        ax.fill_between(E, 0, dos_v * fv, color="#4C72B0", alpha=0.35, label="holes occupy valence")
        ax.plot(E, dos_v, color="#4C72B0", lw=1.6, label="valence DOS (schematic)")
        ax.fill_between(E, 0, dos_c * fc, color="#C44E52", alpha=0.35, label="electrons occupy conduction")
        ax.plot(E, dos_c, color="#C44E52", lw=1.6, label="conduction DOS (schematic)")
        ax.axvline(Eg, color="k", ls=":", lw=1)
        inversion = (mu_c - mu_v) > Eg
        ax.set_title(title + ("\n→ optical gain possible" if inversion else "\n→ absorption dominates"))
        ax.set_xlabel("energy (eV)")
        ax.set_ylabel("DOS × occupation (arb.)")
        ax.set_xlim(0, 2.4)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
        print(f"    {title}:  μ_c-μ_v = {mu_c - mu_v:.2f} eV   gap = {Eg:.2f} eV   gain? {inversion}")

    fig.tight_layout()
    path = savefig(fig, __file__, "qe_recap_semiconductor_inversion.png")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# 4. 1D photonic crystal: Bloch bands of a bilayer dielectric stack
# ---------------------------------------------------------------------------


def bilayer_bloch_cos(omega: np.ndarray, n1: float, n2: float, d1: float, d2: float) -> np.ndarray:
    """
    cos(K Λ) for a 1D photonic crystal at normal incidence (c = 1).

    Allowed bands: |cos(K Λ)| ≤ 1.  Gaps appear where the formula exceeds 1.
    """
    k1 = n1 * omega
    k2 = n2 * omega
    mismatch = (n1 / n2 + n2 / n1) / 2.0
    return np.cos(k1 * d1) * np.cos(k2 * d2) - mismatch * np.sin(k1 * d1) * np.sin(k2 * d2)


def demo_photonic_bands() -> Path:
    n1, n2 = 1.5, 3.4
    d1 = d2 = 0.5
    period = d1 + d2
    omega = np.linspace(1e-3, 8.5, 4000)
    cosk = bilayer_bloch_cos(omega, n1, n2, d1, d2)
    allowed = np.abs(cosk) <= 1.0

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    K = np.full_like(omega, np.nan)
    K[allowed] = np.arccos(np.clip(cosk[allowed], -1.0, 1.0)) / period
    ax.plot(K, omega, "o", ms=1.2, color="#4C72B0", label="allowed Bloch modes")
    ax.plot(-K, omega, "o", ms=1.2, color="#4C72B0")
    # Shade a few gaps for readability.
    gap_mask = ~allowed
    in_gap = False
    start = 0
    first_gap = True
    for i, g in enumerate(gap_mask):
        if g and not in_gap:
            start = i
            in_gap = True
        elif not g and in_gap:
            ax.axhspan(omega[start], omega[i], color="#C44E52", alpha=0.12, label="photonic gap" if first_gap else None)
            first_gap = False
            in_gap = False

    n_gap_samples = int(np.sum(gap_mask) / len(omega) * 100)
    print(f"    1D stack n=({n1}, {n2}): about {n_gap_samples}% of the plotted spectrum sits in a gap")

    ax.set_xlabel(r"Bloch wavevector  $K$  (units of $1/\Lambda$)")
    ax.set_ylabel(r"frequency  $\omega$  ($c=1$)")
    ax.set_title("1D photonic crystal: allowed bands and gaps")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = savefig(fig, __file__, "qe_recap_photonic_bands.png")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# 5. Surface plasmon polariton on a metal / dielectric interface
# ---------------------------------------------------------------------------


def spp_wavevector(omega: np.ndarray, omega_p: float, eps_d: float) -> np.ndarray:
    """Lossless Drude metal: ε_m = 1 - ω_p²/ω².  Bound SPP exists for ε_m + ε_d < 0."""
    eps_m = 1.0 - (omega_p / omega) ** 2
    disc = eps_m * eps_d / (eps_m + eps_d)
    k = (omega / 1.0) * np.sqrt(disc + 0j)
    bound = (eps_m + eps_d) < 0
    out = np.full_like(omega, np.nan, dtype=float)
    out[bound] = np.real(k[bound])
    return out


def demo_spp() -> Path:
    omega_p = 1.0
    eps_d = 1.0  # air
    omega = np.linspace(0.05, 0.95 * omega_p / np.sqrt(1 + eps_d) * 0.999, 800)
    k_spp = spp_wavevector(omega, omega_p, eps_d)
    k_light = omega  # air light line, c = 1
    omega_spp = omega_p / np.sqrt(1 + eps_d)

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ax.plot(k_light, omega, "k--", lw=1.4, label="light line in air")
    ax.plot(k_spp, omega, color="#8172B2", lw=2.4, label="bound SPP")
    ax.axhline(omega_spp, color="#C44E52", ls=":", lw=1.3, label=r"SPP limit  $\omega_p/\sqrt{1+\varepsilon_d}$")
    ax.set_xlabel(r"wavevector  $k$  ($c=1$)")
    ax.set_ylabel(r"frequency  $\omega$")
    ax.set_title("Surface plasmon polariton: dispersion vs the light line")
    ax.set_xlim(0, 4.2)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    path = savefig(fig, __file__, "qe_recap_spp.png")
    plt.close(fig)
    print(f"    SPP asymptotic frequency / ω_p = {omega_spp:.3f}  (air, lossless Drude)")
    print("    The SPP sits to the right of the light line: extra momentum is needed to couple in.")
    return path


# ---------------------------------------------------------------------------
# 6. Quantum dot = 3D particle in a box
# ---------------------------------------------------------------------------


def box_levels(n_max: int, hbar2_over_2mL2: float) -> list[tuple[float, tuple[int, int, int]]]:
    levels = []
    for nx in range(1, n_max + 1):
        for ny in range(1, n_max + 1):
            for nz in range(1, n_max + 1):
                e = hbar2_over_2mL2 * (nx**2 + ny**2 + nz**2)
                levels.append((e, (nx, ny, nz)))
    levels.sort(key=lambda item: (item[0], item[1]))
    return levels


def demo_quantum_dot() -> Path:
    """GaAs-like cube, L = 8 nm, m* = 0.067 m_e. Energies in meV above the band edge."""
    hbar = 1.054571817e-34
    m_e = 9.1093837e-31
    mstar = 0.067 * m_e
    L = 8e-9
    qe = 1.602176634e-19
    pre = (hbar**2 * np.pi**2) / (2 * mstar * L**2) / qe * 1e3  # meV

    levels = box_levels(4, pre)
    # Degeneracy: group by energy.
    unique: dict[float, int] = {}
    for e, _qn in levels:
        key = round(e, 6)
        unique[key] = unique.get(key, 0) + 1

    energies = np.array(list(unique.keys()))
    degeneracy = np.array(list(unique.values()))
    print(f"    Cube L=8 nm, m*=0.067 m_e: ground state E_111 = {energies[0]:.1f} meV")
    print(f"    First few levels (meV, degeneracy):")
    for e, g in list(zip(energies, degeneracy))[:6]:
        print(f"      {e:7.1f}   g={g}")

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    for e, g in zip(energies[:12], degeneracy[:12]):
        ax.hlines(e, 0.2, 0.8, colors="#55A868", lw=2.2)
        ax.text(0.86, e, f"g={g}", va="center", fontsize=8)
    ax.set_xlim(0, 1.4)
    ax.set_xticks([])
    ax.set_ylabel("confinement energy above the band edge (meV)")
    ax.set_title("Quantum dot: particle-in-a-cube spectrum")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    path = savefig(fig, __file__, "qe_recap_quantum_dot.png")
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Course map
# ---------------------------------------------------------------------------


def print_course_map() -> None:
    heading(
        "Quantum electronics — course recap",
        "Optics & Quantum Information  ·  original notes + runnable demos",
    )
    _fill(
        "The course is the hardware layer of quantum information: how light, "
        "atoms and solids produce coherent photons and confined electrons — "
        "the physical objects we later treat as qubits."
    )
    print("\n  Course spine (themes, not a copy of the lectures)")
    bullets(
        [
            "Optics refresh: Maxwell waves, the photon, refraction / interfaces.",
            "Atomic transitions: spontaneous vs stimulated emission, two-level Rabi.",
            "Laser rate equations: 3-level vs 4-level, threshold, photon build-up.",
            "Semiconductor lasers: bands, doping, DOS, Fermi occupation, diodes.",
            "Fiber lasers: rare-earth doped fiber, cavity vs MOPA, pump diodes.",
            "Photonic crystals: Bloch photons, band gaps, defects, PC fibers.",
            "Plasmonics: surface plasmon polaritons, sub-wavelength confinement.",
            "Quantum dots: 0D confinement and discrete optical transitions.",
            "Ultrafast / pulses: how a laser leaves CW and becomes a clock.",
        ]
    )
    print("\n  Recorded lectures in the local (unpublished) archive")
    bullets(
        [
            "2026-05-19, 05-26, 05-28, 06-04, 06-09, 06-11, 06-16, 06-18,",
            "2026-07-14, 07-16, 07-21, 07-28, 09-15  —  13 sessions, May–September 2026.",
        ]
    )
    print("\n  Already published in this folder")
    bullets(
        [
            "01_rabi_oscillations.ipynb — driven two-level Schrödinger equation.",
            "02_semiconductor_states_and_dos.ipynb — wells, DOS, Fermi–Dirac, 2D.",
        ]
    )


def main() -> None:
    print_course_map()

    section(1, "Light: why the laser exists")
    _fill(
        "Maxwell already gives waves; Einstein's photon gives packets of energy "
        "ħω. Engineering optics exploded only when a coherent optical oscillator "
        "appeared — the laser. Everything below is the physics of that oscillator "
        "and of the nanostructures that guide, confine or generate its light."
    )

    section(2, "Two-level atom and Rabi flopping")
    _fill(
        "A qubit is a two-level system. A near-resonant drive H = (Δ/2) Z + (Ω/2) X "
        "makes the excited population oscillate at the effective Rabi frequency "
        "√(Ω²+Δ²). On resonance the inversion is complete; off resonance it is not. "
        "That is a π-pulse: the hardware origin of an X gate."
    )
    path = demo_rabi()
    print(f"    figure → {path}")

    section(3, "Laser rate equations: threshold is a balance")
    _fill(
        "A 4-level laser needs less pump than a 3-level one because the lower "
        "laser level empties quickly, so inversion is cheaper. Threshold is the "
        "point where stimulated gain exactly cancels cavity loss. Below it the "
        "photon number stays near the spontaneous seed; above it the field "
        "switches on, often with relaxation oscillations."
    )
    path = demo_rate_equations()
    print(f"    figure → {path}")

    section(4, "Semiconductor laser: inversion in bands")
    _fill(
        "In a diode the 'levels' are bands. Optical gain requires a quasi-Fermi "
        "separation larger than the gap, so that conduction states at the photon "
        "energy are more occupied than the valence states. Density of states "
        "tells us how many of those states exist; Fermi–Dirac tells us how they "
        "are filled. Quantum wells flatten the DOS and concentrate the gain."
    )
    path = demo_semiconductor_inversion()
    print(f"    figure → {path}")

    section(5, "Fiber lasers: a doped waveguide as the gain medium")
    _fill(
        "Replace the bulk crystal with a glass fiber doped with rare-earth ions "
        "(Yb, Er, Tm). Pump diodes at 915/976 nm invert the ions; emission sits "
        "near 1.0 μm (Yb) or 1.5 μm (Er). Two architectures dominate: a standing-"
        "wave cavity, or a MOPA (a weak seeder amplified in one direction). The "
        "fiber is both the gain medium and the waveguide."
    )

    section(6, "Photonic crystals: Bragg for photons")
    _fill(
        "A periodic dielectric does to photons what the atomic lattice does to "
        "electrons: Bloch modes and forbidden bands. In 1D this is a multilayer "
        "Bragg stack; in 2D/3D you get waveguides and high-Q cavities by "
        "intentional defects, and photonic-crystal fibers by a periodic cladding."
    )
    path = demo_photonic_bands()
    print(f"    figure → {path}")

    section(7, "Surface plasmons: light glued to a metal")
    _fill(
        "At a metal/dielectric interface a TM surface wave — the SPP — binds "
        "to the free charges. Its dispersion lies beyond the light line, so the "
        "mode is evanescent on both sides and can be squeezed below the "
        "diffraction limit. Coupling in requires extra momentum (grating, prism, "
        "near field). This is the plasmonic route to nanoscale photonics."
    )
    path = demo_spp()
    print(f"    figure → {path}")

    section(8, "Quantum dots: artificial atoms")
    _fill(
        "Confining an electron in all three directions discretizes the spectrum. "
        "A cube of side L is the particle-in-a-box textbook limit: "
        "E ∝ (n_x² + n_y² + n_z²)/L², with degeneracies from permutations. "
        "Real dots add Coulomb charging and selection rules; the idea is the same: "
        "size tunes the color, just as a well tunes a laser."
    )
    path = demo_quantum_dot()
    print(f"    figure → {path}")

    section(9, "From this course to a qubit")
    bullets(
        [
            "Two-level atom + π pulse          →  X / √X gates (see notebook 01).",
            "Cavity + stimulated emission      →  a coherent photon bus.",
            "Quantum well / dot                →  discrete charged or excitonic qubits.",
            "Photonic crystal / SPP waveguide  →  on-chip routing of those photons.",
            "Semiconductor / fiber laser       →  the classical pump that still runs the lab.",
        ]
    )

    section(10, "What to remember")
    bullets(
        [
            "A laser is inversion + stimulated emission + a cavity that stores the mode.",
            "4-level pumping reaches threshold with less power than 3-level pumping.",
            "In semiconductors, inversion is a statement about quasi-Fermi levels vs the gap.",
            "Periodicity opens gaps for photons; a metal/dielectric interface binds an SPP.",
            "0D confinement (a dot) is the same Schrödinger problem as a well, in 3 axes.",
            "Rabi flopping is how a classical field writes a gate on a two-level qubit.",
        ]
    )

    print("\n  Next steps")
    bullets(
        [
            "Add T1/T2 decay to notebook 01 (Lindblad) and watch Rabi contrast die.",
            "Turn the rate-equation demo into a pump-vs-output LI curve.",
            "Compute Bragg reflectivity of a finite stack (transfer matrix).",
            "Compare 3D / 2D / 0D DOS on one plot (extend notebook 02).",
        ]
    )
    print()


if __name__ == "__main__":
    main()
