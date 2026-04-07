# ============================================================
#  Module : Affichage des résultats
#  Auteur : Ivann
#  Branche : feat/affichage-resultats
# ============================================================

from __future__ import annotations

import random
import shutil
import sys
import textwrap

import coach_sport_nutrition as coach


# ---------- DONNÉES HARMONISÉES ----------

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


# ---------- FONCTIONS UTILITAIRES ----------

def couleurs_actives() -> bool:
    return sys.stdout.isatty()


def colorer(texte: str, couleur: str) -> str:
    if not couleurs_actives():
        return texte
    return f"{COULEURS[couleur]}{texte}{COULEURS['reset']}"


def largeur_interface() -> int:
    colonnes = shutil.get_terminal_size(fallback=(88, 24)).columns
    return max(60, min(colonnes, 88))


def centrer(texte: str, largeur: int) -> str:
    return texte.center(largeur)


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


# ---------- FONCTIONS D'AFFICHAGE ----------

def afficher_entete() -> None:
    largeur = largeur_interface()
    print()
    print(colorer("=" * largeur, "magenta"))
    print(colorer(centrer("COACH SPORT & NUTRITION", largeur), "gras"))
    print(colorer(centrer("Ton programme personnalisé", largeur), "bleu"))
    print(colorer("=" * largeur, "magenta"))


def choisir_option(
    titre: str,
    sous_titre: str,
    options: list[tuple[str, str]],
    couleur: str,
) -> str:
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
        print(colorer("Choix invalide. Merci de saisir un numéro proposé.", "jaune"))


def generer_programme(objectif: str, niveau: str) -> dict[str, str]:
    # Utilise la structure SEANCES[objectif][niveau] du module séances
    seance  = random.choice(coach.SEANCES[objectif][niveau])
    repas   = random.choice(coach.REPAS[objectif])
    conseil = random.choice(coach.CONSEILS)
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


def afficher_resultats(objectif: str, niveau: str, programme: dict[str, str]) -> None:
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

    print()
    print(construire_bloc("REPAS CONSEILLÉ",  [programme["repas"]],   "magenta"))

    print()
    print(construire_bloc("CONSEIL SANTÉ",    [programme["conseil"]], "jaune"))


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
        print(colorer("Choix invalide. Merci de saisir 1 ou 2.", "jaune"))


def afficher_pied_page() -> None:
    print()
    print(construire_bloc(
        "À BIENTÔT",
        ["Merci d'avoir utilisé le Coach Sport & Nutrition.",
         "Reviens quand tu veux pour un nouveau programme !"],
        "magenta",
    ))


# ---------- PROGRAMME PRINCIPAL ----------

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
