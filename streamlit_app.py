# ============================================================
#  Coach Sport & Nutrition - Version Streamlit (web)
#  Auteurs : Nicolas, Jordy, Ivann, Cheikh
# ============================================================

from __future__ import annotations

import csv
import io
import random
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

import repas_nutrition as nutrition
import seances_sport as sport

# ==================== CONFIG ====================

DB_PATH = "coach_sport.db"
DATE_FORMAT = "%d/%m/%Y %H:%M"
STATUT_A_FAIRE = "À faire"
STATUT_FAIT = "Fait"

LABELS_OBJ = {"prise de masse": "Prise de masse", "seche": "Sèche", "maintien": "Maintien"}
LABELS_NIV = {"debutant": "Débutant", "intermediaire": "Intermédiaire", "confirme": "Confirmé"}

OBJECTIFS = list(LABELS_OBJ.keys())
NIVEAUX = list(LABELS_NIV.keys())

SEANCES = sport.SEANCES
REPAS = nutrition.REPAS
CONSEILS = nutrition.CONSEILS_NUTRITION

st.set_page_config(
    page_title="Coach Sport & Nutrition",
    page_icon="🏋️",
    layout="wide",
)

# ==================== BASE DE DONNÉES ====================

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
    c.execute("PRAGMA table_info(historique)")
    cols = {row[1] for row in c.fetchall()}
    if "statut" not in cols:
        c.execute(
            f"ALTER TABLE historique ADD COLUMN statut TEXT NOT NULL DEFAULT '{STATUT_A_FAIRE}'"
        )
    conn.commit()
    conn.close()


def sauvegarder_profil(prenom, age, poids, imc, objectif):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM profil")
    c.execute(
        "INSERT INTO profil (prenom, age, poids, imc, objectif) VALUES (?,?,?,?,?)",
        (prenom, age, poids, round(imc, 1), objectif),
    )
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
    c.execute(
        """
        INSERT INTO historique (date, objectif, niveau, seance, duree, repas, calories, proteines, conseil, statut)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            datetime.now().strftime(DATE_FORMAT),
            objectif, niveau, seance, duree, repas, calories, proteines, conseil,
            STATUT_A_FAIRE,
        ),
    )
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid


def mettre_a_jour_note(item_id, note):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE historique SET note=? WHERE id=?", (note, item_id))
    conn.commit()
    conn.close()


def mettre_a_jour_statut(item_id, statut):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE historique SET statut=? WHERE id=?", (statut, item_id))
    conn.commit()
    conn.close()


def mettre_a_jour_repas_programme(item_id, repas, calories, proteines):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE historique SET repas=?, calories=?, proteines=? WHERE id=?",
        (repas, calories, proteines, item_id),
    )
    conn.commit()
    conn.close()


def charger_historique(objectif="Tous", niveau="Tous", statut="Tous"):
    conn = get_conn()
    c = conn.cursor()
    requete = """
        SELECT id, date, objectif, niveau, duree, calories, note, statut
        FROM historique
    """
    conditions, params = [], []
    if objectif != "Tous":
        conditions.append("objectif = ?")
        params.append(objectif)
    if niveau != "Tous":
        conditions.append("niveau = ?")
        params.append(niveau)
    if statut != "Tous":
        conditions.append("statut = ?")
        params.append(statut)
    if conditions:
        requete += " WHERE " + " AND ".join(conditions)
    requete += " ORDER BY id DESC"
    c.execute(requete, params)
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


def compter_programmes_faits_semaine():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT date, statut FROM historique")
    rows = c.fetchall()
    conn.close()
    semaine = datetime.now().isocalendar()[:2]
    total = 0
    for date_str, statut in rows:
        if statut != STATUT_FAIT:
            continue
        try:
            d = datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            continue
        if d.isocalendar()[:2] == semaine:
            total += 1
    return total


def compter_programmes_a_faire():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM historique WHERE statut=?", (STATUT_A_FAIRE,))
    total = c.fetchone()[0]
    conn.close()
    return total


def exporter_csv_bytes() -> bytes:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        SELECT date, objectif, niveau, duree, repas, calories, proteines, conseil, note, statut
        FROM historique ORDER BY id DESC
        """
    )
    rows = c.fetchall()
    conn.close()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(
        ["Date", "Objectif", "Niveau", "Durée", "Repas", "Calories",
         "Protéines", "Conseil", "Note", "Statut"]
    )
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")


# ==================== UTILS ====================

def calories_pour_app(repas):
    return repas["calories"].replace("kcal", "").strip()


def proteines_pour_app(repas):
    return repas["proteines"].split(" de ")[0].strip()


def calculer_imc(poids, taille_cm):
    taille_m = taille_cm / 100
    return poids / (taille_m ** 2)


