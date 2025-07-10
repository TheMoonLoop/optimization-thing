import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def derivada_central(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

def newton_raphson(funcion, x0, iteraciones):
    puntos = [x0]
    for _ in range(iteraciones):
        df = derivada_central(funcion, x0)
        ddf = derivada_central(lambda x: derivada_central(funcion, x), x0)

        if ddf == 0:
            break

        x0 = x0 - df / ddf
        puntos.append(x0)

    return x0, puntos

def run(funcion, intervalo):
    st.subheader("Método de Newton-Raphson")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="newton_")
    if resultado[0] is None:
        return

    (a, b), _, _, iteraciones = resultado
    x0 = (a + b) / 2

    resultado_final, puntos = newton_raphson(funcion, x0, iteraciones)

    st.success(f"Raíz estimada (mínimo): x = {resultado_final:.6f}")

    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'k-', label="f(x)")
    ax.plot(puntos, [funcion(x) for x in puntos], 'ro', label="Iteraciones")
    ax.axvline(resultado_final, color="g", linestyle="--", label="Resultado")
    ax.grid()
    ax.legend()
    st.pyplot(fig)
