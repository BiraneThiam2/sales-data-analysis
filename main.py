#1. Importation des bibliothèques et chargement du dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('dataset_ventes_analyse_pandas.csv')



#2. Exploration des données
print("Les 10 premières lignes du DataFrame :")
print(df.head(10))

print("Le nb de ligne et de colonnes du DataFrame :")
print(df.shape)

print("Le type de données de chaque colonne du DataFrame :")
print(df.info())

print("Le résumé statistique du DataFrame :")
print(df.describe())

print("Les valeurs manquantes du DataFrame :")
print(df.isna().sum())

print("Les doublons: ")
print(df.duplicated().sum())



#3. Nettoyage des données

#Doublons
print("SUPPRIMONSONS LES DOUBLONS")
df = df.drop_duplicates()

#Valeurs manquantes
print("Traitons les valeurs manquantes")
df['Gender'] = df["Gender"].fillna(df["Gender"].mode()[0])
df['City'] = df["City"].fillna(df["City"].mode()[0])
df['Satisfaction'] = df["Satisfaction"].fillna(df["Satisfaction"].median())

#Normalisation du texte
print("Corrigeons les noms des villes")
df["City"] = df["City"].str.strip().str.lower()
df["City"] = df["City"].str.title()
df["City"] = df["City"].replace({"Thies": "Thiès"})

df["Payment_Method"] = df["Payment_Method"].str.strip().str.lower().str.title()
df["Payment_Method"] = df["Payment_Method"].replace({"Especes": "Espèces"})
df['Product'] = df["Product"].str.strip().str.lower().str.title()

#Dates
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

#Prix anormaux et manquants
print("Nombre de prix anormaux :", (df["Unit_Price"] <= 0).sum())
print("Nombre de prix manquants :", df["Unit_Price"].isna().sum())
mediane_prix = df.loc[df["Unit_Price"] > 0, "Unit_Price"].median()
df.loc[df["Unit_Price"] <= 0, "Unit_Price"] = mediane_prix
df["Unit_Price"] = df["Unit_Price"].fillna(mediane_prix)

#Ventes incoherentes
df_incoherent = df[
    ~np.isclose(df["Total_Sales"], df["Quantity"] * df["Unit_Price"])
]
print("Nombre de ventes incohérentes :", len(df_incoherent))

#Quantites anormales
print("Nombre de quantités anormales :", (df["Quantity"] <= 0).sum())
mediane_quantite = df.loc[df["Quantity"] > 0, "Quantity"].median()
df.loc[df["Quantity"] <= 0, "Quantity"] = mediane_quantite

df["Total_Sales"] = df["Quantity"] * df["Unit_Price"]

#Ages anormaux
condition = (df["Age"] < 18) | (df["Age"] > 90)
print("Les âges anormaux :", condition.sum())
df.loc[condition, "Age"] = np.nan
print("Âges manquants :", df["Age"].isna().sum())
df["Age"] = df["Age"].fillna(df["Age"].median())



#4. Analyse statistique
print("Etudions l'age des clients :")
print("Age moyen :", df["Age"].mean())
print("Age median :", df["Age"].median())
print("Age min :", df["Age"].min())
print("Age max :", df["Age"].max())
print("ecart type :", df["Age"].std())


print("Etudions les quantités vendues :")
print("Quantité moyenne :", df["Quantity"].mean())
print("Quantité mediane :", df["Quantity"].median())
print("Quantité min :", df["Quantity"].min())
print("Quantité max :", df["Quantity"].max())
print("ecart type :", df["Quantity"].std())


print("Etudions les prix unitaires :")
print("Prix unitaire moyen :", df["Unit_Price"].mean())
print("Prix unitaire median :", df["Unit_Price"].median())
print("Prix unitaire min :", df["Unit_Price"].min())
print("Prix unitaire max :", df["Unit_Price"].max())
print("ecart type :", df["Unit_Price"].std())


print("Etudions les ventes totales :")
print("Ventes totales moyennes :", df["Total_Sales"].mean())
print("Ventes totales medianes :", df["Total_Sales"].median())
print("Ventes totales min :", df["Total_Sales"].min())
print("Ventes totales max :", df["Total_Sales"].max())
print("Somme des ventes totales :", df["Total_Sales"].sum())
print("ecart type :", df["Total_Sales"].std())


print("Etudions la satisfaction des clients :")
print("Satisfaction moyenne :", df["Satisfaction"].mean())
print("Satisfaction mediane :", df["Satisfaction"].median())
print("Satisfaction min :", df["Satisfaction"].min())
print("Satisfaction max :", df["Satisfaction"].max())



#5. Visualisation
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

#Chiffre d'affaires par catégorie
ventes_categorie = df.groupby("Category")["Total_Sales"].sum()
axes[0,0].bar(ventes_categorie.index, ventes_categorie.values / 1_000_000, color="#3b6fb0")
axes[0,0].set_title("Chiffre d'affaires par catégorie")
axes[0,0].set_xlabel("Catégorie")
axes[0,0].set_ylabel("Chiffre d'affaires (millions)")

#Évolution mensuelle
ventes_mensuelles = df.groupby(df["Date"].dt.to_period("M"))["Total_Sales"].sum()
axes[0,1].plot(ventes_mensuelles.index.astype(str), ventes_mensuelles.values / 1_000_000, marker="o", color="blue")
axes[0,1].set_title("Évolution du chiffre d'affaires par mois")
axes[0,1].set_xlabel("Mois")
axes[0,1].set_ylabel("Chiffre d'affaires (millions)")
axes[0,1].tick_params(axis="x", rotation=45)

#Moyens de paiement
paiement = df['Payment_Method'].value_counts()
axes[1,0].pie(paiement.values, autopct='%1.1f%%', startangle=90, pctdistance=0.75)
axes[1,0].set_title("Répartition des moyens de paiement")
axes[1,0].legend(paiement.index, title="Moyens de paiement", loc="center left", bbox_to_anchor=(1, 0.5))

#Top 5 des produits
produits_vendus = df.groupby("Product")["Quantity"].sum().nlargest(5).sort_values()
axes[1,1].barh(produits_vendus.index, produits_vendus.values, color="orange")
axes[1,1].set_title("Top 5 des produits les plus vendus")
axes[1,1].set_xlabel("Quantité vendue")
axes[1,1].set_ylabel("Produit")

plt.tight_layout()



#6. Exportation et conclusion

#Export du dataset nettoyé et des graphiques
df.to_csv('dataset_ventes_analyse_pandas_cleaned.csv', index=False)
fig.savefig('graphiques_ventes.png', dpi=150)

#Interprétation des résultats
ca_total = df["Total_Sales"].sum()
print("CONCLUSION")
print("Chiffre d'affaires total :", ca_total)
print("Catégorie la plus rentable :", ventes_categorie.idxmax(),
      "(", round(ventes_categorie.max() / ca_total * 100, 1), "% du CA )")
print("Meilleur mois :", ventes_mensuelles.idxmax())
print("Mois le plus faible :", ventes_mensuelles.idxmin())
print("Moyen de paiement le plus utilisé :", paiement.idxmax())
print("Produit le plus vendu :", produits_vendus.idxmax())

plt.show()
