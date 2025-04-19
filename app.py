
import streamlit as st
import pandas as pd
import sqlite3
import os
from scraper_avito import scrape_voitures_selenium
from datetime import datetime, timedelta


st.set_page_config(page_title="Voitures Avito", layout="wide",page_icon="https://credit-immo.avito.ma/storage/pwa/avitosalaf/icons/384x384.png")
st.title("🚗 Recherche automatique de voitures sur Avito")

LAST_UPDATE_FILE = "last_update.txt"

def get_last_update():
    if not os.path.exists(LAST_UPDATE_FILE):
        return None
    with open(LAST_UPDATE_FILE, "r") as f:
        return datetime.fromisoformat(f.read().strip())

def set_last_update():
    with open(LAST_UPDATE_FILE, "w") as f:
        f.write(datetime.now().isoformat())

DB_PATH = "voitures.db"

if not os.path.exists(DB_PATH) or get_last_update() is None or datetime.now() - get_last_update() > timedelta(hours=24):
    st.info("🔄 Base de données introuvable ou obsolète. Lancement du scraping...")
    try:
        scrape_voitures_selenium()
        set_last_update()  # Mettre à jour la date de la dernière mise à jour
        st.success("✅ Scraping terminé et base de données mise à jour.")
    except Exception as e:
        st.error(f"❌ Une erreur s'est produite lors du scraping : {e}")

#  Choix du budget AVANT de charger les données
budget = st.slider("💰 Budget maximum (DH)",value=100000 ,min_value=10000, max_value=500000, step=5000)

# Charger les données filtrées depuis SQLite
@st.cache_data
def load_filtered_data(budget_max):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM voitures WHERE \"Prix\" <= ? ORDER BY \"Prix\" ASC"
    df = pd.read_sql_query(query, conn, params=(budget_max,))
    conn.close()
    return df


# Charger les données filtrées selon le budget
df_filtré = load_filtered_data(budget)

st.download_button(
    "📥 Télécharger les résultats (.csv)",
    df_filtré.to_csv(index=False).encode('utf-8'),
    "voitures_filtrées.csv",
    "text/csv"
)
if df_filtré.empty:
    st.warning(f"⚠️ Aucune voiture trouvée pour un budget ≤ {budget:,} DH.")
else:
    st.write(f"🔍 {len(df_filtré)} voiture(s) trouvée(s) pour un budget ≤ {budget:,} DH")
#  Affichage des résultats
for _, row in df_filtré.iterrows():
    with st.container():
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(row["Image"], width=180)
        with cols[1]:
            st.subheader(row["Titre"])
            st.write(f"💸 **Prix :** {row['Prix']:,} DH")
            st.markdown(f"[🔗 Voir l'annonce sur Avito]({row['Lien']})")
        st.markdown("---")