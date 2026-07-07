
import numpy as np
import matplotlib.pyplot as plt

# griglia spaziale
x = np.linspace(-5, 5, 1000)

# esempio: gaussiana (pacchetto d'onda)
sigma = 1.0
psi = np.exp(-x**2 / (2 * sigma**2))          # ampiezza reale
psi = psi.astype(complex)                      # in generale psi e' complessa

# normalizzazione: int_{-inf}^{+inf} |psi|^2 dx = 1
dx = x[1] - x[0]
norm = np.sqrt(np.sum(np.abs(psi)**2) * dx)
psi = psi / norm

# densita' di probabilita'
prob = np.abs(psi)**2

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

ax[0].plot(x, psi.real, label="Re ψ(x)")
ax[0].plot(x, psi.imag, label="Im ψ(x)")
ax[0].set_title("Wave function")
ax[0].legend()
ax[0].grid(True, alpha=0.3)

ax[1].plot(x, prob)
ax[1].set_title("|ψ(x)|²")
ax[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()   # oppure plt.savefig("wavefunction.png")


# |0> in posizione (non ha senso fisico puro, ma utile per esercizi discreti)
# Qui: autostato del pozzo infinito n=1

L = 10.0
x = np.linspace(0, L, 1000)
n = 1
psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
psi = psi.astype(complex)

# pacchetto con momento medio k0
k0 = 2.0
sigma = 0.8
psi = np.exp(-x**2 / (4 * sigma**2)) * np.exp(1j * k0 * x)

import numpy as np
import matplotlib.pyplot as plt

# parametri
N = 512
L = 20.0
x = np.linspace(-L/2, L/2, N, endpoint=False)
dx = x[1] - x[0]
k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
hbar = 1.0
m = 1.0

# stato iniziale
sigma = 1.0
k0 = 2.0
psi = np.exp(-x**2 / (2 * sigma**2)) * np.exp(1j * k0 * x)
psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx)

dt = 0.01
steps = 200

def propagate_free(psi, dt):
    # evoluzione libera nel dominio dei momenti
    phase = np.exp(-1j * (hbar * k**2 / (2 * m)) * dt)
    psi_k = np.fft.fft(psi)
    psi_k *= phase
    return np.fft.ifft(psi_k)

# animazione / snapshot
for t in range(steps):
    psi = propagate_free(psi, dt)

prob = np.abs(psi)**2
plt.plot(x, prob)
plt.title(f"Probability density at t = {steps * dt:.2f}")
plt.xlabel("x")
plt.ylabel("|ψ(x,t)|²")
plt.grid(True, alpha=0.3)
plt.show()

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

Omega = 1.0

def schrodinger_2level(t, y):
    c0, c1 = y[0] + 1j*y[1], y[2] + 1j*y[3]
    dc0 = -1j * (Omega / 2) * c1
    dc1 = -1j * (Omega / 2) * c0
    return [dc0.real, dc0.imag, dc1.real, dc1.imag]

y0 = [1, 0, 0, 0]   # |0> iniziale
t_span = (0, 10)
t_eval = np.linspace(0, 10, 500)

sol = solve_ivp(schrodinger_2level, t_span, y0, t_eval=t_eval)

c1 = sol.y[2] + 1j * sol.y[3]
P1 = np.abs(c1)**2

plt.plot(sol.t, P1)
plt.xlabel("t")
plt.ylabel("P(|1>)")
plt.title("Rabi oscillations")
plt.grid(True, alpha=0.3)
plt.show()