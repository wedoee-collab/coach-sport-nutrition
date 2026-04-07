# ============================================================
#  Coach Sport & Nutrition — Programme Principal
#  Assemblage des modules de l'équipe
#  Auteurs : Nicolas, Jordy, Ivann, Cheikh
# ============================================================

from __future__ import annotations

import random
import shutil
import sys
import textwrap

# ---------- DONNÉES SÉANCES (Nicolas) ----------

SEANCES = {
    "prise de masse": {
        "debutant": [
            {"duree": "45 min", "seance": "Échauffement 5 min + 3x10 pompes + 3x12 squats + 3x10 fentes + 3x15 abdominaux + retour au calme 5 min"},
            {"duree": "45 min", "seance": "Échauffement 5 min + 3x10 dips sur chaise + 3x12 soulevé de terre léger + 3x10 rowing haltères + retour au calme 5 min"},
            {"duree": "45 min", "seance": "Échauffement 5 min + 3x12 développé couché haltères légers + 3x10 curl biceps + 3x12 élévations latérales + retour au calme 5 min"},
        ],
        "intermediaire": [
            {"duree": "1h", "seance": "Échauffement 10 min + 4x10 développé couché + 4x10 rowing barre + 4x12 squats haltères + 4x15 abdominaux + retour au calme 5 min"},
            {"duree": "1h", "seance": "Échauffement 10 min + 4x8 soulevé de terre + 4x10 tractions assistées + 4x12 presse à cuisses + 4x15 crunchs + retour au calme 5 min"},
            {"duree": "1h", "seance": "Échauffement 10 min + 4x10 squat bulgare + 4x10 développé militaire + 4x12 curl marteau + 4x10 triceps poulie + retour au calme 5 min"},
        ],
        "confirme": [
            {"duree": "1h30", "seance": "Échauffement 10 min + 5x5 squat lourd + 5x5 développé couché lourd + 4x8 rowing barre + 4x10 tractions lestées + 4x12 curl + 4x12 triceps barre + gainage 3x1 min + retour au calme 10 min"},
            {"duree": "1h30", "seance": "Échauffement 10 min + 5x5 soulevé de terre + 5x5 développé militaire + 4x8 squat bulgare + 4x10 dips lestés + 4x12 élévations latérales + abdos 4x20 + retour au calme 10 min"},
            {"duree": "1h30", "seance": "Échauffement 10 min + Push/Pull/Legs : 4x8 développé incliné + 4x8 rowing unilatéral + 4x10 leg press + 4x12 curl incliné + 4x12 extensions triceps + mollets 4x20 + retour au calme 10 min"},
        ],
    },
    "seche": {
        "debutant": [
            {"duree": "45 min", "seance": "Échauffement 5 min + circuit 3 tours : 15 squats / 10 pompes / 20 abdominaux / 15 fentes / 30 sec gainage + retour au calme 5 min"},
            {"duree": "45 min", "seance": "Échauffement 5 min + 20 min marche rapide + circuit 2 tours : 15 squats sautés / 10 burpees / 20 mountain climbers + retour au calme 5 min"},
            {"duree": "45 min", "seance": "Échauffement 5 min + tabata 4 rounds (20s effort / 10s repos) : jumping jacks / squats / pompes / abdominaux + retour au calme 10 min"},
        ],
        "intermediaire": [
            {"duree": "1h", "seance": "Échauffement 10 min + HIIT 30 min (30s sprint / 30s repos x15) + circuit muscu 3 tours : 15 squats haltères / 12 pompes déclinées / 20 abdominaux + retour au calme 10 min"},
            {"duree": "1h", "seance": "Échauffement 10 min + 4x15 fentes marchées + 4x20 squats sautés + 4x15 pompes + 4x20 mountain climbers + 20 min vélo intensité modérée + retour au calme 5 min"},
            {"duree": "1h", "seance": "Échauffement 10 min + circuit 4 tours : burpees x12 / tractions x8 / dips x12 / gainage 45 sec / corde à sauter 1 min + retour au calme 10 min"},
        ],
        "confirme": [
            {"duree": "1h30", "seance": "Échauffement 10 min + HIIT 20 min (sprint 20s / repos 10s x20) + muscu sèche 4x15 squat / 4x15 développé couché / 4x15 rowing + cardio 25 min elliptique intensité haute + retour au calme 10 min"},
            {"duree": "1h30", "seance": "Échauffement 10 min + CrossFit : 5 rounds de 21 thrusters / 15 tractions / 9 burpees + 30 min course fractionnée (1 min rapide / 1 min lent) + retour au calme 10 min"},
            {"duree": "1h30", "seance": "Échauffement 10 min + circuit full body 5 tours : deadlift x10 / box jump x12 / pompes archer x8 / kettlebell swing x15 / corde à sauter 1 min + cardio 20 min + retour au calme 10 min"},
        ],
    },
    "maintien": {
        "debutant": [
            {"duree": "45 min", "seance": "Échauffement 5 min + 30 min marche rapide ou vélo léger + 3x10 squats + 3x10 pompes + 3x15 abdominaux + étirements 5 min"},
            {"duree": "45 min", "seance": "Échauffement 5 min + yoga débutant 20 min + 3x12 fentes + 3x10 dips chaise + 3x15 crunchs + retour au calme 5 min"},
            {"duree": "45 min", "seance": "Échauffement 5 min + 25 min natation douce + 2x15 squats + 2x10 pompes + gainage 3x30 sec + étirements 5 min"},
        ],
        "intermediaire": [
            {"duree": "1h", "seance": "Échauffement 10 min + 30 min course légère + 3x12 squats haltères + 3x10 développé épaules + 3x15 abdominaux + étirements 10 min"},
            {"duree": "1h", "seance": "Échauffement 10 min + circuit 3 tours équilibré : 12 squats / 10 tractions assistées / 15 abdos / 12 fentes / 10 pompes + 20 min cardio modéré + retour au calme 5 min"},
            {"duree": "1h", "seance": "Échauffement 10 min + 35 min vélo intensité moyenne + 3x12 rowing + 3x12 développé couché + gainage 3x45 sec + étirements 5 min"},
        ],
        "confirme": [
            {"duree": "1h30", "seance": "Échauffement 10 min + 40 min course à allure modérée + full body 4x10 : squat / développé couché / rowing barre / développé militaire / curl + gainage 4x1 min + retour au calme 10 min"},
            {"duree": "1h30", "seance": "Échauffement 10 min + 30 min natation / vélo / elliptique + muscu entretien 4x10 : soulevé de terre / tractions / dips / fentes lestées + abdos 4x20 + étirements 10 min"},
            {"duree": "1h30", "seance": "Échauffement 10 min + Pilates ou yoga avancé 30 min + muscu fonctionnelle 4x12 : kettlebell swing / turkish get-up / box jump / fentes rotatives + cardio 20 min + retour au calme 10 min"},
        ],
    },
}

