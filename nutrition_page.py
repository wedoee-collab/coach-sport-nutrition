# ============================================================
#  Page Nutrition — Coach Sport & Nutrition
#  Saisie d'un aliment + quantité → macronutriments & micronutriments
# ============================================================

from nutrition_service import parse_input, get_nutrition, lister_aliments

# ---------- AFFICHAGE ----------

def afficher_nutrition(resultat):
    """Affiche les valeurs nutritionnelles dans le style de l'application."""
    print("\n" + "=" * 50)
    print("       VALEURS NUTRITIONNELLES")
    print("=" * 50)

    print(f"\nAliment  : {resultat['aliment'].replace('_', ' ').capitalize()}")
    print(f"Quantité : {resultat['quantite']} g")

    print("\n--- MACRONUTRIMENTS ---")
    m = resultat["macros"]
    print(f"  Protéines : {m['proteines']} g")
    print(f"  Glucides  : {m['glucides']} g")
    print(f"  Lipides   : {m['lipides']} g")
    print(f"  Calories  : {m['calories']} kcal")

    print("\n--- MICRONUTRIMENTS ---")
    mu = resultat["micros"]
    print(f"  Zinc       : {mu['zinc']} mg")
    print(f"  Fer        : {mu['fer']} mg")
    print(f"  Magnésium  : {mu['magnesium']} mg")
    print(f"  Vitamine C : {mu['vitamine_c']} mg")
    print(f"  Vitamine D : {mu['vitamine_d']} µg")
    print(f"  Calcium    : {mu['calcium']} mg")
    print(f"  Potassium  : {mu['potassium']} mg")

    print("\n" + "=" * 50)


def afficher_aliments_disponibles():
    """Affiche la liste des aliments reconnus par le service."""
    aliments = lister_aliments()
    print("\nAliments disponibles :")
    for nom in aliments:
        print(f"  - {nom}")


def demander_saisie():
    """Demande la saisie de l'utilisateur et retourne le texte brut."""
    print("\nExemples de saisie :")
    print("  150g poulet")
    print("  200g saumon")
    print("  100g brocoli")
    print("  50g amandes")
    return input("\nTon aliment et sa quantité : ").strip()


def demander_rejouer():
    """Demande si l'utilisateur veut analyser un autre aliment."""
    reponse = input("\nVeux-tu analyser un autre aliment ? (oui / non) : ").strip().lower()
    return reponse in ["oui", "o", "yes", "y"]


# ---------- PROGRAMME PRINCIPAL ----------

def main():
    print("=" * 50)
    print("   ANALYSE NUTRITIONNELLE — Coach Sport & Nutrition")
    print("=" * 50)

    afficher_aliments_disponibles()

    continuer = True

    while continuer:
        texte = demander_saisie()

        if not texte:
            print("Saisie vide. Merci d'entrer un aliment et une quantité.")
            continue

        quantite, cle = parse_input(texte)

        if cle is None:
            print("\nAliment non reconnu. Vérifie l'orthographe ou consulte la liste ci-dessus.")
        else:
            resultat = get_nutrition(cle, quantite)
            afficher_nutrition(resultat)

        continuer = demander_rejouer()

    print("\nBonne nutrition ! À bientôt.")


# Lancement de la page
if __name__ == "__main__":
    main()
