# app.py

import streamlit as st
import pandas as pd
import sqlite3
import os
from scraper_avito import scrape_voitures_selenium

st.set_page_config(page_title="🚗 Voitures Avito", layout="wide")
st.title("🚗 Recherche automatique de voitures sur Avito")

DB_PATH = "voitures.db"

# 🔁 Scraping si la base n'existe pas
if not os.path.exists(DB_PATH):
    st.info("🔄 Scraping en cours (1ère exécution)...")
    scrape_voitures_selenium()  

# 🎯 Choix du budget AVANT de charger les données
budget = st.slider("💰 Budget maximum (DH)", min_value=10000, max_value=500000, step=5000)

# 📦 Charger les données filtrées depuis SQLite
@st.cache_data
def load_filtered_data(budget_max):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM voitures WHERE \"Prix (DH)\" <= ? ORDER BY \"Prix (DH)\" ASC"
    df = pd.read_sql_query(query, conn, params=(budget_max,))
    conn.close()
    return df

# Charger les données filtrées selon le budget
df_filtré = load_filtered_data(budget)

st.write(f"🔍 {len(df_filtré)} voiture(s) trouvée(s) pour un budget ≤ {budget:,} DH")

# 🖼️ Affichage des résultats
for _, row in df_filtré.iterrows():
    with st.container():
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(row["Image"], width=180)
        with cols[1]:
            st.subheader(row["Titre"])
            st.write(f"💸 **Prix :** {row['Prix (DH)']:,} DH")
            st.markdown(f"[🔗 Voir l'annonce sur Avito]({row['Lien']})")
        st.markdown("---")

# 📥 Export CSV
st.download_button(
    "📥 Télécharger les résultats (.csv)",
    df_filtré.to_csv(index=False).encode('utf-8'),
    "voitures_filtrées.csv",
    "text/csv"
)
