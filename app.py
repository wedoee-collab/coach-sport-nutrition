# ============================================================
#  Coach Sport & Nutrition — Interface Tkinter + SQLite
#  Auteurs : Nicolas, Jordy, Ivann, Cheikh
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
from datetime import datetime

# ==================== BASE DE DONNÉES ====================

def init_db():
    """Crée la base de données et la table historique si elle n'existe pas."""
    conn = sqlite3.connect("coach_sport.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            objectif    TEXT NOT NULL,
            niveau      TEXT NOT NULL,
            seance      TEXT NOT NULL,
            duree       TEXT NOT NULL,
            repas       TEXT NOT NULL,
            calories    TEXT NOT NULL,
            proteines   TEXT NOT NULL,
            conseil     TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def sauvegarder_programme(objectif, niveau, seance, duree, repas, calories, proteines, conseil):
    """Sauvegarde un programme généré dans l'historique."""
    conn = sqlite3.connect("coach_sport.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historique (date, objectif, niveau, seance, duree, repas, calories, proteines, conseil)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        objectif, niveau, seance, duree, repas, calories, proteines, conseil
    ))
    conn.commit()
    conn.close()

def charger_historique():
    """Charge tous les programmes depuis la base de données."""
    conn = sqlite3.connect("coach_sport.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, objectif, niveau, duree, repas, calories FROM historique ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def supprimer_historique():
    """Supprime tout l'historique."""
    conn = sqlite3.connect("coach_sport.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM historique")
    conn.commit()
    conn.close()

# ==================== DONNÉES ====================

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

REPAS = {
    "prise de masse": [
        {"nom": "Riz complet + blanc de poulet + brocolis + fromage blanc", "calories": "650 kcal", "proteines": "55g protéines"},
        {"nom": "Pâtes complètes + thon + tomates + huile d'olive", "calories": "600 kcal", "proteines": "45g protéines"},
        {"nom": "Steak haché 5% + patate douce + épinards + yaourt protéiné", "calories": "700 kcal", "proteines": "60g protéines"},
        {"nom": "Omelette 4 œufs + avocat + pain complet + fromage blanc", "calories": "620 kcal", "proteines": "40g protéines"},
        {"nom": "Saumon + quinoa + haricots verts + huile d'olive", "calories": "680 kcal", "proteines": "50g protéines"},
    ],
    "seche": [
        {"nom": "Salade de poulet grillé + légumes verts + vinaigrette citron", "calories": "350 kcal", "proteines": "40g protéines"},
        {"nom": "Soupe de légumes maison + œuf dur + fruit frais", "calories": "280 kcal", "proteines": "20g protéines"},
        {"nom": "Saumon vapeur + haricots verts + quinoa (petite portion)", "calories": "380 kcal", "proteines": "35g protéines"},
        {"nom": "Blanc de poulet + courgettes sautées + riz basmati (80g)", "calories": "320 kcal", "proteines": "38g protéines"},
        {"nom": "Thon en boîte + salade verte + tomates + concombre + citron", "calories": "250 kcal", "proteines": "30g protéines"},
    ],
    "maintien": [
        {"nom": "Bowl : riz, avocat, légumes rôtis, œuf mollet", "calories": "500 kcal", "proteines": "25g protéines"},
        {"nom": "Wrap complet : jambon, crudités, houmous", "calories": "450 kcal", "proteines": "22g protéines"},
        {"nom": "Omelette aux légumes + pain complet + salade verte", "calories": "420 kcal", "proteines": "28g protéines"},
        {"nom": "Poulet rôti + légumes du four + pomme de terre", "calories": "480 kcal", "proteines": "35g protéines"},
        {"nom": "Soupe de lentilles + pain complet + yaourt nature", "calories": "430 kcal", "proteines": "24g protéines"},
    ],
}

CONSEILS = {
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

LABELS_OBJECTIF = {"prise de masse": "Prise de masse", "seche": "Sèche", "maintien": "Maintien"}
LABELS_NIVEAU   = {"debutant": "Débutant", "intermediaire": "Intermédiaire", "confirme": "Confirmé"}

# ==================== INTERFACE ====================

class CoachApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Coach Sport & Nutrition")
        self.geometry("800x650")
        self.resizable(False, False)
        self.configure(bg="#0f1117")

        # Variables
        self.objectif_var = tk.StringVar(value="")
        self.niveau_var   = tk.StringVar(value="")

        self._build_ui()
        init_db()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#0f1117")
        header.pack(fill="x", pady=(20, 0))
        tk.Label(header, text="COACH SPORT & NUTRITION",
                 font=("Courier", 22, "bold"), fg="#00ff88", bg="#0f1117").pack()
        tk.Label(header, text="Ton programme personnalisé",
                 font=("Courier", 11), fg="#555e6e", bg="#0f1117").pack()

        # Séparateur
        tk.Frame(self, bg="#00ff88", height=2).pack(fill="x", padx=30, pady=12)

        # Onglets
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#0f1117", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1a1d26", foreground="#888",
                        font=("Courier", 10, "bold"), padding=[20, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", "#0f1117")],
                  foreground=[("selected", "#00ff88")])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=0)

        self.tab_programme = tk.Frame(self.notebook, bg="#0f1117")
        self.tab_historique = tk.Frame(self.notebook, bg="#0f1117")

        self.notebook.add(self.tab_programme, text="  Programme  ")
        self.notebook.add(self.tab_historique, text="  Historique  ")

        self._build_tab_programme()
        self._build_tab_historique()

    def _build_tab_programme(self):
        tab = self.tab_programme

        # Objectif
        tk.Label(tab, text="OBJECTIF", font=("Courier", 10, "bold"),
                 fg="#00ff88", bg="#0f1117").pack(anchor="w", padx=30, pady=(20, 6))

        obj_frame = tk.Frame(tab, bg="#0f1117")
        obj_frame.pack(fill="x", padx=30)
        for label, val in [("Prise de masse", "prise de masse"), ("Sèche", "seche"), ("Maintien", "maintien")]:
            tk.Radiobutton(obj_frame, text=label, variable=self.objectif_var, value=val,
                           font=("Courier", 11), fg="#cccccc", bg="#0f1117",
                           selectcolor="#1a1d26", activebackground="#0f1117",
                           activeforeground="#00ff88").pack(side="left", padx=15)

        # Niveau
        tk.Label(tab, text="NIVEAU", font=("Courier", 10, "bold"),
                 fg="#00ff88", bg="#0f1117").pack(anchor="w", padx=30, pady=(16, 6))

        niv_frame = tk.Frame(tab, bg="#0f1117")
        niv_frame.pack(fill="x", padx=30)
        for label, val in [("Débutant", "debutant"), ("Intermédiaire", "intermediaire"), ("Confirmé", "confirme")]:
            tk.Radiobutton(niv_frame, text=label, variable=self.niveau_var, value=val,
                           font=("Courier", 11), fg="#cccccc", bg="#0f1117",
                           selectcolor="#1a1d26", activebackground="#0f1117",
                           activeforeground="#00ff88").pack(side="left", padx=15)

        # Bouton générer
        btn = tk.Button(tab, text="⚡  GÉNÉRER MON PROGRAMME",
                        font=("Courier", 12, "bold"), fg="#0f1117", bg="#00ff88",
                        activebackground="#00cc66", activeforeground="#0f1117",
                        relief="flat", cursor="hand2", pady=10,
                        command=self._generer)
        btn.pack(fill="x", padx=30, pady=16)

        # Zone résultats
        tk.Frame(tab, bg="#1a1d26", height=1).pack(fill="x", padx=30)

        self.result_frame = tk.Frame(tab, bg="#0f1117")
        self.result_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self.lbl_placeholder = tk.Label(self.result_frame,
                                        text="Sélectionne un objectif et un niveau,\npuis génère ton programme.",
                                        font=("Courier", 11), fg="#444", bg="#0f1117", justify="center")
        self.lbl_placeholder.pack(expand=True)

    def _build_tab_historique(self):
        tab = self.tab_historique

        tk.Label(tab, text="HISTORIQUE DES PROGRAMMES",
                 font=("Courier", 10, "bold"), fg="#00ff88", bg="#0f1117").pack(anchor="w", padx=30, pady=(20, 10))

        # Tableau
        cols = ("Date", "Objectif", "Niveau", "Durée", "Repas", "Calories")
        self.tree = ttk.Treeview(tab, columns=cols, show="headings", height=12)

        style = ttk.Style()
        style.configure("Treeview", background="#1a1d26", foreground="#cccccc",
                        fieldbackground="#1a1d26", font=("Courier", 9), rowheight=28)
        style.configure("Treeview.Heading", background="#0f1117", foreground="#00ff88",
                        font=("Courier", 9, "bold"))
        style.map("Treeview", background=[("selected", "#00ff8833")])

        largeurs = [120, 120, 110, 70, 220, 90]
        for col, larg in zip(cols, largeurs):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larg, anchor="w")

        scroll = ttk.Scrollbar(tab, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=(0, 10))
        scroll.pack(side="left", fill="y", pady=(0, 10))

        tk.Button(tab, text="🗑  Effacer l'historique",
                  font=("Courier", 10), fg="#ff4444", bg="#1a1d26",
                  relief="flat", cursor="hand2", pady=6,
                  command=self._effacer_historique).pack(pady=(0, 15))

    def _generer(self):
        objectif = self.objectif_var.get()
        niveau   = self.niveau_var.get()

        if not objectif or not niveau:
            messagebox.showwarning("Sélection manquante", "Choisis un objectif ET un niveau avant de générer.")
            return

        seance_data = random.choice(SEANCES[objectif][niveau])
        repas_data  = random.choice(REPAS[objectif])
        conseil     = random.choice(CONSEILS[objectif])

        # Sauvegarder en BDD
        sauvegarder_programme(
            LABELS_OBJECTIF[objectif], LABELS_NIVEAU[niveau],
            seance_data["seance"], seance_data["duree"],
            repas_data["nom"], repas_data["calories"], repas_data["proteines"],
            conseil
        )

        # Afficher les résultats
        for w in self.result_frame.winfo_children():
            w.destroy()

        def bloc(titre, lignes, couleur="#00ff88"):
            f = tk.Frame(self.result_frame, bg="#1a1d26", pady=10, padx=14)
            f.pack(fill="x", pady=4)
            tk.Label(f, text=titre, font=("Courier", 9, "bold"),
                     fg=couleur, bg="#1a1d26").pack(anchor="w")
            for l in lignes:
                tk.Label(f, text=l, font=("Courier", 10), fg="#cccccc",
                         bg="#1a1d26", wraplength=680, justify="left").pack(anchor="w", pady=1)

        bloc("🏋  SÉANCE DE SPORT",
             [f"Durée : {seance_data['duree']}", seance_data["seance"]], "#00ff88")
        bloc("🍽  REPAS CONSEILLÉ",
             [repas_data["nom"], f"{repas_data['calories']}  •  {repas_data['proteines']}"], "#ff9f43")
        bloc("💡  CONSEIL NUTRITION", [conseil], "#54a0ff")

        # Rafraîchir historique
        self._charger_historique()

    def _charger_historique(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in charger_historique():
            self.tree.insert("", "end", values=row)

    def _effacer_historique(self):
        if messagebox.askyesno("Confirmation", "Supprimer tout l'historique ?"):
            supprimer_historique()
            self._charger_historique()

    def run(self):
        self._charger_historique()
        self.mainloop()

# ==================== LANCEMENT ====================

if __name__ == "__main__":
    app = CoachApp()
    app.run()
