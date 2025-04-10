from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time

def scrape_voitures_selenium(budget, max_pages=2):

    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    
    # Lancer le navigateur
   
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print(driver.title)
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
                    print(f"✅ Annonce retenue - Titre: {title} | Prix: {price} DH")  
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
    print(f"Nombre d'annonces trouvées (prix ≤ {budget} DH) : {len(voitures)}")

    return pd.DataFrame(voitures)
