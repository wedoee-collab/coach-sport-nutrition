# ============================================================
#  Nutrition Service — Module isolé
#  Fournit : parsing de l'entrée utilisateur + données nutritionnelles
# ============================================================

# ---------- BASE DE DONNÉES NUTRITIONNELLE (pour 100 g / 100 ml) ----------
# Chaque entrée contient :
#   macros  : proteines (g), glucides (g), lipides (g), calories (kcal)
#   micros  : zinc (mg), fer (mg), magnesium (mg),
#             vitamine_c (mg), vitamine_d (µg), calcium (mg), potassium (mg)

ALIMENTS = {
    "poulet": {
        "noms": ["poulet", "blanc de poulet", "blanc poulet", "chicken"],
        "macros": {
            "proteines": 31.0,
            "glucides":  0.0,
            "lipides":   3.6,
            "calories":  165,
        },
        "micros": {
            "zinc":       1.0,
            "fer":        1.0,
            "magnesium":  29,
            "vitamine_c": 0.0,
            "vitamine_d": 0.1,
            "calcium":    15,
            "potassium":  256,
        },
    },
    "saumon": {
        "noms": ["saumon", "salmon"],
        "macros": {
            "proteines": 20.0,
            "glucides":  0.0,
            "lipides":   13.0,
            "calories":  208,
        },
        "micros": {
            "zinc":       0.6,
            "fer":        0.8,
            "magnesium":  29,
            "vitamine_c": 3.9,
            "vitamine_d": 16.0,
            "calcium":    12,
            "potassium":  490,
        },
    },
    "thon": {
        "noms": ["thon", "tuna"],
        "macros": {
            "proteines": 28.0,
            "glucides":  0.0,
            "lipides":   1.0,
            "calories":  116,
        },
        "micros": {
            "zinc":       0.6,
            "fer":        1.0,
            "magnesium":  35,
            "vitamine_c": 0.0,
            "vitamine_d": 6.7,
            "calcium":    10,
            "potassium":  444,
        },
    },
    "oeuf": {
        "noms": ["oeuf", "oeufs", "egg", "eggs"],
        "macros": {
            "proteines": 13.0,
            "glucides":  1.1,
            "lipides":   11.0,
            "calories":  155,
        },
        "micros": {
            "zinc":       1.3,
            "fer":        1.8,
            "magnesium":  12,
            "vitamine_c": 0.0,
            "vitamine_d": 2.0,
            "calcium":    56,
            "potassium":  138,
        },
    },
    "boeuf": {
        "noms": ["boeuf", "steak", "viande", "beef"],
        "macros": {
            "proteines": 26.0,
            "glucides":  0.0,
            "lipides":   15.0,
            "calories":  250,
        },
        "micros": {
            "zinc":       6.3,
            "fer":        2.6,
            "magnesium":  21,
            "vitamine_c": 0.0,
            "vitamine_d": 0.1,
            "calcium":    18,
            "potassium":  318,
        },
    },
    "riz": {
        "noms": ["riz", "riz complet", "rice"],
        "macros": {
            "proteines": 2.7,
            "glucides":  28.0,
            "lipides":   0.3,
            "calories":  130,
        },
        "micros": {
            "zinc":       0.6,
            "fer":        0.2,
            "magnesium":  12,
            "vitamine_c": 0.0,
            "vitamine_d": 0.0,
            "calcium":    10,
            "potassium":  35,
        },
    },
    "pates": {
        "noms": ["pates", "pâtes", "pasta", "spaghetti"],
        "macros": {
            "proteines": 5.0,
            "glucides":  31.0,
            "lipides":   0.9,
            "calories":  157,
        },
        "micros": {
            "zinc":       0.5,
            "fer":        0.9,
            "magnesium":  18,
            "vitamine_c": 0.0,
            "vitamine_d": 0.0,
            "calcium":    7,
            "potassium":  44,
        },
    },
    "patate_douce": {
        "noms": ["patate douce", "patate_douce", "sweet potato"],
        "macros": {
            "proteines": 1.6,
            "glucides":  20.0,
            "lipides":   0.1,
            "calories":  86,
        },
        "micros": {
            "zinc":       0.3,
            "fer":        0.6,
            "magnesium":  25,
            "vitamine_c": 2.4,
            "vitamine_d": 0.0,
            "calcium":    30,
            "potassium":  337,
        },
    },
    "brocoli": {
        "noms": ["brocoli", "broccoli", "brocolis"],
        "macros": {
            "proteines": 2.8,
            "glucides":  7.0,
            "lipides":   0.4,
            "calories":  34,
        },
        "micros": {
            "zinc":       0.4,
            "fer":        0.7,
            "magnesium":  21,
            "vitamine_c": 89.2,
            "vitamine_d": 0.0,
            "calcium":    47,
            "potassium":  316,
        },
    },
    "avoine": {
        "noms": ["avoine", "flocons d'avoine", "flocons avoine", "oats"],
        "macros": {
            "proteines": 17.0,
            "glucides":  66.0,
            "lipides":   7.0,
            "calories":  389,
        },
        "micros": {
            "zinc":       3.9,
            "fer":        4.7,
            "magnesium":  177,
            "vitamine_c": 0.0,
            "vitamine_d": 0.0,
            "calcium":    54,
            "potassium":  429,
        },
    },
    "amandes": {
        "noms": ["amandes", "amande", "almonds"],
        "macros": {
            "proteines": 21.0,
            "glucides":  22.0,
            "lipides":   50.0,
            "calories":  579,
        },
        "micros": {
            "zinc":       3.1,
            "fer":        3.7,
            "magnesium":  270,
            "vitamine_c": 0.0,
            "vitamine_d": 0.0,
            "calcium":    264,
            "potassium":  733,
        },
    },
    "quinoa": {
        "noms": ["quinoa"],
        "macros": {
            "proteines": 4.4,
            "glucides":  21.0,
            "lipides":   1.9,
            "calories":  120,
        },
        "micros": {
            "zinc":       1.1,
            "fer":        1.5,
            "magnesium":  64,
            "vitamine_c": 0.0,
            "vitamine_d": 0.0,
            "calcium":    17,
            "potassium":  172,
        },
    },
    "epinards": {
        "noms": ["epinards", "épinards", "spinach"],
        "macros": {
            "proteines": 2.9,
            "glucides":  3.6,
            "lipides":   0.4,
            "calories":  23,
        },
        "micros": {
            "zinc":       0.5,
            "fer":        2.7,
            "magnesium":  79,
            "vitamine_c": 28.1,
            "vitamine_d": 0.0,
            "calcium":    99,
            "potassium":  558,
        },
    },
}

