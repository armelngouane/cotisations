import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(page_icon="static/Logo_EEC.jpg")

# Titre de l'app
st.title("🔍 Cotisations Mensuelles CDC 2025")
st.write("Tapez une partie de votre nom (ex. : 'NGOUANE' ou 'Marie') et cliquez sur 'Rechercher' pour voir vos infos.")

# Charger le fichier Excel
@st.cache_data
def load_data():
    # Lire la feuille principale
    df_main = pd.read_excel('COTISATIONS MENSUELLES CDC 2025 AU 05-10-25.xlsx', sheet_name=0, header=0)
    
    # Supprimer les colonnes inutiles (duplicat et vide)
    df_main = df_main.drop(columns=['Noms et prénoms.1', 'Unnamed: 3'], errors='ignore')
    
    # Renommer les colonnes des mois pour simplifier (enlever 'Cotisations ')
    df_main = df_main.rename(columns={
        'Cotisations Janvier': 'Janvier',
        'Cotisations Février': 'Février',
        'Cotisations Mars': 'Mars',
        'Cotisations Avril': 'Avril',
        'Cotisations Mai': 'Mai',
        'Cotisations Juin': 'Juin',
        'Cotisations Juillet': 'Juillet',
        'Cotisations Aout': 'Août',
        'Cotisations Septembre': 'Septembre',
        'Cotisations Octobre': 'Octobre',
        'décémbre': 'Décembre'
        # 'Novembre' est déjà sans prefixe
    })
    
    # Nettoyer : garder seulement les lignes avec N° valide (gérer les floats comme 1.0)
    df_main = df_main[df_main['N°'].notna() & df_main['N°'].apply(lambda x: str(x).replace('.0', '').isdigit())]
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
            # Afficher les colonnes pertinentes, incluant les nouvelles
            columns_to_display = ['N°', 'Noms et prénoms', 'Soldes au 31/12/2024', 'Janvier', 'Février', 'Mars',
                                  'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre',
                                  'Novembre', 'Décembre', 'Soldes cumulés', 'CEPCA', 'TENUES', 
                                  'Fête de récolte ', 'PROMESSES', 'AGAPE']
            # Filtrer seulement les colonnes existantes pour éviter erreurs
            existing_columns = [col for col in columns_to_display if col in df_main.columns]
            st.dataframe(resultats[existing_columns], 
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
st.sidebar.write("- Pour les réclamations, notez les chiffres et contactez la trésorière.")