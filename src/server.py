from fastmcp import FastMCP
from src.prediction_model import PredictionModel
import pathlib
MODEL_DIR = pathlib.Path(__file__).resolve().parent.parent / "models"
mcp = FastMCP("Demo 🚀")



model = PredictionModel(MODEL_DIR / "model.joblib")

@mcp.tool
def add(a: int, b: int) -> str:
    """Add two numbers"""
    return f"{a + b}"

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return (a * b)+8

@mcp.tool
def meaning_of_life() -> str:
    """Return the meaning of life"""
    return "Manger des frites"

@mcp.tool
def predict_price(surface_reelle_bati: float, surface_terrain: float, nombre_pieces_principales: int, type_local: str) -> float:
    """Predict the price of a property based on its features."""
    features = {
        "Surface_reelle_bati": surface_reelle_bati,
        "Surface_terrain": surface_terrain,
        "Nombre_pieces_principales": nombre_pieces_principales,
        "Type_local": type_local
    }
    predicted_price = model.predict(features)
    return predicted_price

if __name__ == "__main__":
    mcp.run(transport="sse")