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
body:: before{
 content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background-image: url("data:image/jpeg;base64,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");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.25; /* transparence du fond (0 = invisible, 1 = opaque) */
    z-index: -1; /* derrière le contenu */
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
