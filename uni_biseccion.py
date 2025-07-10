import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def derivada_central(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)

def biseccion_derivada(funcion, a, b, epsilon, iteraciones):
    puntos = [a, b]
    for _ in range(iteraciones):
        z = (a + b) / 2
        puntos.append(z)
        fz_deriv = derivada_central(funcion, z)
        if abs(fz_deriv) <= epsilon:
            break
        if fz_deriv < 0:
            a = z
        else:
            b = z
    return puntos, [funcion(x) for x in puntos]

def run(funcion, intervalo):
    st.subheader("Método de Bisección (por derivada)")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="biseccion_")
    if resultado[0] is None:
        return

    (a, b), _, precision, iteraciones = resultado

    puntos, valores = biseccion_derivada(funcion, a, b, epsilon=precision, iteraciones=iteraciones)

    st.success(f"Última estimación: x ≈ {puntos[-1]:.6f}, f(x) ≈ {valores[-1]:.6f}")

    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color="black")
    ax.plot(puntos, valores, 'ro', label="Iteraciones")
    ax.axvline(puntos[-1], color="green", linestyle="--", label="Resultado")
    ax.grid(), ax.legend()
    st.pyplot(fig)
