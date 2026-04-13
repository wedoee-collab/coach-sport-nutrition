# ============================================================
#  Coach Sport & Nutrition - Version Streamlit (web)
#  Auteurs : Nicolas, Jordy, Ivann, Cheikh
# ============================================================

from __future__ import annotations

import csv
import hashlib
import io
import os
import random
import sqlite3
from datetime import datetime

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

# ==================== AUTHENTIFICATION ====================

PBKDF2_ITERATIONS = 200_000


def hasher_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return derived.hex(), salt.hex()


def verifier_password(password: str, hash_hex: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    derived, _ = hasher_password(password, salt)
    return derived == hash_hex


def creer_utilisateur(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if len(username) < 3:
        return False, "Le nom d'utilisateur doit faire au moins 3 caractères."
    if len(password) < 6:
        return False, "Le mot de passe doit faire au moins 6 caractères."
    hash_hex, salt_hex = hasher_password(password)
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM users")
        is_admin = 1 if c.fetchone()[0] == 0 else 0
        c.execute(
            "INSERT INTO users (username, password_hash, salt, created_at, is_admin) VALUES (?,?,?,?,?)",
            (username, hash_hex, salt_hex, datetime.now().strftime(DATE_FORMAT), is_admin),
        )
        conn.commit()
        msg = f"Compte créé pour {username}."
        if is_admin:
            msg += " 👑 Premier compte → tu es administrateur."
        return True, msg
    except sqlite3.IntegrityError:
        return False, "Ce nom d'utilisateur est déjà pris."
    finally:
        conn.close()


def authentifier(username: str, password: str) -> tuple[int | None, bool]:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, password_hash, salt, is_admin FROM users WHERE username=?", (username.strip(),))
    row = c.fetchone()
    conn.close()
    if not row:
        return None, False
    user_id, hash_hex, salt_hex, is_admin = row
    if verifier_password(password, hash_hex, salt_hex):
        return user_id, bool(is_admin)
    return None, False


def lister_utilisateurs():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT u.id, u.username, u.created_at, u.is_admin,
               (SELECT COUNT(*) FROM historique h WHERE h.user_id = u.id) AS nb_prog,
               (SELECT MAX(date) FROM historique h WHERE h.user_id = u.id) AS derniere
        FROM users u
        ORDER BY u.id ASC
    """)
    rows = c.fetchall()
    conn.close()
    return rows


def basculer_admin(user_id: int) -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return False
    nouveau = 0 if row[0] else 1
    c.execute("UPDATE users SET is_admin=? WHERE id=?", (nouveau, user_id))
    conn.commit()
    conn.close()
    return bool(nouveau)


def supprimer_utilisateur(user_id: int):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM historique WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM profil WHERE user_id=?", (user_id,))
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


def reinitialiser_mot_de_passe(user_id: int, nouveau_password: str) -> tuple[bool, str]:
    if len(nouveau_password) < 6:
        return False, "Le mot de passe doit faire au moins 6 caractères."
    hash_hex, salt_hex = hasher_password(nouveau_password)
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET password_hash=?, salt=? WHERE id=?", (hash_hex, salt_hex, user_id))
    conn.commit()
    conn.close()
    return True, "Mot de passe réinitialisé."


def compter_admins() -> int:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE is_admin=1")
    n = c.fetchone()[0]
    conn.close()
    return n


def stats_globales() -> dict:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    nb_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM historique")
    nb_prog = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM historique WHERE statut=?", (STATUT_FAIT,))
    nb_faits = c.fetchone()[0]
    c.execute("SELECT objectif, COUNT(*) FROM historique GROUP BY objectif ORDER BY 2 DESC")
    par_obj = c.fetchall()
    conn.close()
    return {
        "nb_users": nb_users,
        "nb_prog": nb_prog,
        "nb_faits": nb_faits,
        "par_obj": par_obj,
    }


# ==================== BASE DE DONNÉES ====================

def get_conn():
    return sqlite3.connect(DB_PATH)


def _ajouter_colonne_si_absente(c, table: str, colonne: str, definition: str):
    c.execute(f"PRAGMA table_info({table})")
    cols = {row[1] for row in c.fetchall()}
    if colonne not in cols:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {colonne} {definition}")


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt          TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            is_admin      INTEGER NOT NULL DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS profil (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id  INTEGER NOT NULL,
            prenom   TEXT NOT NULL,
            age      INTEGER,
            poids    REAL,
            imc      REAL,
            objectif TEXT,
            UNIQUE(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id   INTEGER NOT NULL,
            date      TEXT NOT NULL,
            objectif  TEXT NOT NULL,
            niveau    TEXT NOT NULL,
            seance    TEXT NOT NULL,
            duree     TEXT NOT NULL,
            repas     TEXT NOT NULL,
            calories  TEXT NOT NULL,
            proteines TEXT NOT NULL,
            conseil   TEXT NOT NULL,
            note      INTEGER DEFAULT 0,
            statut    TEXT NOT NULL DEFAULT 'À faire'
        )
    """)

    _ajouter_colonne_si_absente(c, "historique", "statut", f"TEXT NOT NULL DEFAULT '{STATUT_A_FAIRE}'")
    _ajouter_colonne_si_absente(c, "historique", "user_id", "INTEGER NOT NULL DEFAULT 0")
    _ajouter_colonne_si_absente(c, "profil", "user_id", "INTEGER NOT NULL DEFAULT 0")
    _ajouter_colonne_si_absente(c, "users", "is_admin", "INTEGER NOT NULL DEFAULT 0")

    conn.commit()
    conn.close()


def sauvegarder_profil(user_id, prenom, age, poids, imc, objectif):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM profil WHERE user_id=?", (user_id,))
    c.execute(
        "INSERT INTO profil (user_id, prenom, age, poids, imc, objectif) VALUES (?,?,?,?,?,?)",
        (user_id, prenom, age, poids, round(imc, 1), objectif),
    )
    conn.commit()
    conn.close()


def charger_profil(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT prenom, age, poids, imc, objectif FROM profil WHERE user_id=? LIMIT 1",
        (user_id,),
    )
    row = c.fetchone()
    conn.close()
    return row


def sauvegarder_programme(user_id, objectif, niveau, seance, duree, repas, calories, proteines, conseil):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO historique (user_id, date, objectif, niveau, seance, duree, repas, calories, proteines, conseil, statut)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            user_id,
            datetime.now().strftime(DATE_FORMAT),
            objectif, niveau, seance, duree, repas, calories, proteines, conseil,
            STATUT_A_FAIRE,
        ),
    )
    pid = c.lastrowid
    conn.commit()
    conn.close()
    return pid


