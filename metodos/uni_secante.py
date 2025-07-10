import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def derivada_central(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)

def metodo_secante(funcion, x1, x2, epsilon, iteraciones):
    puntos = [x1, x2]
    for _ in range(iteraciones):
        f1 = derivada_central(funcion, x1)
        f2 = derivada_central(funcion, x2)
        denom = f2 - f1
        if denom == 0:
            break
        x3 = x2 - f2 * (x2 - x1) / denom
        puntos.append(x3)
        if abs(derivada_central(funcion, x3)) <= epsilon:
            break
        x1, x2 = x2, x3
    return puntos, [funcion(x) for x in puntos]

def run(funcion, intervalo):
    st.subheader("Método de la Secante (por derivada)")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="secante_")
    if resultado[0] is None:
        return

    (a, b), _, precision, iteraciones = resultado

    puntos, valores = metodo_secante(funcion, a, b, epsilon=precision, iteraciones=iteraciones)

    st.success(f"Última estimación: x ≈ {puntos[-1]:.6f}, f(x) ≈ {valores[-1]:.6f}")

    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="f(x)", color="black")
    ax.plot(puntos, valores, 'ro', label="Iteraciones")
    ax.axvline(puntos[-1], color="green", linestyle="--", label="Resultado")
    ax.grid(), ax.legend()
    st.pyplot(fig)
