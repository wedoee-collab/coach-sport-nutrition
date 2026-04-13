# Coach Sport & Nutrition

Application qui génère des programmes sport + nutrition personnalisés selon ton objectif (prise de masse, sèche, maintien) et ton niveau (débutant, intermédiaire, confirmé).

Auteurs : Nicolas, Jordy, Ivann, Cheikh — BTS SIO SLAM

## Versions disponibles

- **`streamlit_app.py`** — version web (recommandée pour l'hébergement en ligne)
- `app_v2.py` — version desktop Tkinter (complète : profil, IMC, historique, suivi)
- `app.py` — version desktop Tkinter (basique)

## Installation locale

```bash
pip install -r requirements.txt
```

## Lancer la version web (Streamlit)

```bash
streamlit run streamlit_app.py
```

L'application s'ouvre dans le navigateur sur `http://localhost:8501`.

## Lancer la version desktop

```bash
python app_v2.py
```

## Hébergement en ligne (Streamlit Community Cloud — gratuit)

1. Pousser le projet sur un dépôt **GitHub public**.
2. Aller sur https://share.streamlit.io et se connecter avec GitHub.
3. Cliquer sur **New app**, sélectionner le repo, la branche `main`, et le fichier `streamlit_app.py`.
4. Cliquer sur **Deploy**. L'app sera disponible sur une URL publique en quelques minutes.

⚠️ La base SQLite (`coach_sport.db`) est stockée sur le disque éphémère du serveur : les données peuvent être effacées au redémarrage. Pour de la persistance réelle, migrer vers PostgreSQL (Supabase, Neon, etc.).

## Autres options d'hébergement

- **Render** / **Railway** / **Fly.io** — supportent Streamlit avec `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- **Hugging Face Spaces** — créer un Space « Streamlit » et y pousser le code

## Structure du projet

```
.
├── streamlit_app.py        # Interface web (Streamlit)
├── app_v2.py               # Interface desktop Tkinter v2
├── app.py                  # Interface desktop Tkinter v1
├── seances_sport.py        # Données séances (Nicolas)
├── repas_nutrition.py      # Données repas et conseils (Cheikh)
├── questions-utilisateur.py# Saisie console (Jordy)
├── affichage_resultats.py  # Affichage console (Ivann)
├── requirements.txt
└── README.md
```
