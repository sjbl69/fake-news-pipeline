#  Fake News Detection Pipeline

Projet de création d’un pipeline ETL permettant de collecter, transformer et stocker des données multimodales (texte + image) afin d’entraîner un modèle de détection de fake news.

---

##  Objectifs du projet

* Extraire automatiquement des données depuis différentes sources (API, datasets, réseaux sociaux)
* Transformer et nettoyer les données (texte + image)
* Stocker les données dans un format exploitable
* Orchestrer le pipeline avec Apache Airflow
* Construire un dataset fiable, traçable et maintenable

---

##  Structure du projet

```
fake-news-pipeline/
│
├── src/                    
│   ├── extract/
│   ├── transform/
│   ├── load/
│
├── data/                   
├── dags/                   
├── notebooks/              
│
├── config.py
├── requirements.txt
├── README.md
```

---

#  Étape 1 : Exploration des sources de données

##  Objectif

Identifier des sources multimodales (texte + image) pertinentes pour entraîner un modèle de détection de fake news, en analysant leur qualité, leur accessibilité et leur potentiel d’utilisation.

---

##  Source 1 : News API

###  Lien officiel

https://newsapi.org/

###  Description

API REST fournissant des articles d’actualité issus de nombreuses sources internationales.

###  Caractéristiques

* Type : articles
* Modalités :

  * Texte : oui (titre, description)
  * Image : oui (URL, parfois absente)
* Format : JSON
* Langue : multilingue (majoritairement anglais)

###  Authentification

* Clé API obligatoire (`apiKey`)

###  Pagination

* `page` et `pageSize`

###  Limites API

* Limitation du nombre de requêtes (plan gratuit)
* Accès restreint à certaines sources

###  Volume estimé

* Plusieurs milliers d’articles/jour

###  Images

* Non garanties → filtrage nécessaire

###  Licence

* Usage personnel et développement autorisé
* Redistribution brute interdite

###  Labels

 Aucun label fake/real

 Utilisation prévue :

* données “réelles”
* enrichissement du dataset
* mise à jour continue

---

##  Source 2 : Reddit

###  Lien officiel

https://www.reddit.com/dev/api/

###  Description

Plateforme sociale contenant des publications texte et image, incluant potentiellement de la désinformation.

###  Caractéristiques

* Type : posts utilisateurs
* Modalités :

  * Texte : oui
  * Image : oui (variable)
  * Format : JSON

###  Langue

* Principalement anglais

###  Authentification

* OAuth via API (librairie `praw`)

###  Pagination

* basée sur `after` / `limit`

###  Limites API

* Rate limit strict
* restrictions sur certains contenus

###  Volume estimé

* Très élevé (millions de posts)

### Images

* Très hétérogènes

###  Licence

* Respect des conditions d’utilisation Reddit

###  Labels

 Aucun

 Utilisation prévue :

* données bruitées réalistes
* détection de patterns de désinformation

---

##  Source 3 : FakeNewsNet

###  Lien officiel

https://github.com/KaiDMML/FakeNewsNet

###  Description

Dataset académique conçu pour la détection de fake news.

###  Caractéristiques

* Type : articles
* Modalités :

  * Texte : oui
  * Image : oui (partielle)
* Format : JSON / CSV

###  Langue

* Anglais

###  Labels

 Fake / Real

###  Volume estimé

* Quelques milliers d’articles

###  Images

* Disponibilité partielle

###  Licence

* Usage académique / recherche

 Utilisation prévue :

* dataset principal d’entraînement

---

##  Source 4 : NewsData.io

###  Lien officiel

https://newsdata.io/

###  Description

API alternative pour récupérer des actualités internationales.

###  Caractéristiques

* Texte : oui
* Image : oui
* Format : JSON
* Langue : multilingue

###  Authentification

* API key

###  Pagination

* oui

###  Limites

* quotas API

###  Labels

 Aucun

 Utilisation :

* source complémentaire

---

#  Schéma de données cible

```json
{
  "id": "uuid",
  "title": "Titre",
  "text": "Contenu",
  "article_url": "...",
  "image_url": "...",
  "image_path": "...",
  "source_name": "...",
  "language": "en",
  "published_at": "...",
  "collected_at": "...",
  "label": "fake / real / null",
  "raw_source": "news_api / reddit / fakenewsnet"
}
```

 Ce schéma garantit :

* unicité des données
* traçabilité
* lien texte-image fiable

---

Gestion des labels

Seule la source FakeNewsNet fournit des labels fiables (fake / real).

Les autres sources (News API, Reddit, NewsData.io) ne contiennent aucun label.

Stratégie adoptée :
- FakeNewsNet est utilisé pour l’entraînement supervisé
- Les autres sources servent à enrichir le dataset
- Ces données pourront être utilisées pour du pré-entraînement ou du semi-supervisé

  

#  Points de vigilance

* Associer correctement texte et image
* Vérifier la disponibilité des images
* Ne pas confondre opinion et désinformation
* Respecter les licences des données
* Conserver toutes les métadonnées utiles

---

#  Conclusion

Les sources sélectionnées sont complémentaires :

* News API et NewsData.io → données réelles et mises à jour
* Reddit → données bruitées et réalistes
* FakeNewsNet → données labellisées

 Seul FakeNewsNet permet un entraînement direct.
 Les autres sources servent à enrichir et actualiser le dataset.

---
## Étape 2 - Extraction automatisée

