import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="Mon Pokédex", page_icon="🧬", layout="wide")

# --- Fonctions utilitaires ---
def load_image_base64(file_path):
    """
    Charge une image et la convertit en chaîne base64.
    """
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def inject_css(css_path):
    """
    Injecte une feuille de style CSS dans l'application Streamlit.
    """
    with open(css_path) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def set_background_image(image_path):
    """
    Applique une image de fond à l'application via base64.
    """
    bg_base64 = load_image_base64(image_path)
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/webp;base64,{bg_base64}");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
        </style>
    """, unsafe_allow_html=True)


# --- Setup du CSS et du fond ---
inject_css("style.css")
set_background_image("fond.avif")

# --- Chargement des images ---
pokeball_icon = load_image_base64("pokeball_icon.webp")
pokedex_screen = load_image_base64("ecran_pokedex.png")

# --- Mise en page ---
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown(f'<img src="data:image/png;base64,{pokedex_screen}" class="pokedex-image">', unsafe_allow_html=True)

with col2:
    # Affichage du bouton stylisé
    st.markdown(f"""
        <div class="custom-upload-wrapper">
            <input type="file" id="file-upload" name="file-upload" accept="image/*">
            <label for="file-upload" class="upload-button">
                <img src="data:image/png;base64,{pokeball_icon}" />
                Charger un Pokémon
                <span style="margin-left:auto;">▼</span>
            </label>
        </div>
        <style>
            .custom-upload-wrapper {{
                position: relative;
                width: fit-content;
                margin: auto;
            }}

            .custom-upload-wrapper input[type="file"] {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                opacity: 0;
                cursor: pointer;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Récupération de l’image envoyée
    uploaded_file = st.file_uploader(
        label="a",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        key="file-upload-native"
    )



# --- Affichage de l’image chargée ---
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Ton Pokémon !", use_container_width=True)

    # À ce stade tu peux appeler ton modèle :
    # prediction = ton_modele.predict(preprocess(image))
    # st.write(f"Ce Pokémon est : {prediction}")