def recommander_objectif(imc):
    if imc < 18.5:
        return "prise de masse", f"IMC {imc:.1f} — Insuffisance pondérale → Prise de masse recommandée"
    if imc < 25:
        return "maintien", f"IMC {imc:.1f} — Poids normal → Maintien recommandé"
    if imc < 30:
        return "seche", f"IMC {imc:.1f} — Surpoids → Sèche recommandée"
    return "seche", f"IMC {imc:.1f} — Obésité → Sèche recommandée"


def generer_programme(objectif, niveau):
    s = random.choice(SEANCES[objectif][niveau])
    r = nutrition.choisir_repas(objectif)
    c = nutrition.choisir_conseil_nutrition(objectif)
    return s, r, c


# ==================== SESSION STATE ====================

def init_state():
    init_db()
    if "current_program_id" not in st.session_state:
        st.session_state.current_program_id = None
    if "current_program" not in st.session_state:
        st.session_state.current_program = None
    if "objectif_pre" not in st.session_state:
        st.session_state.objectif_pre = "maintien"


# ==================== UI ====================

def page_profil():
    st.subheader("👤 Ton profil")

    profil = charger_profil()
    prenom_def = profil[0] if profil else ""
    age_def = int(profil[1]) if profil else 25
    poids_def = float(profil[2]) if profil else 70.0
    taille_def = 175.0

    with st.form("form_profil"):
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prénom", value=prenom_def)
            age = st.number_input("Âge", min_value=10, max_value=100, value=age_def, step=1)
        with col2:
            poids = st.number_input("Poids (kg)", min_value=30.0, max_value=250.0,
                                    value=poids_def, step=0.5)
            taille = st.number_input("Taille (cm)", min_value=120.0, max_value=230.0,
                                     value=taille_def, step=0.5)
        submit = st.form_submit_button("💾 Calculer IMC & Sauvegarder", type="primary")

    if submit:
        if not prenom.strip():
            st.error("Le prénom est requis.")
            return
        imc = calculer_imc(poids, taille)
        obj_reco, msg = recommander_objectif(imc)
        sauvegarder_profil(prenom.strip(), int(age), float(poids), imc, obj_reco)
        st.session_state.objectif_pre = obj_reco
        st.success(f"Bonjour {prenom} ! IMC : {imc:.1f}")
        st.info(msg)
        st.info(f"→ Objectif recommandé : **{LABELS_OBJ[obj_reco]}**")
    elif profil:
        _, msg = recommander_objectif(profil[3])
        st.info(msg)
        st.info(f"→ Objectif recommandé : **{LABELS_OBJ.get(profil[4], profil[4])}**")


def afficher_programme_courant():
    prog = st.session_state.current_program
    if not prog:
        return
    s = prog["seance"]
    r = prog["repas"]
    c = prog["conseil"]
    cal = calories_pour_app(r)
    prot = proteines_pour_app(r)

    st.markdown("### Ton programme")

    with st.container(border=True):
        st.markdown("**🏋️ Séance de sport**")
        st.write(f"Durée : **{s['duree']}**")
        st.write(s["seance"])

    with st.container(border=True):
        st.markdown("**🍽️ Repas conseillé**")
        st.write(r["nom"])
        st.write(f"{cal} kcal • {prot} de protéines")
        if st.button("🔁 Changer le repas", key="btn_changer_repas"):
            changer_repas()
            st.rerun()

    with st.container(border=True):
        st.markdown("**💡 Conseil nutrition**")
        st.write(c)

    st.markdown("**Note ce programme**")
    cols = st.columns(5)
    for i, col in enumerate(cols, start=1):
        if col.button("★" * i, key=f"note_{i}", use_container_width=True):
            mettre_a_jour_note(st.session_state.current_program_id, i)
            st.success(f"Programme noté {i}/5 ★")


def changer_repas():
    prog = st.session_state.current_program
    pid = st.session_state.current_program_id
    if not prog or pid is None:
        return
    objectif = prog["objectif"]
    actuel = prog["repas"]
    autres = [r for r in REPAS[objectif] if r["nom"] != actuel["nom"]]
    if not autres:
        st.warning("Aucun autre repas disponible.")
        return
    nouveau = random.choice(autres)
    cal = calories_pour_app(nouveau)
    prot = proteines_pour_app(nouveau)
    prog["repas"] = nouveau
    mettre_a_jour_repas_programme(pid, nouveau["nom"], cal, prot)


