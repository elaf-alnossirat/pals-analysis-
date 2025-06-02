
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Palworld Dashboard", layout="wide")
st.title("🌐 Palworld Strategic Dashboard")

# Charger les données
df = pd.read_csv("dashboard_data_ready.csv")
df = df.drop_duplicates(subset='code_name')
df["power_score"] = df["hp"].fillna(0) + df["melee_attack"].fillna(0) + df["remote_attack"].fillna(0) + df["defense"].fillna(0)

# KPIs
total_pals = len(df)
avg_hp = round(df["hp"].mean(), 1)
avg_attack = round((df["melee_attack"] + df["remote_attack"]).mean(), 1)
avg_rarity = round(df["rarity"].mean(), 1)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🧬 Total Pals", total_pals)
col2.metric("❤️ HP Moyen", avg_hp)
col3.metric("⚔️ Attaque Moyenne", avg_attack)
col4.metric("💎 Rareté Moyenne", avg_rarity)

st.markdown("---")

# Filtres dans la sidebar
st.sidebar.header("🎛️ Filtres")

rarity_options = sorted(df["rarity"].dropna().unique())
selected_rarities = st.sidebar.multiselect("Rareté", rarity_options, default=rarity_options)

element_options = sorted(df["element_1"].dropna().unique())
selected_elements = st.sidebar.multiselect("Élément", element_options, default=element_options)

filtered_df = df[
    (df["rarity"].isin(selected_rarities)) &
    (df["element_1"].isin(selected_elements))
]

# Graphique top puissance
st.subheader("💥 Top 10 Pals les plus puissants")
top_power = filtered_df[["code_name", "power_score"]].sort_values(by="power_score", ascending=False).head(10)
fig = px.bar(top_power, x="code_name", y="power_score", color="power_score", labels={"code_name": "Pal", "power_score": "Puissance"}, color_continuous_scale="viridis")
fig.update_layout(xaxis_title="", yaxis_title="Puissance")
st.plotly_chart(fig, use_container_width=True)

# === Section Fiche Pal ===
st.markdown("### 🔎 Fiche détaillée d'un Pal")
selected_pal = st.selectbox("Choisir un Pal", df["code_name"].sort_values().unique())
pal_data = df[df["code_name"] == selected_pal].iloc[0]

with st.expander(f"📘 Détails pour {selected_pal}"):
    stats_cols = st.columns(4)
    stats_cols[0].metric("HP", pal_data["hp"])
    stats_cols[1].metric("Attaque mêlée", pal_data["melee_attack"])
    stats_cols[2].metric("Attaque à distance", pal_data["remote_attack"])
    stats_cols[3].metric("Défense", pal_data["defense"])

    st.write("**Rareté :**", pal_data["rarity"])
    st.write("**Élément :**", pal_data["element_1"])
    st.write("**Vitesse de course :**", pal_data["running_speed"])
    st.write("**Score de puissance :**", pal_data["power_score"])

# Tableau interactif
st.markdown("### 📋 Détails des Pals filtrés")
st.dataframe(filtered_df.sort_values(by="power_score", ascending=False), use_container_width=True)
