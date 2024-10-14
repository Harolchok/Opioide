import streamlit as st

# Tabla de equivalencia de opioides (en mg)
opioid_conversion_table = {
    "morfina": 1,
    "oxicodona": 1.5,
    "fentanilo": 0.03,
    "hidromorfona": 4,
    "metadona": 10
}

def calculate_equivalent_dose(current_opioid, target_opioid, current_dose):
    # Convertir la dosis actual al equivalente en morfina
    morphine_equivalent = current_dose * opioid_conversion_table[current_opioid]
    # Convertir la dosis de morfina al equivalente del opioide objetivo
    target_dose = morphine_equivalent / opioid_conversion_table[target_opioid]
    return target_dose

def main():
    st.title("Rotación de Opioides")
    st.write("Ingrese el opioide actual y el opioide al que desea rotar para obtener la dosis equivalente.")

    # Seleccionar opioides y dosis actual
    current_opioid = st.selectbox("Seleccione el opioide actual", list(opioid_conversion_table.keys()))
    target_opioid = st.selectbox("Seleccione el opioide al que desea rotar", list(opioid_conversion_table.keys()))
    current_dose = st.number_input("Ingrese la dosis actual en mg", min_value=0.0, step=1.0)

    if st.button("Calcular Dosis Equivalente"):
        if current_dose > 0:
            target_dose = calculate_equivalent_dose(current_opioid, target_opioid, current_dose)
            st.success(f"La dosis equivalente de {target_opioid} es {target_dose:.2f} mg")
        else:
            st.warning("Por favor, ingrese una dosis válida mayor que 0.")

if __name__ == "__main__":
    main ()
