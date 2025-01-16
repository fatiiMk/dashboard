# Projet de Tableau de Bord Agricole

## Description

Ce projet vise à fournir une plateforme interactive pour l'analyse des données agricoles, combinant des visualisations avancées, des cartes interactives, et des rapports dynamiques pour aider à la gestion des parcelles agricoles et à l'amélioration des rendements.

---

## Fonctionnalités Principales

### 1. Gestion des Données Agricoles
- **Fichier** : `AgriculturalDataManager`
- **Fonctionnalités** :
  - Chargement et prétraitement des données de suivi, météorologiques, des sols, et des rendements.
  - Analyse des patterns temporels et enrichissement des données historiques.
  - Calcul des métriques de risque basées sur les conditions actuelles et historiques.

### 2. Tableau de Bord Interactif
- **Fichier** : `AgriculturalDashboard`
- **Fonctionnalités** :
  - Visualisations interactives avec Bokeh :
    - Historique des rendements.
    - Évolution du NDVI.
    - Prédictions des rendements.
    - Matrice de stress hydrique et précipitations.
  - Sélecteur de parcelle pour mise à jour des graphiques.

### 3. Carte Interactive
- **Fichier** : `AgriculturalMap`
- **Fonctionnalités** :
  - Carte Folium intégrée :
    - Historique des rendements par parcelle.
    - Visualisation du NDVI.
    - Carte de chaleur des zones à risque.
  - Génération de cartes interactives sauvegardées en HTML.

### 4. Interface Intégrée avec Streamlit
- **Fichier** : `IntegratedDashboard`
- **Fonctionnalités** :
  - Combinaison des graphiques interactifs et de la carte.
  - Interface utilisateur conviviale avec Streamlit.
  - Interaction en temps réel avec les données sélectionnées.

### 5. Analyse et Génération de Rapports
- **Fichiers** : `AgriculturalAnalyzer`, `AgriculturalReportGenerator`
- **Fonctionnalités** :
  - Analyse des corrélations entre rendements et facteurs environnementaux.
  - Génération de rapports détaillés au format PDF pour chaque parcelle.
  - Intégration des figures et graphiques dans les rapports.

---

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Environnement virtuel (recommandé)
- Pandoc (pour la génération des rapports PDF)
- pdflatex (pour les moteurs PDF)

### Étapes d'installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/votre-repo/projet-agricole.git
   cd projet-agricole
   ```

2. **Créer un environnement virtuel** :
   ```bash
env\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les fichiers de données** :
   - Placez vos fichiers de données dans le répertoire `data` :
     - `monitoring_cultures.csv`
     - `meteo_detaillee.csv`
     - `sols.csv`
     - `historique_rendements.csv`

5. **Lancer Streamlit pour l'interface** :
   ```bash
   streamlit run src/IntegratedDashboard.py
   ```

---

## Utilisation

1. **Tableau de Bord Interactif** :
   - Sélectionnez une parcelle pour afficher des graphiques et des données spécifiques.
   - Visualisez les prédictions des rendements et les tendances historiques.

2. **Carte Interactive** :
   - Affichez les couches des rendements, du NDVI, et des cartes de chaleur.
   - Explorez les parcelles avec des détails enrichis.

3. **Génération de Rapports** :
   - Lancez la commande suivante pour générer un rapport :
     ```bash
     python src/test_data_manager.py
     ```
   - Les rapports sont enregistrés dans le répertoire `reports` au format PDF.

---

## Structure du Projet

```
projet-agricole/
├── data/                  # Fichiers de données (CSV)
├── reports/               # Rapports générés
├── src/                   # Code source
│   ├── AgriculturalDataManager.py
│   ├── AgriculturalDashboard.py
│   ├── AgriculturalMap.py
│   ├── AgriculturalAnalyzer.py
│   ├── AgriculturalReportGenerator.py
│   ├── IntegratedDashboard.py
│   ├── test_data_manager.py
├── requirements.txt       # Dépendances Python
├── README.md              # Documentation
```

---



---

