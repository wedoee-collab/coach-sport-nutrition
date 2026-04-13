<div align="center">

# 🏋️ Coach Sport & Nutrition

### Documentation complète

*Application web de coaching sportif et nutritionnel personnalisé*

**Projet BTS SIO SLAM** — Nicolas · Jordy · Ivann · Cheikh

---

</div>

## 📑 Sommaire

1. [Présentation générale](#1-présentation-générale)
2. [Architecture du projet](#2-architecture-du-projet)
3. [Système de comptes](#3-système-de-comptes)
4. [Fonctionnalités détaillées](#4-fonctionnalités-détaillées)
5. [Administration](#5-administration)
6. [Données du catalogue](#6-données-du-catalogue)
7. [Base de données](#7-base-de-données)
8. [Installation et lancement](#8-installation-et-lancement)
9. [Hébergement en ligne](#9-hébergement-en-ligne)
10. [Notions Python utilisées](#10-notions-python-utilisées)
11. [Évolutions possibles](#11-évolutions-possibles)
12. [FAQ](#12-faq)
13. [Crédits](#13-crédits)

---

## 1. Présentation générale

### 🎯 Qu'est-ce que c'est ?

**Coach Sport & Nutrition** est une application web qui aide l'utilisateur à structurer sa pratique sportive et son alimentation. En quelques clics, elle permet de :

- 🔐 Créer un **compte personnel** sécurisé
- 👤 Définir un **profil** (âge, poids, taille)
- 📊 Obtenir une **recommandation d'objectif** basée sur l'IMC
- ⚡ Générer un **programme personnalisé** : séance + repas + conseil
- 📈 **Suivre sa progression** dans le temps
- 🛠️ **Administrer** la plateforme (admin uniquement)

### 👥 À qui s'adresse-t-elle ?

| Public | Bénéfice principal |
| :--- | :--- |
| 🆕 **Débutants** | Trouver des séances adaptées sans chercher |
| 💪 **Sportifs réguliers** | Varier entraînements et repas |
| 🔄 **Personnes en reprise** | Recommandation d'objectif basée sur l'IMC |
| 🎓 **Étudiants / curieux** | Découvrir l'équilibre sport + nutrition |

### 💡 Pourquoi cette application ?

> La plupart des sites de coaching sont **payants**, **complexes** ou **bourrés de publicité**.
> Ce projet propose une alternative **simple, gratuite et open-source**.

| ✅ | Avantage |
| :---: | :--- |
| 🆓 | **Gratuite** et open-source |
| 🪶 | **Simple** : 4 onglets, aucune création de compte |
| 🎯 | **Personnalisée** : adaptée à l'objectif et au niveau |
| 🔒 | **Privée** : aucune collecte de données externes |

---

## 2. Architecture du projet

### 🛠️ Stack technique

| Composant | Technologie |
| :--- | :--- |
| **Langage** | Python 3.10+ |
| **Interface web** | [Streamlit](https://streamlit.io) |
| **Base de données** | SQLite (fichier local) |
| **Visualisation** | pandas + `st.line_chart` |
| **Versioning** | Git / GitHub |

### 📁 Structure des fichiers

```
Projet sport nutrition/
│
├── 🌐 streamlit_app.py        ← Application web (point d'entrée)
├── 🖥️  app_v2.py               ← Version desktop Tkinter (équivalente)
├── 🖥️  app.py                  ← Version desktop Tkinter (basique)
│
├── 📦 seances_sport.py        ← 27 séances (3 obj × 3 niv × 3)
├── 📦 repas_nutrition.py      ← 15 repas + 12 conseils
├── 📦 questions-utilisateur.py← Saisie console (CLI)
├── 📦 affichage_resultats.py  ← Affichage console (CLI)
│
├── 💾 coach_sport.db          ← Base SQLite (auto-créée)
│
├── 📄 requirements.txt        ← Dépendances Python
├── 📄 README.md               ← Démarrage rapide
├── 📄 DOCUMENTATION.md        ← Ce fichier
└── 📄 .gitignore
```

### 👥 Répartition du travail (équipe)

| Membre | Module | Responsabilité |
| :--- | :--- | :--- |
| **Nicolas** | `seances_sport.py` | Catalogue des 27 séances de sport |
| **Cheikh** | `repas_nutrition.py` | Repas (calories/protéines) + conseils |
| **Jordy** | `questions-utilisateur.py` | Saisie utilisateur (version console) |
| **Ivann** | `affichage_resultats.py` + intégrations | Affichage console, intégration v2, version Streamlit |

---

## 3. Système de comptes

### 🔐 Authentification

L'application repose sur un système de **comptes utilisateurs personnels**. Chaque utilisateur a ses propres données (profil, historique, suivi) — totalement isolées des autres comptes.

### 🆕 Création de compte

| Champ | Contrainte |
| :--- | :--- |
| **Nom d'utilisateur** | Minimum 3 caractères, unique |
| **Mot de passe** | Minimum 6 caractères |
| **Confirmation** | Doit correspondre au mot de passe |

> 👑 **Le tout premier compte créé devient automatiquement administrateur.**

### 🔑 Sécurité du mot de passe

Les mots de passe ne sont **jamais stockés en clair**.

| Mécanisme | Détail |
| :--- | :--- |
| **Algorithme** | PBKDF2-HMAC-SHA256 (stdlib Python) |
| **Itérations** | 200 000 |
| **Salt** | Aléatoire, 16 octets, unique par utilisateur |
| **Stockage** | `password_hash` et `salt` (hex) en base |

> 🔒 Même en cas de fuite de la base, retrouver les mots de passe demanderait un effort de calcul considérable.

### 🚪 Connexion / Déconnexion

- **Écran d'accueil** avec deux onglets : `Connexion` / `Créer un compte`
- Une fois connecté → **sidebar** affiche le nom + badge (`👑 Admin` ou `Utilisateur`)
- Bouton **🚪 Se déconnecter** dans la sidebar

### 🛡️ Isolation des données

| Donnée | Filtrage |
| :--- | :--- |
| Profil | Lié à `user_id` (un par utilisateur) |
| Programmes (historique) | Filtré par `user_id` à chaque requête |
| Calories suivi | Filtré par `user_id` |
| Export CSV | Contient uniquement les programmes du compte connecté |

> ✅ Un utilisateur **ne peut accéder qu'à ses propres données**, jamais à celles d'un autre compte.

---

## 4. Fonctionnalités détaillées

L'application est organisée en **4 onglets** (5 pour les administrateurs).

<br>

### 4.1 👤 Onglet « Profil & IMC »

> **Utilité** — Enregistrer le profil et obtenir une recommandation d'objectif.

#### 📝 Champs saisis

| Champ | Type | Plage |
| :--- | :--- | :--- |
| Prénom | Texte | — |
| Âge | Entier | 10 – 100 ans |
| Poids | Décimal | 30 – 250 kg |
| Taille | Décimal | 120 – 230 cm |

#### 🧮 Calcul de l'IMC

```python
IMC = poids (kg) / (taille (m))²
```

#### 🎯 Recommandation automatique

| IMC | Catégorie | Objectif recommandé |
| :---: | :--- | :--- |
| `< 18,5` | Insuffisance pondérale | 🥩 **Prise de masse** |
| `18,5 – 24,9` | Poids normal | ⚖️ **Maintien** |
| `25 – 29,9` | Surpoids | 🏃 **Sèche** |
| `≥ 30` | Obésité | 🏃 **Sèche** |

> ✅ Le profil est sauvegardé en base et **rechargé automatiquement** au prochain lancement.
> L'objectif recommandé est **pré-sélectionné** dans l'onglet « Programme ».

<br>

### 4.2 ⚡ Onglet « Programme »

> **Utilité** — Générer un programme personnalisé en un clic.

#### 🎚️ Choix utilisateur

| Paramètre | Options |
| :--- | :--- |
| **Objectif** | Prise de masse · Sèche · Maintien |
| **Niveau** | Débutant · Intermédiaire · Confirmé |

#### 🎁 Ce qui est généré

<table>
<tr>
<td width="33%" align="center">

**🏋️ Séance de sport**

Adaptée à l'objectif **et** au niveau

Durée + détail des exercices

</td>
<td width="33%" align="center">

**🍽️ Repas conseillé**

Repas équilibré pour l'objectif

Calories (kcal) + protéines (g)

</td>
<td width="33%" align="center">

**💡 Conseil nutrition**

Conseil court et actionnable

Lié à l'objectif choisi

</td>
</tr>
</table>

#### 🔘 Actions sur le programme généré

| Bouton | Effet |
| :--- | :--- |
| 🔁 **Changer le repas** | Tire un autre repas du même objectif (la séance reste) |
| ★ **Note 1 à 5** | Évalue le programme pour t'en souvenir |

> 💾 Chaque programme est **automatiquement sauvegardé** avec le statut « À faire ».

<br>

### 4.3 📜 Onglet « Historique »

> **Utilité** — Consulter, filtrer, marquer comme fait, exporter ou supprimer.

#### 🔍 Filtres disponibles (combinables)

| Filtre | Valeurs |
| :--- | :--- |
| **Objectif** | Tous · Prise de masse · Sèche · Maintien |
| **Niveau** | Tous · Débutant · Intermédiaire · Confirmé |
| **Statut** | Tous · À faire · Fait |

#### 📊 Métriques affichées

- 🔢 **Nombre de programmes** affichés (selon les filtres)
- ✅ **Faits cette semaine** (calculé via la date)
- ⏳ **Encore à faire**

#### 📋 Tableau

`Date` · `Objectif` · `Niveau` · `Durée` · `Calories` · `Note (★)` · `Statut`

#### 🔘 Actions disponibles

| Action | Description |
| :--- | :--- |
| ✅ **Marquer comme fait** | Change le statut d'un programme « À faire » |
| 📤 **Exporter CSV** | Télécharge tout l'historique (`historique_coach.csv`) |
| 🗑️ **Effacer l'historique** | Supprime tous les programmes (avec confirmation) |

<br>

### 4.4 📈 Onglet « Suivi calories »

> **Utilité** — Visualiser l'évolution calorique des 20 derniers programmes.

#### 📊 Affichage

- **Graphique en ligne** : calories par programme, **séparé par couleur** (Prise de masse / Sèche / Maintien)
- **Métriques** : total, moyenne, min, max, faits / à faire
- **Tableau détaillé** dépliable

#### 🤔 À quoi ça sert ?

> Repérer si tu **alternes bien** les phases :
> ❌ trop de sèche d'affilée
> ❌ semaines sans rien faire
> ✅ équilibre régulier

---

## 5. Administration

> 👑 Section accessible uniquement aux utilisateurs ayant le rôle **administrateur**.

### 🪪 Comment devenir administrateur ?

Le **tout premier compte créé** sur l'application devient automatiquement administrateur. Les admins suivants peuvent ensuite être promus depuis l'interface d'administration.

### 🛠️ Onglet « Administration »

Un onglet supplémentaire apparaît dans l'interface pour les admins :

#### 📊 Statistiques globales

| Métrique | Description |
| :--- | :--- |
| 👥 **Utilisateurs** | Nombre total de comptes |
| 📋 **Programmes générés** | Total tous utilisateurs confondus |
| ✅ **Programmes faits** | Marqués comme accomplis |
| 📊 **Répartition par objectif** | Diagramme en barres |

#### 👥 Liste des utilisateurs

Tableau présentant chaque compte avec :

| Colonne | Description |
| :--- | :--- |
| `ID` | Identifiant unique |
| `Utilisateur` | Nom de connexion |
| `Créé le` | Date d'inscription |
| `Admin` | 👑 si administrateur |
| `Programmes` | Nombre généré par ce compte |
| `Dernière activité` | Date du dernier programme |

#### ⚙️ Actions sur un utilisateur

Après sélection d'un utilisateur dans la liste déroulante :

| Action | Effet |
| :--- | :--- |
| 👑 **Promouvoir admin** | Ajoute les droits administrateur |
| ⬇️ **Retirer admin** | Enlève les droits administrateur |
| 🔑 **Réinitialiser mot de passe** | Définit un nouveau mot de passe |
| 🗑️ **Supprimer** | Supprime l'utilisateur **et toutes ses données** (cascade) |

### 🛡️ Garde-fous de sécurité

L'interface empêche les actions destructrices irréversibles :

| Garde-fou | Description |
| :--- | :--- |
| ❌ **Auto-suppression** | Un admin ne peut pas supprimer son propre compte |
| ❌ **Dernier admin** | Impossible de retirer ou supprimer le dernier administrateur |
| ✅ **Confirmation** | Toutes les actions destructrices passent par un popover de confirmation |
| 🔄 **Cascade** | La suppression d'un utilisateur efface aussi son `profil` et son `historique` |

---

## 6. Données du catalogue

### 6.1 🏋️ Séances de sport

**27 séances** organisées par objectif et niveau :

```
3 objectifs × 3 niveaux × 3 variantes = 27 séances
```

| Niveau | Durée | Style |
| :--- | :---: | :--- |
| 🟢 **Débutant** | 45 min | Poids du corps, intensité douce |
| 🟡 **Intermédiaire** | 1h | Charges légères/moyennes, plus de volume |
| 🔴 **Confirmé** | 1h30 | Charges lourdes, séries longues, HIIT/CrossFit |

#### Exemples concrets

| Objectif / Niveau | Séance type |
| :--- | :--- |
| Prise de masse · Débutant | 3×10 pompes + 3×12 squats + 3×10 fentes |
| Sèche · Confirmé | HIIT 20 min + muscu sèche + cardio elliptique |
| Maintien · Intermédiaire | 30 min course + circuit équilibré + étirements |

<br>

### 6.2 🍽️ Repas

**15 repas** : 5 par objectif, avec calories et protéines.

| Objectif | Plage calorique | Plage protéines |
| :--- | :---: | :---: |
| 🥩 **Prise de masse** | 600 – 700 kcal | 40 – 60 g |
| 🥗 **Sèche** | 250 – 380 kcal | 20 – 40 g |
| 🍱 **Maintien** | 420 – 500 kcal | 22 – 35 g |

<br>

### 6.3 💡 Conseils nutrition

**12 conseils** (4 par objectif).

> 🥩 **Prise de masse** — *« Mange toutes les 3h pour maintenir un apport protéine constant. »*

> 🥗 **Sèche** — *« Bois 2L d'eau par jour minimum pour éliminer les toxines. »*

> 🍱 **Maintien** — *« Autorise-toi un repas plaisir par semaine, sans culpabiliser. »*

---

## 7. Base de données

📁 **Fichier** : `coach_sport.db` — créé automatiquement au premier lancement.

### 🗂️ Table `users`

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identifiant unique |
| `username` | TEXT UNIQUE | Nom de connexion |
| `password_hash` | TEXT | Hash PBKDF2 du mot de passe (hex) |
| `salt` | TEXT | Salt aléatoire (hex, 16 octets) |
| `created_at` | TEXT | Date d'inscription (`JJ/MM/AAAA HH:MM`) |
| `is_admin` | INTEGER | `1` = administrateur, `0` = utilisateur |

### 🗂️ Table `profil`

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identifiant |
| `user_id` | INTEGER | Lien vers `users.id` |
| `prenom` | TEXT | Prénom utilisateur |
| `age` | INTEGER | Âge |
| `poids` | REAL | Poids (kg) |
| `imc` | REAL | IMC calculé |
| `objectif` | TEXT | Objectif recommandé |

> ℹ️ Un profil **par utilisateur** (contrainte `UNIQUE(user_id)`).

### 🗂️ Table `historique`

| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER PK | Identifiant unique |
| `user_id` | INTEGER | Lien vers `users.id` |
| `date` | TEXT | Format `JJ/MM/AAAA HH:MM` |
| `objectif` | TEXT | Libellé objectif |
| `niveau` | TEXT | Libellé niveau |
| `seance` | TEXT | Description séance |
| `duree` | TEXT | « 45 min » / « 1h » / « 1h30 » |
| `repas` | TEXT | Nom du repas |
| `calories` | TEXT | Valeur sans unité (ex. `650`) |
| `proteines` | TEXT | Valeur avec unité (ex. `55g`) |
| `conseil` | TEXT | Conseil nutrition |
| `note` | INTEGER | Note de 0 à 5 |
| `statut` | TEXT | « À faire » ou « Fait » |

---

## 8. Installation et lancement

### ✅ Prérequis

- 🐍 **Python 3.10** ou supérieur
- 📦 **pip** (gestionnaire de paquets)

### 📥 Installation

```bash
git clone <url-du-repo>
cd "Projet sport nutrition"
pip install -r requirements.txt
```

### 🌐 Lancer la version web (recommandée)

```bash
streamlit run streamlit_app.py
```

> 🔗 L'app s'ouvre sur **http://localhost:8501**

### 🖥️ Lancer la version desktop

```bash
python app_v2.py
```

---

## 9. Hébergement en ligne

### 🚀 Streamlit Community Cloud (gratuit, recommandé)

1. **Pousser** le projet sur un dépôt GitHub **public**
2. Aller sur **https://share.streamlit.io**
3. Connexion **GitHub** → bouton **« New app »**
4. Sélectionner :
   - le dépôt
   - la branche `main`
   - le fichier `streamlit_app.py`
5. Cliquer sur **Deploy** → URL publique en ~2 min ✨

### 🌍 Alternatives

| Plateforme | Gratuit | Spécificité |
| :--- | :---: | :--- |
| **Render** | ✅ (limité) | `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0` |
| **Railway** | 💰 (essai) | Déploiement Git très simple |
| **Fly.io** | ✅ (limité) | Nécessite un Dockerfile |
| **Hugging Face Spaces** | ✅ | Créer un Space « Streamlit » |

### ⚠️ Limite SQLite en production

> Sur Streamlit Cloud, le fichier `coach_sport.db` est sur **disque éphémère**.
> Les données peuvent être **effacées au redémarrage** du conteneur.

**Solutions de persistance** :

| Option | Difficulté |
| :--- | :---: |
| Migrer vers **PostgreSQL** (Supabase, Neon — gratuits) | ⭐⭐ |
| SQLite + stockage cloud (S3, etc.) | ⭐⭐⭐ |
| Limiter à un usage démo / pédagogique (cas actuel) | ⭐ |

---

## 10. Notions Python utilisées

> 🎓 Ce projet illustre les notions du **BTS SIO SLAM**.

| Notion | Où dans le code |
| :--- | :--- |
| Variables, types | Partout |
| Conditions `if/elif/else` | `recommander_objectif()` |
| Boucles `for`, `while` | Chargement historique, validation saisie |
| Fonctions | `generer_programme()`, `calculer_imc()`, etc. |
| Listes et dictionnaires | `SEANCES`, `REPAS`, `CONSEILS_NUTRITION` |
| Module `random` | Tirage aléatoire séances/repas |
| Module `sqlite3` | Persistance des données |
| Module `hashlib` (PBKDF2) | Hachage sécurisé des mots de passe |
| Module `os` (`urandom`) | Génération de salt cryptographique |
| Module `csv` | Export historique |
| Module `tkinter` | Interface desktop (v1, v2) |
| Programmation orientée objet | Classe `CoachApp` (v2) |
| Modules externes | `streamlit`, `pandas` (web) |
| Imports inter-modules | `import seances_sport as sport` |

---

## 11. Évolutions possibles

> 🚀 Pistes d'amélioration pour les versions futures.

| Idée | Difficulté |
| :--- | :---: |
| 🐘 Migration vers PostgreSQL | ⭐⭐ |
| 📧 Récupération de mot de passe par e-mail | ⭐⭐ |
| 🔐 Authentification OAuth (Google, GitHub) | ⭐⭐⭐ |
| 🧮 Calcul des besoins caloriques journaliers (Harris-Benedict) | ⭐ |
| 📄 Génération PDF du programme | ⭐⭐ |
| ⚖️ Suivi du poids dans le temps | ⭐ |
| 🔌 API REST pour intégration mobile | ⭐⭐⭐ |
| 🔔 Notifications de rappel (email / push) | ⭐⭐⭐ |
| 🤖 Recommandations IA (LLM) sur les conseils | ⭐⭐⭐ |

---

## 12. FAQ

<details>
<summary><strong>❓ Mes données sont-elles envoyées sur internet ?</strong></summary>

> Non. En version locale, tout reste sur ton ordinateur (`coach_sport.db`).
> En version hébergée, les données sont stockées sur le serveur Streamlit (éphémère).

</details>

<details>
<summary><strong>❓ Comment réinitialiser totalement l'application ?</strong></summary>

> Supprime le fichier `coach_sport.db`. Il sera recréé au prochain lancement.

</details>

<details>
<summary><strong>❓ Puis-je ajouter mes propres séances/repas ?</strong></summary>

> Oui. Édite directement `seances_sport.py` ou `repas_nutrition.py`.
> Les nouvelles entrées sont prises en compte immédiatement.

</details>

<details>
<summary><strong>❓ Pourquoi y a-t-il deux versions desktop (`app.py` et `app_v2.py`) ?</strong></summary>

> - `app.py` : première version (basique)
> - `app_v2.py` : ajoute profil, IMC, notes, suivi
> - La version Streamlit reprend `app_v2.py` en web

</details>

<details>
<summary><strong>❓ Le port 8501 est déjà utilisé, comment changer ?</strong></summary>

```bash
streamlit run streamlit_app.py --server.port 8765
```

</details>

<details>
<summary><strong>❓ Comment devenir administrateur ?</strong></summary>

> Le **premier compte créé** sur l'application devient automatiquement admin.
> Les admins suivants peuvent ensuite être promus depuis l'onglet « Administration ».

</details>

<details>
<summary><strong>❓ J'ai oublié le mot de passe administrateur, que faire ?</strong></summary>

> Si **un autre admin existe**, il peut réinitialiser ton mot de passe depuis l'onglet « Administration ».
>
> Sinon, accède directement à la base SQLite (`coach_sport.db`) avec un client SQLite et supprime la ligne dans la table `users`. Le prochain compte créé deviendra admin.

</details>

<details>
<summary><strong>❓ Mes données sont-elles isolées des autres utilisateurs ?</strong></summary>

> Oui. Chaque enregistrement (`profil`, `historique`) est lié à un `user_id`. Toutes les requêtes filtrent par `user_id` : un utilisateur ne voit jamais les données d'un autre.

</details>

<details>
<summary><strong>❓ Les mots de passe sont-ils stockés en clair ?</strong></summary>

> Non, jamais. Ils sont **hashés avec PBKDF2-HMAC-SHA256** (200 000 itérations + salt aléatoire de 16 octets unique par utilisateur).

</details>

---

## 13. Crédits

<div align="center">

### 🎓 Projet réalisé en groupe — BTS SIO SLAM

| Membre | Rôle |
| :---: | :--- |
| 👤 **Nicolas** | Module séances sportives |
| 👤 **Jordy** | Module saisie utilisateur |
| 👤 **Ivann** | Module affichage + version Streamlit + intégration |
| 👤 **Cheikh** | Module nutrition |

🐙 Organisation GitHub : **`wedoee-collab`**

---

*Documentation à jour au 13 avril 2026.*

</div>
