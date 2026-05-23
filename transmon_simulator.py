import numpy as np
from scipy.linalg import expm

N_TRANSMONS = 20
FREQ_GHZ = 7e9
HBAR = 1.0545718e-34
omega = 2 * np.pi * FREQ_GHZ
VOLTAGE = np.pi / (omega * 20e-9)
KET_0 = np.array([1, 0], dtype=complex)
resultados = []
PULSE_0 = 0
PULSE_1 = 20e-9
PULSE_SUP = 10e-9
secuencia = [PULSE_0] * 7 + [PULSE_1] * 7 + [PULSE_SUP] * 6

transmon = np.array([1, 0], dtype=complex)

def hamiltoniano(voltage):
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    return (omega / 2) * voltage * sigma_x

def aplicar_pulso(qubit_state, duracion, voltage):
    if duracion == 0:
        return KET_0.copy()
    H = hamiltoniano(voltage)
    U = expm(-1j * H * duracion)
    return U @ qubit_state

def leer_estado(state):
    p0 = abs(state[0])**2
    p1 = abs(state[1])**2
    if p0 > 0.99:
        return "|0⟩"
    elif p1 > 0.99:
        return "|1⟩"
    else:
        return f"superposición p0={p0:.2f} p1={p1:.2f}"

for i, duracion in enumerate(secuencia):
    state = aplicar_pulso(KET_0, duracion, VOLTAGE)
    lectura = leer_estado(state)
    resultados.append(state)
    print(f"Transmon {i+1:02d} | pulso {duracion*1e9:.0f}ns | {lectura}")
