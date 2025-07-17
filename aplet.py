import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulador de dinámica: bloque en plano inclinado con fricción")

st.markdown("""
Calcula la aceleración de un bloque en un plano inclinado con fricción cinética, considerando:
- Masa del bloque
- Ángulo del plano
- Coeficiente de fricción
- Fuerza aplicada paralela al plano (opcional)
""")

# Inputs
m = st.number_input("Masa del bloque (kg)", min_value=0.1, value=5.0, step=0.1)
theta_deg = st.slider("Ángulo del plano inclinado (°)", min_value=0, max_value=90, value=30)
mu = st.number_input("Coeficiente de fricción cinética (μ)", min_value=0.0, max_value=1.0, value=0.2, step=0.01)
F_aplicada = st.number_input("Fuerza aplicada paralela al plano (N)", value=0.0)

# Constantes
g = 9.81  # m/s^2
theta = np.radians(theta_deg)

# Cálculos
# Componentes de fuerzas
peso = m * g
F_gravedad_paralela = peso * np.sin(theta)
F_gravedad_normal = peso * np.cos(theta)
F_friccion = mu * F_gravedad_normal

# Fuerza neta
# La fuerza de fricción siempre actúa en sentido opuesto al movimiento potencial o aplicado
# Suponemos que la fuerza aplicada es paralela al plano, positivo hacia arriba
# El bloque se mueve si la fuerza neta supera la fricción

F_neta = F_aplicada - F_gravedad_paralela - np.sign(F_aplicada - F_gravedad_paralela)*F_friccion

# Ver si se mueve o no (si la fuerza neta no supera fricción estática, aceleración=0)
# Aquí asumimos que fricción cinética ya y que la fuerza aplicada está moviendo el bloque, simplificación

a = F_neta / m

# Mostrar resultados
st.subheader("Resultados")
st.write(f"Peso: {peso:.2f} N")
st.write(f"Componente del peso paralelo al plano: {F_gravedad_paralela:.2f} N")
st.write(f"Fuerza normal: {F_gravedad_normal:.2f} N")
st.write(f"Fuerza de fricción (cinética): {F_friccion:.2f} N")
st.write(f"Fuerza neta: {F_neta:.2f} N")
st.write(f"Aceleración resultante: {a:.2f} m/s²")

# Graficar fuerzas y plano
mostrar_grafico = st.checkbox("Mostrar gráfico de fuerzas")

if mostrar_grafico:
    fig, ax = plt.subplots(figsize=(8,5))

    # Plano inclinado (línea)
    x_plane = np.array([0, 5])
    y_plane = np.tan(theta) * x_plane
    ax.plot(x_plane, y_plane, 'k-', linewidth=3)

    # Bloque en el plano (punto)
    x_block = 2.5
    y_block = np.tan(theta) * x_block
    ax.plot(x_block, y_block, 's', markersize=20, color='brown', label='Bloque')

    # Vector peso
    ax.arrow(x_block, y_block, 0, -1.5, head_width=0.1, head_length=0.2, fc='blue', ec='blue', label='Peso (mg)')

    # Vector fuerza normal (perpendicular al plano)
    Fn_dx = -1.5 * np.sin(theta)
    Fn_dy = 1.5 * np.cos(theta)
    ax.arrow(x_block, y_block, Fn_dx, Fn_dy, head_width=0.1, head_length=0.2, fc='green', ec='green', label='Fuerza Normal (N)')

    # Vector fuerza paralela al plano (peso paralelo)
    Fp_dx = 1.5 * np.cos(theta)
    Fp_dy = 1.5 * np.sin(theta)
    ax.arrow(x_block, y_block, Fp_dx, Fp_dy, head_width=0.1, head_length=0.2, fc='orange', ec='orange', label='Peso Paralelo al plano')

    # Vector fuerza de fricción (opuesto al movimiento)
    # Para dirección, asumimos que la fuerza aplicada mueve hacia arriba o abajo
    sentido_friccion = -np.sign(F_neta) if F_neta != 0 else 0
    Ff_dx = sentido_friccion * 1.2 * np.cos(theta)
    Ff_dy = sentido_friccion * 1.2 * np.sin(theta)
    ax.arrow(x_block, y_block, Ff_dx, Ff_dy, head_width=0.1, head_length=0.2, fc='red', ec='red', label='Fuerza de fricción')

    # Vector fuerza aplicada
    Fa_dx = 1.2 * np.cos(theta)
    Fa_dy = 1.2 * np.sin(theta)
    if F_aplicada < 0:
        Fa_dx, Fa_dy = -Fa_dx, -Fa_dy
    ax.arrow(x_block, y_block, Fa_dx, Fa_dy, head_width=0.1, head_length=0.2, fc='purple', ec='purple', label='Fuerza Aplicada')

    ax.set_xlim(x_block - 2, x_block + 2)
    ax.set_ylim(y_block - 2, y_block + 2)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Fuerzas en el plano inclinado')
    ax.grid(True)

    # Leyenda con líneas
    ax.legend(loc='upper right')

    st.pyplot(fig)
