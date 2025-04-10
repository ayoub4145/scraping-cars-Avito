from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.os_manager import ChromeType
import pandas as pd
import time

# Fonction pour obtenir le driver Firefox
def get_driver():
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")  

    # Retourner un driver Firefox
    return webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )
    
def scrape_voitures_selenium(budget, max_pages=2):

    driver = get_driver()
    voitures = []
    
    
    #page = 1
    #has_next_page = True

    # while has_next_page:
    for page in range(1, max_pages + 1):
        url = f"https://www.avito.ma/fr/maroc/voitures_d_occasion-à_vendre?o={page}"
        driver.get(url)
        time.sleep(3)  # laisser le temps au JS de charger

        # Récupérer tous les blocs d’annonces (chaque annonce est un lien <a>)
        ads = driver.find_elements(By.CSS_SELECTOR, '.sc-1jge648-0.jZXrfL')
        print(f"🔍 {len(ads)} annonces trouvées sur la page {page}")
        # if len(ads) == 0:
        #     has_next_page = False  # Si aucune annonce n'est trouvée, on arrête
        for ad in ads:
            try:
                title = ad.find_element(By.CSS_SELECTOR, '.sc-1x0vz2r-0.iHApav').text
                price_text = ad.find_element(By.CSS_SELECTOR, '.sc-1x0vz2r-0.dJAfqm.sc-b57yxx-3.eTHoJR').text
                image_url = ad.find_element(By.CSS_SELECTOR, '.sc-bsm2tm-3.krcAcS').get_attribute('src')
                link = ad.get_attribute('href')

                # Affichage du titre et du prix récupéré pour déboguer
                print(f"Titre: {title}")
                print(f"Prix récupéré: {price_text}")

                price = int(price_text.replace("DH", "").replace(" ", "").replace(" ", "").strip())

                if price <= budget:
                    voitures.append({
                        "Titre": title,
                        "Prix (DH)": price,
                        "Image": image_url,
                        "Lien": link
                    })

            except Exception as e:
                continue
        #page += 1  # Passer à la page suivante


    driver.quit()
    return pd.DataFrame(voitures)
