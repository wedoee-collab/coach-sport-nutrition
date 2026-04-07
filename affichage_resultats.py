from __future__ import annotations

import random
import shutil
import sys
import textwrap

import coach_sport_nutrition as coach


OBJECTIFS = [
    ("Perdre du poids", "perdre du poids"),
    ("Prendre du muscle", "prendre du muscle"),
    ("Rester en forme", "rester en forme"),
]

NIVEAUX = [
    ("Debutant", "debutant"),
    ("Moyen", "moyen"),
    ("Avance", "avance"),
]

FOCUS_OBJECTIF = {
    "perdre du poids": "Focus cardio et regularite",
    "prendre du muscle": "Focus force et recuperation",
    "rester en forme": "Focus equilibre et endurance",
}

INTENSITE_NIVEAU = {
    "debutant": 35,
    "moyen": 65,
    "avance": 90,
}

COULEURS = {
    "cyan": "\033[96m",
    "vert": "\033[92m",
    "jaune": "\033[93m",
    "bleu": "\033[94m",
    "magenta": "\033[95m",
    "gras": "\033[1m",
    "reset": "\033[0m",
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

    bordure = colorer("+" + "-" * (largeur + 2) + "+", couleur)
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


def afficher_entete() -> None:
    largeur = largeur_interface()
    print()
    print(colorer("=" * largeur, "magenta"))
    print(colorer(centrer("COACH SPORT & NUTRITION", largeur), "gras"))
    print(colorer(centrer("Version avec affichage ameliore", largeur), "bleu"))
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

        print(colorer("Choix invalide. Merci de saisir un numero propose.", "jaune"))


def generer_programme(objectif: str, niveau: str) -> dict[str, str]:
    return {
        "seance": random.choice(coach.SEANCES[niveau]),
        "repas": random.choice(coach.REPAS[objectif]),
        "conseil": random.choice(coach.CONSEILS),
    }


def trouver_label(cle: str, options: list[tuple[str, str]]) -> str:
    for label, valeur in options:
        if valeur == cle:
            return label
    return cle


def afficher_resume(objectif: str, niveau: str) -> None:
    objectif_label = trouver_label(objectif, OBJECTIFS)
    niveau_label = trouver_label(niveau, NIVEAUX)
    intensite = INTENSITE_NIVEAU[niveau]

    lignes = [
        f"Objectif selectionne : {objectif_label}",
        f"Niveau choisi       : {niveau_label}",
        f"Style du programme  : {FOCUS_OBJECTIF[objectif]}",
        f"Intensite du jour   : {barre_progression(intensite)}",
    ]

    print()
    print(construire_bloc("TON PROFIL", lignes, "bleu"))


def afficher_resultats(objectif: str, niveau: str, programme: dict[str, str]) -> None:
    objectif_label = trouver_label(objectif, OBJECTIFS)
    niveau_label = trouver_label(niveau, NIVEAUX)

    print()
    print(
        construire_bloc(
            "PROGRAMME PERSONNALISE",
            [
                f"Profil : {objectif_label} | {niveau_label}",
                "Voici une proposition claire et lisible pour ta session.",
            ],
            "vert",
        )
    )

    print()
    print(construire_bloc("SEANCE SPORT", [programme["seance"]], "cyan"))

    print()
    print(construire_bloc("REPAS CONSEILLE", [programme["repas"]], "magenta"))

    print()
    print(construire_bloc("CONSEIL SANTE", [programme["conseil"]], "jaune"))


def demander_rejouer() -> bool:
    print()
    print(construire_bloc("NOUVELLE GENERATION", ["1. Oui, relancer un programme", "2. Non, quitter"], "bleu"))

    while True:
        reponse = input("\nTon choix : ").strip()
        if reponse == "1":
            return True
        if reponse == "2":
            return False

        print(colorer("Choix invalide. Merci de saisir 1 ou 2.", "jaune"))


def afficher_pied_page() -> None:
    print()
    print(
        construire_bloc(
            "A BIENTOT",
            [
                "Merci d'avoir utilise le coach sport et nutrition.",
                "Reviens quand tu veux pour un nouveau programme.",
            ],
            "magenta",
        )
    )


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