# ---------- DONNÉES REPAS (Cheikh) ----------

REPAS = {
    "prise de masse": [
        {"nom": "Riz complet + blanc de poulet + brocolis + fromage blanc", "calories": "650 kcal", "proteines": "55g de protéines"},
        {"nom": "Pâtes complètes + thon + tomates + huile d'olive", "calories": "600 kcal", "proteines": "45g de protéines"},
        {"nom": "Steak haché 5% + patate douce + épinards + yaourt protéiné", "calories": "700 kcal", "proteines": "60g de protéines"},
        {"nom": "Omelette 4 œufs + avocat + pain complet + fromage blanc", "calories": "620 kcal", "proteines": "40g de protéines"},
        {"nom": "Saumon + quinoa + haricots verts + huile d'olive", "calories": "680 kcal", "proteines": "50g de protéines"},
    ],
    "seche": [
        {"nom": "Salade de poulet grillé + légumes verts + vinaigrette citron", "calories": "350 kcal", "proteines": "40g de protéines"},
        {"nom": "Soupe de légumes maison + œuf dur + fruit frais", "calories": "280 kcal", "proteines": "20g de protéines"},
        {"nom": "Saumon vapeur + haricots verts + quinoa (petite portion)", "calories": "380 kcal", "proteines": "35g de protéines"},
        {"nom": "Blanc de poulet + courgettes sautées + riz basmati (80g)", "calories": "320 kcal", "proteines": "38g de protéines"},
        {"nom": "Thon en boîte + salade verte + tomates + concombre + citron", "calories": "250 kcal", "proteines": "30g de protéines"},
    ],
    "maintien": [
        {"nom": "Bowl : riz, avocat, légumes rôtis, œuf mollet", "calories": "500 kcal", "proteines": "25g de protéines"},
        {"nom": "Wrap complet : jambon, crudités, houmous", "calories": "450 kcal", "proteines": "22g de protéines"},
        {"nom": "Omelette aux légumes + pain complet + salade verte", "calories": "420 kcal", "proteines": "28g de protéines"},
        {"nom": "Poulet rôti + légumes du four + pomme de terre", "calories": "480 kcal", "proteines": "35g de protéines"},
        {"nom": "Soupe de lentilles + pain complet + yaourt nature", "calories": "430 kcal", "proteines": "24g de protéines"},
    ],
}

