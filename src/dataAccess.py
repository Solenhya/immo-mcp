import pandas as pd
from sklearn.model_selection import train_test_split

import logging 
import pathlib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import sys
import os
# Get the directory one level up from the current script
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR= pathlib.Path("data")
# Add the parent folder to sys.path if it's not already there
if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)

def get_data():
    file_path = DATA_DIR / "2025.csv"
    nrows = 10000
    df = pd.read_csv(file_path, nrows=nrows, sep=",")
    logger.info(f"📊 Données chargées: {len(df):,} lignes")
    return df

features = [
    'Surface_reelle_bati',
    'Surface_terrain',
    'Nombre_pieces_principales',
    'Type_local',
    
]

target = ['Valeur_fonciere']

def prepare_features(df):
    print(df.columns)
    df = df[features + target]
    df = df[df['Type_local'].isin(['Maison', 'Appartement'])]
    "rempli les colonnes optionnelles pour ne pas supprimer les lignes"
    df['Surface_terrain'] = df['Surface_terrain'].fillna(0)
    df = df.dropna()
    logger.info(f"données préparées{df.shape}")
    return df
