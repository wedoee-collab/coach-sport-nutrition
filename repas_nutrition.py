# ============================================================
#  Module : Repas et nutrition
#  Auteur : Cheikh
#  Branche : feature/nutrition-page
# ============================================================

import random

# ---------- DONNÉES ----------

# Repas organisés par objectif
REPAS = {
    "prise de masse": [
        {
            "nom": "Riz complet + blanc de poulet + brocolis + fromage blanc",
            "calories": "650 kcal",
            "proteines": "55g de protéines"
        },
        {
            "nom": "Pâtes complètes + thon + tomates + huile d'olive",
            "calories": "600 kcal",
            "proteines": "45g de protéines"
        },
        {
            "nom": "Steak haché 5% + patate douce + épinards + yaourt protéiné",
            "calories": "700 kcal",
            "proteines": "60g de protéines"
        },
        {
            "nom": "Omelette 4 œufs + avocat + pain complet + fromage blanc",
            "calories": "620 kcal",
            "proteines": "40g de protéines"
        },
        {
            "nom": "Saumon + quinoa + haricots verts + huile d'olive",
            "calories": "680 kcal",
            "proteines": "50g de protéines"
        },
    ],

    "seche": [
        {
            "nom": "Salade de poulet grillé + légumes verts + vinaigrette citron",
            "calories": "350 kcal",
            "proteines": "40g de protéines"
        },
        {
            "nom": "Soupe de légumes maison + œuf dur + fruit frais",
            "calories": "280 kcal",
            "proteines": "20g de protéines"
        },
        {
            "nom": "Saumon vapeur + haricots verts + quinoa (petite portion)",
            "calories": "380 kcal",
            "proteines": "35g de protéines"
        },
        {
            "nom": "Blanc de poulet + courgettes sautées + riz basmati (80g)",
            "calories": "320 kcal",
            "proteines": "38g de protéines"
        },
        {
            "nom": "Thon en boîte + salade verte + tomates + concombre + citron",
            "calories": "250 kcal",
            "proteines": "30g de protéines"
        },
    ],

    "maintien": [
        {
            "nom": "Bowl : riz, avocat, légumes rôtis, œuf mollet",
            "calories": "500 kcal",
            "proteines": "25g de protéines"
        },
        {
            "nom": "Wrap complet : jambon, crudités, houmous",
            "calories": "450 kcal",
            "proteines": "22g de protéines"
        },
        {
            "nom": "Omelette aux légumes + pain complet + salade verte",
            "calories": "420 kcal",
            "proteines": "28g de protéines"
        },
        {
            "nom": "Poulet rôti + légumes du four + pomme de terre",
            "calories": "480 kcal",
            "proteines": "35g de protéines"
        },
        {
            "nom": "Soupe de lentilles + pain complet + yaourt nature",
            "calories": "430 kcal",
            "proteines": "24g de protéines"
        },
    ],
}

# Conseils nutrition par objectif
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


# ---------- FONCTIONS ----------

def afficher_repas(objectif):
    """Affiche un repas aléatoire adapté à l'objectif."""

    repas = random.choice(REPAS[objectif])

    print("\n--- REPAS CONSEILLÉ ---")
    print(f"  {repas['nom']}")
    print(f"  Apport : {repas['calories']} | {repas['proteines']}")


def afficher_conseil_nutrition(objectif):
    """Affiche un conseil nutrition adapté à l'objectif."""

    conseil = random.choice(CONSEILS_NUTRITION[objectif])

    print("\n--- CONSEIL NUTRITION ---")
    print(f"  {conseil}")


# ---------- TEST RAPIDE ----------

if __name__ == "__main__":
    for objectif in ["prise de masse", "seche", "maintien"]:
        print(f"\n=== Test objectif : {objectif} ===")
        afficher_repas(objectif)
        afficher_conseil_nutrition(objectif)
