# test_scraper.py
from scraper_avito import scrape_voitures_selenium
import sqlite3
import pandas as pd

# Lancer le scraping
df = scrape_voitures_selenium() 

# Vérifie si la DataFrame n’est pas vide
if df.empty:
    print("❌ Aucun résultat scrappé.")
else:
    print(f"✅ {len(df)} lignes scrapées.")

# Vérifie si la table a bien été créée dans SQLite
try:
    conn = sqlite3.connect("voitures.db")
    result = pd.read_sql("SELECT * FROM voitures", conn)
    print("✅ Table 'voitures' trouvée dans la base !")
    print(result.head())
    conn.close()
except Exception as e:
    print(f"❌ Erreur en lisant la table 'voitures' : {e}")
