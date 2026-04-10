import os
import joblib
import pandas as pd
from fastmcp import FastMCP
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

# Configuration Hugging Face depuis le .env
HF_USER = os.getenv("HF_USERNAME", "Gahnos")
HF_REPO = os.getenv("HF_REPO", "mon-modele-joblib")

# 1. Téléchargement et chargement du modèle au démarrage
model = None
load_error = "Aucune tentative de chargement effectuée."

print(f"🚀 Initialisation du serveur... Récupération du modèle {HF_USER}/{HF_REPO}")
try:
    model_path = hf_hub_download(repo_id=f"{HF_USER}/{HF_REPO}", filename="model.joblib")
    model = joblib.load(model_path)
    print("✅ Modèle chargé avec succès !")
    load_error = None
except Exception as e:
    load_error = str(e)
    print(f"❌ Erreur lors du chargement du modèle : {e}")

# 2. Création du serveur MCP
mcp = FastMCP("Immo Estimator 🚀")

@mcp.tool
def estimer_prix(surface_m2: float = None, nb_pieces: int = None, code_postal: int = None, ville: str = None) -> str:
    """
    Estime le prix d'un bien immobilier en utilisant le modèle IA.
    Args:
        surface_m2: La surface habitable en m2 (optionnel mais recommandé).
        nb_pieces: Le nombre de pièces principales (optionnel).
        code_postal: Le code postal (ex: 75001).
        ville: Le nom de la ville (optionnel).
    """
    if model is None:
        return f"Désolé, le modèle n'est pas disponible. Erreur interne : {load_error}"
    
    # Si des infos cruciales manquent pour le calcul mathématique
    if surface_m2 is None or code_postal is None:
        return f"Pour vous donner une estimation précise à {ville or 'votre ville'}, j'ai besoin de connaître la surface en m2 et le code postal."

    # Valeur par défaut pour le nombre de pièces si l'utilisateur ne le sait pas
    nb_pieces_calc = nb_pieces if nb_pieces is not None else 3
    
    try:
        # Préparation des données dans un DataFrame (requis par ColumnTransformer)
        cols = ["surface", "pieces", "cp", "type"] # Noms génériques
        df_input = pd.DataFrame([[float(surface_m2), int(nb_pieces_calc), int(code_postal), 0]], columns=cols)
        
        prediction = model.predict(df_input)
        prix_estime = prediction[0]
        
        return (f"Analyse terminée pour {ville or code_postal} ! "
                f"Pour un bien de {surface_m2}m² avec {nb_pieces_calc} pièces, "
                f"l'estimation est de {prix_estime:,.0f} €.")
    
    except Exception as e:
        return f"L'outil est connecté mais le calcul a échoué : {str(e)}. Vérifiez que les données correspondent au format attendu par votre modèle."

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0")