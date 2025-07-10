import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def intervalo_mitad(funcion, a, b, iteraciones):
    puntos = []
    for _ in range(iteraciones):
        xm = (a + b) / 2
        puntos.append(xm)
        f1 = funcion(a)
        f2 = funcion(b)
        fm = funcion(xm)

        if f1 < f2:
            b = xm
        else:
            a = xm
    return a, b, puntos

def run(funcion, intervalo):
    st.subheader("Método de División por la Mitad")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="mitad_")
    if resultado[0] is None:
        return

    (a, b), _, _, iteraciones = resultado

    a_final, b_final, puntos = intervalo_mitad(funcion, a, b, iteraciones)

    st.success(f"Intervalo final aproximado: [{a_final:.6f}, {b_final:.6f}]")

    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'k-', label="f(x)")
    ax.plot(puntos, [funcion(x) for x in puntos], 'ro', label="Evaluaciones")
    ax.grid()
    ax.legend()
    st.pyplot(fig)
