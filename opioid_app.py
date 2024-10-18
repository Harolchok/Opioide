import streamlit as st

# Tabla de equivalencia de opioides (en mg y factores de conversión para diferentes vías)
# Esta tabla define los factores de conversión entre diferentes opioides y sus vías de administración.
opioid_conversion_table = {
    "fentanilo": {"oral": None, "iv": 100, "sc": None, "patch": {
        "25": 90,
        "50": 160,
        "75": 200,
        "100": 275,
        "125": 325,
        "150": 400,
        "175": 450,
        "200": 525
    }},
    "buprenorfina": {"oral": None, "iv": None, "sc": None, "patch": {"10": 30, "20": 60, "35": 90, "52.5": 120, "70": 180}},
    "hidromorfona": {"oral": 5, "iv": 5, "sc": 5},
    "oxicodona": {"oral": 1.5, "iv": 2, "sc": 1},
    "morfina": {"oral": 1, "iv": 3, "sc": 2, "intratecal": 100},
    "hidrocodona": {"oral": 1, "iv": None, "sc": None},
    "tapentadol": {"oral": 3.3, "iv": None, "sc": None},
    "tramadol": {"oral": 4, "iv": 10, "sc": None},
    "metadona": {"oral": 5, "iv": None, "sc": None},
    "codeina": {"oral": 10, "iv": None, "sc": None}
}

def convert_to_patch(opioid, morphine_equivalent_dose):
    # Función para convertir morfina equivalente a parches de fentanilo o buprenorfina
    if opioid == "fentanilo":
        for dose, limit in opioid_conversion_table["fentanilo"]["patch"].items():
            if morphine_equivalent_dose <= limit:
                return f"{dose} mcg/h"
    elif opioid == "buprenorfina":
        # Determinar el parche de buprenorfina según la dosis de morfina equivalente
        if morphine_equivalent_dose < 30:
            return 10
        elif 30 <= morphine_equivalent_dose <= 60:
            return 20
        elif 60 < morphine_equivalent_dose <= 90:
            return 35
        elif 90 < morphine_equivalent_dose <= 120:
            return 52.5
        elif morphine_equivalent_dose > 120:
            return 70
    return None

def calculate_metadona_dose(morphine_equivalent_dose):
    # Función para calcular la dosis de metadona basada en la dosis de morfina equivalente
    if morphine_equivalent_dose < 30:
        # Si la dosis es menor a 30 mg, no se puede convertir a metadona
        raise ValueError("La dosis de morfina equivalente debe ser al menos 30 mg para convertir a metadona.")
    elif 30 <= morphine_equivalent_dose <= 90:
        factor = 4  # Factor de conversión 4:1 para dosis entre 30 y 90 mg
    elif 90 < morphine_equivalent_dose <= 300:
        factor = 8  # Factor de conversión 8:1 para dosis entre 90 y 300 mg
    elif morphine_equivalent_dose > 300:
        factor = 12  # Factor de conversión 12:1 para dosis mayores a 300 mg
    return morphine_equivalent_dose / factor

def calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose, conversion_factor):
    # Verificar la disponibilidad de las presentaciones para la conversión
    if opioid_conversion_table[current_opioid][current_route] is None or (target_opioid != "patch" and opioid_conversion_table[target_opioid][target_route] is None):
        raise TypeError("La conversión solicitada no es válida para la combinación de opioide y vía seleccionados.")

    # Convertir la dosis actual al equivalente en morfina oral
    if current_opioid == "morfina" and current_route == "oral":
        morphine_equivalent_dose = current_dose  # Si ya es morfina oral, no es necesario convertir
    elif current_opioid in ["tapentadol", "tramadol", "codeina"]:
        # Para opioides menos potentes que la morfina, dividir la dosis actual por el factor de conversión
        morphine_equivalent_dose = current_dose / opioid_conversion_table[current_opioid][current_route]
    else:
        # Para opioides más potentes o diferentes vías, multiplicar la dosis actual por el factor de conversión
        morphine_equivalent_dose = current_dose * opioid_conversion_table[current_opioid][current_route]
    
    # Convertir la dosis equivalente de morfina a la vía oral si no es ya oral
    if current_route != "oral" and current_opioid != "patch":
        morphine_equivalent_dose = morphine_equivalent_dose * conversion_factor

    # Convertir la dosis equivalente de morfina al opioide objetivo
    if target_opioid == "morfina" and target_route == "oral":
        target_dose = morphine_equivalent_dose  # Si el objetivo es morfina oral, ya tenemos el resultado
    elif target_route == "patch":
        # Si el objetivo es un parche, usar la función convert_to_patch
        return convert_to_patch(target_opioid, morphine_equivalent_dose)
    elif target_opioid == "metadona":
        # Si el objetivo es metadona, primero convertir a morfina oral si no lo es aún
        if current_opioid != "morfina" or current_route != "oral":
            morphine_equivalent_dose = morphine_equivalent_dose / conversion_factor if current_route != "oral" else morphine_equivalent_dose
        # Luego usar la función calculate_metadona_dose para la conversión final
        target_dose = calculate_metadona_dose(morphine_equivalent_dose)
    elif current_opioid == "metadona" and target_opioid == "morfina":
        # Convertir de metadona a morfina utilizando un factor fijo de 5:1
        target_dose = current_dose * 5
    else:
        # Convertir la morfina oral al opioide objetivo
        target_dose = morphine_equivalent_dose / opioid_conversion_table[target_opioid]["oral"]
        # Cambiar la vía de administración si es necesario
        if target_route != "oral":
            target_dose = target_dose / conversion_factor
    
    return target_dose

def main():
    st.title("Rotación de Opioides")
    st.write("Ingrese el opioide actual, la vía de administración y el opioide al que desea rotar con la vía de administración deseada para obtener la dosis equivalente.")

    # Seleccionar el factor de conversión entre oral e IV
    conversion_factor = st.radio("Seleccione el factor de conversión entre oral e IV", (2, 3))

    # Seleccionar opioides, vías de administración y dosis actual
    current_opioid = st.selectbox("Seleccione el opioide actual", list(opioid_conversion_table.keys()))
    current_route = st.selectbox("Seleccione la vía de administración actual", ["oral", "iv", "sc", "patch"])
    target_opioid = st.selectbox("Seleccione el opioide al que desea rotar", list(opioid_conversion_table.keys()))
    target_route = st.selectbox("Seleccione la vía de administración deseada", ["oral", "iv", "sc", "patch", "intratecal"])
    current_dose = st.number_input("Ingrese la dosis actual en mg", min_value=0.0, step=1.0)

    if st.button("Calcular Dosis Equivalente"):
        if current_dose > 0:
            try:
                target_dose = calculate_equivalent_dose(current_opioid, current_route, target_opioid, target_route, current_dose, conversion_factor)
                st.success(f"La dosis equivalente de {target_opioid} ({target_route}) es {target_dose}")
            except TypeError:
                st.error("La conversión solicitada no es válida para la combinación de opioide y vía seleccionados.")
        else:
            st.warning("Por favor, ingrese una dosis válida mayor que 0.")

if __name__ == "__main__":
    main()
