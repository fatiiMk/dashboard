import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from datetime import datetime

class AgriculturalAnalyzer:
    def __init__(self, data_manager):
        """
        Initialise l’analyseur avec le gestionnaire de données

        Cette classe utilise les données historiques et actuelles
        pour générer des insights agronomiques pertinents.
        """
        self.data_manager = data_manager
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def analyze_yield_factors(self, parcelle_id):
        """
        Analyse les facteurs influençant les rendements

        Cette méthode combine les données historiques avec les
        caractéristiques actuelles du sol et le climat pour
        identifier les principaux facteurs de performance.
        """
         # Charger les données pour la parcelle
        yield_data = self.data_manager.yield_history[self.data_manager.yield_history["parcelle_id"] == parcelle_id]
        weather_data = self.data_manager.weather_data
        soil_data = self.data_manager.soil_data[self.data_manager.soil_data["parcelle_id"] == parcelle_id]

        # Fusionner les données
        merged_data = pd.merge(yield_data, weather_data, on="date", how="left")
        merged_data = pd.merge(merged_data, soil_data, on="parcelle_id", how="left")

        # Supprimer les colonnes non pertinentes ou redondantes
        merged_data = merged_data.drop(columns=["date", "parcelle_id"], errors="ignore")

        # Encodage des colonnes catégoriques
        merged_data = pd.get_dummies(merged_data, drop_first=True)

        # Vérification des colonnes disponibles
        print("Colonnes utilisées pour le modèle :", merged_data.columns)

        # Préparation des données pour l'entraînement du modèle
        features = merged_data.drop(columns=["rendement_final"], errors="ignore")
        target = merged_data["rendement_final"]

        # Vérifiez qu'il n'y a pas de valeurs manquantes
        features = features.fillna(0)
        target = target.fillna(target.mean())
        print("Aperçu de 'features' avant entraînement :")
        print(features.head())
        print("Types des colonnes dans 'features' :")
        print(features.dtypes)
        features = features.apply(pd.to_numeric, errors='coerce').fillna(0)
        features['culture_Mais'] = features['culture_Mais'].astype(int)
        features['culture_Tournesol'] = features['culture_Tournesol'].astype(int)
        
        print("Données envoyées au modèle :")
        print(features.head())
        print("Types des colonnes envoyées au modèle :")
        print(features.dtypes)


        print("Validation finale : types des colonnes dans 'features' après conversion :")
        print(features.dtypes)
        




        # Entraîner le modèle
        self.model.fit(features, target)
        feature_importances = pd.DataFrame({
            "Feature": features.columns,
            "Importance": self.model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        return feature_importances


    def _calculate_yield_correlations(self, yield_data, weather_data, soil_data):
        """
        Calcule les corrélations entre les rendements et
        différents facteurs environnementaux.
        """
        # Fusionner les données
        merged_data = pd.merge(yield_data, weather_data, on="date", how="left")
        merged_data = pd.merge(merged_data, soil_data, on="parcelle_id", how="left")

        # Supprimer les colonnes non numériques
        numeric_columns = merged_data.select_dtypes(include=[np.number]).columns
        print("Colonnes numériques utilisées pour les corrélations :", numeric_columns)

        # Vérifiez si "rendement_final" est dans les colonnes numériques
        if "rendement_final" not in numeric_columns:
            raise ValueError("La colonne 'rendement_final' n'est pas numérique ou est absente.")

        # Calcul des corrélations
        correlation_matrix = merged_data[numeric_columns].corr()["rendement_final"].sort_values(ascending=False)
        return correlation_matrix



    def _identify_limiting_factors(self, parcelle_data, correlations):
        """
        Identifie les facteurs limitant le rendement.
        """
        limiting_factors = correlations[correlations < 0.3]
        return limiting_factors

    def _analyze_performance_trend(self, parcelle_data):
        """
        Analyse la tendance de performance de la parcelle
        en identifiant les motifs significatifs.
        """
        yield_series = parcelle_data[["date", "rendement_final"]].set_index("date")
        
        # Calcul de la tendance avec une fenêtre ajustable
        yield_series["trend"] = yield_series["rendement_final"].rolling(window=5, min_periods=1).mean()
        
        # Remplir les valeurs NaN avec la méthode forward-fill
        yield_series["trend"].fillna(method="bfill", inplace=True)
        
        return yield_series


    def _detect_yield_breakpoints(self, yield_series):
        """
        Détecte les changements significatifs dans la série temporelle des rendements.
        """
        # Calculer les différences
        differences = yield_series.diff().dropna()

        # Calculer les scores Z
        z_scores = stats.zscore(differences)

        # Créer un masque logique pour détecter les points de rupture
        breakpoints_mask = np.abs(z_scores) > 2

        # Réindexer le masque logique pour aligner avec l'index de yield_series
        aligned_breakpoints_mask = pd.Series(breakpoints_mask, index=yield_series.index[1:]).reindex(yield_series.index, fill_value=False)

        # Filtrer les points de rupture
        breakpoints = yield_series[aligned_breakpoints_mask]
        
        return breakpoints


    def _analyze_yield_stability(self, yield_series):
        """
        Analyse la stabilité des rendements au fil du temps.
        """
        stability_metrics = {
            "Standard Deviation": yield_series.std(),
            "Coefficient of Variation": yield_series.std() / yield_series.mean(),
        }
        return stability_metrics

    def _calculate_stability_index(self, yield_series):
        """
        Calcule un index de stabilité personnalisé.
        """
        trend = LinearRegression().fit(
            np.arange(len(yield_series)).reshape(-1, 1),
            yield_series
        ).coef_[0]

        variability = yield_series.std()
        stability_index = trend / (1 + variability)
        return stability_index
