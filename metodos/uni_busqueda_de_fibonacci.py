import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from FuncCtrls import configurar_parametros

def fibonacci(n):
    F = [1, 1]
    for i in range(2, n+1):
        F.append(F[-1] + F[-2])
    return F

def metodo_fibonacci(funcion, a, b, n):
    puntos = []
    F = fibonacci(n)
    for k in range(1, n):
        l1 = a + (F[n-k-1]/F[n-k+1]) * (b - a)
        l2 = a + (F[n-k]/F[n-k+1]) * (b - a)
        f1 = funcion(l1)
        f2 = funcion(l2)
        puntos.extend([l1, l2])

        if f1 > f2:
            a = l1
        else:
            b = l2
    return a, b, puntos

def run(funcion, intervalo):
    st.subheader("Método de Fibonacci")

    resultado = configurar_parametros(funcion, intervalo, clave_prefix="fib_")
    if resultado[0] is None:
        return

    (a, b), _, _, iteraciones = resultado

    a_final, b_final, puntos = metodo_fibonacci(funcion, a, b, iteraciones)

    st.success(f"Intervalo final aproximado: [{a_final:.6f}, {b_final:.6f}]")

    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'k-', label="f(x)")
    ax.plot(puntos, [funcion(x) for x in puntos], 'ro', label="Evaluaciones")
    ax.grid()
    ax.legend()
    st.pyplot(fig)
