import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def evaluar_vecinos(f, x, delta):
    vecinos = []
    for i in range(len(x)):
        for d in [delta, -delta]:
            punto = x.copy()
            punto[i] += d
            vecinos.append(punto)
    return vecinos

def hooke_jeeves(funcion, x0, delta_inicial, precision, max_iter):
    x_base = np.array(x0)
    delta = delta_inicial
    k = 0
    trayecto = [x_base.copy()]

    while delta > precision and k < max_iter:
        mejora = False
        vecinos = evaluar_vecinos(funcion, x_base, delta)
        x_nuevo = x_base

        for vecino in vecinos:
            if funcion(vecino) < funcion(x_nuevo):
                x_nuevo = vecino
                mejora = True

        if mejora:
            x_base = x_nuevo
            trayecto.append(x_base.copy())
        else:
            delta /= 2

        k += 1

    return x_base, trayecto

def run(funcion, intervalo):
    st.subheader("Método de Hooke-Jeeves")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="hooke_")
    if resultado[0] is None:
        return

    (x_range, y_range), _, precision, iteraciones = resultado
    x0 = [(x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2]
    st.markdown(f"Punto inicial: {x0}")

    resultado_final, trayecto = hooke_jeeves(funcion, x0, delta_inicial=1.0, precision=precision, max_iter=iteraciones)

    st.success(f"Resultado final: {resultado_final}")

    x = np.linspace(x_range[0], x_range[1], 300)
    y = np.linspace(y_range[0], y_range[1], 300)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: funcion([x, y]))(X, Y)

    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, levels=50, cmap="viridis")
    ax.plot([p[0] for p in trayecto], [p[1] for p in trayecto], "ro--", label="Iteraciones")
    ax.plot(resultado_final[0], resultado_final[1], "g*", markersize=12, label="Resultado")
    ax.set_title("Método de Hooke-Jeeves")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    st.pyplot(fig)
