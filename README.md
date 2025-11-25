# Data Exploration 

### Cette partie du projet consiste à analyser et explorer le dataset Online Retail II afin de comprendre sa structure, vérifier la qualité des données et produire les premiers indicateurs utiles pour la suite (modélisation, segmentation, application Streamlit).

Le notebook utilisé est : 02_data_exploration.ipynb.

Il contient :
- Chargement des données brutes et intégration du nettoyage du Membre 2.
- Analyse descriptive (dimensions, types, valeurs manquantes, incohérences).
- Visualisations principales : évolution des ventes, distributions prix/quantités, analyse par pays.
  
# Cohort Analysis
### Cette étape du projet consiste à construire les cohortes d’acquisition, mesurer la rétention client dans le temps et analyser la dynamique de chiffre d’affaires par âge de cohorte. Le but est de comprendre le comportement post-acquisition des clients et de fournir les matrices nécessaires au calcul de la CLV empirique et à l’application Streamlit.
Le notebook utilisé est : 03_cohort_analysis.ipynb.
Il contient :
-Préparation temporelle des données : création de InvoiceMonth, AcqMonth (mois d’acquisition) et CohortAge (M+0, M+1, ...).
-	Construction des matrices de cohortes :
-cohort_counts : nombre de clients actifs par cohorte et par âge,
-cohort_revenue : chiffre d’affaires généré par cohorte et par âge.
-Calcul des taux de rétention : ratio entre le nombre de clients actifs à M+t et l’effectif initial de la cohorte (M+0).
-Visualisations principales :
-heatmap de rétention par cohorte,
-heatmap du revenu par âge de cohorte,
-densité du chiffre d’affaires moyen selon l’âge.
-Résultats clés observés :
-forte baisse de rétention entre M+0 et M+1,
-stabilisation d’un noyau fidèle à partir de M+3,
o	concentration de la valeur client principalement sur les trois premiers mois,
o	cohortes anciennes (2009–2010) plus volumineuses et plus rentables.
•	Exports produits :
o	cohort_counts.csv,
o	cohort_revenue.csv,
o	graphiques pour la présentation Streamlit dans docs.


# rfm clv formulee

Cette étape consiste à construire la table RFM complète, segmenter les clients selon leur comportement d’achat et estimer la Customer Lifetime Value (CLV) via une formule fermée. Le notebook utilise les données nettoyées fournies par le Membre 2.

### Contenu du travail

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


