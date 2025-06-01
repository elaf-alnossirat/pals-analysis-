#  Pals Analysis - Analyse de données sur Palworld

##  Contexte

**Non, ce ne sont pas des Pokémon… ce sont des Pals !**  
Dans ce projet, on plonge dans l’univers de **Palworld (Eidolon Parlu)**, un jeu multijoueur de crafting, survie et exploration. À mi-chemin entre gestion de campement et baston de créatures, on s’est demandé :  
 *Et si on analysait ces fameuses bestioles pour optimiser notre stratégie ?*

---

##  Objectif

L’objectif principal : **analyser les données des Pals** à partir d’un dataset extrait du jeu.  
On veut mieux comprendre leurs caractéristiques, compétences, forces, faiblesses, et plus encore.  
Le tout, en mode data analyst / gamer 👾.

---

##  Données

Le projet repose sur **6 tables principales** importées dans une base de données MariaDB / MySQL :

- `combat-attribute`
- `job-skill`
- `hidden-attribute`
- `refresh-area`
- `ordinary-boss-attribute`
- `tower-boss-attribute`

Les données incluent des infos comme : attributs, rareté, taille, vitesse, compétences, zones d’apparition, comportement, etc.

---

##  Stack technique

- **Base de données :** MariaDB / MySQL
- **Manipulation & visualisation :** Python (Pandas, Matplotlib, Seaborn)
- **App Web interactive :** Streamlit
- **Outils complémentaires :** HeidiSQL, Jupyter Notebook

---

##  Étapes réalisées

1. **Installation de MariaDB** + création de la base `palworld_database`
2. **Import des 6 tables** dans la base
3. **Nettoyage & normalisation** des données
4. **Analyse exploratoire** avec SQL et Python :
   - Répartition des catégories, rareté, taille, HP, etc.
   - Analyse des compétences de travail
   - Corrélations entre stats de combat
   - Équilibrage d’équipe optimale
   - Pals adaptés au travail de nuit ou à la production
   - Strat de capture basée sur la probabilité
5. **Création d’une application Streamlit** nommée **Palstream** pour explorer les résultats de manière interactive

---

##  Résultats clés

Quelques exemples de ce qu’on a pu découvrir :

- Les 10 Pals les plus puissants selon leurs stats de combat
- La rareté moyenne des Pals les plus offensifs
- Les compétences les plus rares ou répandues
- Quels Pals sont les plus adaptés à la production ou au combat ?
- Une team équilibrée de 5 Pals pour survivre efficacement dans Palworld

---

##  Lancer le projet

1. **Clone le repo :**
   ```bash
   git clone https://github.com/ton-user/pals-analysis.git
   cd pals-analysis
