import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import markdown
import os
import pandas as pd

class AgriculturalReportGenerator:
    def __init__(self, analyzer, data_manager):
        """
        Initialise le générateur de rapports avec l’analyseur
        et le gestionnaire de données.
        """
        self.analyzer = analyzer
        self.data_manager = data_manager

    def generate_parcelle_report(self, parcelle_id):
        try:
            print(f"Test de génération de rapport pour la parcelle {parcelle_id}...")

            yield_data = self.data_manager.yield_history[self.data_manager.yield_history["parcelle_id"] == parcelle_id]
            weather_data = self.data_manager.weather_data
            soil_data = self.data_manager.soil_data[self.data_manager.soil_data["parcelle_id"] == parcelle_id]

            # Fusionner les données
            merged_data = pd.merge(yield_data, weather_data, on="date", how="left")
            merged_data = pd.merge(merged_data, soil_data, on="parcelle_id", how="left")
            print("Colonnes après fusion :", merged_data.columns)
            print("Types des colonnes après fusion :", merged_data.dtypes)
           
            if "vitesse_vent" in merged_data.columns:
                print("Valeurs uniques dans 'vitesse_vent':", merged_data["vitesse_vent"].unique())
    

            # Analyse des facteurs
           

            analysis = self.analyzer.analyze_yield_factors(parcelle_id)
            analysis_numeric = analysis["Importance"]
            print("Données dans 'analysis' :")
            print(analysis_numeric)
            print("Types des colonnes dans 'analysis' :")
            print(analysis_numeric.dtypes)
            
            # Calcul des corrélations
            correlation_matrix = self.analyzer._calculate_yield_correlations(
                yield_data=self.data_manager.yield_history,
                weather_data=self.data_manager.weather_data,
                soil_data=self.data_manager.soil_data,
            )
            print(correlation_matrix.head()) 


            # Combine soil_data et yield_history si nécessaire
            current_state = soil_data[soil_data["parcelle_id"] == parcelle_id]
            if current_state.empty:
                raise ValueError(f"Aucune donnée trouvée pour la parcelle {parcelle_id} dans soil_data.")


            # Générer les recommandations
            recommendations = self._generate_recommendations(analysis_numeric,current_state)

            # Création du rapport
            markdown_content = self._create_markdown_report(parcelle_id, analysis_numeric, merged_data, recommendations)
            figures_path = self._generate_report_figures(parcelle_id,correlation_matrix)

            # Conversion en PDF
            pdf_file_path = self._convert_to_pdf(markdown_content, figures_path)
            print(f"Rapport généré avec succès : {pdf_file_path}")

        except Exception as e:
            print(f"Erreur lors de la génération du rapport : {e}")


    def _create_markdown_report(self, parcelle_id, analysis_numeric, current_state, recommendations):
        markdown_content = f"""
        # Rapport Agricole pour la Parcelle {parcelle_id}

        ## Analyse des Facteurs Influents
        {analysis_numeric.to_markdown()}
        print("Données d'analyse utilisées dans le rapport :")
        print(analysis.head())
        print("Types des colonnes d'analyse :")
        print(analysis.dtypes)
        



        ## Données Actuelles
        {current_state.head().to_markdown()}

        ## Recommandations
        {recommendations}
        """
        return markdown_content


    def _generate_report_figures(self, parcelle_id,correlation_matrix):
        figures_path = f"reports/figures/{parcelle_id}/"
        os.makedirs(figures_path, exist_ok=True)
        print("Données pour le graphique de corrélation :")
        print(correlation_matrix)


        self._plot_yield_evolution(parcelle_id, f"{figures_path}/yield_evolution.png")
        self._plot_correlation_matrix(correlation_matrix, f"{figures_path}/correlation_matrix.png")

        return figures_path

    def _plot_yield_evolution(self, parcelle_id, save_path):
        yield_data = self.data_manager.yield_history
        yield_data = yield_data[yield_data["parcelle_id"] == parcelle_id]

        if yield_data.empty:
            raise ValueError(f"Aucune donnée trouvée pour la parcelle {parcelle_id}.")

        plt.figure(figsize=(10, 6))
        plt.plot(yield_data["date"], yield_data["rendement_final"], marker='o')
        plt.title(f"Évolution des rendements pour {parcelle_id}")
        plt.xlabel("Date")
        plt.ylabel("Rendement")
        plt.grid()
        plt.savefig(save_path)
        plt.close()

    def _plot_correlation_matrix(self, correlation_matrix, save_path):
        """
            Affiche une matrice de corrélation pour les facteurs influençant le rendement final.
            """
        if isinstance(correlation_matrix, pd.Series):
            plt.figure(figsize=(12, 8))
            sns.heatmap(correlation_matrix.to_frame(), annot=True, cmap="coolwarm", fmt=".2f", cbar=False)
            plt.title("Corrélations avec le rendement final")
            plt.savefig(save_path)
            plt.close()
        else:
            print("Erreur : Les données de corrélation ne sont pas au format attendu (pd.Series).")

    def _plot_stability_analysis(self, stability_data, save_path):
        """
        Visualise l’analyse de stabilité des rendements.
        """
        plt.figure(figsize=(8, 6))
        plt.bar(stability_data.keys(), stability_data.values(), color='skyblue')
        plt.title("Analyse de Stabilité")
        plt.xlabel("Métriques")
        plt.ylabel("Valeurs")
        plt.savefig(save_path)
        plt.close()

    def _format_historical_analysis(self, analysis):
        """
        Formater l’analyse historique.
        """
        return f"Les tendances historiques montrent une évolution significative avec des rendements moyens de {analysis['rendement_estime'].mean():.2f}."

    def _format_limiting_factors(self, factors):
        """
        Transformer les facteurs limitants en recommandations.
        """
        formatted_factors = "\n".join(
            [f"- {factor}: Influence faible ({value:.2f})" for factor, value in factors.items()]
        )
        return f"Les facteurs limitants identifiés sont :\n{formatted_factors}"

    def _generate_recommendations(self, analysis_numeric, current_state):
        """
        Génère des recommandations basées sur les analyses et l'état actuel.
        """
        recommendations = []
        print("Données pour le graphique de corrélation :")
        print(analysis_numeric)


        # Exemples de recommandations basées sur l'analyse
        if analysis_numeric.max() > 0.5:
            recommendations.append("Investir dans l'amélioration des pratiques culturales pour maximiser les facteurs influents clés.")
        else:
            recommendations.append("Focus sur l'amélioration des sols et la gestion de l'eau.")


        return "\n".join(recommendations)


    import os

    def _convert_to_pdf(self, markdown_content, figures_path):
        # Chemin des fichiers
        markdown_file = os.path.join("reports", "temp_report.md")
        pdf_file = os.path.join("reports", "final_report.pdf")

        # Vérifier l'existence des répertoires
        os.makedirs(os.path.dirname(markdown_file), exist_ok=True)

        # Sauvegarder le fichier Markdown
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Fichier Markdown enregistré à : {markdown_file}")

        # Vérifier que le fichier existe
        if not os.path.isfile(markdown_file):
            raise FileNotFoundError(f"Le fichier Markdown {markdown_file} est introuvable.")

        # Commande Pandoc
        try:
            result = subprocess.run(
                ["pandoc", markdown_file, "-o", pdf_file],
                check=True,  # Soulève une exception si la commande échoue
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Conversion réussie. PDF généré à : {pdf_file}")
            return pdf_file
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la conversion Pandoc : {e.stderr.decode()}")
            raise e


