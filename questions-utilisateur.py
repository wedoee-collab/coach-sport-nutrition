def choisir_objectif():
    """Demande l'objectif avec une boucle de validation."""
    while True:
        print("\n🎯 Quel est ton objectif ?")
        print("  1. Perdre du poids")
        print("  2. Prendre du muscle")
        print("  3. Rester en forme")

        choix = input("\nTon choix (1, 2 ou 3) : ").strip()

        if choix == "1":
            return "perdre du poids"
        elif choix == "2":
            return "prendre du muscle"
        elif choix == "3":
            return "rester en forme"
        else:
            print("⚠️ Erreur : Peux-tu choisir entre 1, 2 ou 3 ?")

def choisir_niveau():
    """Demande le niveau avec une boucle de validation."""
    while True:
        print("\n⚡ Quel est ton niveau sportif ?")
        print("  1. Débutant")
        print("  2. Moyen")
        print("  3. Avancé")

        choix = input("\nTon choix (1, 2 ou 3) : ").strip()

        if choix == "1":
            return "debutant"
        elif choix == "2":
            return "moyen"
        elif choix == "3":
            return "avance"
        else:
            print("⚠️ Erreur : Merci de saisir 1, 2 ou 3 pour valider ton niveau.")

def demander_rejouer():
    """Vérifie si l'utilisateur veut continuer proprement."""
    reponse = input("\n🔄 Veux-tu un nouveau programme ? (oui / non) : ").strip().lower()
    # On accepte plusieurs variantes de "oui"
    return reponse in ["oui", "o", "yes", "y", "ok"]