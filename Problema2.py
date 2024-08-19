import pandas as pd
df_winemag = pd.read_csv("./data/winemag-data-130k-v2.csv")

# Explorando el DataFrame

print(df_winemag.head()) #Viendo todo el dataframe

print(df_winemag.shape) #Explorando el tamaño del dataframe

print(df_winemag.columns) #Explorando las columnas del DF

print(df_winemag['taster_name'].head()) #Explorando el nombre de los catadores

print(df_winemag['description'].head()) #Explorando la descripcion de los vinos

# Renombrando columnas

df_renombrado = df_winemag.rename(columns={'Unnamed: 0' : 'Codigo', 'country' : 'pais', 'taster_name' : 'Sommelier'}) #Se cambian de nombre 3 columnas
print(df_renombrado.head())

# Creando columnas

def tier(points: int): #Creando una categoría en base al puntaje del vino
    if points >= 80 and points <= 84:
        return 'Tier 4'
    elif points >=85 and points <= 89:
        return 'Tier 3'
    elif points >=90 and points <= 94:
        return 'Tier 2'
    elif points >=95 and points <= 99:
        return 'Tier 1'
    else:
        return 'Tier S'

df_renombrado['Tier'] = df_renombrado.points.apply(tier)

df_renombrado.to_excel('./data/winemag0.xlsx', index = False)

df_paises = pd.read_csv("https://gist.githubusercontent.com/kintero/7d1db891401f56256c79/raw/a61f6d0dda82c3f04d2e6e76c3870552ef6cf0c6/paises.csv")

df_renombrado = pd.merge(df_renombrado, df_paises, how = "left", left_on= "pais", right_on="nombre") #Agregando columna de continente

print(df_renombrado.head())
print(df_renombrado.shape)

#df_renombrado.to_excel('./data/winemagggggg.xlsx', index = False)