def mettre_a_jour_note(user_id, item_id, note):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE historique SET note=? WHERE id=? AND user_id=?", (note, item_id, user_id))
    conn.commit()
    conn.close()


def mettre_a_jour_statut(user_id, item_id, statut):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE historique SET statut=? WHERE id=? AND user_id=?", (statut, item_id, user_id))
    conn.commit()
    conn.close()


def mettre_a_jour_repas_programme(user_id, item_id, repas, calories, proteines):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE historique SET repas=?, calories=?, proteines=? WHERE id=? AND user_id=?",
        (repas, calories, proteines, item_id, user_id),
    )
    conn.commit()
    conn.close()


def charger_historique(user_id, objectif="Tous", niveau="Tous", statut="Tous"):
    conn = get_conn()
    c = conn.cursor()
    requete = """
        SELECT id, date, objectif, niveau, duree, calories, note, statut
        FROM historique WHERE user_id=?
    """
    params = [user_id]
    if objectif != "Tous":
        requete += " AND objectif = ?"
        params.append(objectif)
    if niveau != "Tous":
        requete += " AND niveau = ?"
        params.append(niveau)
    if statut != "Tous":
        requete += " AND statut = ?"
        params.append(statut)
    requete += " ORDER BY id DESC"
    c.execute(requete, params)
    rows = c.fetchall()
    conn.close()
    return rows


