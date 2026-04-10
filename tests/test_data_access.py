"""
Tests unitaires pour src/dataAccess.py
"""
import pytest
import pandas as pd


# ─────────────────────────────────────────────
# Constantes
# ─────────────────────────────────────────────

def test_features_contains_expected_columns():
    from src.dataAccess import features
    assert "Surface_reelle_bati" in features
    assert "Surface_terrain" in features
    assert "Nombre_pieces_principales" in features
    assert "Type_local" in features


def test_target_contains_valeur_fonciere():
    from src.dataAccess import target
    assert "Valeur_fonciere" in target


# ─────────────────────────────────────────────
# prepare_features
# ─────────────────────────────────────────────

def test_prepare_features_filtres_type_local_non_residentiel(sample_df):
    from src.dataAccess import prepare_features
    result = prepare_features(sample_df)
    assert all(t in ["Maison", "Appartement"] for t in result["Type_local"])


def test_prepare_features_supprime_local_industriel(sample_df):
    from src.dataAccess import prepare_features
    result = prepare_features(sample_df)
    # "Local industriel" retiré → 3 lignes restantes
    assert len(result) == 3


def test_prepare_features_remplit_surface_terrain_nan(sample_df):
    from src.dataAccess import prepare_features
    result = prepare_features(sample_df)
    assert result["Surface_terrain"].isna().sum() == 0
    # Les NaN doivent être remplacés par 0
    assert 0.0 in result["Surface_terrain"].values


def test_prepare_features_supprime_lignes_nan_restantes():
    from src.dataAccess import prepare_features
    df = pd.DataFrame({
        "Surface_reelle_bati": [80.0, None, 120.0],
        "Surface_terrain": [100.0, 0.0, 300.0],
        "Nombre_pieces_principales": [3, 2, 5],
        "Type_local": ["Maison", "Maison", "Appartement"],
        "Valeur_fonciere": [250000.0, 180000.0, 400000.0],
    })
    result = prepare_features(df)
    assert result.isna().sum().sum() == 0


def test_prepare_features_retourne_uniquement_colonnes_attendues(sample_df):
    from src.dataAccess import prepare_features, features, target
    result = prepare_features(sample_df)
    assert set(result.columns) == set(features + target)


def test_prepare_features_ignore_colonnes_supplementaires(sample_df):
    from src.dataAccess import prepare_features, features, target
    sample_df["colonne_extra"] = "valeur"
    result = prepare_features(sample_df)
    assert "colonne_extra" not in result.columns


def test_prepare_features_df_vide_retourne_df_vide():
    from src.dataAccess import prepare_features
    df = pd.DataFrame(columns=[
        "Surface_reelle_bati", "Surface_terrain",
        "Nombre_pieces_principales", "Type_local", "Valeur_fonciere",
    ])
    result = prepare_features(df)
    assert len(result) == 0


# ─────────────────────────────────────────────
# get_data
# ─────────────────────────────────────────────

def test_get_data_appelle_read_csv(patched_access_io):
    from src.dataAccess import get_data
    df = get_data()
    patched_access_io.assert_called_once()
    assert isinstance(df, pd.DataFrame)


def test_get_data_retourne_dataframe(patched_access_io):
    from src.dataAccess import get_data
    result = get_data()
    assert isinstance(result, pd.DataFrame)
