import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Configuration de la page
st.set_page_config(page_title="Analyse des Pals - Palworld", layout="wide")
st.title("\U0001F9E0 Analyse Stratégique des Pals - Palworld")

# Connexion à la base de données via SQLAlchemy
@st.cache_resource
def connect_to_database():
    url = "mysql+pymysql://root:root@localhost/palworld_database"
    engine = create_engine(url)
    return engine

engine = connect_to_database()

# Fonction d'exécution de requêtes
@st.cache_data
def run_query(query):
    return pd.read_sql(query, engine)

# Affichage des graphiques

def plot_bar(df, x_col, y_col, title, xlabel, ylabel, color='skyblue', rotation=45):
    fig, ax = plt.subplots()
    df.plot(kind="bar", x=x_col, y=y_col, legend=False, color=color, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=rotation)
    st.pyplot(fig)

def plot_hist(data, title, xlabel, ylabel, color='salmon'):
    fig, ax = plt.subplots()
    ax.hist(data, bins=20, color=color, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

# Tabs : Combat / Camp
combat_tab, camp_tab = st.tabs(["\U0001F6E1️ Optimisation Combat", "⚒️ Gestion de Campement"])

# ----- Onglet Combat ----- #
with combat_tab:
    st.subheader("⚔️ Analyse des Pals pour le Combat")

    # Filtres interactifs multiples avec case à cocher
    rarity_options = list(run_query("SELECT DISTINCT rarity FROM combat_attribute WHERE rarity IS NOT NULL AND rarity != '' ORDER BY CAST(rarity AS UNSIGNED);")["rarity"])
    show_all_rarities = st.checkbox("Afficher toutes les raretés", value=True)
    if show_all_rarities:
        rarity_filter = rarity_options
    else:
        rarity_filter = st.multiselect("Filtrer par raretés :", options=rarity_options, default=rarity_options)

    rarity_condition = "" if not rarity_filter else f"AND rarity IN ({', '.join([f'\'{r}\'' for r in rarity_filter])})"

    # Points de vie (HP) avec filtre
    query_hp = f"""
    SELECT hp FROM combat_attribute
    WHERE hp IS NOT NULL AND hp > 0 {rarity_condition};
    """
    df_hp = run_query(query_hp)
    plot_hist(df_hp["hp"], "Distribution des points de vie des Pals", "HP", "Nombre de Pals")

    # Rareté (graphique global)
    query_rarity = """
    SELECT rarity, COUNT(*) AS count
    FROM combat_attribute
    WHERE rarity IS NOT NULL AND rarity != ''
    GROUP BY rarity
    ORDER BY CAST(rarity AS UNSIGNED);
    """
    df_rarity = run_query(query_rarity)
    df_rarity["rarity"] = df_rarity["rarity"].astype(str)
    plot_bar(df_rarity, "rarity", "count", "Distribution de la rareté des Pals", "Rareté", "Nombre de Pals", color="goldenrod", rotation=0)

# ----- Onglet Campement ----- #
with camp_tab:
    st.subheader("⚒️ Répartition des Pals pour la Production")

    # Filtres interactifs multiples avec case à cocher
    size_options = list(run_query("SELECT DISTINCT size FROM hidden_attribute WHERE size IS NOT NULL AND size != ''; ")["size"])
    show_all_sizes = st.checkbox("Afficher toutes les tailles", value=True)
    if show_all_sizes:
        size_filter = size_options
    else:
        size_filter = st.multiselect("Filtrer par tailles :", options=size_options, default=size_options)

    size_condition = "" if not size_filter else f"AND size IN ({', '.join([f'\'{s}\'' for s in size_filter])})"

    # Taille
    query_size = f"""
    SELECT size, COUNT(*) AS count
    FROM hidden_attribute
    WHERE size IS NOT NULL AND size != '' {size_condition}
    GROUP BY size;
    """
    df_size = run_query(query_size)
    plot_bar(df_size, "size", "count", "Distribution des tailles de Pals", "Taille", "Nombre de Pals", color="skyblue")

    # Catégorie (Genus)
    query_genus = """
    SELECT genuscategory, COUNT(*) AS count
    FROM hidden_attribute
    WHERE genuscategory IS NOT NULL AND genuscategory != ''
    GROUP BY genuscategory
    ORDER BY count DESC;
    """
    df_genus = run_query(query_genus)
    plot_bar(df_genus, "genuscategory", "count", "Distribution des catégories de Pals", "Catégorie", "Nombre de Pals", color="lightgreen", rotation=90)
