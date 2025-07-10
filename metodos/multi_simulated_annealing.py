import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def simulated_annealing(funcion, x0, sigma, alpha, pasos, w):
    x = np.array(x0)
    mejor = x.copy()
    f_mejor = funcion(mejor)
    T = 1.0
    ruta = [x.copy()]
    historial = [f_mejor]
    iteracion = 0

    while iteracion < pasos and T > 1e-8:
        for _ in range(w):
            vecino = x + np.random.normal(0, sigma, size=len(x))
            f_vecino = funcion(vecino)

            if f_vecino < f_mejor:
                mejor = vecino.copy()
                f_mejor = f_vecino
                x = vecino.copy()
            else:
                delta = f_vecino - funcion(x)
                if np.exp(-delta / T) >= np.random.uniform():
                    x = vecino.copy()

            ruta.append(x.copy())
            historial.append(f_mejor)

        T *= alpha
        iteracion += 1

    return mejor, historial, ruta

def run(funcion, intervalo):
    st.subheader("Método de Recocido Simulado (Simulated Annealing)")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="anneal_")
    if resultado[0] is None:
        return

    (x_range, y_range), _, precision, iteraciones = resultado
    x0 = [(x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2]

    alpha = st.slider("Factor de enfriamiento (alpha)", min_value=0.80, max_value=0.99, step=0.01, value=0.95)
    w = st.slider("Vecinos por temperatura (w)", min_value=1, max_value=50, value=20)

    mejor, historial, ruta = simulated_annealing(
        lambda v: funcion(v[0], v[1]), x0, sigma=precision, alpha=alpha, pasos=iteraciones, w=w
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
    ax.set_title("Simulated Annealing")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    st.pyplot(fig)
