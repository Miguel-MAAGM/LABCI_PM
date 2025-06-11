import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.patches as patches

# Parámetros del sistema
r = 0.50              # radio del giro (metros)
receiver = np.array([1.0, 0.0])  # receptor fijo a 1 m sobre el eje X
lambda_ = 0.005      # longitud de onda (5 mm para 60 GHz)

# Ángulos (0° a 360°)
theta_vals = np.linspace(0, 2 * np.pi, 120)

# Crear figura
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-0.8, 1.2)
ax.set_ylim(-0.8, 0.8)
ax.set_aspect('equal')
ax.set_title("Movimiento del transmisor")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.grid(True)

# Dibujar círculo de rotación
circle = patches.Circle((0, 0), r, fill=False, linestyle='--', color='gray')
ax.add_patch(circle)

# Elementos dinámicos
tx_dot, = ax.plot([], [], 'ko', label='Transmisor T(θ)')
rx_dot, = ax.plot(receiver[0], receiver[1], 'rs', label='Receptor R', markersize=8)
line_d, = ax.plot([], [], 'orange', label='Distancia d(θ)')
text_phase = ax.text(-0.75, 0.7, '', fontsize=10, color='blue')
text_theta = ax.text(-0.75, 0.6, '', fontsize=10, color='green')
ax.legend()

# Función de animación
def update(frame):
    theta = theta_vals[frame]
    tx_x = r * np.cos(theta)
    tx_y = r * np.sin(theta)
    tx_pos = np.array([tx_x, tx_y])

    # Actualizar puntos y línea
    tx_dot.set_data(tx_x, tx_y)
    line_d.set_data([tx_x, receiver[0]], [tx_y, receiver[1]])

    # Calcular distancia y fase
    dist = np.linalg.norm(receiver - tx_pos)
    phase = -2 * np.pi * dist / lambda_

    # Mostrar textos
    #text_phase.set_text(f"Fase: {phase:.2f} rad")
    text_theta.set_text(f"Ángulo: {np.degrees(theta):.1f}°")

    return tx_dot, line_d, text_phase, text_theta

# Crear animación
ani = FuncAnimation(fig, update, frames=len(theta_vals), interval=80, blit=True)

# Guardar como GIF
ani.save("transmisor_fase_animado.gif", writer=PillowWriter(fps=15))
print("GIF guardado como 'transmisor_fase_animado.gif'")
