# ============================================================
#  Coach Sport & Nutrition v2 — Interface Tkinter + SQLite
#  Auteurs : Nicolas, Jordy, Ivann, Cheikh
# ============================================================

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import csv
import os
from datetime import datetime

# ==================== BASE DE DONNÉES ====================

DB_PATH = "coach_sport.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS profil (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            prenom   TEXT NOT NULL,
            age      INTEGER,
            poids    REAL,
            imc      REAL,
            objectif TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            date      TEXT NOT NULL,
            objectif  TEXT NOT NULL,
            niveau    TEXT NOT NULL,
            seance    TEXT NOT NULL,
            duree     TEXT NOT NULL,
            repas     TEXT NOT NULL,
            calories  TEXT NOT NULL,
            proteines TEXT NOT NULL,
            conseil   TEXT NOT NULL,
            note      INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def sauvegarder_profil(prenom, age, poids, imc, objectif):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM profil")
    c.execute("INSERT INTO profil (prenom, age, poids, imc, objectif) VALUES (?,?,?,?,?)",
              (prenom, age, poids, round(imc, 1), objectif))
    conn.commit()
    conn.close()

def charger_profil():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT prenom, age, poids, imc, objectif FROM profil LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row

def sauvegarder_programme(objectif, niveau, seance, duree, repas, calories, proteines, conseil):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO historique (date, objectif, niveau, seance, duree, repas, calories, proteines, conseil)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (datetime.now().strftime("%d/%m/%Y %H:%M"), objectif, niveau, seance, duree, repas, calories, proteines, conseil))
    conn.commit()
    conn.close()

def mettre_a_jour_note(item_id, note):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE historique SET note=? WHERE id=?", (note, item_id))
    conn.commit()
    conn.close()

def charger_historique():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, date, objectif, niveau, duree, calories, note FROM historique ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def charger_calories_suivi():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT date, objectif, calories FROM historique ORDER BY id ASC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return rows

def supprimer_historique():
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM historique")
    conn.commit()
    conn.close()

