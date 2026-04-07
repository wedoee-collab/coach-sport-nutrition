# ============================================================
#  Coach Sport & Nutrition
#  Programme Python - BTS SIO SLAM
# ============================================================

import random

# ---------- DONNÉES ----------

# Séances de sport par niveau
SEANCES = {
    "debutant": [
        "20 min de marche rapide + 10 pompes + 15 squats",
        "30 min de vélo léger + 20 abdominaux",
        "15 min de corde à sauter + 3 séries de fentes",
    ],
    "moyen": [
        "30 min de course + 3x15 pompes + 3x20 squats",
        "45 min de natation + gainage 3x45 sec",
        "Circuit training 40 min : burpees, tractions, squats sautés",
    ],
    "avance": [
        "1h de course fractionnée (sprint 30s / récup 1min) x10",
        "Séance musculation full body 1h + 20 min cardio HIIT",
        "CrossFit 45 min : thrusters, traction, kettlebell + gainage",
    ],
}

# Repas par objectif
REPAS = {
    "perdre du poids": [
        "Salade de poulet grillé, légumes verts, vinaigrette citron",
        "Soupe de légumes maison + œuf dur + fruit frais",
        "Saumon vapeur + haricots verts + quinoa (petite portion)",
    ],
    "prendre du muscle": [
        "Riz complet + blanc de poulet + brocolis + fromage blanc",
        "Pâtes complètes + thon + tomates + huile d'olive",
        "Steak haché 5% + patate douce + épinards + yaourt protéiné",
    ],
    "rester en forme": [
        "Bowl : riz, avocat, légumes rôtis, œuf mollet",
        "Wrap complet : jambon, crudités, houmous",
        "Omelette aux légumes + pain complet + salade verte",
    ],
}

# Conseils santé
CONSEILS = [
    "Bois au moins 1,5L d'eau par jour, surtout avant et après l'effort.",
    "Dors 7 à 9h par nuit : le corps se reconstruit pendant le sommeil.",
    "Evite les sodas et privilégie l'eau ou les infusions sans sucre.",
    "Mange lentement et sans écran pour mieux ressentir la satiété.",
    "Prends un encas protéiné (yaourt, amandes) après ta séance.",
    "Ne saute pas le petit-déjeuner si tu t'entraînes le matin.",
]

# ---------- FONCTIONS ----------

def choisir_objectif():
    """Demande et retourne l'objectif de l'utilisateur."""
    print("\nQuel est ton objectif ?")
    print("  1. Perdre du poids")
    print("  2. Prendre du muscle")
    print("  3. Rester en forme")

    choix = input("\nTon choix (1/2/3) : ").strip()

    if choix == "1":
        return "perdre du poids"
    elif choix == "2":
        return "prendre du muscle"
    elif choix == "3":
        return "rester en forme"
    else:
        print("Choix invalide, objectif par défaut : rester en forme.")
        return "rester en forme"


def choisir_niveau():
    """Demande et retourne le niveau sportif de l'utilisateur."""
    print("\nQuel est ton niveau sportif ?")
    print("  1. Débutant")
    print("  2. Moyen")
    print("  3. Avancé")

    choix = input("\nTon choix (1/2/3) : ").strip()

    if choix == "1":
        return "debutant"
    elif choix == "2":
        return "moyen"
    elif choix == "3":
        return "avance"
    else:
        print("Choix invalide, niveau par défaut : débutant.")
        return "debutant"


def afficher_programme(objectif, niveau):
    """Affiche la séance, le repas et le conseil adaptés."""

    # Sélection aléatoire dans les listes
    seance = random.choice(SEANCES[niveau])
    repas  = random.choice(REPAS[objectif])
    conseil = random.choice(CONSEILS)

    print("\n" + "=" * 50)
    print("       TON PROGRAMME PERSONNALISÉ")
    print("=" * 50)

    print(f"\nObjectif : {objectif.capitalize()}")
    print(f"Niveau   : {niveau.capitalize()}")

    print("\n--- SÉANCE DE SPORT ---")
    print(f"  {seance}")

    print("\n--- IDÉE DE REPAS ---")
    print(f"  {repas}")

    print("\n--- CONSEIL SANTÉ ---")
    print(f"  {conseil}")

    print("\n" + "=" * 50)


def demander_rejouer():
    """Demande si l'utilisateur veut recommencer."""
    reponse = input("\nVeux-tu un nouveau programme ? (oui / non) : ").strip().lower()
    return reponse in ["oui", "o", "yes", "y"]


# ---------- PROGRAMME PRINCIPAL ----------

def main():
    print("=" * 50)
    print("   Bienvenue dans COACH SPORT & NUTRITION !")
    print("=" * 50)

    continuer = True

    while continuer:
        # Récupération des choix utilisateur
        objectif = choisir_objectif()
        niveau   = choisir_niveau()

        # Affichage du programme
        afficher_programme(objectif, niveau)

        # Option recommencer
        continuer = demander_rejouer()

    print("\nBonne séance et bonne nutrition ! À bientôt.")


# Lancement du programme
if __name__ == "__main__":
    from affichage_resultats import main as lancer_programme

    lancer_programme()
