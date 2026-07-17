"""
Playground: wave functions, split-step propagation, and Rabi oscillations.

Three small demos in one file for learning bra/ket and Schrodinger dynamics.
Plots are saved under output/ (no interactive windows).

Run:
    python quantum/00_test_random/Matrixandode.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from _common import banner, savefig


def demo_gaussian() -> None:
    """Static Gaussian wave packet: psi(x) and |psi|^2."""
    print("\n[Demo 1] Gaussian wave packet")
    x = np.linspace(-5, 5, 1000)
    dx = x[1] - x[0]
    sigma = 1.0
    psi = np.exp(-x**2 / (2 * sigma**2)).astype(complex)
    psi /= np.sqrt(np.sum(np.abs(psi) ** 2) * dx)
    prob = np.abs(psi) ** 2

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(x, psi.real, label="Re psi(x)")
    axes[0].plot(x, psi.imag, label="Im psi(x)")
    axes[0].set_title("Wave function")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(x, prob)
    axes[1].set_title("|psi(x)|^2")
    axes[1].grid(True, alpha=0.3)
    path = savefig(fig, __file__, "gaussian_wavepacket.png")
    plt.close(fig)
    print(f"  Plot saved to: {path}")


def demo_free_propagation() -> None:
    """Free-particle evolution via FFT split-step (momentum grid k)."""
    print("\n[Demo 2] Free propagation (split-step FFT)")
    N = 512
    L = 20.0
    x = np.linspace(-L / 2, L / 2, N, endpoint=False)
    dx = x[1] - x[0]
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)  # momentum / wavenumber grid
    hbar, m = 1.0, 1.0

    sigma, k0 = 1.0, 2.0
    psi = np.exp(-x**2 / (2 * sigma**2)) * np.exp(1j * k0 * x)
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dx)

    dt, steps = 0.01, 200

    def propagate_free(state: np.ndarray, dt_step: float) -> np.ndarray:
        phase = np.exp(-1j * (hbar * k**2 / (2 * m)) * dt_step)
        psi_k = np.fft.fft(state)
        psi_k *= phase
        return np.fft.ifft(psi_k)

    for _ in range(steps):
        psi = propagate_free(psi, dt)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, np.abs(psi) ** 2)
    ax.set_title(f"Probability density at t = {steps * dt:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("|psi(x,t)|^2")
    ax.grid(True, alpha=0.3)
    path = savefig(fig, __file__, "free_propagation.png")
    plt.close(fig)
    print(f"  Plot saved to: {path}")


def demo_rabi() -> None:
    """Two-level Rabi oscillations from the Schrodinger equation."""
    print("\n[Demo 3] Rabi oscillations (two-level system)")
    omega = 1.0

    def schrodinger_2level(t, y):
        c0 = y[0] + 1j * y[1]
        c1 = y[2] + 1j * y[3]
        dc0 = -1j * (omega / 2) * c1
        dc1 = -1j * (omega / 2) * c0
        return [dc0.real, dc0.imag, dc1.real, dc1.imag]

    sol = solve_ivp(
        schrodinger_2level,
        (0, 10),
        [1, 0, 0, 0],
        t_eval=np.linspace(0, 10, 500),
    )
    p1 = np.abs(sol.y[2] + 1j * sol.y[3]) ** 2

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(sol.t, p1)
    ax.set_xlabel("t")
    ax.set_ylabel("P(|1>)")
    ax.set_title("Rabi oscillations")
    ax.grid(True, alpha=0.3)
    path = savefig(fig, __file__, "rabi_oscillations.png")
    plt.close(fig)
    print(f"  Plot saved to: {path}")


def main() -> None:
    banner("Matrixandode playground")
    demo_gaussian()
    demo_free_propagation()
    demo_rabi()
    print("\nDone.")


if __name__ == "__main__":
    main()