def charger_calories_suivi(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT date, objectif, calories FROM historique WHERE user_id=? ORDER BY id ASC LIMIT 20",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()
    return rows


def supprimer_historique(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM historique WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()


def compter_programmes_faits_semaine(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT date, statut FROM historique WHERE user_id=?", (user_id,))
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


def compter_programmes_a_faire(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) FROM historique WHERE statut=? AND user_id=?",
        (STATUT_A_FAIRE, user_id),
    )
    total = c.fetchone()[0]
    conn.close()
    return total


def exporter_csv_bytes(user_id) -> bytes:
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        SELECT date, objectif, niveau, duree, repas, calories, proteines, conseil, note, statut
        FROM historique WHERE user_id=? ORDER BY id DESC
        """,
        (user_id,),
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
    st.session_state.setdefault("user_id", None)
    st.session_state.setdefault("username", None)
    st.session_state.setdefault("is_admin", False)
    st.session_state.setdefault("current_program_id", None)
    st.session_state.setdefault("current_program", None)
    st.session_state.setdefault("objectif_pre", "maintien")


def reset_session_user():
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False
    st.session_state.current_program_id = None
    st.session_state.current_program = None
    st.session_state.objectif_pre = "maintien"


# ==================== ECRAN AUTH ====================

def page_auth():
    st.title("🏋️ Coach Sport & Nutrition")
    st.caption("Connecte-toi ou crée un compte pour commencer.")

    tab_login, tab_register = st.tabs(["🔐 Connexion", "🆕 Créer un compte"])

    with tab_login:
        with st.form("form_login"):
            username = st.text_input("Nom d'utilisateur", key="login_user")
            password = st.text_input("Mot de passe", type="password", key="login_pwd")
            submit = st.form_submit_button("Se connecter", type="primary", use_container_width=True)
        if submit:
            uid, is_admin = authentifier(username, password)
            if uid is None:
                st.error("Identifiants incorrects.")
            else:
                st.session_state.user_id = uid
                st.session_state.username = username.strip()
                st.session_state.is_admin = is_admin
                profil = charger_profil(uid)
                if profil and profil[4]:
                    st.session_state.objectif_pre = profil[4]
                st.success(f"Bienvenue {username} !")
                st.rerun()

    with tab_register:
        with st.form("form_register"):
            new_user = st.text_input("Nom d'utilisateur (3 caractères min.)", key="reg_user")
            new_pwd = st.text_input("Mot de passe (6 caractères min.)", type="password", key="reg_pwd")
            new_pwd2 = st.text_input("Confirmer le mot de passe", type="password", key="reg_pwd2")
            submit = st.form_submit_button("Créer le compte", type="primary", use_container_width=True)
        if submit:
            if new_pwd != new_pwd2:
                st.error("Les mots de passe ne correspondent pas.")
            else:
                ok, msg = creer_utilisateur(new_user, new_pwd)
                if ok:
                    st.success(msg + " Tu peux te connecter dans l'onglet « Connexion ».")
                else:
                    st.error(msg)


# ==================== UI APP ====================

def page_profil():
    user_id = st.session_state.user_id
    st.subheader("👤 Ton profil")

    profil = charger_profil(user_id)
    prenom_def = profil[0] if profil else st.session_state.username or ""
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
        sauvegarder_profil(user_id, prenom.strip(), int(age), float(poids), imc, obj_reco)
        st.session_state.objectif_pre = obj_reco
        st.success(f"Bonjour {prenom} ! IMC : {imc:.1f}")
        st.info(msg)
        st.info(f"→ Objectif recommandé : **{LABELS_OBJ[obj_reco]}**")
    elif profil:
        _, msg = recommander_objectif(profil[3])
        st.info(msg)
        st.info(f"→ Objectif recommandé : **{LABELS_OBJ.get(profil[4], profil[4])}**")


def afficher_programme_courant():
    user_id = st.session_state.user_id
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
            mettre_a_jour_note(user_id, st.session_state.current_program_id, i)
            st.success(f"Programme noté {i}/5 ★")


def changer_repas():
    user_id = st.session_state.user_id
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
    mettre_a_jour_repas_programme(user_id, pid, nouveau["nom"], cal, prot)


def page_programme():
    user_id = st.session_state.user_id
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
            user_id,
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
    user_id = st.session_state.user_id
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

    rows = charger_historique(user_id, f_obj, f_niv, f_stat)
    faits_sem = compter_programmes_faits_semaine(user_id)
    a_faire = compter_programmes_a_faire(user_id)

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
            mettre_a_jour_statut(user_id, choix[0], STATUT_FAIT)
            st.success("Programme marqué comme fait.")
            st.rerun()
    else:
        st.caption("Aucun programme à faire dans la sélection.")

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "📤 Exporter CSV",
            data=exporter_csv_bytes(user_id),
            file_name="historique_coach.csv",
            mime="text/csv",
        )
    with col_b:
        with st.popover("🗑️ Effacer l'historique"):
            st.warning("Cette action est irréversible.")
            if st.button("Confirmer la suppression", type="primary"):
                supprimer_historique(user_id)
                st.session_state.current_program = None
                st.session_state.current_program_id = None
                st.rerun()


def page_suivi():
    user_id = st.session_state.user_id
    st.subheader("📈 Suivi des calories")

    rows = charger_calories_suivi(user_id)
    faits_sem = compter_programmes_faits_semaine(user_id)
    a_faire = compter_programmes_a_faire(user_id)

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


# ==================== SIDEBAR ====================

def sidebar_utilisateur():
    with st.sidebar:
        badge = "👑 Admin" if st.session_state.is_admin else "Utilisateur"
        st.markdown(f"### 👤 {st.session_state.username}")
        st.caption(f"Connecté · {badge}")
        if st.button("🚪 Se déconnecter", use_container_width=True):
            reset_session_user()
            st.rerun()


# ==================== PAGE ADMIN ====================

def page_admin():
    st.subheader("🛠️ Administration")

    stats = stats_globales()
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Utilisateurs", stats["nb_users"])
    c2.metric("📋 Programmes générés", stats["nb_prog"])
    c3.metric("✅ Programmes faits", stats["nb_faits"])

    if stats["par_obj"]:
        st.markdown("**Répartition par objectif**")
        df_obj = pd.DataFrame(stats["par_obj"], columns=["Objectif", "Nombre"])
        st.bar_chart(df_obj.set_index("Objectif"))

    st.divider()
    st.markdown("### 👥 Liste des utilisateurs")

    users = lister_utilisateurs()
    df_users = pd.DataFrame(
        users,
        columns=["ID", "Utilisateur", "Créé le", "Admin", "Programmes", "Dernière activité"],
    )
    df_users["Admin"] = df_users["Admin"].apply(lambda x: "👑" if x else "")
    df_users["Dernière activité"] = df_users["Dernière activité"].fillna("—")
    st.dataframe(df_users, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### ⚙️ Actions sur un utilisateur")

    options = [(u[0], u[1], bool(u[3])) for u in users]
    if not options:
        st.info("Aucun utilisateur.")
        return

    choix = st.selectbox(
        "Sélectionner un utilisateur",
        options,
        format_func=lambda x: f"#{x[0]} — {x[1]}" + (" 👑" if x[2] else ""),
    )
    target_id, target_name, target_is_admin = choix
    is_self = target_id == st.session_state.user_id
    nb_admins = compter_admins()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Rôle**")
        if is_self and target_is_admin and nb_admins == 1:
            st.caption("⚠️ Tu es le seul admin.")
            st.button("Retirer admin", disabled=True, use_container_width=True)
        elif target_is_admin:
            if st.button("⬇️ Retirer admin", use_container_width=True, key="demote"):
                if nb_admins <= 1:
                    st.error("Impossible : il doit rester au moins un admin.")
                else:
                    basculer_admin(target_id)
                    if is_self:
                        st.session_state.is_admin = False
                    st.success(f"{target_name} n'est plus admin.")
                    st.rerun()
        else:
            if st.button("👑 Promouvoir admin", use_container_width=True, key="promote"):
                basculer_admin(target_id)
                st.success(f"{target_name} est maintenant admin.")
                st.rerun()

    with col2:
        st.markdown("**Mot de passe**")
        with st.popover("🔑 Réinitialiser", use_container_width=True):
            new_pwd = st.text_input("Nouveau mot de passe", type="password", key=f"pwd_{target_id}")
            if st.button("Confirmer", key=f"pwd_btn_{target_id}"):
                ok, msg = reinitialiser_mot_de_passe(target_id, new_pwd)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    with col3:
        st.markdown("**Suppression**")
        if is_self:
            st.caption("⚠️ Tu ne peux pas te supprimer.")
            st.button("Supprimer", disabled=True, use_container_width=True)
        else:
            with st.popover("🗑️ Supprimer", use_container_width=True):
                st.warning(f"Supprimer **{target_name}** et toutes ses données ?")
                if st.button("Confirmer la suppression", type="primary", key=f"del_{target_id}"):
                    if target_is_admin and nb_admins <= 1:
                        st.error("Impossible : il doit rester au moins un admin.")
                    else:
                        supprimer_utilisateur(target_id)
                        st.success(f"{target_name} supprimé.")
                        st.rerun()


# ==================== MAIN ====================

def main():
    init_state()

    if st.session_state.user_id is None:
        page_auth()
        return

    sidebar_utilisateur()

    st.title("🏋️ Coach Sport & Nutrition")
    st.caption(f"Bienvenue **{st.session_state.username}** • Profil • IMC • Programmes • Suivi")

    onglets = ["👤 Profil & IMC", "⚡ Programme", "📜 Historique", "📈 Suivi calories"]
    if st.session_state.is_admin:
        onglets.append("🛠️ Administration")

    tabs = st.tabs(onglets)
    with tabs[0]:
        page_profil()
    with tabs[1]:
        page_programme()
    with tabs[2]:
        page_historique()
    with tabs[3]:
        page_suivi()
    if st.session_state.is_admin:
        with tabs[4]:
            page_admin()


main()
