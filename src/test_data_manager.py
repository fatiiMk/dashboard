from data_manager import AgriculturalDataManager
from agricultural_analyzer import AgriculturalAnalyzer
from agricultural_report_generator import AgriculturalReportGenerator
import subprocess




# Charger les données
data_manager = AgriculturalDataManager()
data_manager.load_data()

# Initialiser les classes
analyzer = AgriculturalAnalyzer(data_manager)
report_generator = AgriculturalReportGenerator(analyzer, data_manager)

# Identifier une parcelle pour le test
parcelle_id = "P001"



# Générer un rapport pour cette parcelle
print(f"Test de génération de rapport pour la parcelle {parcelle_id}...")
try:
    report_generator.generate_parcelle_report(parcelle_id)
    print("Rapport généré avec succès.")
except Exception as e:
    print(f"Erreur lors de la génération du rapport : {e}")



# Charger les données via le data_manager
'''data_manager = AgriculturalDataManager()
data_manager.load_data()

# Initialiser l'analyste agricole
analyzer = AgriculturalAnalyzer(data_manager)

# Tester la méthode `analyze_yield_factors`
parcelle_id = "P001"
factors = analyzer.analyze_yield_factors(parcelle_id)
print(f"Facteurs influençant les rendements pour la parcelle {parcelle_id} :")
print(factors)

# Tester les corrélations entre les rendements et les facteurs environnementaux
yield_history = data_manager.yield_history
weather_data = data_manager.weather_data
print(weather_data.columns)
soil_data = data_manager.soil_data

try:
    correlations = analyzer._calculate_yield_correlations(yield_history, weather_data, soil_data)
    print("Corrélations calculées avec succès :")
    print(correlations)
except ValueError as e:
    print(f"Erreur : {e}")

# Identifier les facteurs limitants pour une parcelle donnée
correlations = analyzer._calculate_yield_correlations(yield_history, weather_data, soil_data)
limiting_factors = analyzer._identify_limiting_factors(yield_history, correlations)
print("Facteurs limitants identifiés :")
print(limiting_factors)

# Analyse de tendance de performance
yield_series = data_manager.yield_history[data_manager.yield_history["parcelle_id"] == "P001"]["rendement_final"]
trend = analyzer._analyze_performance_trend(yield_history)
print(f"Tendance de performance pour la parcelle P001 : {trend}")

# Détection de points de rupture

breakpoints = analyzer._detect_yield_breakpoints(yield_series)
print(f"Points de rupture détectés dans les rendements : {breakpoints}")

# Analyse de stabilité

stability_metrics = analyzer._analyze_yield_stability(yield_series)
print(f"Analyse de stabilité pour la parcelle P001 : {stability_metrics}")

# Calcul de l'index de stabilité
stability_index = analyzer._calculate_stability_index(yield_series)
print(f"Index de stabilité pour la parcelle P001 : {stability_index}")'''






'''# Initialisation
data_manager = AgriculturalDataManager()

# Étape 1 : Charger les données
try:
    print("Chargement des données...")
    data_manager.load_data()
    print("Données chargées avec succès.")
except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")

# Étape 2 : Configurer les indices temporels
try:
    print("Configuration des indices temporels...")
    data_manager._setup_temporal_indices()
    print("Indices temporels configurés avec succès.")
except Exception as e:
    print(f"Erreur lors de la configuration des indices temporels : {e}")

# Étape 3 : Vérifier la cohérence temporelle
try:
    print("Vérification de la cohérence temporelle...")
    data_manager._verify_temporal_consistency()
    print("Cohérence temporelle vérifiée avec succès.")
except Exception as e:
    print(f"Erreur lors de la vérification temporelle : {e}")

# Étape 4 : Préparer les caractéristiques
try:
    print("Préparation des caractéristiques...")
    features = data_manager.prepare_features()
    print("Caractéristiques préparées avec succès.")
    print(features.head())
except Exception as e:
    print(f"Erreur lors de la préparation des caractéristiques : {e}")

# Étape 5 : Analyser les patterns temporels
try:
    parcelle_id = 'P001'  # Remplacez par une parcelle existante
    print(f"Analyse des patterns temporels pour la parcelle {parcelle_id}...")
    trend, seasonal, resid = data_manager.get_temporal_patterns(parcelle_id)
    print("Analyse des patterns temporels réussie.")
except Exception as e:
    print(f"Erreur lors de l'analyse des patterns temporels : {e}")

# Étape 6 : Calculer les métriques de risque
try:
    print("Calcul des métriques de risque...")
    risk_metrics = data_manager.calculate_risk_metrics(features)
    print("Métriques de risque calculées avec succès.")
    print(risk_metrics.head())
except Exception as e:
    print(f"Erreur lors du calcul des métriques de risque : {e}")

# Étape 7 : Analyse approfondie des rendements
try:
    print(f"Analyse approfondie des rendements pour la parcelle {parcelle_id}...")
    analysis = data_manager.analyze_yield_patterns(parcelle_id)
    print("Analyse approfondie réussie.")
    print(analysis)
except Exception as e:
    print(f"Erreur lors de l'analyse des rendements : {e}")'''
    


