# pokemon_nn

## Pokedex CNN - Classification d'images de Pokémon
Ce projet consiste à entraîner un modèle de deep learning (CNN) capable de reconnaître automatiquement les Pokémon de la 1ʳᵉ génération à partir d'une image. 
Le modèle a été entraîné sur des images de 64x64 pixels en couleur.
Malheureusement il manque quelques pokémons, au lieu d'avoir les 151, on en a 142 ... 

Nous l'avons déployé avec une UI streamlit. (Où des fonctionnalités supplémentaires ont été déployées)
Les images étant trop volumineuses elles ne sont pas hébergées ici mais le lien de téléchargement est dans le notebook principal.

## Structure du projet 

pokemon_nn/
│
├── pokedex_64x64.keras        # Modèle entraîné sauvegardé avec nos poids
├── README.md                  
├── notebook/                  # Notebooks du projet
├── requirements/              # Afin d'avoir l'environnement pour cloner le projet
└── img_best/                  # Répertoire contenant les plus belles images (pour l'affichage streamlit)
└── streamlit_vrs/             # Déploiement de l'UI de notre pokédex


## Contenu final du projet

- **CNN personnalisé** capable de reconnaitre les pokémons, comme un vrai pokédex. Mais il faudra rester à Kanto. 
- Déploiement afin de permettre à l'utilisateur d'en profiter. (En lui donnant notamment les statistiques du pokémon prédit, ...) 

# Pour cloner le projet 
git clone https://github.com/votrecompte/pokemon_nn.git
cd pokemon_nn
pip install -r requirements.txt
