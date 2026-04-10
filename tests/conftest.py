"""Fixtures partagées — portée 'function' (défaut) : chaque test reçoit sa propre copie isolée.
Les fixtures de patch I/O utilisent monkeypatch pour isoler les tests du filesystem.
"""
import pytest
import pandas as pd
import numpy as np
from types import SimpleNamespace
from unittest.mock import MagicMock


# ─────────────────────────────────────────────
# Données brutes (avant traitement)
# ─────────────────────────────────────────────

@pytest.fixture
def raw_df():
    """DataFrame brut simulant le fichier source séparé par pipes (virgules françaises)."""
    return pd.DataFrame({
        "Type local": ["Maison", "Appartement", "Maison"],
        "Surface reelle bati": ["80,5", "50,0", "120,3"],
        "Nombre pieces principales": ["3", "2", "5"],
        "Surface terrain": ["100,0", None, "300,5"],
        "Valeur fonciere": ["250000,0", "180000,0", None],
    })


# ─────────────────────────────────────────────
# Données traitées (prêtes pour prepare_features)
# ─────────────────────────────────────────────

@pytest.fixture
def sample_df():
    """DataFrame traité — copie isolée par test."""
    return pd.DataFrame({
        "Surface_reelle_bati": [80.0, 50.0, 120.0, 200.0],
        "Surface_terrain": [100.0, None, 300.0, None],
        "Nombre_pieces_principales": [3, 2, 5, 4],
        "Type_local": ["Maison", "Appartement", "Local industriel", "Maison"],
        "Valeur_fonciere": [250000.0, 180000.0, 500000.0, 400000.0],
    })


# ─────────────────────────────────────────────
# Dicts de features pour la prédiction
# ─────────────────────────────────────────────

@pytest.fixture
def features_maison():
    """Features d'une maison — nouveau dict par test."""
    return {
        "Surface_reelle_bati": 100.0,
        "Surface_terrain": 200.0,
        "Nombre_pieces_principales": 4,
        "Type_local": "Maison",
    }


@pytest.fixture
def features_appartement():
    """Features d'un appartement — nouveau dict par test."""
    return {
        "Surface_reelle_bati": 55.0,
        "Surface_terrain": 0.0,
        "Nombre_pieces_principales": 2,
        "Type_local": "Appartement",
    }


# ─────────────────────────────────────────────
# Monkeypatching I/O — dataProcessing
# ─────────────────────────────────────────────

@pytest.fixture
def patched_process_io(monkeypatch, raw_df):
    """Remplace pd.read_csv et pathlib.Path.mkdir dans src.dataProcessing
    pour empêcher tout accès disque. Retourne le mock read_csv.
    """
    mock_read = MagicMock(return_value=raw_df.copy())
    monkeypatch.setattr("src.dataProcessing.pd.read_csv", mock_read)
    monkeypatch.setattr("src.dataProcessing.pathlib.Path.mkdir", MagicMock())
    return mock_read


# ─────────────────────────────────────────────
# Monkeypatching I/O — dataAccess
# ─────────────────────────────────────────────

@pytest.fixture
def patched_access_io(monkeypatch, sample_df):
    """Remplace pd.read_csv dans src.dataAccess pour empêcher tout accès disque.
    Retourne le mock read_csv.
    """
    mock_read = MagicMock(return_value=sample_df.copy())
    monkeypatch.setattr("src.dataAccess.pd.read_csv", mock_read)
    return mock_read


# ─────────────────────────────────────────────
# Mock sklearn + Monkeypatching I/O — PredictionModel
# ─────────────────────────────────────────────

@pytest.fixture
def mock_sklearn():
    """Mock pipeline sklearn retournant 300 000,0 par défaut."""
    m = MagicMock()
    m.predict.return_value = np.array([300000.0])
    return m


@pytest.fixture
def patched_model_io(monkeypatch, mock_sklearn):
    """Remplace pathlib.Path.exists et joblib.load dans src.prediction_model.
    Retourne un namespace avec .sklearn (mock pipeline) et .load (mock joblib.load).
    """
    mock_load = MagicMock(return_value=mock_sklearn)
    monkeypatch.setattr("src.prediction_model.pathlib.Path.exists", lambda self: True)
    monkeypatch.setattr("src.prediction_model.joblib.load", mock_load)
    return SimpleNamespace(sklearn=mock_sklearn, load=mock_load)


@pytest.fixture
def patched_model_absent(monkeypatch):
    """Simule un fichier modèle absent (Path.exists → False).
    Retourne le mock download_model pour les assertions d'appel.
    """
    mock_download = MagicMock()
    monkeypatch.setattr("src.prediction_model.pathlib.Path.exists", lambda self: False)
    monkeypatch.setattr(
        "src.prediction_model.hugging_model_play.download_model", mock_download
    )
    return mock_download
