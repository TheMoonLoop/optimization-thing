import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def gradiente(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        xh1, xh2 = x.copy(), x.copy()
        xh1[i] += h
        xh2[i] -= h
        grad.append((f(xh1[0], xh1[1]) - f(xh2[0], xh2[1])) / (2 * h))
    return np.array(grad)

def hessiano(f, x, h=1e-5):
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            xp, xm = x.copy(), x.copy()
            xp[i] += h
            xp[j] += h
            xm[i] -= h
            xm[j] -= h
            fpp = f(xp[0], xp[1])
            fmm = f(xm[0], xm[1])
            xp[i] -= 2*h
            xm[j] -= 2*h
            fpm = f(xp[0], xp[1])
            fmp = f(xm[0], xm[1])
            H[i, j] = (fpp + fmm - fpm - fmp) / (4 * h**2)
    return H

def newton(f, x0, epsilon, max_iter):
    x = x0.copy()
    trayecto = [x.copy()]
    for _ in range(max_iter):
        g = gradiente(f, x)
        H = hessiano(f, x)
        try:
            delta = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError:
            break
        x = x + delta
        trayecto.append(x.copy())
        if np.linalg.norm(g) < epsilon:
            break
    return x, trayecto

def run(funcion, intervalo):
    st.subheader("Método de Newton Multivariable")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="newton_")
    if resultado[0] is None:
        return

    (x_range, y_range), _, epsilon, iteraciones = resultado
    x0 = np.array([(x_range[0] + x_range[1]) / 2, (y_range[0] + y_range[1]) / 2])
    st.markdown(f"Punto inicial: {x0}")

    resultado_final, trayecto = newton(funcion, x0, epsilon, iteraciones)

    st.success(f"Resultado final: {resultado_final}")

    x = np.linspace(x_range[0], x_range[1], 300)
    y = np.linspace(y_range[0], y_range[1], 300)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda x, y: funcion(x, y))(X, Y)

    fig, ax = plt.subplots()
    ax.contourf(X, Y, Z, levels=50, cmap="viridis")
    ax.plot([p[0] for p in trayecto], [p[1] for p in trayecto], "ro--", label="Iteraciones")
    ax.plot(resultado_final[0], resultado_final[1], "g*", markersize=12, label="Resultado")
    ax.set_title("Método de Newton")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    st.pyplot(fig)
