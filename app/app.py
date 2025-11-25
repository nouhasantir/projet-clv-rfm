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
from utils import load_all, compute_kpis_global, get_retention_matrix, load_rfm


# ---------------------------------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------------------------------
st.set_page_config(
    page_title="Cohortes & CLV - Marketing",
    layout="wide"
)

st.title("📈 Application Cohortes & CLV (Version intégration)")

# PAGE 1 : OVERVIEW (KPIs)
if page == "Overview (KPIs)":
    ...
# ---------------------------------------------------
# PAGE 2 : EXPLORATION GLOBALE (inspirée du notebook d'explo)
# ---------------------------------------------------
elif page == "Exploration (global)":
    st.subheader("Exploration globale des cohortes")

    st.markdown(
        """
        Cette page reprend une partie des analyses du notebook d'exploration :
        distribution des tailles de cohortes, répartition du CA, et dynamique
        globale de la valeur par âge.
        """
    )

    acq_col = "AcqMonth"

    # 1) Taille des cohortes (nombre de clients à l'âge 0)
    st.markdown("### Taille des cohortes (clients à l’acquisition)")
    if "0" in cohort_counts.columns:
        cohort_sizes = cohort_counts[[acq_col, "0"]].set_index(acq_col)["0"]

        fig_a, ax_a = plt.subplots(figsize=(10, 4))
        cohort_sizes.plot(kind="bar", ax=ax_a)
        ax_a.set_title("Nombre de clients par cohorte d’acquisition")
        ax_a.set_xlabel("Cohorte (AcqMonth)")
        ax_a.set_ylabel("Nombre de clients (âge 0)")
        plt.xticks(rotation=90)
        st.pyplot(fig_a)
    else:
        st.warning("La colonne '0' n'est pas disponible dans cohort_counts.")

    st.markdown("---")

    # 2) CA total par cohorte
    st.markdown("### Chiffre d’affaires total par cohorte")

    age_cols_revenue = [c for c in cohort_revenue.columns if c != acq_col]
    coh_ca = cohort_revenue[age_cols_revenue].sum(axis=1)
    coh_ca.index = cohort_revenue[acq_col]

    fig_b, ax_b = plt.subplots(figsize=(10, 4))
    coh_ca.plot(kind="bar", ax=ax_b, color="tab:green")
    ax_b.set_title("CA total par cohorte d’acquisition")
    ax_b.set_xlabel("Cohorte (AcqMonth)")
    ax_b.set_ylabel("Chiffre d’affaires total")
    plt.xticks(rotation=90)
    st.pyplot(fig_b)

    st.markdown(
        "On observe quelles cohortes ont généré le plus de valeur globale "
        "(effet volume × qualité des clients)."
    )

    st.markdown("---")

    # 3) Densité de CA par âge (similar à ton graphique 'age_revenue')
    st.markdown("### Densité de CA par âge de cohorte (toutes cohortes)")

    ca_by_age = cohort_revenue[age_cols_revenue].mean(axis=0)
    ca_by_age.index = ca_by_age.index.astype(int)
    ca_by_age = ca_by_age.sort_index()

    fig_c, ax_c = plt.subplots(figsize=(8, 4))
    ax_c.bar(ca_by_age.index, ca_by_age.values)
    ax_c.set_title("CA moyen par âge de cohorte (densité de valeur)")
    ax_c.set_xlabel("Âge de cohorte (mois)")
    ax_c.set_ylabel("CA moyen")
    st.pyplot(fig_c)

    st.caption(
        "Ce graphique est l’équivalent de ta 'densité de chiffre d’affaires par âge de cohorte' "
        "dans le notebook de cohortes : il montre où se concentre la valeur dans le temps."
    )



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
# ---------------------------------------------------
# PAGE : SEGMENTS RFM
# ---------------------------------------------------
elif page == "Segments (placeholder)":
    st.subheader("Segments RFM")

    rfm = get_rfm_data()
    if rfm is None:
        st.warning(
            "Les données RFM ne sont pas encore disponibles "
            "(fichier `data/rfm_segments.csv` manquant)."
        )
    else:
        st.markdown(
            """
            Cette page présente la **segmentation RFM** (Recency, Frequency, Monetary)
            et permet de prioriser les actions CRM par segment.
            """
        )

        # KPIs globaux RFM
        nb_clients = rfm["CustomerID"].nunique() if "CustomerID" in rfm.columns else len(rfm)
        nb_segments = rfm["Segment"].nunique() if "Segment" in rfm.columns else None

        col1, col2, col3 = st.columns(3)
        col1.metric("Clients segmentés", f"{nb_clients}")
        if nb_segments is not None:
            col2.metric("Nombre de segments", f"{nb_segments}")
        if "Monetary" in rfm.columns:
            col3.metric("Monetary moyen", f"{rfm['Monetary'].mean():.2f}")

        st.markdown("---")

        # Table des segments : agrégation
        if "Segment" in rfm.columns:
            st.markdown("### Vue agrégée par segment")

            agg_cols = {}
            if "CustomerID" in rfm.columns:
                agg_cols["CustomerID"] = "nunique"
            if "Monetary" in rfm.columns:
                agg_cols["Monetary"] = "sum"
            if "Recency" in rfm.columns:
                agg_cols["Recency"] = "mean"
            if "Frequency" in rfm.columns:
                agg_cols["Frequency"] = "mean"

            seg_agg = rfm.groupby("Segment").agg(agg_cols)
            seg_agg = seg_agg.rename(
                columns={
                    "CustomerID": "Nb_clients",
                    "Monetary": "CA_total",
                    "Recency": "Recency_moy",
                    "Frequency": "Frequency_moy",
                }
            )
            seg_agg = seg_agg.reset_index()

            st.dataframe(seg_agg, use_container_width=True)

            st.caption(
                "Chaque ligne correspond à un segment RFM. "
                "`Nb_clients` = effectif du segment, `CA_total` = chiffre d'affaires total, "
                "`Recency_moy` = nombre moyen de jours depuis le dernier achat, "
                "`Frequency_moy` = nombre moyen d'achats."
            )

            st.markdown("---")

            # Graphiques : volume & CA par segment
            colg1, colg2 = st.columns(2)

            with colg1:
                fig_s1, ax_s1 = plt.subplots(figsize=(5, 4))
                ax_s1.bar(seg_agg["Segment"], seg_agg["Nb_clients"])
                ax_s1.set_title("Nombre de clients par segment")
                ax_s1.set_xlabel("Segment RFM")
                ax_s1.set_ylabel("Nb clients")
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig_s1)

            with colg2:
                if "CA_total" in seg_agg.columns:
                    fig_s2, ax_s2 = plt.subplots(figsize=(5, 4))
                    ax_s2.bar(seg_agg["Segment"], seg_agg["CA_total"])
                    ax_s2.set_title("CA total par segment")
                    ax_s2.set_xlabel("Segment RFM")
                    ax_s2.set_ylabel("CA total")
                    plt.xticks(rotation=45, ha="right")
                    st.pyplot(fig_s2)

            st.markdown("---")

            # Focus sur un segment avec recommandations
            st.markdown("### Focus sur un segment & recommandations CRM")

            chosen_segment = st.selectbox(
                "Choisir un segment à analyser",
                seg_agg["Segment"].tolist()
            )

            subset = rfm[rfm["Segment"] == chosen_segment]
            st.write(f"**{len(subset)} clients** dans le segment *{chosen_segment}*.")

            if "Monetary" in subset.columns:
                st.write(f"- CA moyen par client : **{subset['Monetary'].mean():.2f}**")
            if "Recency" in subset.columns:
                st.write(f"- Recency moyenne : **{subset['Recency'].mean():.1f}**")
            if "Frequency" in subset.columns:
                st.write(f"- Frequency moyenne : **{subset['Frequency'].mean():.2f}**")

            st.markdown("#### Idées d’actions CRM (exemples)")

            if "champ" in chosen_segment.lower() or "champion" in chosen_segment.lower():
                st.markdown(
                    """
                    - ✅ **Conserver la valeur** : programmes VIP, early access, nouveautés.
                    - 💌 Emails personnalisés, avantages exclusifs.
                    - 🎯 Objectif : **augmenter la fréquence** sans trop de remises.
                    """
                )
            elif "risque" in chosen_segment.lower():
                st.markdown(
                    """
                    - ⚠️ **Relance ciblée** : offre de réactivation, coupon de retour.
                    - 📆 Scénarios d’email marketing automatisés.
                    - 🎯 Objectif : réduire le churn sur des clients historiquement bons.
                    """
                )
            elif "nouveau" in chosen_segment.lower() or "new" in chosen_segment.lower():
                st.markdown(
                    """
                    - 🍼 **Onboarding** : séquence de bienvenue, découverte du catalogue.
                    - 🙌 Rassurer (livraison, SAV) + premières incitations à racheter.
                    - 🎯 Objectif : transformer en clients réguliers.
                    """
                )
            else:
                st.markdown(
                    """
                    - Analyse plus fine à réaliser selon le profil du segment.
                    - Actions possibles : campagnes dédiées, cross-sell, up-sell.
                    """
                )

        else:
            st.warning("La colonne 'Segment' est absente du fichier rfm_segments.csv.")

@st.cache_data
def get_rfm_data():
    try:
        rfm = load_rfm()
        return rfm
    except FileNotFoundError:
        return None