### Installation
pip install -r requirements.txt

Créer un fichier `.env` :
NEWS_API_KEY=your_key

### Exécution
python -m src.extract.news_api

### Sortie
- JSON dans data/raw/
- Images dans data/raw/images/

### Limites
- Dépend du quota API
- Certaines images peuvent être invalides
- Pagination limitée

- ## Étape 3 : Pipeline de transformation

Description du pipeline :
- Nettoyage des textes
- Validation des articles
- Normalisation des dates
- Structuration des données

Lancement :

```bash
python src/transform/pipeline.py
```

<img width="1645" height="911" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/099c70d4-2a7e-44bd-af85-fd534194beb1" />


#  Étape 4 : Orchestration du pipeline avec Airflow

##  Objectif

Mettre en place un pipeline ETL automatisé et orchestré afin de :

- Automatiser les étapes de traitement des données
- Structurer le flux de données
- Superviser les exécutions
- Garantir la reproductibilité du pipeline

---

##  Architecture du pipeline

Le pipeline est composé de trois tâches principales :

###  extract_task
- Récupération des données via News API
- Vérification de la validité des données
- Sauvegarde dans `data/raw/raw_data.json`

---

###  transform_task
- Nettoyage des textes
- Normalisation des champs
- Structuration des données
- Sauvegarde dans `data/processed/clean_data.json`

---

###  load_task
- Simulation du chargement des données
- Préparation pour une future base de données ou modèle de machine learning

---

##  Ordonnancement des tâches

Les tâches sont exécutées dans l’ordre suivant : extract_task → transform_task → load_task


Si une tâche échoue, les suivantes ne sont pas exécutées.

---

##  Implémentation technique

Le DAG est défini dans le fichier : dags/etl_pipeline.py


Le pipeline utilise :

- PythonOperator pour exécuter les fonctions Python
- Un DAG Airflow pour définir les dépendances et la planification

Configuration du DAG :

```python
dag = DAG(
    dag_id="etl_multimodal_pipeline",
    schedule_interval="0 2 * * *",
    catchup=False
)

```

## Monitoring

Airflow permet :

Visualisation des DAGs
Suivi des exécutions en temps réel
Accès aux logs détaillés
Identification rapide des erreurs

Interface disponible sur :

http://localhost:8080

Gestion des erreurs
Vérification de la présence de la clé API (NEWS_API_KEY)
Arrêt du pipeline si aucune donnée n’est récupérée
Logs explicites pour faciliter le debug

 ##  Variables d’environnement


Créer un fichier .env : NEWS_API_KEY=your_api_key

Ce fichier est exclu du dépôt via .gitignore.

## Lancer le pipeline

Démarrer Airflow : airflow standalone

Puis lancer le DAG via l’interface web.


## Gestion des données

Les données sont organisées en trois niveaux :

data/raw/ : données brutes
data/processed/ : données transformées
data/final/ : données prêtes à être utilisées

## Résultat

Le pipeline est :

Fonctionnel
Automatisé
Reproductible
Supervisé via Airflow

Les trois tâches (extract, transform, load) s’exécutent correctement et produisent des données exploitables.

##  Étape 5 — Évaluation et visualisation des performances

###  Objectif

L’objectif de cette étape est d’évaluer l’efficacité du pipeline ETL à l’aide d’indicateurs de performance (KPI), puis de mettre en place un système de visualisation et de monitoring pour suivre son comportement en production.

---

###  Indicateurs de performance (KPI)

Les KPI suivants ont été définis :

* **Précision des données (%)** : proportion de données valides après transformation
* **Volume de données** : nombre total d’entrées traitées
* **Temps d’exécution (s)** : estimation du temps nécessaire au traitement
* **Coût estimé (€)** : approximation du coût en fonction du volume de données

Ces indicateurs permettent d’évaluer la qualité, la performance et la scalabilité du pipeline.

---

###  Tableau de bord (Streamlit)

Un dashboard interactif a été développé avec **Streamlit** pour visualiser les KPI en temps réel.

Fonctionnalités :

* Affichage des KPI principaux (volume, validité, temps, coût)
* Visualisation graphique de la répartition des données (valides vs invalides)
* Aperçu des données traitées
* Gestion du cas où aucune donnée n’est disponible

Lancement du dashboard :

```bash
python -m streamlit run dashboard/app.py
```

---

###  Plan de monitoring

Un plan de monitoring a été mis en place afin d’assurer le suivi du pipeline en production.

####  Surveillance des KPI

* **Qualité des données** : alerte si < 90% de données valides
* **Performance** : alerte si le temps d’exécution dépasse un seuil critique
* **Volume** : détection d’anomalies dans les données traitées

---

####  Logs

Le pipeline génère des logs permettant de tracer :

* le début et la fin des tâches
* le nombre de données traitées
* les erreurs éventuelles

---

####  Gestion des alertes

Des alertes peuvent être déclenchées en cas de :

* absence de données
* taux de validité trop faible
* échec d’une étape du pipeline

---

####  Fréquence de monitoring

* Vérification à chaque exécution du pipeline
* Analyse régulière des KPI
* Surveillance continue en environnement de production

---

###  Remarque

Dans cette version, certaines métriques (temps et coût) sont simulées afin de valider la structure du monitoring.
Le pipeline est conçu pour permettre une intégration future avec des métriques réelles (logs détaillés, Airflow, outils de monitoring).

---



