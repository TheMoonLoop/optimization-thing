import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def golden_section(funcion, a, b, iteraciones):
    puntos = []
    gr = (np.sqrt(5) + 1) / 2
    for _ in range(iteraciones):
        x1 = b - (b - a) / gr
        x2 = a + (b - a) / gr
        f1 = funcion(x1)
        f2 = funcion(x2)
        puntos.extend([x1, x2])

        if f1 < f2:
            b = x2
        else:
            a = x1
    return a, b, puntos

def run(funcion, intervalo):
    st.subheader("Golden Section Search")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="gold_")
    if resultado[0] is None:
        return

    (a, b), _, _, iteraciones = resultado

    a_final, b_final, puntos = golden_section(funcion, a, b, iteraciones)

    st.success(f"Intervalo final aproximado: [{a_final:.6f}, {b_final:.6f}]")

    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'k-', label="f(x)")
    ax.plot(puntos, [funcion(x) for x in puntos], 'ro', label="Evaluaciones")
    ax.grid()
    ax.legend()
    st.pyplot(fig)
