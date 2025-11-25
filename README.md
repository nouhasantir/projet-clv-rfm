# Data Exploration 

### Cette partie du projet consiste à analyser et explorer le dataset Online Retail II afin de comprendre sa structure, vérifier la qualité des données et produire les premiers indicateurs utiles pour la suite (modélisation, segmentation, application Streamlit).

Le notebook utilisé est : 02_data_exploration.ipynb.

#### Contenu du travail
- Chargement des données brutes et intégration du nettoyage du Membre 2.
- Analyse descriptive (dimensions, types, valeurs manquantes, incohérences).
- Visualisations principales : évolution des ventes, distributions prix/quantités, analyse par pays.
  
# Cohort analysis

### Cette étape construit les cohortes d’acquisition et mesure la rétention client dans le temps afin de comprendre le comportement post-acquisition. Les matrices produites servent ensuite au calcul de la CLV empirique et à l’application Streamlit.

#### Contenu du travail

- **Préparation temporelle** : création de `InvoiceMonth`, `AcqMonth` (mois d’acquisition) et `CohortAge` (M+0, M+1, ...).
- **Matrices de cohortes** :
  - `cohort_counts` : nombre de clients actifs par cohorte et âge,
  - `cohort_revenue` : chiffre d’affaires par cohorte et âge.
- **Rétention** : calcul du taux de rétention = actifs à M+t / effectif d’origine (M+0).
- **Visualisations principales** :
  - heatmap de rétention,
  - heatmap du revenu par âge de cohorte,
  - courbe de densité du CA moyen selon l’âge.
- **Principaux enseignements** :
  - forte chute de rétention entre M+0 et M+1,
  - stabilisation d’un noyau fidèle après M+3,
  - majorité de la valeur concentrée sur les trois premiers mois,
  - cohortes 2009–2010 plus grandes et plus rentables.
- **Exports générés** :
  - `cohort_counts.csv`,
  - `cohort_revenue.csv`,
  - figures pour la présentation Streamlit dans `docs/`.


# rfm clv formulee

### Cette étape consiste à construire la table RFM complète, segmenter les clients selon leur comportement d’achat et estimer la Customer Lifetime Value (CLV) via une formule fermée. Le notebook utilise les données nettoyées fournies par le Membre 2.

#### Contenu du travail

- **Préparation des données** : transactions sans doublons, retours exclus, montants corrigés.
- **Calcul RFM** :
  - Recency (jours depuis la dernière commande),
  - Frequency (nombre de factures distinctes),
  - Monetary (total dépensé par client).
- **Scores RFM** : attribution de scores 1–5 (quintiles) puis création du score combiné `RFM_Score = R*100 + F*10 + M`.
- **Segmentation marketing** : identification de segments opérationnels (Champions, Loyal, At-risk, Promising, Others).
- **Mesures clés** :
  - ARPU (revenu moyen par client actif),
  - r (taux de rétention mensuel).
- **CLV via formule fermée** :  
  `CLV = ARPU × r / (1 + d − r)`  
  avec un taux d’actualisation d = 1%.
  Résultats produits : CLV globale et CLV par segment RFM.
- **Export final** : fichier `clean_data/customers_rfm.xlsx` contenant RFM, scores, segments, ARPU et CLV pour exploitation dans l’application Streamlit.


