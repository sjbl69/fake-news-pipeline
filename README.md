#  Fake News Detection Pipeline

Projet de création d’un pipeline ETL permettant de collecter, transformer et stocker des données multimodales (texte + image) afin d’entraîner un modèle de détection de fake news.

---

##  Objectifs du projet

* Extraire automatiquement des données depuis différentes sources (API, datasets, réseaux sociaux)
* Transformer et nettoyer les données (texte + image)
* Stocker les données dans un format exploitable
* Orchestrer le pipeline avec Apache Airflow
* Construire un dataset fiable et maintenable

---

##  Structure du projet

```
fake-news-pipeline/

├── src/                    
│   ├── extract/
│   ├── transform/
│   ├── load/
│
├── data/                    # données
├── dags/                    # pipelines Airflow
├── notebooks/               # exploration
│
├── config.py
├── requirements.txt
├── README.md
```

---

#  Étape 1 : Exploration des sources de données

##  Objectif

Identifier des sources de données multimodales (texte + image) pertinentes pour entraîner un modèle de détection de fake news.

---

##  Source 1 : News API

###  Description

API fournissant des articles d’actualité provenant de nombreuses sources internationales.

###  Caractéristiques

* Type de données : articles
* Modalités :

  * Texte : (titre, description)
  * Image : (URL)
* Format : JSON
* Langue : multilingue
* Labels :  non disponibles

###  Méthode d’extraction

* API REST avec Python (`requests`)

###  Avantages

* Données propres et structurées
* Facile à utiliser

###  Limites

* Pas de labels

---

##  Source 2 : Reddit

###  Description

Plateforme sociale permettant de récupérer des publications utilisateurs.

###  Caractéristiques

* Type de données : posts
* Modalités :

  * Texte : oui
  * Image : oui
* Format : JSON
* Langue : anglais
* Labels :  non disponibles

###  Méthode d’extraction

* API via `praw`

###  Avantages

* Données réalistes
* Présence potentielle de fake news

###  Limites

* Données bruitées
* Nécessite nettoyage

---

##  Source 3 : FakeNewsNet

###  Description

Dataset académique dédié à la détection de fake news.

###  Caractéristiques

* Type de données : articles
* Modalités :

  * Texte : oui
  * Image : oui (selon cas)
* Format : JSON / CSV
* Langue : anglais
* Labels :  disponibles (fake / real)

###  Méthode d’extraction

* Téléchargement direct
* Lecture avec `pandas`

###  Avantages

* Données labellisées
* Idéal pour entraînement

### Limites

* Dataset statique

---

##  Source 4 : NewsData.io

###  Description

API alternative pour récupérer des actualités internationales.

###  Caractéristiques

* Type de données : articles
* Modalités :

  * Texte : oui
  * Image : oui
* Format : JSON
* Langue : multilingue
* Labels :  non disponibles

###  Méthode d’extraction

* API REST

---

##  Format de données cible

```json
{
  "title": "Titre",
  "text": "Contenu",
  "image_url": "URL image",
  "source": "Nom source",
  "date": "YYYY-MM-DD",
  "label": "fake / real / null"
}
```

---

##  Points de vigilance

* Associer correctement texte et image
* Conserver les métadonnées (source, date, URL)
* Ne pas confondre opinion et désinformation
* Vérifier les droits d’utilisation des données

---

##  Conclusion

Les sources sélectionnées permettent de construire un dataset :

* riche
* multimodal
* partiellement labellisé

 Ce socle est essentiel pour entraîner un modèle de détection de fake news performant.


