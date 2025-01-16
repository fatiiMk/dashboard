import streamlit as st
from streamlit.components.v1 import html
from streamlit_folium import folium_static
from map_visualization import AgriculturalMap
from dashboard import AgriculturalDashboard
from data_manager import AgriculturalDataManager
import os


class IntegratedDashboard:
    def __init__(self, data_manager):
        """
        Crée un tableau de bord intégré combinant graphiques Bokeh et carte Folium.
        """
        self.data_manager = data_manager
        self.bokeh_dashboard = AgriculturalDashboard(data_manager)  # Graphiques Bokeh
        self.map_view = AgriculturalMap(data_manager)              # Carte Folium

    def initialize_visualizations(self):
        """
        Initialise toutes les composantes visuelles.
        """

        
        file_path = 'static/carte.html'

        self.map_view.save_map(file_path)
        
        

          

    def update_visualizations(self, parcelle_id):
        """
        Met à jour toutes les visualisations pour une parcelle donnée.
        """
        # Mettre à jour les graphiques Bokeh
        self.bokeh_dashboard.update_plots(attr=None, old=None, new=parcelle_id)

        # Mettre à jour la carte Folium
        self.map_view.update_map(parcelle_id)



# Charger les données
data_manager = AgriculturalDataManager()
data_manager.load_data()
# print("Parcelle IDs :", data_manager.get_parcelle_ids())

# Créer un tableau de bord intégré
dashboard = IntegratedDashboard(data_manager)

# Initialiser les visualisations
dashboard.initialize_visualizations()

# Interface Streamlit
st.title("Tableau de Bord Agricole Intégré")

# Sélection de la parcelle
parcelle_ids = data_manager.get_parcelle_ids()
selected_parcelle = st.selectbox("Sélectionnez une parcelle :", parcelle_ids)

# Mettre à jour les visualisations pour la parcelle sélectionnée
dashboard.bokeh_dashboard.update_plots(attr=None, old=None, new=selected_parcelle)
dashboard.map_view.update_map(selected_parcelle)

# Affichage des graphiques Bokeh
st.subheader("Visualisations Bokeh")
bokeh_layout = dashboard.bokeh_dashboard.create_layout()
st.bokeh_chart(bokeh_layout, use_container_width=True)

# Affichage de la carte Folium
st.subheader("Carte Folium")
map_path = 'static/carte.html'

# Intégrer la carte Folium via une iframe HTML avec style responsive
# Intégrer la carte Folium via une iframe HTML en occupant toute la largeur et une grande hauteur
iframe_code = '''
<div style="display: flex; justify-content: center; align-items: center; width: 100%;">
    <iframe src="http://localhost:8503/carte.html" 
            sandbox="allow-same-origin allow-scripts" 
            style="width: 100%; height: 1000px; border: none;">
    </iframe>
</div>'''

st.components.v1.html(iframe_code, height=500, width=1000)

