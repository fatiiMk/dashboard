import folium
from folium import plugins
from branca.colormap import LinearColormap
import numpy as np
import os


class AgriculturalMap:
    def __init__(self, data_manager):
        """
        Initialise la carte avec le gestionnaire de données.
        """
        self.data_manager = data_manager
        self.map = None
        self.yield_colormap = LinearColormap(
            colors=['red', 'yellow', 'green'],
            vmin=0,
            vmax=12,  # Rendement maximum en tonnes/ha
            caption="Rendements (tonnes/ha)"
        )

    def create_base_map(self):
        """
        Crée la carte de base centrée sur les parcelles.
        """
        center_lat = self.data_manager.soil_data['latitude'].mean()
        center_lon = self.data_manager.soil_data['longitude'].mean()
        self.map = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

    def add_yield_history_layer(self,):
        """
        Ajoute une couche visualisant l’historique des rendements.
        """
        data = self.data_manager.yield_history.merge(
            self.data_manager.soil_data[['parcelle_id', 'latitude', 'longitude']],
            on='parcelle_id',
            how='left'
        )
        yield_layer = folium.FeatureGroup(name="Marqueurs d'Historique des Rendements")

        for _, row in data.iterrows():
            if not np.isnan(row['latitude']) and not np.isnan(row['longitude']):
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=7,
                    color=self.yield_colormap(row['rendement_final']),
                    fill=True,
                    fill_opacity=0.7,
                    popup=(
                        f"Parcelle: {row['parcelle_id']}<br>Date: {row['date']}<br>"
                        f"Rendement Estimé: {row['rendement_estime']:.2f} tonnes/ha<br>"
                        f"Rendement Final: {row['rendement_final']:.2f} tonnes/ha"
                    ),
                ).add_to(yield_layer)
        yield_layer.add_to(self.map)
        
          


    def add_current_ndvi_layer(self):
        """
        Ajoute une couche NDVI avec un nombre limité de points pour améliorer les performances.
        """
        valid_data = self.data_manager.monitoring_data.dropna(subset=['latitude', 'longitude', 'ndvi', 'lai'])

        # Limiter le nombre de points affichés
        max_points = 1000  # Réduire à 1000 points maximum
        if len(valid_data) > max_points:
            valid_data = valid_data.sample(n=max_points, random_state=42)

        ndvi_layer = folium.FeatureGroup(name="NDVI actuel")

        for _, row in valid_data.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"NDVI: {row['ndvi']:.2f}<br>LAI: {row['lai']:.2f}",
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(ndvi_layer)
            ndvi_layer.add_to(self.map)



    def add_risk_heatmap(self):
        """
        Ajoute une carte de chaleur des zones à risque.
        """
        # Filtrage des données pour exclure les valeurs nulles ou trop faibles
        heat_data = self.data_manager.monitoring_data[
            self.data_manager.monitoring_data['stress_hydrique'] > 0
        ][['latitude', 'longitude', 'stress_hydrique']].dropna()

        if heat_data.empty:
            print("Aucune donnée significative pour la heatmap.")
            return

        # Normalisation des valeurs de stress_hydrique
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        heat_data['stress_hydrique_normalized'] = scaler.fit_transform(
            heat_data[['stress_hydrique']]
        )

        # Préparation des données pour la heatmap
        heatmap_data = [
            [row['latitude'], row['longitude'], row['stress_hydrique_normalized']]
            for _, row in heat_data.iterrows()
        ]


        # Création de la couche heatmap
        heatmap_layer = folium.FeatureGroup(name="Carte de Chaleur des Risques")
        plugins.HeatMap(heatmap_data, min_opacity=0.2, radius=15, blur=10).add_to(heatmap_layer)
        heatmap_layer.add_to(self.map)



    def update_map(self, parcelle_id):
        """
        Met à jour la carte interactive pour la parcelle sélectionnée.
        """
        self.create_base_map()
        self.add_yield_history_layer()
        self.add_current_ndvi_layer()
        self.add_risk_heatmap()
        folium.LayerControl().add_to(self.map)
        print(f"Carte mise à jour pour la parcelle {parcelle_id}")
        file_path = 'static/carte.html'
        self.map.save(file_path)
        print(f"Carte mise à jour pour la parcelle {parcelle_id} et sauvegardée dans {file_path}")
        
    


    def save_map(self, file_path):
        """
        Sauvegarde la carte dans un fichier HTML.
        """
        self.create_base_map()
        self.add_yield_history_layer()
        self.add_current_ndvi_layer()
        self.add_risk_heatmap()
        folium.LayerControl().add_to(self.map)
        self.map.save(file_path)
        
