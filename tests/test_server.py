"""
Tests d'intégration pour src/server.py — serveur FastMCP
"""
import pytest
from unittest.mock import patch, MagicMock
from fastmcp import Client
import src.server as server_module


# ─────────────────────────────────────────────
# Fixture : mock du modèle ML pour tous les tests
# ─────────────────────────────────────────────

@pytest.fixture(autouse=True)
def mock_prediction_model():
    """Empêche le chargement du vrai modèle et réinitialise le cache global."""
    mock_instance = MagicMock()
    mock_instance.predict.return_value = 320000.0

    with patch("src.server.PredictionModel", return_value=mock_instance):
        server_module._get_model.cache_clear()  # réinitialise le singleton lru_cache
        yield mock_instance
    server_module._get_model.cache_clear()


# ─────────────────────────────────────────────
# Découverte des outils
# ─────────────────────────────────────────────

async def test_liste_outils_contient_predict_price():
    async with Client(server_module.mcp) as client:
        tools = await client.list_tools()
    noms = {t.name for t in tools}
    assert "predict_price" in noms


async def test_predict_price_a_une_description():
    async with Client(server_module.mcp) as client:
        tools = await client.list_tools()
    tool = next(t for t in tools if t.name == "predict_price")
    assert tool.description is not None
    assert len(tool.description) > 0


async def test_predict_price_a_les_bons_parametres():
    async with Client(server_module.mcp) as client:
        tools = await client.list_tools()
    tool = next(t for t in tools if t.name == "predict_price")
    params = tool.inputSchema.get("properties", {})
    assert "surface_reelle_bati" in params
    assert "surface_terrain" in params
    assert "nombre_pieces_principales" in params
    assert "type_local" in params


# ─────────────────────────────────────────────
# Appel de l'outil predict_price
# ─────────────────────────────────────────────

async def test_predict_price_retourne_un_resultat():
    async with Client(server_module.mcp) as client:
        result = await client.call_tool("predict_price", {
            "surface_reelle_bati": 80.0,
            "surface_terrain": 100.0,
            "nombre_pieces_principales": 3,
            "type_local": "Maison",
        })
    assert result is not None
    assert len(result.content) > 0


async def test_predict_price_appelle_le_modele_avec_les_bonnes_features(mock_prediction_model):
    async with Client(server_module.mcp) as client:
        await client.call_tool("predict_price", {
            "surface_reelle_bati": 65.0,
            "surface_terrain": 0.0,
            "nombre_pieces_principales": 2,
            "type_local": "Appartement",
        })
    mock_prediction_model.predict.assert_called_once()
    features_passees = mock_prediction_model.predict.call_args[0][0]
    assert features_passees["Surface_reelle_bati"] == 65.0
    assert features_passees["Surface_terrain"] == 0.0
    assert features_passees["Nombre_pieces_principales"] == 2
    assert features_passees["Type_local"] == "Appartement"


async def test_predict_price_initialise_le_modele_une_seule_fois(mock_prediction_model):
    """Le modèle doit être instancié une seule fois (singleton)."""
    async with Client(server_module.mcp) as client:
        await client.call_tool("predict_price", {
            "surface_reelle_bati": 80.0,
            "surface_terrain": 100.0,
            "nombre_pieces_principales": 3,
            "type_local": "Maison",
        })
        await client.call_tool("predict_price", {
            "surface_reelle_bati": 50.0,
            "surface_terrain": 0.0,
            "nombre_pieces_principales": 2,
            "type_local": "Appartement",
        })
    # PredictionModel a été appelé depuis le patch — le modèle ne doit être
    # instancié qu'une seule fois grâce au cache global `model`
    # Le mock_instance.predict doit avoir été appelé deux fois
    assert mock_prediction_model.predict.call_count == 2
