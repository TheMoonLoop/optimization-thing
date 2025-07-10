import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import uuid
from FuncCtrls import configurar_parametros

def nelder_mead(funcion, x_start, y_start, precision, iteraciones):
    alpha = 1
    gamma = 2
    rho   = 0.5
    sigma = 0.5

    p1 = np.array([x_start, y_start])
    p2 = p1 + np.array([precision, 0])
    p3 = p1 + np.array([0, precision])
    puntos = [p1.copy()]

    for _ in range(iteraciones):
        simplex = sorted([p1, p2, p3], key=lambda p: funcion(p[0], p[1]))
        p1, p2, p3 = simplex
        puntos.append(p1.copy())

        centroid = (p1 + p2) / 2

        p_reflex = centroid + alpha * (centroid - p3)
        f_reflex = funcion(p_reflex[0], p_reflex[1])
        f1 = funcion(p1[0], p1[1])
        f2 = funcion(p2[0], p2[1])
        f3 = funcion(p3[0], p3[1])

        if f1 <= f_reflex < f2:
            p3 = p_reflex
        elif f_reflex < f1:
            p_expand = centroid + gamma * (p_reflex - centroid)
            if funcion(p_expand[0], p_expand[1]) < f_reflex:
                p3 = p_expand
            else:
                p3 = p_reflex
        else:
            p_contra = centroid + rho * (p3 - centroid)
            if funcion(p_contra[0], p_contra[1]) < f3:
                p3 = p_contra
            else:
                p2 = p1 + sigma * (p2 - p1)
                p3 = p1 + sigma * (p3 - p1)
    return p1, puntos

def run(funcion, intervalo):
    st.subheader("Método de Nelder-Mead (Simplex)")
    clave_unica = "nelder_" + str(uuid.uuid4())
    resultado = configurar_parametros(funcion, intervalo, clave_prefix=clave_unica)
    if resultado[0] is None:
        return

    intervalo_mod, _, precision, iteraciones = resultado
    if (
        not isinstance(intervalo_mod, tuple)
        or len(intervalo_mod) != 2
        or not all(isinstance(sub, tuple) and len(sub) == 2 for sub in intervalo_mod)
    ):
        st.error("Esta función requiere dos variables (x, y) con intervalos correctamente definidos.")
        return

    x_range, y_range = intervalo_mod

    x0 = (x_range[0] + x_range[1]) / 2
    y0 = (y_range[0] + y_range[1]) / 2

    st.markdown(f"Punto inicial: ({x0:.3f}, {y0:.3f})")
    resultado_final, trayecto = nelder_mead(funcion, x0, y0, precision, iteraciones)
    st.success(f"Punto estimado de mínimo: ({resultado_final[0]:.6f}, {resultado_final[1]:.6f})")

    x = np.linspace(x_range[0], x_range[1], 300)
    y = np.linspace(y_range[0], y_range[1], 300)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: funcion(x, y))(X, Y)

    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, levels=50, cmap="viridis")
    ax.plot([p[0] for p in trayecto], [p[1] for p in trayecto], 'ro--', label="Iteraciones")
    ax.plot(resultado_final[0], resultado_final[1], 'g*', markersize=12, label="Resultado")
    ax.set_title("Trayectoria del método Nelder-Mead")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    st.pyplot(fig)
