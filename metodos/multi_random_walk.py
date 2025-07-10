import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def random_walk(funcion, x0, sigma, pasos):
    x = np.array(x0)
    mejor = x.copy()
    mejor_valor = funcion(mejor)
    ruta = [mejor.copy()]
    historial = [mejor_valor]

    for _ in range(pasos):
        candidato = x + np.random.normal(0, sigma, size=len(x))
        val = funcion(candidato)
        if val < mejor_valor:
            mejor = candidato.copy()
            mejor_valor = val
        ruta.append(mejor.copy())
        historial.append(mejor_valor)
        x = candidato
    return mejor, historial, ruta

def run(funcion, intervalo):
    st.subheader("Método de Caminata Aleatoria")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="random_")
    if resultado[0] is None:
        return

    (x_range, y_range), _, precision, iteraciones = resultado
    x0 = [(x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2]

    mejor, historial, ruta = random_walk(
        lambda v: funcion(v[0], v[1]), x0, sigma=precision, pasos=iteraciones
    )

    st.success(f"Mejor solución: {mejor} con valor mínimo {historial[-1]:.6f}")

    x = np.linspace(x_range[0], x_range[1], 300)
    y = np.linspace(y_range[0], y_range[1], 300)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: funcion(x, y))(X, Y)

    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, levels=50, cmap="viridis")
    ax.plot([p[0] for p in ruta], [p[1] for p in ruta], "r--o", label="Trayectoria")
    ax.plot(mejor[0], mejor[1], "g*", markersize=12, label="Resultado final")
    ax.set_title("Caminata Aleatoria")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    st.pyplot(fig)
