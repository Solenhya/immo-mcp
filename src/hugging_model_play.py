import os
from dotenv import load_dotenv
from huggingface_hub import HfApi
import pathlib
MODEL_DIR = pathlib.Path().parent / "models"

load_dotenv()

api = HfApi(token=os.getenv("HF_TOKEN"))

repo_id = f"{os.getenv('HF_USERNAME')}/{os.getenv('HF_REPO')}"

def upload_model():
    api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)
    api.upload_file(
        path_or_fileobj=MODEL_DIR / "model.joblib",  # le fichier modèle
        path_in_repo="model.joblib",     # nom dans le repo
        repo_id=repo_id,
        repo_type="model"
    )

if __name__ == "__main__":
    upload_model()