# ---------- FONCTIONS DU SERVICE ----------

def _chercher_aliment(texte):
    """Recherche un aliment dans la base par correspondance de mots-clés.
    Retourne la clé interne de l'aliment ou None si non trouvé."""
    texte = texte.lower().strip()
    for cle, donnees in ALIMENTS.items():
        for nom in donnees["noms"]:
            if nom in texte:
                return cle
    return None


def parse_input(texte):
    """Analyse une saisie du type '150g poulet' ou 'poulet 200g'.
    Retourne un tuple (quantite_g: float, cle_aliment: str) ou (None, None)."""
    import re

    # Extraction de la quantité (ex. 150g, 200 g)
    match_quantite = re.search(r"(\d+(?:[.,]\d+)?)\s*g\b", texte, re.IGNORECASE)
    quantite = float(match_quantite.group(1).replace(",", ".")) if match_quantite else 100.0

    cle = _chercher_aliment(texte)
    return quantite, cle


def get_nutrition(cle_aliment, quantite_g):
    """Calcule les valeurs nutritionnelles pour une quantité donnée.
    Retourne un dict avec 'aliment', 'quantite', 'macros', 'micros'
    ou None si l'aliment est inconnu."""
    if cle_aliment is None or cle_aliment not in ALIMENTS:
        return None

    donnees = ALIMENTS[cle_aliment]
    ratio = quantite_g / 100.0

    macros = {k: round(v * ratio, 1) for k, v in donnees["macros"].items()}
    micros = {k: round(v * ratio, 2) for k, v in donnees["micros"].items()}

    return {
        "aliment":  cle_aliment,
        "quantite": quantite_g,
        "macros":   macros,
        "micros":   micros,
    }


def lister_aliments():
    """Retourne la liste des noms affichables de tous les aliments disponibles."""
    return [donnees["noms"][0] for donnees in ALIMENTS.values()]
