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
import repas_nutrition as nutrition
import seances_sport as sport

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

SEANCES = sport.SEANCES
REPAS = nutrition.REPAS
CONSEILS = nutrition.CONSEILS_NUTRITION


def calories_pour_app(repas: dict[str, str]) -> str:
    return repas["calories"].replace("kcal", "").strip()


def proteines_pour_app(repas: dict[str, str]) -> str:
    return repas["proteines"].split(" de ")[0].strip()

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
        r = nutrition.choisir_repas(objectif)
        c = nutrition.choisir_conseil_nutrition(objectif)
        calories = calories_pour_app(r)
        proteines = proteines_pour_app(r)

        sauvegarder_programme(
            LABELS_OBJ[objectif], LABELS_NIV[niveau],
            s["seance"], s["duree"],
            r["nom"], calories, proteines, c
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
        bloc("🍽  REPAS CONSEILLÉ", [r["nom"], f"{calories} kcal  •  {proteines} protéines"], ORANGE)
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
