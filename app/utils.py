# ===============================================
# app/utils.py
# Module utilitaire contenant toutes les fonctions
# nécessaires au chargement des données,
# au calcul des KPIs globaux,
# et à la génération de la matrice de rétention.
# ===============================================

import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# CHEMIN D'ACCÈS AUX DONNÉES
# ---------------------------------------------------
# __file__ = chemin du fichier utils.py
# parents[1] = remonte d'un dossier (app/) vers la racine du projet
# / "data" = ajoute le dossier data/ à la fin
#
# Résultat : data/ est trouvé automatiquement, même si le projet
# est déplacé sur un autre ordinateur.
# ---------------------------------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


# ---------------------------------------------------
# FONCTIONS DE CHARGEMENT DES DONNÉES
# ---------------------------------------------------
def load_cohort_counts():
    """
    Charge le fichier cohort_counts.csv
    Ce fichier contient :
    - AcqMonth (cohorte d'acquisition)
    - Colonnes 0,1,2,... représentant l'âge de cohorte
    - Valeurs = nombre de clients actifs
    """
    return pd.read_csv(DATA_DIR / "cohort_counts.csv")


def load_cohort_revenue():
    """
    Charge le fichier cohort_revenue.csv
    Ce fichier contient :
    - AcqMonth (cohorte d'acquisition)
    - Colonnes 0,1,2,... représentant l'âge de cohorte
    - Valeurs = revenu généré durant ce mois d'âge
    """
    return pd.read_csv(DATA_DIR / "cohort_revenue.csv")


def load_all():
    """
    Charge les deux fichiers et les retourne ensemble.
    Utile pour l'app Streamlit.
    """
    cohort_counts = load_cohort_counts()
    cohort_revenue = load_cohort_revenue()
    return cohort_counts, cohort_revenue


# ---------------------------------------------------
# CALCUL DES KPIs GLOBAUX
# ---------------------------------------------------
def compute_kpis_global(cohort_counts: pd.DataFrame, cohort_revenue: pd.DataFrame):
    """
    Calcule trois KPIs essentiels pour la page d'Overview Streamlit :
    - clients_acquis : nombre total de clients (âge 0)
    - ca_total       : chiffre d'affaires total (toutes cohortes x âges)
    - clv_moyenne    : CA moyen généré par client (approximation CLV)
    """

    acq_col = "AcqMonth"

    # Colonnes d'âge (toutes sauf AcqMonth)
    age_cols_counts = [c for c in cohort_counts.columns if c != acq_col]
    age_cols_revenue = [c for c in cohort_revenue.columns if c != acq_col]

    # Vérification que la colonne "0" existe (âge 0 = acquisition)
    if "0" not in cohort_counts.columns:
        raise KeyError("La colonne '0' (âge 0) est absente de cohort_counts.")

    # 1) Nombre total de clients acquis = somme des effectifs à l'âge 0
    nb_clients_acquis = cohort_counts["0"].sum()

    # 2) CA total = somme de toutes les cases du tableau de revenus
    ca_total = cohort_revenue[age_cols_revenue].sum().sum()

    # 3) CLV moyenne = CA total / nombre de clients acquis
    clv_moyenne = ca_total / nb_clients_acquis if nb_clients_acquis > 0 else None

    return {
        "clients_acquis": nb_clients_acquis,
        "ca_total": ca_total,
        "clv_moyenne": clv_moyenne,
    }


# ---------------------------------------------------
# MATRICE DE RÉTENTION
# ---------------------------------------------------
def get_retention_matrix(cohort_counts: pd.DataFrame):
    """
    Construit une matrice de rétention prête à être visualisée (heatmap).

    Rétention = count(age_k) / count(age_0)

    - Index    : AcqMonth (cohortes)
    - Colonnes : âges 0,1,2,... (mois après acquisition)
    - Valeurs  : taux de rétention entre 0 et 1
    """

    acq_col = "AcqMonth"

    if acq_col not in cohort_counts.columns:
        raise KeyError("La colonne 'AcqMonth' est absente de cohort_counts.")

    # Colonnes d'âge
    age_cols = [c for c in cohort_counts.columns if c != acq_col]

    if "0" not in cohort_counts.columns:
        raise KeyError("La colonne '0' (âge 0) est absente de cohort_counts.")

    # Calcul de la rétention : chaque ligne divisée par sa valeur d'âge 0
    retention = cohort_counts[age_cols].div(cohort_counts["0"], axis=0)

    # Rétablir AcqMonth avant de convertir en index
    retention.insert(0, acq_col, cohort_counts[acq_col])
    retention = retention.set_index(acq_col)

    return retention
def load_rfm():
    """
    Charge le fichier rfm_segments.csv contenant la segmentation RFM.

    Colonnes typiques :
    - CustomerID
    - Recency, Frequency, Monetary
    - RFM_Score
    - Segment (Champions, À risque, Potentiel, etc.)
    - Revenue (facultatif)
    """
    return pd.read_csv(DATA_DIR / "rfm_segments.csv")
