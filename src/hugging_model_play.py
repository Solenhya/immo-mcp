import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, hf_hub_download
import pathlib
MODEL_DIR = pathlib.Path(__file__).resolve().parent.parent / "models"

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

def download_model():
    path = hf_hub_download(repo_id=repo_id, filename="model.joblib",local_dir=MODEL_DIR)
    return path

if __name__ == "__main__":
    upload_model()