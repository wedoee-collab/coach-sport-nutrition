from __future__ import annotations

import ast
import re
import unicodedata
from pathlib import Path

import coach_sport_nutrition as coach
import seances_sport as sport


ROOT_DIR = Path(__file__).resolve().parent
QUESTIONNAIRE_PATH = ROOT_DIR / "questions-utilisateur.py"


def normaliser_texte(valeur: str) -> str:
    texte = unicodedata.normalize("NFKD", valeur)
    texte = texte.encode("ascii", "ignore").decode("ascii")
    return " ".join(texte.lower().split())


def formater_minutes(total_minutes: int) -> str:
    heures, minutes = divmod(total_minutes, 60)
    if heures and minutes:
        return f"{heures}h{minutes:02d}"
    if heures:
        return f"{heures}h"
    return f"{minutes} min"


def convertir_duree_en_minutes(duree: str) -> int:
    texte = duree.strip().lower().replace(" ", "")
    if texte.endswith("min"):
        return int(texte[:-3])

    match = re.fullmatch(r"(?P<heures>\d+)h(?P<minutes>\d{0,2})", texte)
    if not match:
        raise ValueError(f"Format de duree non gere: {duree}")

    heures = int(match.group("heures"))
    minutes = int(match.group("minutes") or 0)
    return heures * 60 + minutes


def charger_questionnaire() -> ast.Module:
    source = QUESTIONNAIRE_PATH.read_text(encoding="utf-8")
    return ast.parse(source, filename=str(QUESTIONNAIRE_PATH))


def extraire_retours_litteraux(nom_fonction: str) -> list[str]:
    arbre = charger_questionnaire()

    for noeud in arbre.body:
        if isinstance(noeud, ast.FunctionDef) and noeud.name == nom_fonction:
            valeurs: list[str] = []
            deja_vus: set[str] = set()

            for sous_noeud in ast.walk(noeud):
                if not isinstance(sous_noeud, ast.Return):
                    continue
                if not isinstance(sous_noeud.value, ast.Constant):
                    continue
                if not isinstance(sous_noeud.value.value, str):
                    continue

                valeur = sous_noeud.value.value
                cle = normaliser_texte(valeur)
                if cle not in deja_vus:
                    deja_vus.add(cle)
                    valeurs.append(valeur)

            return valeurs

    raise ValueError(f"Fonction introuvable dans le questionnaire: {nom_fonction}")


def calculer_statistiques_questionnaire() -> dict[str, object]:
    objectifs = extraire_retours_litteraux("choisir_objectif")
    niveaux = extraire_retours_litteraux("choisir_niveau")

    return {
        "objectifs": objectifs,
        "niveaux": niveaux,
        "nb_objectifs": len(objectifs),
        "nb_niveaux": len(niveaux),
        "nb_profils": len(objectifs) * len(niveaux),
    }


def calculer_statistiques_programme_principal() -> dict[str, object]:
    objectifs = list(coach.REPAS.keys())
    niveaux = list(coach.SEANCES.keys())

    nb_seances = sum(len(seances) for seances in coach.SEANCES.values())
    nb_repas = sum(len(repas) for repas in coach.REPAS.values())
    nb_conseils = len(coach.CONSEILS)
    nb_combinaisons = sum(
        len(seances) * len(repas) * nb_conseils
        for seances in coach.SEANCES.values()
        for repas in coach.REPAS.values()
    )

    return {
        "objectifs": objectifs,
        "niveaux": niveaux,
        "nb_seances": nb_seances,
        "nb_repas": nb_repas,
        "nb_conseils": nb_conseils,
        "nb_combinaisons": nb_combinaisons,
    }


def calculer_statistiques_seances_sport() -> dict[str, object]:
    lignes: list[dict[str, object]] = []

    for objectif, niveaux in sport.SEANCES.items():
        for niveau, seances in niveaux.items():
            for seance in seances:
                lignes.append(
                    {
                        "objectif": objectif,
                        "niveau": niveau,
                        "duree_minutes": convertir_duree_en_minutes(seance["duree"]),
                    }
                )

    par_objectif: dict[str, dict[str, int]] = {}
    par_niveau: dict[str, dict[str, int]] = {}

    for ligne in lignes:
        objectif = str(ligne["objectif"])
        niveau = str(ligne["niveau"])
        duree_minutes = int(ligne["duree_minutes"])

        par_objectif.setdefault(objectif, {"nb_seances": 0, "total_minutes": 0})
        par_objectif[objectif]["nb_seances"] += 1
        par_objectif[objectif]["total_minutes"] += duree_minutes

        par_niveau.setdefault(niveau, {"nb_seances": 0, "total_minutes": 0})
        par_niveau[niveau]["nb_seances"] += 1
        par_niveau[niveau]["total_minutes"] += duree_minutes

    total_minutes = sum(int(ligne["duree_minutes"]) for ligne in lignes)
    moyenne_minutes = total_minutes // len(lignes)

    return {
        "nb_objectifs": len(sport.SEANCES),
        "nb_niveaux": len({niveau for niveaux in sport.SEANCES.values() for niveau in niveaux}),
        "nb_seances": len(lignes),
        "total_minutes": total_minutes,
        "moyenne_minutes": moyenne_minutes,
        "par_objectif": par_objectif,
        "par_niveau": par_niveau,
    }


def mesurer_recouvrement(source: list[str], cible: list[str]) -> dict[str, object]:
    source_normalise = {normaliser_texte(valeur) for valeur in source}
    cible_normalise = {normaliser_texte(valeur) for valeur in cible}
    communs = source_normalise & cible_normalise

    return {
        "nb_communs": len(communs),
        "nb_total_source": len(source_normalise),
        "elements_communs": sorted(communs),
    }


