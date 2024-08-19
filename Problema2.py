import pandas as pd
import sqlite3
from sqlalchemy import create_engine

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

# Generacion de reportes

#Reporte 1

# Mejor vino puntuado por continente
report1 = df_renombrado.groupby('continente').apply(
    lambda x: x.loc[x['points'].idxmax()]
).reset_index(drop=True)

print("\nVinos mejor puntuados por continente:")
print(report1[['continente', 'title', 'points', 'price']])

#Reporte 2

# Promedio de precio de vino por país
report2 = df_renombrado.groupby('pais').agg({
    'price': 'mean',
}).reset_index().sort_values(by='price', ascending=False)

print("\nPromedio de precio de vino según país, ordenado por precio:")
print(report2)


#Reporte 3

# Agrupar por categoría 'Tier' y calcular el conteo y precio promedio
report3 = df_renombrado.groupby('Tier').agg({
    'title': 'count',
    'price': 'mean'
}).reset_index().rename(columns={'title': 'Number_of_Wines'}).sort_values(by='Number_of_Wines', ascending=False)

print("\nDistribución de vinos por categoría 'Tier':")
print(report3)

#Reporte 4

# Ordenar por precio y obtener los 10 vinos más caros por continente
top_10_expensive_wines = df_renombrado.sort_values(by=['continente', 'price'], ascending=[True, False]).groupby('continente').head(10)

print("\nTop 10 vinos más caros por continente:")
print(top_10_expensive_wines[['continente', 'title', 'price']])

# Exportando reportes a la carpeta 'reportes_generados'

# 1. CSV
report1.to_csv("./reportes_generados/report1_vinos_mejor_puntuados_por_continente.csv", index=False)
report2.to_csv("./reportes_generados/report2_promedio_precio_y_reviews_por_pais.csv", index=False)
report3.to_csv("./reportes_generados/report3_distribucion_por_categoria_tier.csv", index=False)
top_10_expensive_wines.to_csv("./reportes_generados/report4_top_10_vinos_mas_caros_por_continente.csv", index=False)

# 2. XLSX
report1.to_excel('./reportes_generados/report1_vinos_mejor_puntuados_por_continente.xlsx', index = False)
report2.to_excel("./reportes_generados/report2_promedio_precio_y_reviews_por_pais.xlsx", index=False)
report3.to_excel("./reportes_generados/report3_distribucion_por_categoria_tier.xlsx", index=False)
top_10_expensive_wines.to_excel("./reportes_generados/report4_top_10_vinos_mas_caros_por_continente.xlsx", index=False)

# 3. SQLITE
conn = sqlite3.connect("reportes.db") #los reportes irán a reportes.db dentro del repositorio
report1.to_sql("vinos_mejor_puntuados", conn, if_exists='replace', index=False)
report2.to_sql("promedio_precio_por_pais", conn, if_exists='replace', index=False)
report3.to_sql("distribucion_por_tier", conn, if_exists='replace', index=False)
top_10_expensive_wines.to_sql("top_10_vinos_caros", conn, if_exists='replace', index=False)
conn.close()

#ENVIO MASIVO DE CORREOS

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import os 
smtp_server = 'smtp.gmail.com'  # Cambia esto al servidor SMTP que estés utilizando
smtp_port = 587  # Cambia esto al puerto adecuado
sender_email = 'bchr1241@gmail.com'
sender_password = open('token.txt').read().strip() #os.environ['gmail_pass'] #

# Detalles del correo electrónico
receiver_email = 'bj.chavezr@alum.up.edu.pe'
subject = 'Re-envio Reporte Vinos'
body = 'Adjunto lo solicitado'

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Adjuntar archivo
file_path = './reportes_generados/report1_vinos_mejor_puntuados_por_continente.xlsx'  # Cambia la ruta al archivo que quieras adjuntar
with open(file_path, 'rb') as file:
    attachment = MIMEApplication(file.read(), _subtype="csv")
    attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
    msg.attach(attachment)

# Iniciar la conexión con el servidor SMTP
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Iniciar el modo seguro
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())

print('Correo enviado exitosamente')




