import streamlit as st
from scraper_avito import scrape_voitures_selenium

st.title("🚗Voitures Avito")

budget = st.number_input("💰 Budget max (DH)", value=100000)

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
            st.image(row['Image'], width=300)
            st.markdown(f"### {row['Titre']}")
            st.markdown(f"💸 {row['Prix (DH)']} DH")
            st.markdown(f"[🔗 Voir annonce]({row['Lien']})")
            st.markdown("---")

