#  Plan de Monitoring - Fake News Pipeline

## Objectif

Mettre en place un système de surveillance du pipeline ETL afin d’assurer sa fiabilité, sa performance et la qualité des données en production.

---

##  KPI surveillés

### 1. Qualité des données

* Pourcentage de données valides (%)
* Nombre de valeurs manquantes

 Seuil d’alerte :

* < 90% de données valides

---

### 2. Performance

* Temps d’exécution du pipeline
* Temps par étape (extract / transform / load)

 Seuil d’alerte :

* Pipeline > 60 secondes

---

### 3. Volume et coût

* Nombre de données traitées
* Coût estimé en fonction du volume

 Seuil d’alerte :

* Volume anormalement élevé

---

##  Logs

Le pipeline utilise le module Python `logging` pour tracer :

* le démarrage et la fin de chaque étape
* le nombre de données traitées
* les erreurs rencontrées

Exemple :

* extract start / end
* transform start / end
* load start / end

---

##  Gestion des erreurs

Les cas suivants sont surveillés :

* absence de données extraites
* fichier intermédiaire manquant
* erreur lors du chargement

En cas d’erreur :

* arrêt du pipeline
* message explicite dans les logs

---

##  Fréquence de monitoring

* Vérification à chaque exécution du pipeline
* Analyse régulière des KPI via le dashboard Streamlit
* Surveillance continue en production

---

##  Remarque

Certaines métriques (temps et coût) sont actuellement simulées dans le cadre d’une validation pédagogique.
Le pipeline est conçu pour intégrer des métriques réelles (logs détaillés, Airflow, monitoring avancé).
