import os
import joblib
from fastmcp import FastMCP
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

# Configuration Hugging Face depuis le .env
HF_USER = os.getenv("HF_USERNAME", "Gahnos")
HF_REPO = os.getenv("HF_REPO", "mon-modele-joblib")

# 1. Téléchargement et chargement du modèle au démarrage
print(f"🚀 Initialisation du serveur... Récupération du modèle {HF_USER}/{HF_REPO}")
try:
    model_path = hf_hub_download(repo_id=f"{HF_USER}/{HF_REPO}", filename="model.joblib")
    model = joblib.load(model_path)
    print("✅ Modèle chargé avec succès !")
except Exception as e:
    print(f"❌ Erreur lors du chargement du modèle : {e}")
    model = None

# 2. Création du serveur MCP
mcp = FastMCP("Immo Estimator 🚀")

@mcp.tool
def add(a: int, b: int) -> str:
    """Additionne deux nombres."""
    return f"{a + b}"

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplie deux nombres."""
    return (a * b)

@mcp.tool
def estimer_prix(surface_m2: float, nb_pieces: int, code_postal: int) -> str:
    """
    Estime le prix d'un bien immobilier en utilisant le modèle IA.
    Args:
        surface_m2: La surface habitable en m2.
        nb_pieces: Le nombre de pièces principales.
        code_postal: Le code postal (ex: 75001).
    """
    if model is None:
        return "Désolé, le modèle d'estimation n'est pas disponible pour le moment."
    
    try:
        # NOTE : Adapte cette partie selon les colonnes attendues par ton modèle Scikit-Learn
        # Exemple : prediction = model.predict([[surface_m2, nb_pieces, code_postal]])
        
        # Pour l'instant on simule si on n'est pas sûr des colonnes
        # Mais le modèle est bien chargé en mémoire (variable 'model')
        return f"Modèle connecté ! Estimation en cours pour {surface_m2}m² avec {nb_pieces} pièces dans le {code_postal}."
    except Exception as e:
        return f"Erreur lors de la prédiction : {str(e)}"

@mcp.tool
def meaning_of_life() -> str:
    """Retourne le sens de la vie."""
    return "Manger des frites (et faire de l'IA)"

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0")