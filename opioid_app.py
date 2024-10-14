import streamlit as st

# Tabla de equivalencia de opioides (en mg y factores de conversión para diferentes vías)
opioid_conversion_table = {
    "fentanilo": {"oral": None, "iv": 1, "sc": 1, "oral_factor": 100},
    "buprenorfina": {"oral": None, "iv": None, "sc": None, "oral_factor": 75},
    "hidromorfona": {"oral": 5, "iv": 3, "sc": 2},
    "oxicodona": {"oral": 1.5, "iv": 2, "sc": 1},
    "morfina": {"oral": 1, "iv": 3, "sc": 2},
    "hidrocodona": {"oral": 1, "iv": None, "sc": None},
    "tapentadol": {"oral": 3.3, "iv": None, "sc": None},
    "tramadol": {"oral": 4, "iv": 1.2, "sc": None}
}

def calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose):
    # Convertir la dosis actual al equivalente en morfina (oral)
    morphine_equivalent = current_dose * opioid_conversion_table[current_opioid][current_route]
    # Convertir la dosis de morfina al equivalente del opioide objetivo en la vía deseada
    target_dose = morphine_equivalent / opioid_conversion_table[target_opioid][target_route]
    return target_dose

def main():
    st.title("Rotación de Opioides")
    st.write("Ingrese el opioide actual, la vía de administración y el opioide al que desea rotar con la vía de administración deseada para obtener la dosis equivalente.")

    # Seleccionar opioides, vías de administración y dosis actual
    current_opioid = st.selectbox("Seleccione el opioide actual", list(opioid_conversion_table.keys()))
    current_route = st.selectbox("Seleccione la vía de administración actual", ["oral", "iv", "sc"])
    target_opioid = st.selectbox("Seleccione el opioide al que desea rotar", list(opioid_conversion_table.keys()))
    target_route = st.selectbox("Seleccione la vía de administración deseada", ["oral", "iv", "sc"])
    current_dose = st.number_input("Ingrese la dosis actual en mg", min_value=0.0, step=1.0)

    if st.button("Calcular Dosis Equivalente"):
        if current_dose > 0:
            try:
                target_dose = calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose)
                st.success(f"La dosis equivalente de {target_opioid} ({target_route}) es {target_dose:.2f} mg")
            except TypeError:
                st.error("La conversión solicitada no es válida para la combinación de opioide y vía seleccionados.")
        else:
            st.warning("Por favor, ingrese una dosis válida mayor que 0.")

if __name__ == "__main__":
    main()
