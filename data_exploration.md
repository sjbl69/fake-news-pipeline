#  Rapport d’exploration de données

##  Objectif

L’objectif de cette exploration est d’analyser les données extraites depuis l’API News afin d’évaluer leur qualité, leur structure et leur pertinence pour un modèle de détection de fake news.

---

##  Source des données

- Source : NewsAPI
- Type : Articles de presse
- Format : JSON
- Volume : Variable selon la requête API

---

##  Structure des données brutes

Les données récupérées contiennent les champs suivants :

| Champ        | Type      | Description |
|-------------|----------|------------|
| title       | string   | Titre de l’article |
| description | string   | Résumé de l’article |
| content     | string   | Contenu principal |
| url         | string   | Lien vers l’article |
| urlToImage  | string   | URL de l’image |
| publishedAt | datetime | Date de publication |

---

##  Analyse exploratoire

### 1. Données manquantes

- Certaines lignes ne contiennent pas de `content`
- Le champ `urlToImage` est parfois vide ou null
- Quelques articles ont un `title` vide

 Impact : perte d’information pour le modèle

---

### 2. Qualité des données

- Présence de caractères spéciaux et bruit (HTML, symboles)
- Texte parfois tronqué (limitation API)
- Sources hétérogènes (styles différents)

 Impact : nécessite un nettoyage pour le NLP

---

### 3. Doublons

- Possibilité de doublons sur le champ `title`
- Certains articles identiques publiés par différentes sources

 Solution : suppression des doublons

---

### 4. Cohérence des données

- Les champs principaux sont globalement cohérents
- Format des dates correct (`publishedAt`)
- URLs généralement valides

---

##  Problèmes identifiés

- Données incomplètes
- Texte bruité
- Présence de doublons
- Images parfois absentes ou invalides

---

##  Actions de transformation appliquées

Pour rendre les données exploitables :

- Suppression des lignes sans `title` ou `content`
- Nettoyage du texte (suppression HTML, caractères spéciaux)
- Conversion en minuscules
- Suppression des doublons
- Création de nouvelles variables :
  - `cleaned_text`
  - `text_length`
  - `has_image`

---

##  Structure des données après transformation

| Champ          | Description |
|---------------|------------|
| title         | Titre |
| content       | Contenu brut |
| cleaned_text  | Texte nettoyé |
| text_length   | Longueur du texte |
| has_image     | Présence d’image (booléen) |

---

##  Conclusion

Les données extraites sont exploitables après transformation.  
Le pipeline de nettoyage permet d’obtenir un dataset structuré et adapté à un modèle de classification de fake news.

