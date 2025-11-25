# ===============================================
# app/app.py
# Application Streamlit principale :
# - Affiche les KPIs globaux (Overview)
# - Affiche la heatmap de rétention (Cohortes)
# ===============================================

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from utils import load_all, compute_kpis_global, get_retention_matrix

# ---------------------------------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------------------------------
st.set_page_config(
    page_title="Cohortes & CLV - Marketing",
    layout="wide"
)

st.title("📈 Application Cohortes & CLV (Version intégration)")


# ---------------------------------------------------
# CHARGEMENT DES DONNÉES
# ---------------------------------------------------
@st.cache_data
def get_data():
    cohort_counts, cohort_revenue = load_all()
    return cohort_counts, cohort_revenue

cohort_counts, cohort_revenue = get_data()


# ---------------------------------------------------
# SIDEBAR : navigation simple
# ---------------------------------------------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview (KPIs)", "Cohortes (heatmap)", "Segments (placeholder)", "Scénarios (placeholder)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Filtres futurs :**")
st.sidebar.caption("Période, pays, type client, retours... (à intégrer plus tard)")


# ---------------------------------------------------
# PAGE 1 : OVERVIEW (KPIs)
# ---------------------------------------------------
if page == "Overview (KPIs)":
    st.subheader("Vue globale (KPIs)")

    # Calcul des KPIs globaux
    kpis = compute_kpis_global(cohort_counts, cohort_revenue)

    col1, col2, col3 = st.columns(3)
    col1.metric("Clients acquis", f"{kpis['clients_acquis']:.0f}")
    col2.metric("CA total", f"{kpis['ca_total']:.2f}")
    col3.metric("CLV moyenne (approx.)", f"{kpis['clv_moyenne']:.2f}")

    st.markdown("---")
    st.markdown(
        """
        Ces indicateurs sont calculés à partir des matrices agrégées :

        - **Clients acquis** : somme des effectifs à l'âge 0 dans `cohort_counts`
        - **CA total** : somme de toutes les valeurs de `cohort_revenue`
        - **CLV moyenne approximative** : CA total / nombre de clients acquis

        Ils servent de base pour paramétrer les autres vues (cohortes, segments, scénarios).
        """
    )


# ---------------------------------------------------
# PAGE 2 : COHORTES (HEATMAP)
# ---------------------------------------------------
elif page == "Cohortes (heatmap)":
    st.subheader("Analyse des cohortes d’acquisition")

    st.markdown(
        """
        Cette vue permet de visualiser la **rétention** par cohorte d’acquisition.
        Chaque cellule de la heatmap représente le **taux de clients encore actifs**
        à un âge donné (en mois) pour une cohorte donnée.
        """
    )

    # Matrice de rétention
    ret_matrix = get_retention_matrix(cohort_counts)

    # Option de focus sur un sous-ensemble d'âges
    all_ages = [int(c) for c in ret_matrix.columns]
    min_age, max_age = min(all_ages), max(all_ages)

    selected_max_age = st.slider(
        "Âge maximum de cohorte à afficher (mois)",
        min_value=min_age,
        max_value=max_age,
        value=max_age
    )

    # Filtrer les colonnes de la heatmap
    cols_to_show = [str(a) for a in range(min_age, selected_max_age + 1)]
    ret_to_plot = ret_matrix[cols_to_show]

    # Heatmap
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(
        ret_to_plot,
        cmap="Blues",
        ax=ax,
        fmt=".2f"
    )
    ax.set_title("Heatmap de rétention par cohorte", fontsize=16)
    ax.set_xlabel("Âge de cohorte (mois)")
    ax.set_ylabel("Cohorte d’acquisition (AcqMonth)")

    st.pyplot(fig)

    st.markdown(
        """
        **Lecture de la heatmap :**
        - Chaque **ligne** = une cohorte d’acquisition (mois d’entrée des clients)
        - Chaque **colonne** = l’âge de la cohorte (M+0, M+1, …)
        - Chaque **case** = proportion de clients encore actifs à cet âge

        Les zones plus foncées indiquent des cohortes qui retiennent mieux leurs clients.
        """
    )


# ---------------------------------------------------
# PAGE 3 : SEGMENTS (PLACEHOLDER)
# ---------------------------------------------------
elif page == "Segments (placeholder)":
    st.subheader("Segments RFM (à intégrer)")

    st.info(
        """
        Cette page est un **placeholder** pour l'intégration future des segments RFM.
        
        Elle pourra afficher :
        - Une table des segments RFM (Champions, À risque, etc.)
        - Les volumes, CA, marge, panier moyen par segment
        - Les recommandations d’activation CRM (où investir / où réduire)

        Pour le moment, les données RFM ne sont pas encore intégrées dans ce projet.
        """
    )


# ---------------------------------------------------
# PAGE 4 : SCÉNARIOS (PLACEHOLDER)
# ---------------------------------------------------
elif page == "Scénarios (placeholder)":
    st.subheader("Scénarios de rétention / marge / remises (à intégrer)")

    st.info(
        """
        Cette page est un **placeholder** pour les futures simulations de scénarios.

        Elle pourra permettre :
        - d’ajuster la rétention (r), la marge, les remises
        - de recalculer une CLV théorique par cohorte / segment
        - de comparer un **baseline** vs **scénario** (Δ CLV, Δ CA, Δ rétention)

        Ces fonctionnalités seront ajoutées une fois que les modules CLV / RFM seront finalisés.
        """
    )
