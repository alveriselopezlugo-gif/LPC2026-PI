import numpy as np
import matplotlib.pyplot as plt

# Datos de ejemplo
x = np.linspace(1.0, 10.0, 100)

# Utilidad (entre -3 y -13)
utilidad = -3 - 10 * (x - 1) / 9

# Porcentaje (entre 0 y 100)
porcentaje = 100 * (1 - np.exp(-(x - 1) / 3))

# Crear figura y eje principal
fig, ax1 = plt.subplots(figsize=(8, 5))

# Eje Y izquierdo: utilidad
linea1 = ax1.plot(
    x, utilidad,
    color='indigo',
    linewidth=2,
    label='Utilidad'
)
ax1.set_xlabel('X')
ax1.set_ylabel('Utilidad')
ax1.set_ylim(-13, -3)

# Cuadrícula
ax1.grid(True)

# Eje Y derecho: porcentaje
ax2 = ax1.twinx()

linea2 = ax2.plot(
    x, porcentaje,
    color='orange',
    linestyle='--',
    linewidth=2,
    label='Porcentaje'
)
ax2.set_ylabel('Porcentaje (%)')
ax2.set_ylim(0, 100)

# Leyenda unificada abajo a la derecha
lineas = linea1 + linea2
etiquetas = [l.get_label() for l in lineas]

ax1.legend(
    lineas,
    etiquetas,
    loc='lower right'
)

plt.title('Simulación')
plt.tight_layout()
plt.show()