def page_programme():
    st.subheader("⚡ Génère ton programme")

    objectif_idx = OBJECTIFS.index(st.session_state.objectif_pre) if st.session_state.objectif_pre in OBJECTIFS else 2

    col1, col2 = st.columns(2)
    with col1:
        objectif = st.radio(
            "Objectif",
            OBJECTIFS,
            index=objectif_idx,
            format_func=lambda x: LABELS_OBJ[x],
            horizontal=True,
        )
    with col2:
        niveau = st.radio(
            "Niveau",
            NIVEAUX,
            index=0,
            format_func=lambda x: LABELS_NIV[x],
            horizontal=True,
        )

    if st.button("⚡ GÉNÉRER MON PROGRAMME", type="primary", use_container_width=True):
        s, r, c = generer_programme(objectif, niveau)
        cal = calories_pour_app(r)
        prot = proteines_pour_app(r)
        pid = sauvegarder_programme(
            LABELS_OBJ[objectif], LABELS_NIV[niveau],
            s["seance"], s["duree"],
            r["nom"], cal, prot, c,
        )
        st.session_state.current_program_id = pid
        st.session_state.current_program = {
            "objectif": objectif, "niveau": niveau,
            "seance": s, "repas": r, "conseil": c,
        }

    if st.session_state.current_program:
        st.divider()
        afficher_programme_courant()


def page_historique():
    st.subheader("📜 Historique des programmes")

    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        f_obj = st.selectbox("Objectif", ["Tous", "Prise de masse", "Sèche", "Maintien"])
    with col2:
        f_niv = st.selectbox("Niveau", ["Tous", "Débutant", "Intermédiaire", "Confirmé"])
    with col3:
        f_stat = st.selectbox("Statut", ["Tous", STATUT_A_FAIRE, STATUT_FAIT])
    with col4:
        st.write("")
        st.write("")
        if st.button("Réinitialiser"):
            st.rerun()

    rows = charger_historique(f_obj, f_niv, f_stat)
    faits_sem = compter_programmes_faits_semaine()
    a_faire = compter_programmes_a_faire()

    c1, c2, c3 = st.columns(3)
    c1.metric("Programmes affichés", len(rows))
    c2.metric("Faits cette semaine", faits_sem)
    c3.metric("Encore à faire", a_faire)

    if not rows:
        st.info("Aucun programme dans l'historique.")
        return

    df = pd.DataFrame(
        rows,
        columns=["ID", "Date", "Objectif", "Niveau", "Durée", "Calories", "Note", "Statut"],
    )
    df["Note"] = df["Note"].apply(lambda n: "★" * n if n else "-")
    df["Calories"] = df["Calories"].astype(str) + " kcal"
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

    st.markdown("**Actions sur un programme**")
    options_a_faire = [
        (rid, f"#{rid} — {date} — {obj} / {niv}")
        for rid, date, obj, niv, _, _, _, statut in rows
        if statut == STATUT_A_FAIRE
    ]
    if options_a_faire:
        choix = st.selectbox(
            "Marquer comme fait",
            options_a_faire,
            format_func=lambda x: x[1],
        )
        if st.button("✅ Marquer comme fait"):
            mettre_a_jour_statut(choix[0], STATUT_FAIT)
            st.success("Programme marqué comme fait.")
            st.rerun()
    else:
        st.caption("Aucun programme à faire dans la sélection.")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "📤 Exporter CSV",
            data=exporter_csv_bytes(),
            file_name="historique_coach.csv",
            mime="text/csv",
        )
    with col_b:
        with st.popover("🗑️ Effacer l'historique"):
            st.warning("Cette action est irréversible.")
            if st.button("Confirmer la suppression", type="primary"):
                supprimer_historique()
                st.session_state.current_program = None
                st.session_state.current_program_id = None
                st.rerun()


def page_suivi():
    st.subheader("📈 Suivi des calories")

    rows = charger_calories_suivi()
    faits_sem = compter_programmes_faits_semaine()
    a_faire = compter_programmes_a_faire()

    if not rows:
        st.info("Aucune donnée disponible. Génère des programmes pour suivre tes calories.")
        return

    data = []
    for date, obj, cal in rows:
        try:
            data.append({"date": date, "objectif": obj, "calories": int(cal)})
        except (ValueError, TypeError):
            pass

    if not data:
        return

    df = pd.DataFrame(data)

    chart_df = df.pivot_table(
        index=df.index, columns="objectif", values="calories", aggfunc="first"
    )
    st.line_chart(chart_df)

    cals = [d["calories"] for d in data]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", len(cals))
    c2.metric("Moyenne", f"{sum(cals)//len(cals)} kcal")
    c3.metric("Min", f"{min(cals)} kcal")
    c4.metric("Max", f"{max(cals)} kcal")
    c5.metric("Faits / À faire", f"{faits_sem} / {a_faire}")

    with st.expander("Détail des programmes"):
        st.dataframe(df, use_container_width=True, hide_index=True)


# ==================== MAIN ====================

def main():
    init_state()

    st.title("🏋️ Coach Sport & Nutrition")
    st.caption("Profil • IMC • Programmes personnalisés • Suivi")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["👤 Profil & IMC", "⚡ Programme", "📜 Historique", "📈 Suivi calories"]
    )
    with tab1:
        page_profil()
    with tab2:
        page_programme()
    with tab3:
        page_historique()
    with tab4:
        page_suivi()


main()
