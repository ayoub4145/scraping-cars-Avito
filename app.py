import streamlit as st
from scraper_avito import scrape_voitures_selenium

st.set_page_config(
    page_title="Avito Car Scraper",  
    page_icon="https://play-lh.googleusercontent.com/buf02418eUSzj_A0nn21WCdC3qo8qKjju2DA4uYf5eQtEJ0QFtBHZJ120u-elJVT6Us",                     
    layout="wide",                       # or "centered"
    initial_sidebar_state="auto"        # or "expanded", "collapsed"
)
page_bg_img = '''
<style>
/* Image de fond avec opacité (transparence) */
[data-testid="stAppViewContainer"] {
    position: relative;
    background-image: url("https://e0.pxfuel.com/wallpapers/119/566/desktop-wallpaper-top-71-car-background-spot-new-super-car-thumbnail.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.75);  /* Couche blanche semi-transparente pour lisibilité */
    z-index: -1;
}

/* Header transparent avec flou */
[data-testid="stHeader"], .st-emotion-cache-18ni7ap {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title("🚗Voitures Avito")

budget = st.number_input("💰 Budget max (DH)", value=100000,step=50000)

if st.button("🔍 Chercher"):
    st.info("Chargement...")
    df = scrape_voitures_selenium(budget)

    if df.empty:
        st.warning("Aucune voiture trouvée.")
    else:
        # Bouton pour exporter en CSV
        st.subheader("Exporter les résultats")
        csv_button = st.download_button(
        label="📥 Exporter en CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="voitures_avito.csv",
        mime="text/csv"
        )
        for _, row in df.iterrows():
            if 'Image' in row and isinstance(row['Image'], str) and row['Image'].startswith(('http://', 'https://')):
                st.image(row['Image'], width=300)
            else:
                st.warning("Image non disponible")
            st.markdown(f"### {row['Titre']}")
            if 'Prix (DH)' in row and isinstance(row['Prix (DH)'], (int, float)):
                st.markdown(f"💸 {row['Prix (DH)']} DH")
            else:
                st.warning("Prix non disponible")
            st.markdown(f"[🔗 Voir annonce]({row.Lien})")
            st.markdown("---")
st.markdown("### À propos")
st.markdown("Cette application utilise le web scraping pour extraire des annonces de voitures d'occasion sur Avito. Les données sont récupérées en temps réel et affichées ici.")
st.markdown("**Note:** Veuillez respecter les conditions d'utilisation du site [Avito](https://www.avito.ma/) lors de l'utilisation de cette application.")
st.markdown("Développé par [Ayoub BERHILI](https://github.com/ayoub4145)")
