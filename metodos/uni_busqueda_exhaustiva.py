import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from FuncCtrls import configurar_parametros

def busqueda_exhaustiva_iterativa(funcion, a, b, n):
    dx = (b - a) / n
    x1 = a
    x2 = x1 + dx
    x3 = x2 + dx

    puntos_x = [x1, x2, x3]
    puntos_y = [funcion(x1), funcion(x2), funcion(x3)]

    while x3 <= b:
        f1, f2, f3 = funcion(x1), funcion(x2), funcion(x3)
        puntos_x.append(x3)
        puntos_y.append(f3)

        if f1 >= f2 <= f3:
            return x2, puntos_x, puntos_y  # Mínimo local

        x1, x2 = x2, x3
        x3 = x2 + dx

    return None, puntos_x, puntos_y

def run(funcion, intervalo):
    st.subheader("Búsqueda Exhaustiva")

    resultado = configurar_parametros(funcion, intervalo)
    if resultado[0] is None:
        return

    intervalo_mod, n_puntos, precision, iteraciones = resultado

    a, b = intervalo_mod

    minimo, x_eval, y_eval = busqueda_exhaustiva_iterativa(funcion, a, b, n_puntos)

    if minimo is not None:
        st.success(f"Mínimo local aproximado encontrado en x = {minimo:.6f}")
    else:
        st.warning("No se encontró un mínimo local en este intervalo.")

    # Graficar
    x_vals = np.linspace(a, b, 1000)
    y_vals = np.vectorize(funcion)(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, 'k-', label='Función f(x)')
    ax.plot(x_eval, y_eval, 'ro', label='Evaluaciones')

    if minimo is not None:
        ax.axvline(minimo, color='g', linestyle='--', label=f'Mínimo estimado en x = {minimo:.4f}')

    ax.set_title(f'Búsqueda Exhaustiva con precisión {precision}')
    ax.set_xlabel('x'), ax.set_ylabel('f(x)')
    ax.grid(), ax.legend()
    st.pyplot(fig)