CONSEILS_NUTRITION = {
    "prise de masse": [
        "Mange toutes les 3h pour maintenir un apport protéiné constant.",
        "Prends un shaker protéiné dans les 30 min après ta séance.",
        "Privilégie les glucides complexes : riz, pâtes, patate douce.",
        "Dors 8h minimum : c'est pendant le sommeil que le muscle se construit.",
    ],
    "seche": [
        "Bois 2L d'eau par jour minimum pour éliminer les toxines.",
        "Évite les sucres rapides et les aliments ultra-transformés.",
        "Mange des légumes à volonté : peu caloriques et rassasiants.",
        "Ne saute pas de repas : ça ralentit le métabolisme.",
    ],
    "maintien": [
        "Mange équilibré : 1/2 légumes, 1/4 protéines, 1/4 glucides.",
        "Bois au moins 1,5L d'eau par jour.",
        "Fais 3 repas par jour à heures régulières.",
        "Autorise-toi un repas plaisir par semaine, sans culpabiliser.",
    ],
}

# ---------- AFFICHAGE (Ivann) ----------

OBJECTIFS = [
    ("Prise de masse", "prise de masse"),
    ("Sèche", "seche"),
    ("Maintien", "maintien"),
]

NIVEAUX = [
    ("Débutant", "debutant"),
    ("Intermédiaire", "intermediaire"),
    ("Confirmé", "confirme"),
]

FOCUS_OBJECTIF = {
    "prise de masse": "Focus force et récupération",
    "seche":          "Focus cardio et dépense calorique",
    "maintien":       "Focus équilibre et endurance",
}

INTENSITE_NIVEAU = {
    "debutant":      35,
    "intermediaire": 65,
    "confirme":      90,
}

COULEURS = {
    "cyan":    "\033[96m",
    "vert":    "\033[92m",
    "jaune":   "\033[93m",
    "bleu":    "\033[94m",
    "magenta": "\033[95m",
    "gras":    "\033[1m",
    "reset":   "\033[0m",
}

def couleurs_actives() -> bool:
    return sys.stdout.isatty()

def colorer(texte: str, couleur: str) -> str:
    if not couleurs_actives():
        return texte
    return f"{COULEURS[couleur]}{texte}{COULEURS['reset']}"

def largeur_interface() -> int:
    colonnes = shutil.get_terminal_size(fallback=(88, 24)).columns
    return max(60, min(colonnes, 88))

def envelopper_lignes(lignes: list[str], largeur: int) -> list[str]:
    resultat: list[str] = []
    for ligne in lignes:
        morceaux = textwrap.wrap(ligne, width=largeur) or [""]
        resultat.extend(morceaux)
    return resultat

def construire_bloc(titre: str, lignes: list[str], couleur: str = "cyan") -> str:
    largeur = largeur_interface() - 4
    contenu = envelopper_lignes(lignes, largeur)
    bordure     = colorer("+" + "-" * (largeur + 2) + "+", couleur)
    titre_ligne = f"| {titre.center(largeur)} |"
    rendu = [bordure, colorer(titre_ligne, couleur), bordure]
    for ligne in contenu:
        rendu.append(f"| {ligne.ljust(largeur)} |")
    rendu.append(bordure)
    return "\n".join(rendu)

def barre_progression(valeur: int, maximum: int = 100, largeur: int = 24) -> str:
    ratio = 0 if maximum <= 0 else max(0, min(valeur / maximum, 1))
    pleins = round(ratio * largeur)
    return f"[{'#' * pleins}{'.' * (largeur - pleins)}] {int(ratio * 100)}%"

def trouver_label(cle: str, options: list[tuple[str, str]]) -> str:
    for label, valeur in options:
        if valeur == cle:
            return label
    return cle

