import streamlit as st
from models import animal_prediction, new_animal
from ml import predict, train_model , get_info_model

st.title("Predicción simple de animales")

n_legs = st.selectbox("Número de patas", options=[2, 4], key="n_legs_prediccion")
height = st.number_input("Altura (m)", min_value=0.0, key="height_prediccion")
weight = st.number_input("Peso (kg)", min_value=0.0, key="weight_prediccion")
has_wings = st.checkbox("¿Tiene alas?", key="has_wings_prediccion")
has_tail = st.checkbox("¿Tiene cola?", key="has_tail_prediccion")

if st.button("Predecir"):
    animal = animal_prediction(
        walks_on_n_legs=n_legs,
        height=height,
        weight=weight,
        has_wings=has_wings,
        has_tail=has_tail,
    )
    try:
        prediction = predict(animal)
        st.success(f"Especie predicha: **{prediction[0]}**")  # Asumiendo respuesta lista con un string
    except Exception as e:
        st.error(f"Error en la predicción: {e}")



st.title("Reentreno de modelo con un nuevo animal")

n_legs = st.selectbox("Número de patas", options=[2, 4], key="n_legs_reentreno")
height = st.number_input("Altura (m)", min_value=0.0, key="height_reentreno")
weight = st.number_input("Peso (kg)", min_value=0.0, key="weight_reentreno")
has_wings = st.checkbox("¿Tiene alas?", key="has_wings_reentreno")
has_tail = st.checkbox("¿Tiene cola?", key="has_tail_reentreno")
label= st.selectbox("Etiqueta (label) numérica para especie",options=[1,2,3, 4], key="label_reentreno")


if st.button("Reentrenar modelo"):
    try:
        animal = new_animal(
            walks_on_n_legs=n_legs,
            height=height,
            weight=weight,
            has_wings=has_wings,
            has_tail=has_tail,
            label= label
        )
        result = train_model(animal)
        st.success(f"Respuesta del servidor: {result['message']}")
    except Exception as e:
        st.error(f"Error en reentreno: {e}")
        

st.title("Información del modelo")
if st.button("Get Info"):
    try:
        model_info = get_info_model()
        st.json(model_info)
    except Exception as e:
        st.error(f"Error al obtener información del modelo: {e}")