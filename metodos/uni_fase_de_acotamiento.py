import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def diferencia_central(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

def fase_de_acotamiento(funcion, x0, delta, max_iter):
    puntos = [x0]
    f_derivada = lambda x: diferencia_central(funcion, x)

    if f_derivada(x0) > 0:
        delta = -delta

    x1 = x0 + delta
    puntos.append(x1)

    for _ in range(max_iter):
        if funcion(x1) < funcion(x0):
            x0 = x1
            x1 = x0 + delta
            puntos.append(x1)
        else:
            break

    x2 = x1
    x1 = x0
    x0 = x0 - delta

    a = min(x0, x2)
    b = max(x0, x2)
    return a, b, puntos

def run(funcion, intervalo):
    st.subheader("Método de Fase de Acotamiento")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="fase_")
    if resultado[0] is None:
        return

    (a, b), _, precision, iteraciones = resultado

    x0 = (a + b) / 2
    delta = precision

    st.markdown(f"Parámetros seleccionados: x₀ = {x0:.4f}, Δ = {delta}, iteraciones = {iteraciones}")

    a_final, b_final, puntos = fase_de_acotamiento(funcion, x0, delta, iteraciones)

    st.success(f"Intervalo acotado: [{a_final:.6f}, {b_final:.6f}]")

    # Visualización
    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color="black")
    ax.axvline(a_final, color="blue", linestyle="--", label="a")
    ax.axvline(b_final, color="blue", linestyle="--", label="b")
    ax.plot(puntos, [funcion(x) for x in puntos], 'ro', label="Evaluaciones")
    ax.set_title("Fase de Acotamiento")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid()
    ax.legend()
    st.pyplot(fig)
