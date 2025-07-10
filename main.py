import streamlit as st
import numpy as np
import importlib
import os

st.set_page_config(page_title="Optimización - Proyecto Final", layout="centered")
VALOR_DEFECTO_METODO = "Selecciona un método"

if "categoria_radio" not in st.session_state:
    st.session_state.categoria_radio = "Métodos Univariable"

if "select_uni" not in st.session_state:
    st.session_state.select_uni = VALOR_DEFECTO_METODO

if "select_multi" not in st.session_state:
    st.session_state.select_multi = VALOR_DEFECTO_METODO

if "seleccion" not in st.session_state:
    st.session_state.seleccion = None

metodos_path = "metodos"
uni_modulos = {}
multi_modulos = {}

funciones = {
    "uni": {
        "Área Lata": (lambda r: 2*np.pi*r**2 + 500/r, (0.1, 10)),
        "Volumen Caja": (lambda l: -(4*l**3 - 60*l**2 + 200*l), (2, 3)),
        "Función 1": (lambda x: x**2 + 54/x if x != 0 else float('inf'), (0.1, 10)),
        "Función 2": (lambda x: x**3 + 2*x - 3, (0, 5)),
        "Función 3": (lambda x: x**4 + x**2 - 33, (-2.5, 2.5)),
        "Función 4": (lambda x: 3*x**4 - 8*x**3 - 6*x**2 + 12*x, (-1.5, 3))
    },
    "multi": {
        "Rastrigin": (
            lambda x: 10*len(x) + sum(xi**2 - 10 * np.cos(2*np.pi*xi) for xi in x),
            (-5.12, 5.12)
        ),
        "Ackley": (
            lambda x: -20 * np.exp(-0.2 * np.sqrt(1/len(x) * sum(xi**2 for xi in x)))
                      - np.exp(1/len(x) * sum(np.cos(2*np.pi*xi) for xi in x))
                      + 20 + np.exp(1),
            (-32.768, 32.768)
        ),
        "Sphere": (lambda x: sum(xi**2 for xi in x), (-100, 100)),
        "Rosenbrock": (
            lambda x: sum(100 * (x[i + 1] - x[i]**2)**2 + (1 - x[i])**2 for i in range(len(x) - 1)),
            (-100, 100)
        ),
        "Beale": (
            lambda x,y: (1.5 - x + x*y)**2
                        + (2.25 - x + x*y**2)**2
                        + (2.625 - x + x*y**3)**2,
            ((-4.5, 4.5), (-4.5, 4.5))
        ),
        "Booth": (lambda x,y: (x + 2*y - 7)**2 + (2*x + y - 5)**2, (-10,10), (-10,10)),
        "Himmelblau": (lambda x,y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2, ((-5, 5), (-5, 5))),
        "McCormick": (lambda x,y: np.sin(x+y) + (x-y)**2 - 1.5*x + 2.5*y + 1, (-1.5,4), (-3,4))
    }
}

for filename in os.listdir(metodos_path):
    if filename.endswith(".py") and filename != "__init__.py":
        nombre_archivo = filename[:-3]
        try:
            modulo = importlib.import_module(f"{metodos_path}.{nombre_archivo}")
            if hasattr(modulo, "run"):
                nombre_legible = nombre_archivo.replace("_", " ").title()
                if nombre_archivo.startswith("uni_"):
                    nombre_legible = nombre_archivo[4:].replace("_", " ").title()
                    uni_modulos[nombre_legible] = modulo
                elif nombre_archivo.startswith("multi_"):
                    nombre_legible = nombre_archivo[6:].replace("_", " ").title()
                    multi_modulos[nombre_legible] = modulo
        except Exception as e:
            st.warning(f"No se pudo cargar {nombre_archivo}: {e}")

with st.sidebar:
    categoria = st.radio(
        "Selecciona una categoría",
        ["Métodos Univariable", "Métodos Multivariable"],
        key="categoria_radio",
        index=0
    )

    # Selección de método univariable
    if categoria == "Métodos Univariable" and uni_modulos:
        opciones_uni = list(uni_modulos.keys())
        seleccion = st.selectbox(
            "Método univariable",
            [VALOR_DEFECTO_METODO] + opciones_uni,
            key="select_uni"
        )
        # Validación
        if seleccion in opciones_uni:
            st.session_state.seleccion = seleccion
        else:
            st.session_state.seleccion = None
        st.session_state.select_multi = VALOR_DEFECTO_METODO

    # Selección de método multivariable
    elif categoria == "Métodos Multivariable" and multi_modulos:
        opciones_multi = list(multi_modulos.keys())
        seleccion = st.selectbox(
            "Método multivariable",
            [VALOR_DEFECTO_METODO] + opciones_multi,
            key="select_multi"
        )
        if seleccion in opciones_multi:
            st.session_state.seleccion = seleccion
        else:
            st.session_state.seleccion = None
        st.session_state.select_uni = VALOR_DEFECTO_METODO

    # Funciones univariable
    if categoria == "Métodos Univariable":
        metodo_seleccionado = st.session_state.get("select_uni", VALOR_DEFECTO_METODO)
        funciones_desactivado = metodo_seleccionado == VALOR_DEFECTO_METODO

        opciones_func_uni = list(funciones["uni"].keys())
        seleccion_funcion = st.selectbox(
            "Selecciona una función univariable",
            opciones_func_uni,
            key="funcion_select_uni",
            disabled=funciones_desactivado
        )

        if not funciones_desactivado and seleccion_funcion in opciones_func_uni:
            funcion_actual, intervalo_actual = funciones["uni"][seleccion_funcion]
        else:
            funcion_actual, intervalo_actual = None, None

    # Funciones multivariable
    elif categoria == "Métodos Multivariable":
        metodo_seleccionado = st.session_state.get("select_multi", VALOR_DEFECTO_METODO)
        funciones_desactivado = metodo_seleccionado == VALOR_DEFECTO_METODO

        opciones_func_multi = list(funciones["multi"].keys())
        seleccion_funcion = st.selectbox(
            "Selecciona una función multivariable",
            opciones_func_multi,
            key="funcion_select_multi",
            disabled=funciones_desactivado
        )

        if not funciones_desactivado and seleccion_funcion in opciones_func_multi:
            funcion_actual, intervalo_actual = funciones["multi"][seleccion_funcion]
        else:
            funcion_actual, intervalo_actual = None, None

if not st.session_state.seleccion:
    st.title("Métodos de Optimización")
    st.markdown("Selecciona un método en el menú lateral para visualizarlo.")
else:
    seleccion = st.session_state.seleccion

    if seleccion in uni_modulos:
        if funcion_actual is not None and intervalo_actual is not None:
            uni_modulos[seleccion].run(funcion_actual, intervalo_actual)
        else:
            st.warning("Selecciona una función univariable válida.")
    
    elif seleccion in multi_modulos:
        if funcion_actual is not None and intervalo_actual is not None:
            multi_modulos[seleccion].run(funcion_actual, intervalo_actual)
        else:
            st.warning("Selecciona una función multivariable válida.")
