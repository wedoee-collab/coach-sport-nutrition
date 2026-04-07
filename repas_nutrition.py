import random


REPAS = {
    "prise de masse": [
        {
            "nom": "Riz complet + blanc de poulet + brocolis + fromage blanc",
            "calories": "650 kcal",
            "proteines": "55g de proteines",
        },
        {
            "nom": "Pates completes + thon + tomates + huile d'olive",
            "calories": "600 kcal",
            "proteines": "45g de proteines",
        },
        {
            "nom": "Steak hache 5% + patate douce + epinards + yaourt proteine",
            "calories": "700 kcal",
            "proteines": "60g de proteines",
        },
        {
            "nom": "Omelette 4 oeufs + avocat + pain complet + fromage blanc",
            "calories": "620 kcal",
            "proteines": "40g de proteines",
        },
        {
            "nom": "Saumon + quinoa + haricots verts + huile d'olive",
            "calories": "680 kcal",
            "proteines": "50g de proteines",
        },
    ],
    "seche": [
        {
            "nom": "Salade de poulet grille + legumes verts + vinaigrette citron",
            "calories": "350 kcal",
            "proteines": "40g de proteines",
        },
        {
            "nom": "Soupe de legumes maison + oeuf dur + fruit frais",
            "calories": "280 kcal",
            "proteines": "20g de proteines",
        },
        {
            "nom": "Saumon vapeur + haricots verts + quinoa (petite portion)",
            "calories": "380 kcal",
            "proteines": "35g de proteines",
        },
        {
            "nom": "Blanc de poulet + courgettes sautees + riz basmati (80g)",
            "calories": "320 kcal",
            "proteines": "38g de proteines",
        },
        {
            "nom": "Thon en boite + salade verte + tomates + concombre + citron",
            "calories": "250 kcal",
            "proteines": "30g de proteines",
        },
    ],
    "maintien": [
        {
            "nom": "Bowl : riz, avocat, legumes rotis, oeuf mollet",
            "calories": "500 kcal",
            "proteines": "25g de proteines",
        },
        {
            "nom": "Wrap complet : jambon, crudites, houmous",
            "calories": "450 kcal",
            "proteines": "22g de proteines",
        },
        {
            "nom": "Omelette aux legumes + pain complet + salade verte",
            "calories": "420 kcal",
            "proteines": "28g de proteines",
        },
        {
            "nom": "Poulet roti + legumes du four + pomme de terre",
            "calories": "480 kcal",
            "proteines": "35g de proteines",
        },
        {
            "nom": "Soupe de lentilles + pain complet + yaourt nature",
            "calories": "430 kcal",
            "proteines": "24g de proteines",
        },
    ],
}


CONSEILS_NUTRITION = {
    "prise de masse": [
        "Mange toutes les 3h pour maintenir un apport proteine constant.",
        "Prends un shaker proteine dans les 30 min apres ta seance.",
        "Privilegie les glucides complexes : riz, pates, patate douce.",
        "Dors 8h minimum : c'est pendant le sommeil que le muscle se construit.",
    ],
    "seche": [
        "Bois 2L d'eau par jour minimum pour eliminer les toxines.",
        "Evite les sucres rapides et les aliments ultra-transformes.",
        "Mange des legumes a volonte : peu caloriques et rassasiants.",
        "Ne saute pas de repas : ca ralentit le metabolisme.",
    ],
    "maintien": [
        "Mange equilibre : 1/2 legumes, 1/4 proteines, 1/4 glucides.",
        "Bois au moins 1,5L d'eau par jour.",
        "Fais 3 repas par jour a heures regulieres.",
        "Autorise-toi un repas plaisir par semaine, sans culpabiliser.",
    ],
}


def choisir_repas(objectif: str) -> dict[str, str]:
    return random.choice(REPAS[objectif])


def choisir_conseil_nutrition(objectif: str) -> str:
    return random.choice(CONSEILS_NUTRITION[objectif])
