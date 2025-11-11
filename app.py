import streamlit as st
import pandas as pd
import numpy as np

# Logo de l'app
st.set_page_config(page_icon="static/Logo_EEC.jpg")


# Titre de l'app
st.title("🔍 Cotisations Mensuelles CDC 2025")
st.write("Tapez une partie de votre nom (ex. : 'NGOUANE' ou 'Marie') et cliquez sur 'Rechercher' pour voir vos infos.")

# Charger le fichier Excel
@st.cache_data
def load_data():
    # Lire la feuille principale (LISTE 1 et 2)
    df_main = pd.read_excel('COTISATIONS MENSUELLES CDC 2025 AU 05-10-25.xlsx', sheet_name=0, header=4)
    df_main.columns = ['N°', 'Noms et prénoms', 'Solde au 31/12/2024', 'Janvier', 'Février', 'Mars', 
                       'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 
                       'Renflouement caisse', 'Cotisations échues', 'Cotisations période', 
                       'Solde période', 'Solde cumulé', 'CEPCA']
    
    # Nettoyer : garder seulement les lignes avec N° valide
    df_main = df_main[df_main['N°'].notna() & df_main['N°'].apply(lambda x: str(x).isdigit() or pd.isna(x))]
    df_main = df_main.dropna(subset=['Noms et prénoms'])
    df_main = df_main[df_main['Noms et prénoms'] != 'TOTAL']  # Exclure les totaux
    
    # Lire les contributions supplémentaires (feuille 2)
    df_contribs = pd.read_excel('COTISATIONS MENSUELLES CDC 2025 AU 05-10-25.xlsx', sheet_name=1, header=None)
    df_contribs.columns = ['Nom', 'Montant', 'Description']
    df_contribs = df_contribs.dropna(subset=['Nom'])
    
    return df_main, df_contribs

df_main, df_contribs = load_data()

# Interface de recherche
nom_recherche = st.text_input("Entrez une partie de votre nom :", placeholder="Ex. : NGOUANE")
if st.button("🔍 Rechercher"):
    if nom_recherche:
        # Recherche insensible à la casse
        resultats = df_main[df_main['Noms et prénoms'].str.contains(nom_recherche, case=False, na=False)]
        
        if not resultats.empty:
            st.success(f"Trouvé {len(resultats)} résultat(s) :")
            st.dataframe(resultats[['N°', 'Noms et prénoms', 'Solde au 31/12/2024', 'Janvier', 'Février', 'Mars', 
                                    'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 
                                    'Solde cumulé', 'CEPCA']], 
                         use_container_width=True, hide_index=True)
            
            # Vérifier contributions supplémentaires
            contribs = df_contribs[df_contribs['Nom'].str.contains(nom_recherche, case=False, na=False)]
            if not contribs.empty:
                st.subheader("Contributions supplémentaires :")
                st.dataframe(contribs, use_container_width=True, hide_index=True)
        else:
            st.warning("Aucun résultat trouvé. Vérifiez l'orthographe ou essayez une autre partie du nom.")
    else:
        st.info("Veuillez entrer un nom pour rechercher.")

# Astuce pour l'utilisation
st.sidebar.title("💡 Astuces")
st.sidebar.write("- Tapez au moins 3-4 lettres pour de meilleurs résultats.")
st.sidebar.write("- Si plusieurs personnes ont des noms similaires, tous s'afficheront.")