def afficher_entete() -> None:
    largeur = largeur_interface()
    print()
    print(colorer("=" * largeur, "magenta"))
    print(colorer("COACH SPORT & NUTRITION".center(largeur), "gras"))
    print(colorer("Ton programme personnalisé".center(largeur), "bleu"))
    print(colorer("=" * largeur, "magenta"))

def afficher_pied_page() -> None:
    print()
    print(construire_bloc(
        "À BIENTÔT",
        ["Merci d'avoir utilisé le Coach Sport & Nutrition.",
         "Reviens quand tu veux pour un nouveau programme !"],
        "magenta",
    ))

# ---------- QUESTIONS (Jordy) ----------

def choisir_option(titre: str, sous_titre: str, options: list[tuple[str, str]], couleur: str) -> str:
    lignes = [sous_titre, ""]
    for index, (label, _) in enumerate(options, start=1):
        lignes.append(f"{index}. {label}")
    print()
    print(construire_bloc(titre, lignes, couleur))
    while True:
        choix = input("\nTon choix : ").strip()
        if choix.isdigit():
            index = int(choix) - 1
            if 0 <= index < len(options):
                return options[index][1]
        print(colorer("⚠️  Choix invalide. Merci de saisir un numéro proposé.", "jaune"))

def demander_rejouer() -> bool:
    print()
    print(construire_bloc(
        "CONTINUER ?",
        ["1. Oui, générer un nouveau programme", "2. Non, quitter"],
        "bleu",
    ))
    while True:
        reponse = input("\nTon choix : ").strip()
        if reponse == "1":
            return True
        if reponse == "2":
            return False
        print(colorer("⚠️  Choix invalide. Merci de saisir 1 ou 2.", "jaune"))

# ---------- PROGRAMME PRINCIPAL ----------

def generer_programme(objectif: str, niveau: str) -> dict:
    seance  = random.choice(SEANCES[objectif][niveau])
    repas   = random.choice(REPAS[objectif])
    conseil = random.choice(CONSEILS_NUTRITION[objectif])
    return {
        "duree":   seance["duree"],
        "seance":  seance["seance"],
        "repas":   repas,
        "conseil": conseil,
    }

def afficher_resume(objectif: str, niveau: str) -> None:
    objectif_label = trouver_label(objectif, OBJECTIFS)
    niveau_label   = trouver_label(niveau, NIVEAUX)
    intensite      = INTENSITE_NIVEAU[niveau]
    lignes = [
        f"Objectif sélectionné : {objectif_label}",
        f"Niveau choisi        : {niveau_label}",
        f"Style du programme   : {FOCUS_OBJECTIF[objectif]}",
        f"Intensité du jour    : {barre_progression(intensite)}",
    ]
    print()
    print(construire_bloc("TON PROFIL", lignes, "bleu"))

def afficher_resultats(objectif: str, niveau: str, programme: dict) -> None:
    objectif_label = trouver_label(objectif, OBJECTIFS)
    niveau_label   = trouver_label(niveau, NIVEAUX)
    print()
    print(construire_bloc(
        "PROGRAMME PERSONNALISÉ",
        [f"Profil : {objectif_label} | {niveau_label}",
         "Voici ta proposition pour cette session."],
        "vert",
    ))
    print()
    print(construire_bloc(
        "SÉANCE DE SPORT",
        [f"Durée : {programme['duree']}", programme["seance"]],
        "cyan",
    ))
    repas = programme["repas"]
    print()
    print(construire_bloc(
        "REPAS CONSEILLÉ",
        [repas["nom"], f"Apport : {repas['calories']} | {repas['proteines']}"],
        "magenta",
    ))
    print()
    print(construire_bloc("CONSEIL NUTRITION", [programme["conseil"]], "jaune"))

def main() -> None:
    afficher_entete()
    continuer = True
    while continuer:
        objectif = choisir_option(
            "OBJECTIF",
            "Choisis ce que tu veux travailler aujourd'hui.",
            OBJECTIFS,
            "cyan",
        )
        niveau = choisir_option(
            "NIVEAU",
            "Choisis le niveau qui te correspond.",
            NIVEAUX,
            "vert",
        )
        programme = generer_programme(objectif, niveau)
        afficher_resume(objectif, niveau)
        afficher_resultats(objectif, niveau, programme)
        continuer = demander_rejouer()
    afficher_pied_page()

if __name__ == "__main__":
    main()
