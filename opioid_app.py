import streamlit as st

# Tabla de equivalencia de opioides (en mg y factores de conversión para diferentes vías)
opioid_conversion_table = {
    "fentanilo": {"oral": None, "iv": 100, "sc": 100, "patch": {
        "25": 90,
        "50": 160,
        "75": 200,
        "100": 275,
        "125": 325,
        "150": 400,
        "175": 450,
        "200": 525
    }},
    "buprenorfina": {"oral": None, "iv": None, "sc": None, "patch": {"low": 10, "medium": 20, "high": 35}},
    "hidromorfona": {"oral": 5, "iv": 5, "sc": 5},
    "oxicodona": {"oral": 0.67, "iv": 2, "sc": 1},
    "morfina": {"oral": 1, "iv": 3, "sc": 2, "intratecal": 100},
    "hidrocodona": {"oral": 1, "iv": None, "sc": None},
    "tapentadol": {"oral": 0.303, "iv": None, "sc": None},
    "tramadol": {"oral": 4, "iv": 10, "sc": None},
    "metadona": {"oral": None, "iv": None, "sc": None},
    "codeina": {"oral": 0.1, "iv": None, "sc": None}
}

def calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose):
    if target_opioid == "fentanilo" and target_route == "patch" or target_route == "intratecal":
        # Definir rangos según DEMOD para parches de fentanilo
        demod = current_dose / opioid_conversion_table[current_opioid][current_route]
        for dose, limit in opioid_conversion_table["fentanilo"]["patch"].items():
            if demod <= limit:
                return f"{dose} mcg/h"
    elif target_opioid == "buprenorfina" and target_route == "patch":
        demod = current_dose / opioid_conversion_table[current_opioid][current_route]
        if demod <= 60:
            return opioid_conversion_table["buprenorfina"]["patch"]["low"]
        elif 60 < demod <= 180:
            return opioid_conversion_table["buprenorfina"]["patch"]["medium"]
        else:
            return opioid_conversion_table["buprenorfina"]["patch"]["high"]
    elif target_opioid == "metadona":
        # Calcular DEMOD para determinar el factor de conversión adecuado
        demod = current_dose * opioid_conversion_table[current_opioid][current_route]
        if demod <= 90:
            factor = 4
        elif 90 < demod <= 300:
            factor = 8
        else:
            factor = 12
        # Convertir morfina a metadona usando el factor correspondiente
        return demod / factor
    elif current_opioid == "metadona" and target_opioid == "morfina":
        # Convertir metadona a morfina usando un factor fijo de 5
        return current_dose * 5
    else:
        # Convertir la dosis actual al equivalente en morfina intravenosa si es necesario
        if current_route != "iv":
            current_dose = current_dose * opioid_conversion_table[current_opioid][current_route] / opioid_conversion_table["morfina"]["iv"]
        # Convertir la dosis de morfina intravenosa al opioide objetivo
        if target_opioid == "fentanilo" and target_route == "iv":
            target_dose = current_dose / 100
        elif target_opioid == "morfina" and target_route == "intratecal":
            target_dose = current_dose / 100
        else:
            target_dose = current_dose / opioid_conversion_table[target_opioid][target_route]
        return target_dose

def main():
    st.title("Rotación de Opioides")
    st.write("Ingrese el opioide actual, la vía de administración y el opioide al que desea rotar con la vía de administración deseada para obtener la dosis equivalente.")

    # Seleccionar opioides, vías de administración y dosis actual
    current_opioid = st.selectbox("Seleccione el opioide actual", list(opioid_conversion_table.keys()))
    current_route = st.selectbox("Seleccione la vía de administración actual", ["oral", "iv", "sc"])
    target_opioid = st.selectbox("Seleccione el opioide al que desea rotar", list(opioid_conversion_table.keys()))
    target_route = st.selectbox("Seleccione la vía de administración deseada", ["oral", "iv", "sc", "patch", "intratecal"])
    current_dose = st.number_input("Ingrese la dosis actual en mg", min_value=0.0, step=1.0)

    if st.button("Calcular Dosis Equivalente"):
        if current_dose > 0:
            try:
                target_dose = calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose)
                st.success(f"La dosis equivalente de {target_opioid} ({target_route}) es {target_dose}")
            except TypeError:
                st.error("La conversión solicitada no es válida para la combinación de opioide y vía seleccionados.")
        else:
            st.warning("Por favor, ingrese una dosis válida mayor que 0.")

if __name__ == "__main__":
    main()
