import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import os
import base64
import io
import matplotlib.pyplot as plt

# 0) Configuration de la page (à appeler avant tout autre st.*)
st.set_page_config(
    page_title="Mon Pokédex",
    page_icon="🧬",
    layout="wide"
)

# 1) Chargement du modèle (cache)
@st.cache_resource
def get_model():
    return load_model('pokedex_64x64_fixed.h5')

# 2) Reconstruction des class_names depuis les dossiers (cache)
@st.cache_data
def get_class_names(data_dir: str) -> list[str]:
    ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        image_size=(64, 64),
        batch_size=1,
        shuffle=False
    )
    return ds.class_names

# 3) Chargement des stats Pokémon (cache)
@st.cache_data
def load_stats(path: str = 'stats_pokemon.xlsx') -> pd.DataFrame:
    df = pd.read_excel(path)
    return df.set_index('Nom_en')

def get_pokemon_stats(name: str, stats_df: pd.DataFrame) -> list[float]:
    row = stats_df.loc[name]
    return [float(row[col]) for col in ['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']]

# 4) Fonctions pour CSS et background

def load_image_base64(path: str) -> str:
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

@st.cache_resource
def inject_css(path: str = 'style.css'):
    with open(path) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

@st.cache_resource
def set_background_image(path: str = 'fond.avif'):
    img_b64 = load_image_base64(path)
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url('data:image/webp;base64,{img_b64}');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 5) Configuration du resampling rapide pour sprites et radar
try:
    RESAMPLE = Image.Resampling.BILINEAR
except AttributeError:
    RESAMPLE = Image.BILINEAR

# 6) Template et sprites en cache
@st.cache_resource
def load_base_template(path: str = 'ecran_pokedex.png') -> Image.Image:
    return Image.open(path).convert('RGBA')

@st.cache_resource
def load_pokemon_sprites(data_dir: str = 'IMG_Pokedex') -> dict[str, Image.Image]:
    sprites = {}
    for file in os.listdir(data_dir):
        if file.lower().endswith('.png'):
            name = os.path.splitext(file)[0]
            sprites[name] = Image.open(os.path.join(data_dir, file)).convert('RGBA')
    return sprites

# 7) Génération du radar chart (cache)
@st.cache_data
def get_radar_chart(name: str, stats: list[float], categories: list[str], max_val: float = None, size_px: int = 350) -> Image.Image:
    if max_val is None:
        max_val = max(stats)
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist() + [0]
    stats_loop = stats + [stats[0]]

    fig, ax = plt.subplots(
        figsize=(size_px/100, size_px/100), subplot_kw=dict(polar=True), dpi=100
    )
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)

    ax.plot(angles, stats_loop, linewidth=3)
    ax.fill(angles, stats_loop, alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    for angle, label in zip(angles[:-1], categories):
        ax.text(
            angle, max_val * 1.05, label,
            ha='center', va='center', fontsize=14, fontweight='bold'
        )
    ax.set_yticks([])
    ax.set_ylim(0, max_val)
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    buf = io.BytesIO()
    fig.savefig(buf, format='PNG', transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# 8) Composition finale de l'écran (cache)
@st.cache_data
def compose_pokedex_screen(name: str, stats: list[float], categories: list[str]) -> Image.Image:
    base = load_base_template().copy()
    sprite = load_pokemon_sprites()[name].resize((450,300), RESAMPLE)
    base.paste(sprite, (125,288), sprite)
    radar = get_radar_chart(name, stats, categories)
    base.paste(radar, (885,325), radar)
    return base

# =========== INITIALISATION ===========
inject_css()
set_background_image()

MODEL       = get_model()
class_names = get_class_names('pokemon')
stats_df    = load_stats('stats_pokemon.xlsx')
sacha       = Image.open('sacha.jpg').convert('RGBA')
categories  = ['HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']
BASE_TEMPLATE = load_base_template()

# =========== UI ===========
col1, col2 = st.columns([3,1])
info_slot  = col1.empty()
image_slot = col1.empty()

with col2:
    st.markdown(
        f"""
        <label class='upload-button' for='file-upload'>
            <img src='data:image/png;base64,{load_image_base64('pokeball_icon.webp')}' />
            Charger un Pokémon <span style='margin-left:auto;'>▼</span>
        </label>
        """,
        unsafe_allow_html=True
    )
    uploaded = st.file_uploader('', type=['png','jpg','jpeg'], key='fileInput', label_visibility='collapsed')
    if uploaded:
        st.image(uploaded, use_container_width=True)

if uploaded:
    # Revenir au preprocessing original pour l'image uploadée
    img = Image.open(uploaded).convert('RGB')
    img_resized = img.resize((64,64), Image.LANCZOS)
    x = np.expand_dims(np.array(img_resized), axis=0).astype('float32')

    preds = MODEL.predict(x, verbose=0)[0]
    top1 = int(np.argmax(preds))
    name = class_names[top1]
    score = preds[top1] * 100

    if score > 60:
        stats = get_pokemon_stats(name, stats_df)
        info_slot.markdown(f"## C'est un {name} ! ({score:.2f}%)")
        final = compose_pokedex_screen(name, stats, categories)
        image_slot.image(final, use_container_width=True)
    else:
        info_slot.markdown("## Pas sûr de le reconnaitre, réessaie avec une autre image")
        image_slot.image(sacha, use_container_width=True)
else:
    info_slot.empty()
    image_slot.image(BASE_TEMPLATE, use_container_width=True)
