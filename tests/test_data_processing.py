"""
Tests unitaires pour src/dataProcessing.py
"""
import pytest
import pandas as pd
from unittest.mock import patch


# ─────────────────────────────────────────────
# Logique de renommage (sans I/O)
# ─────────────────────────────────────────────

def test_renommage_colonnes(raw_df):
    """La logique de renommage transforme les espaces en underscores."""
    df = raw_df
    df = df.rename(columns={
        "Type local": "Type_local",
        "Surface reelle bati": "Surface_reelle_bati",
        "Nombre pieces principales": "Nombre_pieces_principales",
        "Surface terrain": "Surface_terrain",
        "Valeur fonciere": "Valeur_fonciere",
    })
    assert "Type_local" in df.columns
    assert "Surface_reelle_bati" in df.columns
    assert "Nombre_pieces_principales" in df.columns
    assert "Surface_terrain" in df.columns
    assert "Valeur_fonciere" in df.columns
    assert "Type local" not in df.columns


def test_conversion_virgule_vers_point():
    """La conversion virgule → point produit des flottants corrects."""
    df = pd.DataFrame({"valeur": ["1,5", "100,25", "0,0", "999999,99"]})
    df["valeur"] = df["valeur"].astype(str).str.replace(",", ".").astype(float)
    assert df["valeur"].tolist() == [1.5, 100.25, 0.0, 999999.99]


def test_suppression_nan_valeur_fonciere():
    """Les lignes sans Valeur_fonciere doivent être supprimées."""
    df = pd.DataFrame({
        "Valeur_fonciere": [250000.0, None, 180000.0],
        "autreCol": [1, 2, 3],
    })
    df = df.dropna(subset=["Valeur_fonciere"])
    assert df["Valeur_fonciere"].isna().sum() == 0
    assert len(df) == 2


# ─────────────────────────────────────────────
# process_data (avec mocks I/O)
# ─────────────────────────────────────────────

def test_process_data_appelle_read_csv(patched_process_io):
    with patch.object(pd.DataFrame, "to_csv", return_value=None):
        from src.dataProcessing import process_data
        process_data("ValeursFoncieres-2025.txt", "2025.csv")
    patched_process_io.assert_called_once()


def test_process_data_supprime_lignes_sans_valeur_fonciere(patched_process_io):
    captured = {}

    def fake_to_csv(path, index=False):
        # `self` est le DataFrame (méthode liée)
        pass

    # On capture le DataFrame passé à to_csv via un side_effect sur l'instance
    original_to_csv = pd.DataFrame.to_csv

    def capturing_to_csv(self, path, index=False):
        captured["df"] = self.copy()

    with patch.object(pd.DataFrame, "to_csv", capturing_to_csv):
        from src import dataProcessing
        dataProcessing.process_data("ValeursFoncieres-2025.txt", "2025.csv")

    result = captured.get("df")
    assert result is not None
    # La ligne avec Valeur_fonciere=None doit avoir été supprimée
    assert result["Valeur_fonciere"].isna().sum() == 0


def test_process_data_renomme_colonnes(patched_process_io):
    captured = {}

    def capturing_to_csv(self, path, index=False):
        captured["df"] = self.copy()

    with patch.object(pd.DataFrame, "to_csv", capturing_to_csv):
        from src import dataProcessing
        dataProcessing.process_data("ValeursFoncieres-2025.txt", "2025.csv")

    result = captured.get("df")
    assert result is not None
    assert "Type_local" in result.columns
    assert "Surface_reelle_bati" in result.columns
    assert "Valeur_fonciere" in result.columns
    # Les anciens noms ne doivent plus exister
    assert "Type local" not in result.columns
    assert "Valeur fonciere" not in result.columns


def test_process_data_convertit_numeriques(patched_process_io):
    captured = {}

    def capturing_to_csv(self, path, index=False):
        captured["df"] = self.copy()

    with patch.object(pd.DataFrame, "to_csv", capturing_to_csv):
        from src import dataProcessing
        dataProcessing.process_data("ValeursFoncieres-2025.txt", "2025.csv")

    result = captured.get("df")
    assert result is not None
    # Les colonnes numériques doivent être de type float, pas str
    assert pd.api.types.is_float_dtype(result["Surface_reelle_bati"])
    assert pd.api.types.is_float_dtype(result["Valeur_fonciere"])
