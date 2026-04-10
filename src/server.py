from fastmcp import FastMCP
from src.prediction_model import PredictionModel
import pathlib
import functools
MODEL_DIR = pathlib.Path(__file__).resolve().parent.parent / "models"
mcp = FastMCP("Demo 🚀")


@functools.lru_cache(maxsize=1)
def _get_model() -> PredictionModel:
    return PredictionModel(MODEL_DIR / "model.joblib")


@mcp.tool
def predict_price(surface_reelle_bati: float, surface_terrain: float, nombre_pieces_principales: int, type_local: str) -> float:
    """Predict the price of a property based on its features."""
    features = {
        "Surface_reelle_bati": surface_reelle_bati,
        "Surface_terrain": surface_terrain,
        "Nombre_pieces_principales": nombre_pieces_principales,
        "Type_local": type_local
    }
    predicted_price = _get_model().predict(features)
    return predicted_price

if __name__ == "__main__":
    mcp.run(transport="sse")