import streamlit as st

# Tabla de equivalencia de opioides (en mg y factores de conversión para diferentes vías)
opioid_conversion_table = {
    "fentanilo": {"iv": 100, "patch": {
        "25": 90, "50": 160, "75": 200, "100": 275, "125": 325, "150": 400, "175": 450, "200": 525
    }},
    "buprenorfina": {"patch": {"10": 30, "20": 60, "35": 90, "52.5": 120, "70": 180}},
    "hidromorfona": {"oral": 5, "iv": 5},
    "oxicodona": {"oral": 1.5, "iv": 2},
    "morfina": {"oral": 1, "iv": 3, "sc": 2},
    "hidrocodona": {"oral": 1},
    "tapentadol": {"oral": 3.3},
    "tramadol": {"oral": 4, "iv": 10},
    "metadona": {"oral": {
        "<=90": 4, "91-300": 8, ">300": 12
    }, "to_morphine_oral": 5},
    "codeina": {"oral": 10}
}

more_potent_opioids = ["hidromorfona", "metadona", "oxicodona", "fentanilo"]
less_potent_opioids = ["tapentadol", "tramadol", "codeina"]


def main():
    st.title("Rotación de Opioides")
    st.write("Ingrese el opioide actual, la vía de administración y el opioide al que desea rotar con la vía de administración deseada para obtener la dosis equivalente.")

    # Organizar la selección de opciones en columnas
    conversion_factor = st.radio("Seleccione el factor de conversión entre morfina oral e IV", (2, 3))
    col1, col2 = st.columns(2)

    with col1:
        # Seleccionar opioides, vías de administración y dosis actual
        current_opioid = st.selectbox("Seleccione el opioide actual", list(opioid_conversion_table.keys()))
        available_routes = [route for route, factor in opioid_conversion_table[current_opioid].items() if factor is not None]
        current_route = st.selectbox("Seleccione la vía de administración actual", available_routes)
        current_dose = st.number_input("Ingrese la dosis actual en mg", min_value=0.0, step=1.0)

    with col2:
        target_opioid = st.selectbox("Seleccione el opioide al que desea rotar", list(opioid_conversion_table.keys()))
        available_target_routes = [route for route, factor in opioid_conversion_table[target_opioid].items() if factor is not None]
        target_route = st.selectbox("Seleccione la vía de administración deseada", available_target_routes)

    if st.button("Calcular Dosis Equivalente"):
        if current_dose > 0:
            try:
                target_dose = calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose, conversion_factor)
                st.success(f"La dosis equivalente de {target_opioid} ({target_route}) es {target_dose}")
            except TypeError:
                st.error("La conversión solicitada no es válida para la combinación de opioide y vía seleccionados.")
            except ValueError as e:
                st.error(str(e))
        else:
            st.warning("Por favor, ingrese una dosis válida mayor que 0.")

def calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose, conversion_factor):
    # Verificar la disponibilidad de las presentaciones para la conversión
    if opioid_conversion_table[current_opioid].get(current_route) is None:
        raise TypeError("La conversión solicitada no es válida para la combinación de opioide y vía seleccionados.")

    # Paso 1: Convertir la dosis actual al equivalente en morfina por la misma vía
    if current_opioid != "morfina":
        morphine_dose = current_dose * opioid_conversion_table[current_opioid][current_route]
    else:
        morphine_dose = current_dose

    # Paso 2: Convertir la dosis de morfina a la vía deseada
    if current_route == "oral" and target_route == "iv":
        morphine_dose = morphine_dose / conversion_factor
    elif current_route == "iv" and target_route == "oral":
        morphine_dose = morphine_dose * conversion_factor

    # Paso 3: Convertir la dosis de morfina al opioide objetivo
    if target_route == "patch" and target_opioid == "fentanilo":
        patch_table = opioid_conversion_table[target_opioid].get("patch", {})
        for dose, limit in patch_table.items():
            if morphine_dose <= limit:
                return f"{dose} mcg/h"
    elif target_opioid == "metadona" and target_route == "oral":
        if morphine_dose <= 90:
            target_dose = morphine_dose / opioid_conversion_table[target_opioid]["oral"]["<=90"]
        elif 90 < morphine_dose <= 300:
            target_dose = morphine_dose / opioid_conversion_table[target_opioid]["oral"]["91-300"]
        else:
            target_dose = morphine_dose / opioid_conversion_table[target_opioid]["oral"][">300"]
    elif current_opioid == "metadona" and target_opioid == "morfina" and current_route == "oral" and target_route == "oral":
        target_dose = current_dose * opioid_conversion_table[current_opioid]["oral"]
    elif target_opioid in more_potent_opioids:
        target_dose = morphine_dose / opioid_conversion_table[target_opioid][target_route]
    elif target_opioid in less_potent_opioids:
        target_dose = morphine_dose * opioid_conversion_table[target_opioid][target_route]
    elif target_opioid == "hidrocodona" or target_opioid == "morfina":
        target_dose = morphine_dose
    else:
        target_dose = morphine_dose / opioid_conversion_table[target_opioid][target_route]
    
    return target_dose

if __name__ == "__main__":
    main()
