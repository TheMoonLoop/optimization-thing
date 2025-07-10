import streamlit as st
import numpy as np
import importlib
import os

# Configuración inicial de la página
st.set_page_config(page_title="Optimización - Proyecto Final", layout="centered")

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 300px;
            max-width: 300px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

VALOR_DEFECTO_METODO = "Selecciona un método"

# Inicialización de variables de sesión (estado)
if "categoria_radio" not in st.session_state:
    st.session_state.categoria_radio = "Métodos Univariable"

if "select_uni" not in st.session_state:
    st.session_state.select_uni = VALOR_DEFECTO_METODO

if "select_multi" not in st.session_state:
    st.session_state.select_multi = VALOR_DEFECTO_METODO

if "seleccion" not in st.session_state:
    st.session_state.seleccion = None

# Ruta donde se encuentran los métodos
metodos_path = "metodos"
uni_modulos = {}    # Diccionario para métodos univariables
multi_modulos = {}  # Diccionario para métodos multivariables

# Diccionario de funciones disponibles para probar los métodos
# Cada categoría contiene funciones junto con sus respectivos rangos
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
            lambda x, y: 20 + (x**2 - 10 * np.cos(2 * np.pi * x)) + (y**2 - 10 * np.cos(2 * np.pi * y)),
            ((-5.12, 5.12), (-5.12, 5.12))
        ),
        "Ackley": (
            lambda x, y: -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
                         - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
                         + 20 + np.exp(1),
            ((-32.768, 32.768), (-32.768, 32.768))
        ),
        "Sphere": (
            lambda x, y: x**2 + y**2,
            ((-100, 100), (-100, 100))
        ),
        "Rosenbrock": (
            lambda x, y: 100 * (y - x**2)**2 + (1 - x)**2,
            ((-100, 100), (-100, 100))
        ),
        "Beale": (
            lambda x, y: (1.5 - x + x*y)**2
                         + (2.25 - x + x*y**2)**2
                         + (2.625 - x + x*y**3)**2,
            ((-4.5, 4.5), (-4.5, 4.5))
        ),
        "Booth": (
            lambda x, y: (x + 2*y - 7)**2 + (2*x + y - 5)**2,
            ((-10, 10), (-10, 10))
        ),
        "Himmelblau": (
            lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2,
            ((-5, 5), (-5, 5))
        ),
        "McCormick": (
            lambda x, y: np.sin(x + y) + (x - y)**2 - 1.5*x + 2.5*y + 1,
            ((-1.5, 4), (-3, 4))
        )
    }
}

# Carga dinámica de módulos desde la carpeta "metodos/"
# Se organizan en univariables y multivariables según el prefijo del archivo
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

# SIDEBAR - Interfaz lateral para seleccionar métodos y funciones
with st.sidebar:
    # Selector de categoría principal
    categoria = st.radio(
        "Selecciona una categoría",
        ["Métodos Univariable", "Métodos Multivariable"],
        key="categoria_radio",
        index=0
    )

    # Selector de métodos univariables
    if categoria == "Métodos Univariable" and uni_modulos:
        opciones_uni = list(uni_modulos.keys())
        seleccion = st.selectbox(
            "Método univariable",
            [VALOR_DEFECTO_METODO] + opciones_uni,
            key="select_uni"
        )
        if seleccion in opciones_uni:
            st.session_state.seleccion = seleccion
        else:
            st.session_state.seleccion = None
        st.session_state.select_multi = VALOR_DEFECTO_METODO

    # Selector de métodos multivariables
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

    # Selector de funciones para métodos univariables
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

    # Selector de funciones para métodos multivariables
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

# CONTENIDO PRINCIPAL
# Si no hay ningún método seleccionado, mostrar mensaje de bienvenida
if not st.session_state.seleccion:
    st.title("Métodos de Optimización")
    st.markdown("Selecciona un método en el menú lateral para visualizarlo.")
else:
    # Ejecutar el método seleccionado
    seleccion = st.session_state.seleccion

    # Método univariable
    if seleccion in uni_modulos:
        if funcion_actual is not None and intervalo_actual is not None:
            uni_modulos[seleccion].run(funcion_actual, intervalo_actual)
        else:
            st.warning("Selecciona una función univariable válida.")
    
    # Método multivariable
    elif seleccion in multi_modulos:
        if funcion_actual is not None and intervalo_actual is not None:
            multi_modulos[seleccion].run(funcion_actual, intervalo_actual)
        else:
            st.warning("Selecciona una función multivariable válida.")
