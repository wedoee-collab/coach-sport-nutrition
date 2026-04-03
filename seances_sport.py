# ============================================================
#  Module : Séances de sport
#  Auteur : Nicolas
#  Branche : feat/seances-sport
# ============================================================

import random

# ---------- DONNÉES ----------

# Séances organisées par objectif ET par niveau
# Chaque séance précise la durée et les exercices
SEANCES = {
    "prise de masse": {
        "debutant": [
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + 3x10 pompes + 3x12 squats + 3x10 fentes + 3x15 abdominaux + retour au calme 5 min"
            },
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + 3x10 dips sur chaise + 3x12 soulevé de terre léger + 3x10 rowing haltères + retour au calme 5 min"
            },
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + 3x12 développé couché haltères légers + 3x10 curl biceps + 3x12 élévations latérales + retour au calme 5 min"
            },
        ],
        "intermediaire": [
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + 4x10 développé couché + 4x10 rowing barre + 4x12 squats haltères + 4x15 abdominaux + retour au calme 5 min"
            },
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + 4x8 soulevé de terre + 4x10 tractions assistées + 4x12 presse à cuisses + 4x15 crunchs + retour au calme 5 min"
            },
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + 4x10 squat bulgare + 4x10 développé militaire + 4x12 curl marteau + 4x10 triceps poulie + retour au calme 5 min"
            },
        ],
        "confirme": [
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + 5x5 squat lourd + 5x5 développé couché lourd + 4x8 rowing barre + 4x10 tractions lestées + 4x12 curl + 4x12 triceps barre + gainage 3x1 min + retour au calme 10 min"
            },
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + 5x5 soulevé de terre + 5x5 développé militaire + 4x8 squat bulgare + 4x10 dips lestés + 4x12 élévations latérales + abdos 4x20 + retour au calme 10 min"
            },
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + Push/Pull/Legs : 4x8 développé incliné + 4x8 rowing unilatéral + 4x10 leg press + 4x12 curl incliné + 4x12 extensions triceps + mollets 4x20 + retour au calme 10 min"
            },
        ],
    },

    "seche": {
        "debutant": [
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + circuit 3 tours : 15 squats / 10 pompes / 20 abdominaux / 15 fentes / 30 sec gainage + retour au calme 5 min"
            },
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + 20 min marche rapide + circuit 2 tours : 15 squats sautés / 10 burpees / 20 mountain climbers + retour au calme 5 min"
            },
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + tabata 4 rounds (20s effort / 10s repos) : jumping jacks / squats / pompes / abdominaux + retour au calme 10 min"
            },
        ],
        "intermediaire": [
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + HIIT 30 min (30s sprint / 30s repos x15) + circuit muscu 3 tours : 15 squats haltères / 12 pompes déclinées / 20 abdominaux + retour au calme 10 min"
            },
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + 4x15 fentes marchées + 4x20 squats sautés + 4x15 pompes + 4x20 mountain climbers + 20 min vélo intensité modérée + retour au calme 5 min"
            },
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + circuit 4 tours : burpees x12 / tractions x8 / dips x12 / gainage 45 sec / corde à sauter 1 min + retour au calme 10 min"
            },
        ],
        "confirme": [
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + HIIT 20 min (sprint 20s / repos 10s x20) + muscu sèche 4x15 squat / 4x15 développé couché / 4x15 rowing + cardio 25 min elliptique intensité haute + retour au calme 10 min"
            },
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + CrossFit : 5 rounds de 21 thrusters / 15 tractions / 9 burpees + 30 min course fractionnée (1 min rapide / 1 min lent) + retour au calme 10 min"
            },
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + circuit full body 5 tours : deadlift x10 / box jump x12 / pompes archer x8 / kettlebell swing x15 / corde à sauter 1 min + cardio 20 min + retour au calme 10 min"
            },
        ],
    },

    "maintien": {
        "debutant": [
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + 30 min marche rapide ou vélo léger + 3x10 squats + 3x10 pompes + 3x15 abdominaux + étirements 5 min"
            },
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + yoga débutant 20 min + 3x12 fentes + 3x10 dips chaise + 3x15 crunchs + retour au calme 5 min"
            },
            {
                "duree": "45 min",
                "seance": "Échauffement 5 min + 25 min natation douce + 2x15 squats + 2x10 pompes + gainage 3x30 sec + étirements 5 min"
            },
        ],
        "intermediaire": [
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + 30 min course légère + 3x12 squats haltères + 3x10 développé épaules + 3x15 abdominaux + étirements 10 min"
            },
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + circuit 3 tours équilibré : 12 squats / 10 tractions assistées / 15 abdos / 12 fentes / 10 pompes + 20 min cardio modéré + retour au calme 5 min"
            },
            {
                "duree": "1h",
                "seance": "Échauffement 10 min + 35 min vélo intensité moyenne + 3x12 rowing + 3x12 développé couché + gainage 3x45 sec + étirements 5 min"
            },
        ],
        "confirme": [
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + 40 min course à allure modérée + full body 4x10 : squat / développé couché / rowing barre / développé militaire / curl + gainage 4x1 min + retour au calme 10 min"
            },
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + 30 min natation / vélo / elliptique + muscu entretien 4x10 : soulevé de terre / tractions / dips / fentes lestées + abdos 4x20 + étirements 10 min"
            },
            {
                "duree": "1h30",
                "seance": "Échauffement 10 min + Pilates ou yoga avancé 30 min + muscu fonctionnelle 4x12 : kettlebell swing / turkish get-up / box jump / fentes rotatives + cardio 20 min + retour au calme 10 min"
            },
        ],
    },
}


# ---------- FONCTIONS ----------

def choisir_objectif_sport():
    """Demande et retourne l'objectif sportif de l'utilisateur."""
    print("\nQuel est ton objectif sportif ?")
    print("  1. Prise de masse")
    print("  2. Sèche")
    print("  3. Maintien")

    choix = input("\nTon choix (1/2/3) : ").strip()

    if choix == "1":
        return "prise de masse"
    elif choix == "2":
        return "seche"
    elif choix == "3":
        return "maintien"
    else:
        print("Choix invalide, objectif par défaut : maintien.")
        return "maintien"


def choisir_niveau():
    """Demande et retourne le niveau sportif de l'utilisateur."""
    print("\nQuel est ton niveau sportif ?")
    print("  1. Débutant")
    print("  2. Intermédiaire")
    print("  3. Confirmé")

    choix = input("\nTon choix (1/2/3) : ").strip()

    if choix == "1":
        return "debutant"
    elif choix == "2":
        return "intermediaire"
    elif choix == "3":
        return "confirme"
    else:
        print("Choix invalide, niveau par défaut : débutant.")
        return "debutant"


def afficher_seance(objectif, niveau):
    """Affiche une séance de sport aléatoire selon l'objectif et le niveau."""

    # Sélection aléatoire dans la liste correspondante
    seance = random.choice(SEANCES[objectif][niveau])

    print("\n--- SÉANCE DE SPORT ---")
    print(f"  Objectif : {objectif.capitalize()}")
    print(f"  Niveau   : {niveau.capitalize()}")
    print(f"  Durée    : {seance['duree']}")
    print(f"  Programme: {seance['seance']}")


# ---------- TEST RAPIDE ----------

if __name__ == "__main__":
    objectif = choisir_objectif_sport()
    niveau   = choisir_niveau()
    afficher_seance(objectif, niveau)
