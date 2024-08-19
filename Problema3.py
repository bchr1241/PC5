import pandas as pd
import requests
import zipfile
import os

# URL del archivo ZIP
url = 'https://netsg.cs.sfu.ca/youtubedata/0303.zip'

# Realiza la solicitud para obtener el archivo ZIP
response = requests.get(url)

# Guardar el archivo ZIP en el disco
zip_file_path = '/workspaces/PC5/0303.zip'
with open(zip_file_path, 'wb') as f:
    f.write(response.content)

# Descomprimir el archivo ZIP
extract_folder = '/workspaces/PC5/descargas_problema3/'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Listar archivos en la carpeta descomprimida
extracted_files = os.listdir(extract_folder)
print(f"Archivos descomprimidos: {extracted_files}")

# Leer el archivo usando pandas
# Ajusta el nombre del archivo según sea necesario
for file_name in extracted_files:
    if file_name.endswith('.tsv') or file_name.endswith('.txt'):
        file_to_read = os.path.join(extract_folder, file_name)
        df = pd.read_csv(file_to_read, sep='\t')
        print(f"Contenido de {file_name}:")
        print(df.head())
