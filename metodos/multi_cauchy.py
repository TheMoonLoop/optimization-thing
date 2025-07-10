import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def gradiente(f, x, deltaX=0.001):
    grad = []
    for i in range(len(x)):
        xp = x.copy()
        xn = x.copy()
        xp[i] += deltaX
        xn[i] -= deltaX
        grad.append((f(xp) - f(xn)) / (2 * deltaX))
    return grad

def w_to_x(w, a, b):
    return w * (b - a) + a

def busqueda_dorada(funcion, epsilon=1e-3, a=0.0, b=1.0):
    PHI = (1 + np.sqrt(5)) / 2 - 1
    aw, bw = 0, 1
    Lw = 1
    while Lw > epsilon:
        w2 = aw + PHI * Lw
        w1 = bw - PHI * Lw
        fx1 = funcion(w_to_x(w1, a, b))
        fx2 = funcion(w_to_x(w2, a, b))
        if fx1 > fx2:
            aw = w1
        else:
            bw = w2
        Lw = bw - aw
    return w_to_x((aw + bw) / 2, a, b)

def cauchy(funcion, x0, epsilon1, epsilon2, M):
    xk = x0
    k = 0
    puntos = [x0.copy()]
    while True:
        grad = np.array(gradiente(funcion, xk))

        if np.linalg.norm(grad) < epsilon1 or k >= M:
            break

        def alpha_funcion(alpha):
            return funcion(xk - alpha * grad)

        alpha = busqueda_dorada(alpha_funcion, epsilon2)
        x_k1 = xk - alpha * grad
        puntos.append(x_k1.copy())

        crit_four = abs(np.dot(gradiente(funcion, x_k1), grad))
        if crit_four <= epsilon2:
            break

        delta = np.linalg.norm(x_k1 - xk) / (np.linalg.norm(xk) + 1e-5)
        if delta <= epsilon1:
            break

        k += 1
        xk = x_k1

    return xk, puntos

def run(funcion, intervalo):
    st.subheader("Método de Cauchy")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="cauchy_")
    if resultado[0] is None:
        return

    (x_range, y_range), _, epsilon1, iteraciones = resultado
    x0 = np.array([(x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2])

    st.markdown(f"Punto inicial: {x0}")

    resultado_final, trayecto = cauchy(funcion, x0, epsilon1, epsilon1, iteraciones)

    st.success(f"Solución encontrada: {resultado_final}")

    x = np.linspace(x_range[0], x_range[1], 300)
    y = np.linspace(y_range[0], y_range[1], 300)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: funcion([x, y]))(X, Y)

    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, levels=50, cmap="viridis")
    ax.plot([p[0] for p in trayecto], [p[1] for p in trayecto], "r--o", label="Iteraciones")
    ax.plot(resultado_final[0], resultado_final[1], "g*", markersize=12, label="Resultado final")
    ax.set_title("Trayectoria del método de Cauchy")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    st.pyplot(fig)
