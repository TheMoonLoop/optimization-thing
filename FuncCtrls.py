import streamlit as st

def configurar_parametros(funcion, intervalo_por_defecto, clave_prefix=""):
    st.markdown("### Parámetros de búsqueda")

    MAX_PUNTOS = 10000  # límite superior para puntos

    # Identificar tipo de función
    es_vector = callable(funcion) and (funcion.__code__.co_argcount == 1)
    es_doble = callable(funcion) and (funcion.__code__.co_argcount == 2)

    # Fila de parámetros: precisión, inferior, superior, iteraciones
    col_prec, col_inf, col_sup, col_iter = st.columns([1.2, 1, 1, 1.3])

    with col_prec:
        precision = st.selectbox(
            "Precisión",
            [0.5, 0.1, 0.01, 0.0001],
            index=1,
            key=clave_prefix + "precision"
        )

    if es_vector:
        with col_inf:
            a = st.number_input("Inferior", value=float(intervalo_por_defecto[0]), key=clave_prefix + "rango_inf")
        with col_sup:
            b = st.number_input("Superior", value=float(intervalo_por_defecto[1]), key=clave_prefix + "rango_sup")
        with col_iter:
            iteraciones = st.number_input(
                "Iteraciones",
                min_value=1,
                max_value=1000,
                value=100,
                step=1,
                key=clave_prefix + "iteraciones"
            )

        if a >= b:
            st.error("El límite inferior debe ser menor que el superior.")
            return None, None, None, None

        n_puntos = int((b - a) / precision)
        if n_puntos > MAX_PUNTOS:
            st.warning(f"Demasiados puntos calculados ({n_puntos}). Se limitará a {MAX_PUNTOS}.")
            n_puntos = MAX_PUNTOS

        return (a, b), n_puntos, precision, iteraciones

    elif es_doble:
        with col_iter:
            iteraciones = st.number_input(
                "Iteraciones",
                min_value=1,
                max_value=1000,
                value=100,
                step=1,
                key=clave_prefix + "iteraciones"
            )

        st.markdown("#### Rango de x e y")
        col_x1, col_x2 = st.columns(2)
        with col_x1:
            x_min = st.number_input("x min", value=float(intervalo_por_defecto[0][0]), key=clave_prefix + "x_min")
        with col_x2:
            x_max = st.number_input("x max", value=float(intervalo_por_defecto[0][1]), key=clave_prefix + "x_max")

        col_y1, col_y2 = st.columns(2)
        with col_y1:
            y_min = st.number_input("y min", value=float(intervalo_por_defecto[1][0]), key=clave_prefix + "y_min")
        with col_y2:
            y_max = st.number_input("y max", value=float(intervalo_por_defecto[1][1]), key=clave_prefix + "y_max")

        if x_min >= x_max or y_min >= y_max:
            st.error("Los límites deben estar correctamente definidos (min < max).")
            return None, None, None, None

        n_puntos = int(((x_max - x_min) + (y_max - y_min)) / (2 * precision))
        if n_puntos > MAX_PUNTOS:
            st.warning(f"Demasiados puntos calculados ({n_puntos}). Se limitará a {MAX_PUNTOS}.")
            n_puntos = MAX_PUNTOS

        return ((x_min, x_max), (y_min, y_max)), n_puntos, precision, iteraciones

    else:
        st.error("No se pudo interpretar el tipo de función.")
        return None, None, None, None