def exporter_csv():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT date, objectif, niveau, duree, repas, calories, proteines, conseil, note FROM historique ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    path = "historique_coach.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Objectif", "Niveau", "Durée", "Repas", "Calories", "Protéines", "Conseil", "Note"])
        writer.writerows(rows)
    return os.path.abspath(path)

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
        {"nom": "Riz complet + blanc de poulet + brocolis + fromage blanc", "calories": "650", "proteines": "55g"},
        {"nom": "Pâtes complètes + thon + tomates + huile d'olive", "calories": "600", "proteines": "45g"},
        {"nom": "Steak haché 5% + patate douce + épinards + yaourt protéiné", "calories": "700", "proteines": "60g"},
        {"nom": "Omelette 4 œufs + avocat + pain complet + fromage blanc", "calories": "620", "proteines": "40g"},
        {"nom": "Saumon + quinoa + haricots verts + huile d'olive", "calories": "680", "proteines": "50g"},
    ],
    "seche": [
        {"nom": "Salade de poulet grillé + légumes verts + vinaigrette citron", "calories": "350", "proteines": "40g"},
        {"nom": "Soupe de légumes maison + œuf dur + fruit frais", "calories": "280", "proteines": "20g"},
        {"nom": "Saumon vapeur + haricots verts + quinoa (petite portion)", "calories": "380", "proteines": "35g"},
        {"nom": "Blanc de poulet + courgettes sautées + riz basmati (80g)", "calories": "320", "proteines": "38g"},
        {"nom": "Thon en boîte + salade verte + tomates + concombre + citron", "calories": "250", "proteines": "30g"},
    ],
    "maintien": [
        {"nom": "Bowl : riz, avocat, légumes rôtis, œuf mollet", "calories": "500", "proteines": "25g"},
        {"nom": "Wrap complet : jambon, crudités, houmous", "calories": "450", "proteines": "22g"},
        {"nom": "Omelette aux légumes + pain complet + salade verte", "calories": "420", "proteines": "28g"},
        {"nom": "Poulet rôti + légumes du four + pomme de terre", "calories": "480", "proteines": "35g"},
        {"nom": "Soupe de lentilles + pain complet + yaourt nature", "calories": "430", "proteines": "24g"},
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

LABELS_OBJ = {"prise de masse": "Prise de masse", "seche": "Sèche", "maintien": "Maintien"}
LABELS_NIV = {"debutant": "Débutant", "intermediaire": "Intermédiaire", "confirme": "Confirmé"}

# IMC
def calculer_imc(poids, taille_cm):
    taille_m = taille_cm / 100
    return poids / (taille_m ** 2)

def recommander_objectif(imc):
    if imc < 18.5:
        return "prise de masse", f"IMC {imc:.1f} — Insuffisance pondérale → Prise de masse recommandée"
    elif imc < 25:
        return "maintien", f"IMC {imc:.1f} — Poids normal → Maintien recommandé"
    elif imc < 30:
        return "seche", f"IMC {imc:.1f} — Surpoids → Sèche recommandée"
    else:
        return "seche", f"IMC {imc:.1f} — Obésité → Sèche recommandée"

# ==================== COULEURS ====================

BG       = "#0f1117"
BG2      = "#1a1d26"
BG3      = "#22263a"
VERT     = "#00ff88"
ORANGE   = "#ff9f43"
BLEU     = "#54a0ff"
ROUGE    = "#ff4757"
TEXTE    = "#cccccc"
GRIS     = "#555e6e"
FONT     = "Courier"

# ==================== APP ====================

class CoachApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Coach Sport & Nutrition v2")
        self.geometry("860x700")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.objectif_var = tk.StringVar(value="")
        self.niveau_var   = tk.StringVar(value="")
        self.selected_id  = None
        init_db()
        self._build_ui()
        self._charger_historique()
        self._charger_profil()

    # ---- UI ----

    def _build_ui(self):
        # Header
        h = tk.Frame(self, bg=BG)
        h.pack(fill="x", pady=(18, 0))
        tk.Label(h, text="COACH SPORT & NUTRITION",
                 font=(FONT, 20, "bold"), fg=VERT, bg=BG).pack()
        tk.Label(h, text="v2 — Profil · IMC · Suivi · Export",
                 font=(FONT, 9), fg=GRIS, bg=BG).pack()
        tk.Frame(self, bg=VERT, height=2).pack(fill="x", padx=30, pady=10)

        # Notebook
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG2, foreground=GRIS,
                        font=(FONT, 9, "bold"), padding=[18, 7])
        style.map("TNotebook.Tab",
                  background=[("selected", BG)],
                  foreground=[("selected", VERT)])

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=20)

        self.t_profil      = tk.Frame(self.nb, bg=BG)
        self.t_programme   = tk.Frame(self.nb, bg=BG)
        self.t_historique  = tk.Frame(self.nb, bg=BG)
        self.t_suivi       = tk.Frame(self.nb, bg=BG)

        self.nb.add(self.t_profil,     text="  Profil & IMC  ")
        self.nb.add(self.t_programme,  text="  Programme  ")
        self.nb.add(self.t_historique, text="  Historique  ")
        self.nb.add(self.t_suivi,      text="  Suivi calories  ")

        self._build_profil()
        self._build_programme()
        self._build_historique()
        self._build_suivi()

    # ---- ONGLET PROFIL ----

    def _build_profil(self):
        t = self.t_profil
        tk.Label(t, text="TON PROFIL", font=(FONT, 11, "bold"),
                 fg=VERT, bg=BG).pack(anchor="w", padx=30, pady=(20, 14))

        form = tk.Frame(t, bg=BG)
        form.pack(fill="x", padx=30)

        fields = [("Prénom", "prenom"), ("Âge", "age"), ("Poids (kg)", "poids"), ("Taille (cm)", "taille")]
        self.profil_vars = {}
        for label, key in fields:
            row = tk.Frame(form, bg=BG)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{label} :", font=(FONT, 10), fg=TEXTE, bg=BG, width=14, anchor="w").pack(side="left")
            var = tk.StringVar()
            self.profil_vars[key] = var
            tk.Entry(row, textvariable=var, font=(FONT, 10), bg=BG2, fg=TEXTE,
                     insertbackground=VERT, relief="flat", width=20).pack(side="left", padx=8)

        tk.Button(t, text="💾  Calculer IMC & Sauvegarder",
                  font=(FONT, 11, "bold"), fg=BG, bg=VERT,
                  relief="flat", cursor="hand2", pady=9,
                  command=self._sauvegarder_profil).pack(fill="x", padx=30, pady=16)

        tk.Frame(t, bg=BG2, height=1).pack(fill="x", padx=30)

        self.imc_frame = tk.Frame(t, bg=BG)
        self.imc_frame.pack(fill="x", padx=30, pady=14)
        self.lbl_imc = tk.Label(self.imc_frame, text="", font=(FONT, 11),
                                fg=ORANGE, bg=BG, justify="left")
        self.lbl_imc.pack(anchor="w")
        self.lbl_reco = tk.Label(self.imc_frame, text="", font=(FONT, 10),
                                 fg=BLEU, bg=BG, justify="left")
        self.lbl_reco.pack(anchor="w", pady=4)

    def _sauvegarder_profil(self):
        try:
            prenom = self.profil_vars["prenom"].get().strip()
            age    = int(self.profil_vars["age"].get())
            poids  = float(self.profil_vars["poids"].get().replace(",", "."))
            taille = float(self.profil_vars["taille"].get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erreur", "Vérifie les valeurs saisies.")
            return

        imc = calculer_imc(poids, taille)
        objectif_reco, message = recommander_objectif(imc)

        sauvegarder_profil(prenom, age, poids, imc, objectif_reco)

        self.lbl_imc.config(text=message)
        self.lbl_reco.config(text=f"→ Objectif recommandé : {LABELS_OBJ[objectif_reco]}")

        # Pré-sélectionner l'objectif dans l'onglet programme
        self.objectif_var.set(objectif_reco)
        messagebox.showinfo("Profil sauvegardé", f"Bonjour {prenom} ! IMC : {imc:.1f}\n{message}")

    def _charger_profil(self):
        row = charger_profil()
        if row:
            prenom, age, poids, imc, objectif = row
            self.profil_vars["prenom"].set(prenom)
            self.profil_vars["age"].set(str(age))
            self.profil_vars["poids"].set(str(poids))
            _, message = recommander_objectif(imc)
            self.lbl_imc.config(text=message)
            self.lbl_reco.config(text=f"→ Objectif recommandé : {LABELS_OBJ.get(objectif, objectif)}")
            self.objectif_var.set(objectif)

    # ---- ONGLET PROGRAMME ----

    def _build_programme(self):
        t = self.t_programme

        tk.Label(t, text="OBJECTIF", font=(FONT, 10, "bold"),
                 fg=VERT, bg=BG).pack(anchor="w", padx=30, pady=(20, 6))
        obj_f = tk.Frame(t, bg=BG)
        obj_f.pack(fill="x", padx=30)
        for label, val in [("Prise de masse", "prise de masse"), ("Sèche", "seche"), ("Maintien", "maintien")]:
            tk.Radiobutton(obj_f, text=label, variable=self.objectif_var, value=val,
                           font=(FONT, 11), fg=TEXTE, bg=BG, selectcolor=BG2,
                           activebackground=BG, activeforeground=VERT).pack(side="left", padx=15)

        tk.Label(t, text="NIVEAU", font=(FONT, 10, "bold"),
                 fg=VERT, bg=BG).pack(anchor="w", padx=30, pady=(14, 6))
        niv_f = tk.Frame(t, bg=BG)
        niv_f.pack(fill="x", padx=30)
        for label, val in [("Débutant", "debutant"), ("Intermédiaire", "intermediaire"), ("Confirmé", "confirme")]:
            tk.Radiobutton(niv_f, text=label, variable=self.niveau_var, value=val,
                           font=(FONT, 11), fg=TEXTE, bg=BG, selectcolor=BG2,
                           activebackground=BG, activeforeground=VERT).pack(side="left", padx=15)

        tk.Button(t, text="⚡  GÉNÉRER MON PROGRAMME",
                  font=(FONT, 12, "bold"), fg=BG, bg=VERT,
                  relief="flat", cursor="hand2", pady=10,
                  command=self._generer).pack(fill="x", padx=30, pady=14)

        tk.Frame(t, bg=BG2, height=1).pack(fill="x", padx=30)

        self.result_frame = tk.Frame(t, bg=BG)
        self.result_frame.pack(fill="both", expand=True, padx=30, pady=8)
        tk.Label(self.result_frame, text="Sélectionne un objectif et un niveau.",
                 font=(FONT, 11), fg=GRIS, bg=BG).pack(expand=True)

    def _generer(self):
        objectif = self.objectif_var.get()
        niveau   = self.niveau_var.get()
        if not objectif or not niveau:
            messagebox.showwarning("Sélection manquante", "Choisis un objectif ET un niveau.")
            return

        s = random.choice(SEANCES[objectif][niveau])
        r = random.choice(REPAS[objectif])
        c = random.choice(CONSEILS[objectif])

        sauvegarder_programme(
            LABELS_OBJ[objectif], LABELS_NIV[niveau],
            s["seance"], s["duree"],
            r["nom"], r["calories"], r["proteines"], c
        )

        for w in self.result_frame.winfo_children():
            w.destroy()

        def bloc(titre, lignes, couleur=VERT):
            f = tk.Frame(self.result_frame, bg=BG2, pady=8, padx=14)
            f.pack(fill="x", pady=3)
            tk.Label(f, text=titre, font=(FONT, 9, "bold"), fg=couleur, bg=BG2).pack(anchor="w")
            for l in lignes:
                tk.Label(f, text=l, font=(FONT, 10), fg=TEXTE, bg=BG2,
                         wraplength=740, justify="left").pack(anchor="w", pady=1)

        bloc("🏋  SÉANCE DE SPORT", [f"Durée : {s['duree']}", s["seance"]], VERT)
        bloc("🍽  REPAS CONSEILLÉ", [r["nom"], f"{r['calories']} kcal  •  {r['proteines']} protéines"], ORANGE)
        bloc("💡  CONSEIL NUTRITION", [c], BLEU)

        # Note
        note_f = tk.Frame(self.result_frame, bg=BG)
        note_f.pack(fill="x", pady=6)
        tk.Label(note_f, text="Note ce programme :", font=(FONT, 9), fg=GRIS, bg=BG).pack(side="left")
        for i in range(1, 6):
            tk.Button(note_f, text="★", font=(FONT, 14), fg=ORANGE, bg=BG,
                      relief="flat", cursor="hand2",
                      command=lambda n=i: self._noter(n)).pack(side="left", padx=2)

        self._charger_historique()
        self._charger_suivi()

    def _noter(self, note):
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT id FROM historique ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        if row:
            mettre_a_jour_note(row[0], note)
            self._charger_historique()
            messagebox.showinfo("Note enregistrée", f"Programme noté {note}/5 ★")

    # ---- ONGLET HISTORIQUE ----

    def _build_historique(self):
        t = self.t_historique

        tk.Label(t, text="HISTORIQUE DES PROGRAMMES", font=(FONT, 10, "bold"),
                 fg=VERT, bg=BG).pack(anchor="w", padx=30, pady=(18, 10))

        cols = ("Date", "Objectif", "Niveau", "Durée", "Calories", "Note")
        self.tree = ttk.Treeview(t, columns=cols, show="headings", height=14)

        style = ttk.Style()
        style.configure("Treeview", background=BG2, foreground=TEXTE,
                        fieldbackground=BG2, font=(FONT, 9), rowheight=26)
        style.configure("Treeview.Heading", background=BG, foreground=VERT,
                        font=(FONT, 9, "bold"))
        style.map("Treeview", background=[("selected", BG3)])

        largeurs = [130, 130, 110, 70, 90, 60]
        for col, larg in zip(cols, largeurs):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=larg, anchor="w")

        scroll = ttk.Scrollbar(t, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=(0, 6))
        scroll.pack(side="left", fill="y", pady=(0, 6))

        btn_f = tk.Frame(t, bg=BG)
        btn_f.pack(fill="x", padx=30, pady=8)
        tk.Button(btn_f, text="📤  Exporter CSV", font=(FONT, 10), fg=BG, bg=BLEU,
                  relief="flat", cursor="hand2", pady=6,
                  command=self._exporter).pack(side="left", padx=(0, 10))
        tk.Button(btn_f, text="🗑  Effacer l'historique", font=(FONT, 10), fg=TEXTE, bg=BG2,
                  relief="flat", cursor="hand2", pady=6,
                  command=self._effacer).pack(side="left")

    def _charger_historique(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in charger_historique():
            id_, date, obj, niv, duree, cal, note = row
            etoiles = "★" * note if note else "-"
            self.tree.insert("", "end", iid=str(id_),
                             values=(date, obj, niv, duree, f"{cal} kcal", etoiles))

    def _exporter(self):
        path = exporter_csv()
        messagebox.showinfo("Export réussi", f"Fichier exporté :\n{path}")

    def _effacer(self):
        if messagebox.askyesno("Confirmation", "Supprimer tout l'historique ?"):
            supprimer_historique()
            self._charger_historique()
            self._charger_suivi()

    # ---- ONGLET SUIVI CALORIES ----

    def _build_suivi(self):
        t = self.t_suivi
        tk.Label(t, text="SUIVI DES CALORIES", font=(FONT, 10, "bold"),
                 fg=VERT, bg=BG).pack(anchor="w", padx=30, pady=(18, 10))

        self.canvas_suivi = tk.Canvas(t, bg=BG2, width=780, height=320,
                                      highlightthickness=0)
        self.canvas_suivi.pack(padx=30, pady=4)

        self.lbl_stats = tk.Label(t, text="", font=(FONT, 9), fg=GRIS, bg=BG, justify="left")
        self.lbl_stats.pack(anchor="w", padx=30, pady=8)

    def _charger_suivi(self):
        rows = charger_calories_suivi()
        c = self.canvas_suivi
        c.delete("all")

        if not rows:
            c.create_text(390, 160, text="Aucune donnée disponible.",
                          font=(FONT, 11), fill=GRIS)
            return

        valeurs = []
        for date, obj, cal in rows:
            try:
                valeurs.append((date, obj, int(cal)))
            except (ValueError, TypeError):
                pass

        if not valeurs:
            return

        W, H = 780, 320
        pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 50

        max_cal = max(v[2] for v in valeurs)
        min_cal = min(v[2] for v in valeurs)
        ecart   = max_cal - min_cal or 1

        def x_pos(i):
            n = len(valeurs)
            return pad_l + (i / max(n - 1, 1)) * (W - pad_l - pad_r)

        def y_pos(cal):
            ratio = (cal - min_cal) / ecart
            return H - pad_b - ratio * (H - pad_t - pad_b)

        # Grille
        for k in range(5):
            y = pad_t + k * (H - pad_t - pad_b) / 4
            val = max_cal - k * ecart / 4
            c.create_line(pad_l, y, W - pad_r, y, fill="#2a2d3a", dash=(4, 4))
            c.create_text(pad_l - 6, y, text=f"{int(val)}", font=(FONT, 7), fill=GRIS, anchor="e")

        # Couleurs par objectif
        coul_obj = {"Prise de masse": VERT, "Sèche": ORANGE, "Maintien": BLEU}

        # Ligne et points
        pts = [(x_pos(i), y_pos(v[2])) for i, v in enumerate(valeurs)]
        for i in range(len(pts) - 1):
            obj = valeurs[i][1]
            couleur = coul_obj.get(obj, VERT)
            c.create_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
                          fill=couleur, width=2)

        for i, (px, py) in enumerate(pts):
            obj     = valeurs[i][1]
            couleur = coul_obj.get(obj, VERT)
            c.create_oval(px-5, py-5, px+5, py+5, fill=couleur, outline="")
            c.create_text(px, py - 14, text=f"{valeurs[i][2]}", font=(FONT, 7), fill=couleur)

        # Axe X
        for i, (date, obj, cal) in enumerate(valeurs):
            px = x_pos(i)
            c.create_text(px, H - pad_b + 14, text=date[:5], font=(FONT, 7), fill=GRIS, angle=0)

        # Légende
        lx = pad_l
        for obj, col in coul_obj.items():
            c.create_rectangle(lx, H - 14, lx + 10, H - 4, fill=col, outline="")
            c.create_text(lx + 14, H - 9, text=obj, font=(FONT, 7), fill=GRIS, anchor="w")
            lx += 130

        # Stats
        total   = len(valeurs)
        moyenne = sum(v[2] for v in valeurs) // total
        self.lbl_stats.config(
            text=f"  {total} programmes générés  •  Moyenne : {moyenne} kcal/repas  •  Min : {min_cal} kcal  •  Max : {max_cal} kcal"
        )

    def run(self):
        self._charger_suivi()
        self.mainloop()

# ==================== LANCEMENT ====================

if __name__ == "__main__":
    app = CoachApp()
    app.run()
