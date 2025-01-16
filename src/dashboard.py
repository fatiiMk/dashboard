from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, HoverTool, Slider
from bokeh.plotting import figure, curdoc
from bokeh.palettes import RdYlBu11
import pandas as pd
import numpy as np
import os
from bokeh.models import Div



class AgriculturalDashboard:
    def __init__(self, data_manager):
        """
        Initialise le tableau de bord avec le gestionnaire de données.
        """
        self.data_manager = data_manager
        self.source = ColumnDataSource(data_manager.monitoring_data)
        self.hist_source = ColumnDataSource(data_manager.yield_history)
        self.selected_parcelle = None
        self.yield_prediction_source = ColumnDataSource(data={"year": [], "predicted_yield": []})
        self.stress_source = ColumnDataSource(data={"stress_hydrique": [], "precipitation": []})



         # Widget pour sélectionner une parcelle
        self.parcelle_selector = Select(
            title="Sélectionner une parcelle",
            value="P001",
            options=self.get_parcelle_options(),
        )
        self.parcelle_selector.on_change("value", self.update_plots)

        self.create_data_sources()

    def create_data_sources(self):
        """
        Prépare les sources de données pour Bokeh.
        """
        self.source.data = self.data_manager.monitoring_data
        self.hist_source.data = self.data_manager.yield_history[
            self.data_manager.yield_history["parcelle_id"] == "P001"
        ].to_dict(orient="list")

    def get_parcelle_options(self):
        """
        Retourne la liste des parcelles disponibles.
        """
        return sorted(self.data_manager.monitoring_data["parcelle_id"].unique())

    def create_yield_history_plot(self):
        """
        Crée un graphique montrant l’évolution historique des rendements.
        """
        p = figure(
            title="Historique des Rendements par Parcelle",
            x_axis_type="datetime",
            x_axis_label="Date",
            y_axis_label="Rendement Final (tonnes/ha)",
            height=400,
        )
        p.line("date", "rendement_final", source=self.hist_source, line_width=2, color="blue", legend_label="Rendement Final")
        

        hover = HoverTool()
        hover.tooltips = [("Date", "@date{%F}"), ("Rendement Final", "@rendement_final")]
        hover.formatters = {"@date": "datetime"}
        p.add_tools(hover)
        p.legend.location = "top_left"
        return p

    def create_ndvi_plot(self):
        """
        Crée un graphique montrant l’évolution du NDVI.
        """
        p = figure(
            title="Évolution du NDVI",
            x_axis_type="datetime",
            x_axis_label="Date",
            y_axis_label="NDVI",
            height=400,
        )
        p.line("date", "ndvi", source=self.source, line_width=2, color="green", legend_label="NDVI")
        

        hover = HoverTool()
        hover.tooltips = [("Date", "@date{%F}"), ("NDVI", "@ndvi")]
        hover.formatters = {"@date": "datetime"}
        p.add_tools(hover)
        p.legend.location = "top_left"
        return p

    def create_stress_matrix(self):
        """
        Crée une matrice de stress combinant stress hydrique et précipitations.
        """
        

        # Créer la figure
        p = figure(
            title="Matrice de Stress",
            x_axis_label="Stress Hydrique",
            y_axis_label="Précipitation",
            height=400,
        )

        # Ajouter les points
        p.circle(
            "stress_hydrique",
            "precipitation",
            source=self.stress_source,
            size=10,
            fill_color="orange",
            line_color="black",
            alpha=0.6,
        )

        hover = HoverTool()
        hover.tooltips = [("Stress Hydrique", "@stress_hydrique"), ("Précipitations", "@precipitation")]
        p.add_tools(hover)

        return p
    
    def predict_yields(self, parcelle_id):
        """
        Calcule les prédictions de rendement pour une parcelle donnée
        basée sur les données historiques.
        """
        parcelle_data = self.data_manager.yield_history[
            self.data_manager.yield_history["parcelle_id"] == parcelle_id
        ]
        if parcelle_data.empty:
            return pd.DataFrame({"date": [], "predicted_yield": []})

        # Régression linéaire simple pour la prédiction
        from sklearn.linear_model import LinearRegression

        X = np.arange(len(parcelle_data)).reshape(-1, 1)
        y = parcelle_data["rendement_final"].values
        model = LinearRegression().fit(X, y)

        future_dates = pd.date_range(parcelle_data["date"].max(), periods=6, freq="M")[1:]
        predictions = model.predict(np.arange(len(parcelle_data), len(parcelle_data) + len(future_dates)).reshape(-1, 1))

        return pd.DataFrame({"date": future_dates, "predicted_yield": predictions})



    def create_yield_prediction_plot(self):
        """
        Crée un graphique de prédiction des rendements.
        """
        p = figure(
            title="Prédiction des Rendements",
            x_axis_type="datetime",
            x_axis_label="Date",
            y_axis_label="Rendement Prévu (tonnes/ha)",
            height=400,
        )
        p.line(
            "date",
            "predicted_yield",
            source=self.yield_prediction_source,
            line_width=2,
            color="purple",
            legend_label="Prédictions",
        )
        p.circle(
            "date",
            "predicted_yield",
            source=self.yield_prediction_source,
            size=8,
            color="purple",
            legend_label="Prédictions",
        )

        hover = HoverTool()
        hover.tooltips = [("Date", "@date{%F}"), ("Rendement Prévu", "@predicted_yield")]
        hover.formatters = {"@date": "datetime"}
        p.add_tools(hover)
        p.legend.location = "top_left"
        return p

    
    def create_layout(self):
        """
        Organise tous les graphiques dans une mise en page cohérente.
        """
        yield_plot = self.create_yield_history_plot()
        ndvi_plot = self.create_ndvi_plot()
        prediction_plot = self.create_yield_prediction_plot()
        try:
            stress_plot = self.create_stress_matrix()
        except Exception as e:
            print(f"Erreur lors de la création de la matrice de stress : {e}")
            stress_plot = figure(title="Erreur lors de la création de la matrice de stress", height=400)

        
        layout = column(
        #row(self.parcelle_selector, width_policy="max"),
        row(yield_plot, ndvi_plot, width_policy="max"),
        row(prediction_plot, stress_plot, width_policy="max"),
        width_policy="max"
    )
        return layout

        #layout = column(self.parcelle_selector, yield_plot, ndvi_plot,prediction_plot,stress_plot)
       
    def prepare_stress_data(self,parcelle_id=None):
        
        
        """
        Prépare les données pour la matrice de stress en combinant
        le stress hydrique et les précipitations.
        """
        data = self.data_manager.prepare_features()

        if "stress_hydrique" not in data or "precipitation" not in data:
            raise ValueError("Les colonnes 'stress_hydrique' ou 'precipitation' sont manquantes.")

        if parcelle_id:
            data = data[data["parcelle_id"] == parcelle_id]

        stress_data = data[["stress_hydrique", "precipitation"]].copy()
        stress_data["stress_hydrique"] = stress_data["stress_hydrique"].fillna(0)
        stress_data["precipitation"] = stress_data["precipitation"].fillna(0)

        return stress_data


    
    

    def update_plots(self, attr, old, new):
        """
         Met à jour les graphiques lorsque la parcelle sélectionnée change.
         """
        self.selected_parcelle = new
        # Filtrer les données pour la parcelle sélectionnée
        parcelle_data = self.data_manager.yield_history[self.data_manager.yield_history["parcelle_id"] == new]
        monitoring_data = self.data_manager.monitoring_data[self.data_manager.monitoring_data["parcelle_id"] == new]
        

        # Mettre à jour les sources
        self.hist_source.data = parcelle_data.to_dict(orient="list")
        self.source.data = monitoring_data.to_dict(orient="list")
        
        # Mettre à jour les données de la matrice de stress
        try:
            stress_data = self.prepare_stress_data(parcelle_id=new)
            self.stress_source.data = stress_data.to_dict(orient="list")
        except ValueError as e:
            print(f"Erreur lors de la préparation des données de stress : {e}")
            self.stress_source.data = {"stress_hydrique": [], "precipitation": []}
        
         # Mise à jour des prédictions
        predictions = self.predict_yields(new)
        self.yield_prediction_source.data = predictions.to_dict(orient="list")
        print("Mise à jour des prédictions :", self.yield_prediction_source.data)
        
        



from data_manager import AgriculturalDataManager
# Charger les données et afficher le tableau de bord
data_manager = AgriculturalDataManager()
data_manager.load_data()

dashboard = AgriculturalDashboard(data_manager)
curdoc().add_root(dashboard.create_layout())

