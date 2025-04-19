from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from webdriver_manager.core.os_manager import ChromeType
import pandas as pd
import time
import sqlite3

def scrape_voitures_selenium():
    driver = None
    conn = None
    try:
        print("🚀 Démarrage du scraping...")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-dev-shm-usage")

        try:
        #     service = EdgeService(executable_path="msedgedriver.exe")
        #     driver = webdriver.Edge(service=service, options=options)
            driver = uc.Chrome(options=options)
        except Exception as e:
            print("❌ Erreur WebDriver :", e)
            return pd.DataFrame()
                # Connexion à la base SQLite
        conn = sqlite3.connect("voitures.db")
        cursor = conn.cursor()

        # Création de la table si elle n'existe pas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS voitures (
            Titre TEXT,
            Prix INTEGER,
            Image TEXT,
            Lien TEXT UNIQUE
        )
        """)
        conn.commit()

        voitures = []
        page = 1

        while True:
            url = f"https://www.avito.ma/fr/maroc/voitures_d_occasion-à_vendre?o={page}"
            print(f"📄 Chargement de la page {page} : {url}")

            driver.get(url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            import random
            time.sleep(random.uniform(3, 6))
            ads = driver.find_elements(By.CSS_SELECTOR, '.sc-1jge648-0.jZXrfL')
            print(f"🔍 Page {page} | {len(ads)} annonces trouvées")

            if len(ads) == 0:
                print("Fin de Scraping sur toutes les pages.")
                break

            for ad in ads:
                try:
                    title = ad.find_element(By.CSS_SELECTOR, '.sc-1x0vz2r-0.iHApav').text
                    price_text = ad.find_element(By.CSS_SELECTOR, '.sc-1x0vz2r-0.dJAfqm.sc-b57yxx-3.eTHoJR').text
                    image_url = ad.find_element(By.CSS_SELECTOR, '.sc-bsm2tm-3.krcAcS').get_attribute('src')
                    link = ad.get_attribute('href')
                    if "non" in price_text.lower(): 
                     print(f"⚠️ Annonce sans prix : {title}")
                     continue
                    price = int(price_text.replace("DH", "").replace(" ", "").replace(" ", "").strip())

                    voitures.append({
                        "Titre": title,
                        "Prix (DH)": price,
                        "Image": image_url,
                        "Lien": link
                    })
                    
                                        # Insérer directement dans la base SQLite
                    try:
                        cursor.execute("""
                        INSERT INTO voitures (Titre, Prix, Image, Lien)
                        VALUES (?, ?, ?, ?)
                        """, (title, price, image_url, link))
                        conn.commit()
                        print(f"💾 Annonce ajoutée : {title}")
                    except sqlite3.IntegrityError:
                        print(f"⚠️ Annonce déjà présente dans la base : {title}")

                except Exception as e:
                    print(f"⚠️ Erreur lors de l'extraction des données : {e}")
                    continue

            page += 1
        print("✅ Scraping terminé.")

        if not voitures:
            print("❌ Aucune voiture scrapée. Vérifiez le site ou les sélecteurs.")
            return pd.DataFrame()

        print(f"✅ Scraping terminé. {len(voitures)} voitures collectées.")
        df = pd.DataFrame(voitures)
        print("🧪 Aperçu des données scrapées :")
        print(df.head())

        # Sauvegarde dans Excel
        #df.to_csv("voitures.xlsx", index=False)

        # Sauvegarde dans SQLite
        try:
            with sqlite3.connect("voitures.db") as conn:
                # Charger les données existantes
                existing_df = pd.read_sql_query("SELECT * FROM voitures", conn)
                print(f"📂 {len(existing_df)} annonces déjà présentes dans la base.")

                # Identifier les nouvelles annonces
                new_df = df[~df['Lien'].isin(existing_df['Lien'])]
                print(f"🆕 {len(new_df)} nouvelles annonces à ajouter.")

                # Ajouter uniquement les nouvelles annonces
                if not new_df.empty:
                    new_df.to_sql("voitures", conn, if_exists="append", index=False)
                    print("💾 Nouvelles annonces ajoutées à la base.")
                else:
                    print("✅ Aucune nouvelle annonce à ajouter.")
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion dans SQLite : {e}")
    finally:
        if driver:
            print("🛑 Fermeture du navigateur.")
            driver.quit()
        if conn:
            print("🔒 Fermeture de la connexion SQLite."    )
            conn.close()     
    return df
