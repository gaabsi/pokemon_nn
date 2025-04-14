import streamlit as st
from PIL import Image
import base64
import io

st.set_page_config(page_title="Mon Pokédex", page_icon="🧬", layout="wide")

# --- Fonctions utilitaires ---
def load_image_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def inject_css(css_path):
    with open(css_path) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def set_background_image(image_path):
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

def merge_images(pokedex_path, pokemon_image, position=(140, 288), size=(450, 300)):
    """
    Superpose l'image du Pokémon sur l'écran du Pokédex.
    - position : (x, y) pour le coin supérieur gauche
    - size : (largeur, hauteur) finale du Pokémon
    """
    pokedex = Image.open(pokedex_path).convert("RGBA")
    pokemon = pokemon_image.convert("RGBA")
    pokemon = pokemon.resize(size)

    pokedex.paste(pokemon, position, pokemon)  # utilisation du canal alpha
    return pokedex

# --- Setup CSS et fond ---
inject_css("style.css")
set_background_image("fond.avif")

pokeball_icon = load_image_base64("pokeball_icon.webp")

# --- Interface ---
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown(f"""
        <label class="upload-button" for="file-upload">
            <img src="data:image/png;base64,{pokeball_icon}" />
            Charger un Pokémon
            <span style="margin-left:auto;">▼</span>
        </label>
    """, unsafe_allow_html=True)
    upload_file = st.file_uploader(" ", type=["png", "jpg", "jpeg"], key="fileInput")
    

with col1:
    if upload_file is not None:
        user_image = Image.open(upload_file)
        merged = merge_images("ecran_pokedex.png", user_image)
        st.image(merged, use_container_width=True)
    else:
        st.image("ecran_pokedex.png", use_container_width=True)
