# scraper_avito.py

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

def scrape_voitures_selenium(max_pages=100):
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

        voitures = []
        page = 1

        while True:
            url = f"https://www.avito.ma/fr/maroc/voitures_d_occasion-à_vendre?o={page}"
            print(f"📄 Chargement de la page {page} : {url}")

            driver.get(url)
            time.sleep(3)

            ads = driver.find_elements(By.CSS_SELECTOR, '.sc-1jge648-0.jZXrfL')
            print(f"🔍 Page {page} | {len(ads)} annonces trouvées")

            if len(ads) == 0 or page > max_pages:
                break

            for ad in ads:
                try:
                    title = ad.find_element(By.CSS_SELECTOR, '.sc-1x0vz2r-0.iHApav').text
                    price_text = ad.find_element(By.CSS_SELECTOR, '.sc-1x0vz2r-0.dJAfqm.sc-b57yxx-3.eTHoJR').text
                    image_url = ad.find_element(By.CSS_SELECTOR, '.sc-bsm2tm-3.krcAcS').get_attribute('src')
                    link = ad.get_attribute('href')
                    if "non" in price_text.lower():  # <-- ignore les prix non spécifiés
                     print(f"⚠️ Annonce sans prix : {title}")
                     continue
                    price = int(price_text.replace("DH", "").replace(" ", "").replace(" ", "").strip())

                    voitures.append({
                        "Titre": title,
                        "Prix (DH)": price,
                        "Image": image_url,
                        "Lien": link
                    })

                except Exception as e:
                    print(f"⚠️ Erreur lors de l'extraction des données : {e}")
                    continue

            page += 1

        driver.quit()
        if not voitures:
            print("❌ Aucune voiture scrapée. Vérifiez le site ou les sélecteurs.")
            return pd.DataFrame()

        print(f"✅ Scraping terminé. {len(voitures)} voitures collectées.")
        df = pd.DataFrame(voitures)
        print("🧪 Aperçu des données scrapées :")
        print(df.head())

        # Sauvegarde dans Excel
        df.to_csv("voitures.xlsx", index=False)

        # Sauvegarde dans SQLite
        try:
            with sqlite3.connect("voitures.db") as conn:
                dtype = {
                    "Titre": "TEXT",
                    "Prix (DH)": "INTEGER",
                    "Image": "TEXT",
                    "Lien": "TEXT"
                }
                df.to_sql("voitures", conn, if_exists="replace", index=False, dtype=dtype)
                print("💾 Données insérées dans la table 'voitures'")
        except Exception as e:
            print(f"❌ Erreur lors de l'insertion dans SQLite : {e}")
    finally:
        driver.quit()
        print("🛑 Fermeture du navigateur.")
        
    return df
