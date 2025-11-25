# Data Exploration 

### Cette partie du projet consiste à analyser et explorer le dataset Online Retail II afin de comprendre sa structure, vérifier la qualité des données et produire les premiers indicateurs utiles pour la suite (modélisation, segmentation, application Streamlit).

Le notebook utilisé est : 02_data_exploration.ipynb.

Il contient :
- Chargement des données brutes et intégration du nettoyage du Membre 2.
- Analyse descriptive (dimensions, types, valeurs manquantes, incohérences).
- Visualisations principales : évolution des ventes, distributions prix/quantités, analyse par pays.

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


