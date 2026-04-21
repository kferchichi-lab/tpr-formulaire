import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
st.set_page_config(page_title="Saisie Arrêts TPR", page_icon="📝")

# Connexion à Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- STYLE CSS ---
st.markdown("""
    <style>
        .stButton > button {
            width: 100%; height: 3em; border-radius: 10px;
            background: linear-gradient(135deg, #0047AB 0%, #00264d 100%);
            color: white; font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ET TITRE ---
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6q1BtDSDgVnJZFo0hOBfQJoDS6OYiub-qfQ&s", width=100)
st.title("Saisie d'incident")

# --- FORMULAIRE ---
presse = st.selectbox("SÉLECTIONNER LA PRESSE :", ["Presse 4", "Presse 6", "Presse 7"], index=None)

if presse:
    with st.form("form_saisie", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date_j = st.date_input("Date", datetime.now())
            poste = st.radio("Poste", ["A", "B", "C"], horizontal=True)
            ref_filiere = st.text_input("Référence Filière")
        
        with col2:
            num_lopin = st.text_input("Numéro du lopin")
            duree = st.number_input("Durée (min)", min_value=1)
            cause = st.selectbox("Cause", ["T - Température", "H - Hydraulique", "O - Outillage", "R - Raclage"])

        obs = st.text_area("Observations")
        submit = st.form_submit_button("ENREGISTRER")

        if submit:
            if not ref_filiere or not num_lopin:
                st.error("Remplissez tous les champs !")
            else:
                # Préparation de la ligne
                nouvelle_ligne = pd.DataFrame([{
                    "Date": date_j.strftime("%d/%m/%Y"),
                    "Heure_Saisie": datetime.now().strftime("%H:%M:%S"),
                    "Presse": presse,
                    "Poste": poste,
                    "Filiere": ref_filiere,
                    "Lopin": num_lopin,
                    "Duree_Min": duree,
                    "Cause": cause,
                    "Observations": obs
                }])
                
                # Lecture et ajout
                existing_data = conn.read(worksheet="Feuille 1")
                updated_df = pd.concat([existing_data, nouvelle_ligne], ignore_index=True)
                conn.update(worksheet="Feuille1", data=updated_df)
                
                st.success("✅ Incident enregistré avec succès !")
                st.snow()
