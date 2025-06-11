import numpy as np
import matplotlib.pyplot as plt

Pt_dBm = 0.0       # Potencia transmitida (dBm)
Gt_dBi = 15.0      # Ganancia antena TX (dBi)
Gr_dBi = 15.0      # Ganancia antena RX (dBi)
f = 60e9           # Frecuencia (Hz)
c = 3e8            # Velocidad de la luz (m/s)
wavelength = c / f  # Longitud de onda (m)

def friis_pr_dBm(d_m, Pt, Gt, Gr, lam):
    fspl_dB = 20*np.log10(4*np.pi*d_m/lam)
    return Pt + Gt + Gr - fspl_dB

# Parámetros del sistema
r = 0.5                       # Radio del plato (m)
delta_x = 0                  # Desfase en X (m)
receiver = np.array([1.0, 0.0])  # Receptor en eje X
wavelength = 0.005           # Longitud de onda (m) (60 GHz)
vueltas = 1                  # Cuántas vueltas da el transmisor

# Ángulos desde 0 hasta 3 vueltas (0° a 1080°)
angles_deg = np.arange(0, 360 * vueltas,1)
angles_rad = np.radians(angles_deg)

# Fase calculada
phase_rad = np.zeros_like(angles_rad)
mag_deg=[]
for i, theta in enumerate(angles_rad):
    tx_x = r * np.cos(theta) + delta_x
    tx_y = r * np.sin(theta)
    d = np.hypot(receiver[0] - tx_x, receiver[1] - tx_y)
    PR = friis_pr_dBm(d, Pt_dBm, Gt_dBi, Gr_dBi, wavelength)
    print(f"Ángulo: {np.degrees(theta):.1f}° - Distancia: {d:.3f} m - Potencia recibida: {PR:.2f} dBm")
    mag_deg.append(PR)
    phase_rad[i] = -2 * np.pi * d / wavelength

# Convertimos a grados
phase_deg = np.degrees(phase_rad)

# Fase enrollada (como lo vería el AD8302: 0–180° o similar)
phase_wrapped = phase_deg % 360
phase_wrapped_180 = phase_wrapped.copy()
phase_wrapped_180[phase_wrapped_180 > 180] -= 360  # Simula un rango ±180°

# Fase desenrollada


phase_unwrapped = np.unwrap(phase_rad)
phase_unwrapped_deg = np.degrees(phase_unwrapped)



phase_ad8302_rad = np.radians(phase_wrapped_180)
phase_ad8302_unwrapped_rad = np.unwrap(phase_ad8302_rad)
phase_ad8302_unwrapped_deg = np.degrees(phase_ad8302_unwrapped_rad)

# Graficar
import matplotlib.pyplot as plt
fig, axs = plt.subplots(5, 1, figsize=(10, 12), sharex=True)

axs[0].plot(angles_deg, phase_wrapped, label='Fase enrollada (0°–360°)')
axs[0].set_ylabel("Fase (°)")
axs[0].set_title("Fase enrollada (como un sensor limitado a 360°)")
axs[0].grid(True)
axs[0].legend()

axs[1].plot(angles_deg, mag_deg, label='MAG(dbm)')
axs[1].set_ylabel("MAG (dBm)")
axs[1].set_title("Magnitud (en base a AD8302)")
axs[1].grid(True)
axs[1].legend()

axs[2].plot(angles_deg, np.abs(phase_wrapped_180), label='Fase AD8302 (±180°)')
axs[2].set_ylabel("Fase (°)")
axs[2].set_title("Fase AD8302 (±90°)")
axs[2].grid(True)
axs[2].set_xlabel("Ángulo de giro (°)")
axs[2].legend()

axs[3].plot(angles_deg, phase_unwrapped_deg, label='Fase desenrollada (acumulada)')
axs[3].set_xlabel("Ángulo de giro (°)")
axs[3].set_ylabel("Fase (°)")
axs[3].set_title("Fase desenrollada (real acumulada)")
axs[3].grid(True)
axs[3].legend()

axs[4].plot(angles_deg, phase_ad8302_unwrapped_deg, label='Fase desenrollada AD8302(acumulada)')
axs[4].set_xlabel("Ángulo de giro (°)")
axs[4].set_ylabel("Fase (°)")
axs[4].set_title("Fase desenrollada (en base a AD8302)")
axs[4].grid(True)
axs[4].legend()


plt.tight_layout()
plt.show()