def calculer_statistiques_alignement(
    questionnaire: dict[str, object],
    programme: dict[str, object],
    sport_detaille: dict[str, object],
) -> dict[str, object]:
    questionnaire_objectifs = list(questionnaire["objectifs"])
    questionnaire_niveaux = list(questionnaire["niveaux"])
    programme_objectifs = list(programme["objectifs"])
    programme_niveaux = list(programme["niveaux"])
    sport_objectifs = list(sport.SEANCES.keys())
    sport_niveaux = list(next(iter(sport.SEANCES.values())).keys())

    objectifs_questionnaire_vers_sport = mesurer_recouvrement(
        questionnaire_objectifs, sport_objectifs
    )
    niveaux_questionnaire_vers_sport = mesurer_recouvrement(
        questionnaire_niveaux, sport_niveaux
    )
    niveaux_programme_vers_sport = mesurer_recouvrement(programme_niveaux, sport_niveaux)
    objectifs_programme_vers_sport = mesurer_recouvrement(
        programme_objectifs, sport_objectifs
    )

    profils_directs = (
        objectifs_questionnaire_vers_sport["nb_communs"]
        * niveaux_questionnaire_vers_sport["nb_communs"]
    )
    profils_questionnaire = (
        int(questionnaire["nb_objectifs"]) * int(questionnaire["nb_niveaux"])
    )

    return {
        "questionnaire_objectifs_vers_sport": objectifs_questionnaire_vers_sport,
        "questionnaire_niveaux_vers_sport": niveaux_questionnaire_vers_sport,
        "programme_objectifs_vers_sport": objectifs_programme_vers_sport,
        "programme_niveaux_vers_sport": niveaux_programme_vers_sport,
        "profils_directs_questionnaire_vers_sport": profils_directs,
        "profils_questionnaire": profils_questionnaire,
        "catalogue_global": (
            int(programme["nb_seances"])
            + int(programme["nb_repas"])
            + int(programme["nb_conseils"])
            + int(sport_detaille["nb_seances"])
        ),
    }


def afficher_statistiques() -> None:
    questionnaire = calculer_statistiques_questionnaire()
    programme = calculer_statistiques_programme_principal()
    sport_detaille = calculer_statistiques_seances_sport()
    alignement = calculer_statistiques_alignement(
        questionnaire=questionnaire,
        programme=programme,
        sport_detaille=sport_detaille,
    )

    print("=" * 60)
    print("STATISTIQUES DU PROJET COACH SPORT & NUTRITION")
    print("=" * 60)

    print("\n1. Questionnaire utilisateur")
    print(f"- {questionnaire['nb_objectifs']} objectifs proposes")
    print(f"- {questionnaire['nb_niveaux']} niveaux proposes")
    print(f"- {questionnaire['nb_profils']} profils utilisateur possibles")

    print("\n2. Programme principal")
    print(f"- {programme['nb_seances']} seances simples disponibles")
    print(f"- {programme['nb_repas']} idees de repas disponibles")
    print(f"- {programme['nb_conseils']} conseils sante disponibles")
    print(f"- {programme['nb_combinaisons']} combinaisons de programmes possibles")

    print("\n3. Module seances sport")
    print(f"- {sport_detaille['nb_seances']} seances detaillees")
    print(f"- {formater_minutes(int(sport_detaille['total_minutes']))} de contenu cumule")
    print(
        f"- Duree moyenne par seance : "
        f"{formater_minutes(int(sport_detaille['moyenne_minutes']))}"
    )

    print("\n- Repartition par objectif")
    for objectif, stats in sport_detaille["par_objectif"].items():
        print(
            f"  - {objectif} : {stats['nb_seances']} seances, "
            f"{formater_minutes(stats['total_minutes'])}"
        )

    print("\n- Repartition par niveau")
    for niveau, stats in sport_detaille["par_niveau"].items():
        moyenne_niveau = stats["total_minutes"] // stats["nb_seances"]
        print(
            f"  - {niveau} : {stats['nb_seances']} seances, "
            f"{formater_minutes(stats['total_minutes'])} au total, "
            f"moyenne {formater_minutes(moyenne_niveau)}"
        )

    print("\n4. Alignement entre modules")
    print(
        "- Objectifs questionnaire -> seances : "
        f"{alignement['questionnaire_objectifs_vers_sport']['nb_communs']}/"
        f"{alignement['questionnaire_objectifs_vers_sport']['nb_total_source']} "
        "identiques textuellement"
    )
    print(
        "- Niveaux questionnaire -> seances : "
        f"{alignement['questionnaire_niveaux_vers_sport']['nb_communs']}/"
        f"{alignement['questionnaire_niveaux_vers_sport']['nb_total_source']} "
        "identiques textuellement"
    )
    print(
        "- Objectifs programme principal -> seances : "
        f"{alignement['programme_objectifs_vers_sport']['nb_communs']}/"
        f"{alignement['programme_objectifs_vers_sport']['nb_total_source']} "
        "identiques textuellement"
    )
    print(
        "- Niveaux programme principal -> seances : "
        f"{alignement['programme_niveaux_vers_sport']['nb_communs']}/"
        f"{alignement['programme_niveaux_vers_sport']['nb_total_source']} "
        "identiques textuellement"
    )
    print(
        "- Profils questionnaire relies directement au module seances : "
        f"{alignement['profils_directs_questionnaire_vers_sport']}/"
        f"{alignement['profils_questionnaire']}"
    )

    print("\n5. Vue globale")
    print(
        f"- {alignement['catalogue_global']} elements de recommandation stockes "
        "dans le projet"
    )


if __name__ == "__main__":
    afficher_statistiques()
