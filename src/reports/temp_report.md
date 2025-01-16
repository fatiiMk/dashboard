
        # Rapport Agricole pour la Parcelle P001

        ## Analyse des Facteurs Influents
        |    |   Importance |
|---:|-------------:|
|  6 |    0.185949  |
| 18 |    0.185236  |
|  0 |    0.155104  |
|  1 |    0.14408   |
|  7 |    0.105879  |
|  2 |    0.0934518 |
|  3 |    0.0891865 |
| 17 |    0.0230779 |
|  4 |    0.0180354 |
|  5 |    0         |
|  8 |    0         |
| 10 |    0         |
| 11 |    0         |
| 12 |    0         |
| 13 |    0         |
| 14 |    0         |
| 15 |    0         |
| 16 |    0         |
|  9 |    0         |
        print("Données d'analyse utilisées dans le rapport :")
        print(analysis.head())
        print("Types des colonnes d'analyse :")
        print(analysis.dtypes)
        



        ## Données Actuelles
        |    | parcelle_id   | date                | culture   |   rendement_estime |   rendement_final |   progression |   temperature |   humidite |   precipitation |   rayonnement_solaire |   vitesse_vent |   direction_vent |   latitude |   longitude | type_sol   |   surface_ha |   capacite_retention_eau |   ph |   matiere_organique |   azote |   phosphore |   potassium |
|---:|:--------------|:--------------------|:----------|-------------------:|------------------:|--------------:|--------------:|-----------:|----------------:|----------------------:|---------------:|-----------------:|-----------:|------------:|:-----------|-------------:|-------------------------:|-----:|--------------------:|--------:|------------:|------------:|
|  0 | P001          | 2020-01-31 00:00:00 | Ble       |               0    |           0       |           0   |          9.26 |      95    |               0 |                     0 |            7   |            185.3 |    33.8534 |      -5.516 | argileux   |         5.07 |                     0.89 |  7.9 |                3.62 |   0.254 |          46 |       255.8 |
|  1 | P001          | 2020-02-29 00:00:00 | Ble       |               0.83 |           0.10043 |          12.1 |         13.44 |      95    |               0 |                     0 |            5.1 |            136.6 |    33.8534 |      -5.516 | argileux   |         5.07 |                     0.89 |  7.9 |                3.62 |   0.254 |          46 |       255.8 |
|  2 | P001          | 2020-03-31 00:00:00 | Ble       |               1.61 |           0.4025  |          25   |         18.39 |      81.34 |               0 |                     0 |            4.9 |            275.7 |    33.8534 |      -5.516 | argileux   |         5.07 |                     0.89 |  7.9 |                3.62 |   0.254 |          46 |       255.8 |
|  3 | P001          | 2020-04-30 00:00:00 | Mais      |               0    |           0       |           0   |         22.66 |      85.06 |               0 |                     0 |            6.9 |            241.6 |    33.8534 |      -5.516 | argileux   |         5.07 |                     0.89 |  7.9 |                3.62 |   0.254 |          46 |       255.8 |
|  4 | P001          | 2020-05-31 00:00:00 | Mais      |               1.6  |           0.2752  |          17.2 |         26.32 |      75.3  |               0 |                     0 |            6.2 |            147.4 |    33.8534 |      -5.516 | argileux   |         5.07 |                     0.89 |  7.9 |                3.62 |   0.254 |          46 |       255.8 |

        ## Recommandations
        Focus sur l'amélioration des sols et la gestion de l'eau.
        