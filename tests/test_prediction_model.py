"""
Tests unitaires pour src/prediction_model.py — classe PredictionModel
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock


# ─────────────────────────────────────────────
# Chargement du modèle
# ─────────────────────────────────────────────

def test_charge_le_modele_depuis_le_fichier(patched_model_io):
    from src.prediction_model import PredictionModel
    PredictionModel("models/model.joblib")
    patched_model_io.load.assert_called_once()


def test_leve_file_not_found_si_modele_absent(patched_model_absent):
    from src.prediction_model import PredictionModel
    with pytest.raises(FileNotFoundError):
        PredictionModel("models/model.joblib")


def test_tente_telechargement_si_modele_absent(patched_model_absent):
    from src.prediction_model import PredictionModel
    with pytest.raises(FileNotFoundError):
        PredictionModel("models/model.joblib")
    patched_model_absent.assert_called_once()


# ─────────────────────────────────────────────
# predict()
# ─────────────────────────────────────────────

def test_predict_retourne_un_float(patched_model_io, features_maison):
    patched_model_io.sklearn.predict.return_value = np.array([350000.0])
    from src.prediction_model import PredictionModel
    pm = PredictionModel("models/model.joblib")
    result = pm.predict(features_maison)
    assert isinstance(result, float)
    assert result == 350000.0


def test_predict_passe_un_dataframe_au_modele(patched_model_io, features_appartement):
    from src.prediction_model import PredictionModel
    pm = PredictionModel("models/model.joblib")
    pm.predict(features_appartement)
    args, _ = patched_model_io.sklearn.predict.call_args
    assert isinstance(args[0], pd.DataFrame)


def test_predict_dataframe_contient_les_bonnes_colonnes(patched_model_io, features_maison):
    from src.dataAccess import features as expected_features
    from src.prediction_model import PredictionModel
    pm = PredictionModel("models/model.joblib")
    pm.predict(features_maison)
    args, _ = patched_model_io.sklearn.predict.call_args
    assert list(args[0].columns) == expected_features


def test_predict_maison_et_appartement_distincts(patched_model_io, features_maison, features_appartement):
    patched_model_io.sklearn.predict.side_effect = [np.array([400000.0]), np.array([200000.0])]
    from src.prediction_model import PredictionModel
    pm = PredictionModel("models/model.joblib")
    prix_maison = pm.predict(features_maison)
    prix_appart = pm.predict(features_appartement)
    assert prix_maison == 400000.0
    assert prix_appart == 200000.0
    assert prix_maison != prix_appart


def test_predict_valeur_positive(patched_model_io, features_maison):
    patched_model_io.sklearn.predict.return_value = np.array([150000.0])
    from src.prediction_model import PredictionModel
    pm = PredictionModel("models/model.joblib")
    result = pm.predict(features_maison)
    assert result > 0

