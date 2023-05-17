import glob
import re
import os
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
        host='195.235.211.197',
        database='pc2ishealther',
        user='pc2is_healther',
        password='pssihealthers'
    )

# Conexión a la base de datos con usuario y contraseña

c = conn.cursor()

# Directorio donde se encuentran los archivos de texto
directorio_general = 'Carpeta Testing'

# Obtener la lista de archivos de texto en el directorio
archivos = glob.glob(f'{directorio_general}/*.txt')

# Directorio donde se moverán los archivos procesados
# Iterar sobre cada carpeta de categoría


# Iterar sobre cada archivo
for archivo in archivos:
    nombre_base = os.path.splitext(archivo)[0]
    categoria = nombre_base.split("_")[1].capitalize()
    print(categoria)
    try:
        with open(archivo, 'r') as file:
            texto = file.read()
    except:
        with open(archivo, 'r', encoding='utf-8') as file:
            texto = file.read()
    try:
        # Extraer el título
        titulo_match = re.search(r"Titulo:(.*)\n", texto)
        titulo = titulo_match.group(1).strip()

        # Extraer el autor
        autor_match = re.search(r"Autor:(.*)\n", texto)
        autor = autor_match.group(1).strip()

        # Extraer la fecha de publicación
        fecha_match = re.search(r"Fecha Publicacion:(.*)\n", texto)
        fecha_publicacion_str = fecha_match.group(1).strip()
        fecha_publicacion = datetime.strptime(fecha_publicacion_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # Extraer el enlace
        enlace_match = re.search(r"Enlace:(.*)\n", texto)
        enlace = enlace_match.group(1).strip()

        # Extraer la entradilla
        entradilla_match = re.search(r"Entradilla:(.*)", texto)
        entradilla = entradilla_match.group(1).strip()

        try:
            # Insertar los valores en la base de datos
            sql = "INSERT INTO recetas (titulo, autor, enlace, fecha_publicacion, texto, categoria) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (titulo, autor, enlace, fecha_publicacion, entradilla, categoria)
            c.execute(sql, values)
        except Exception as e:
            print(os.path.basename(archivo))
            print(e)

        # Mover el archivo al directorio "Done"
        current_dir = os.getcwd()
        done_dir = os.path.join(current_dir, f'Done {categoria}')
        done_path = os.path.join(done_dir, os.path.basename(archivo))
        os.makedirs(done_dir, exist_ok=True)
        os.rename(archivo, done_path)
        print(f"El archivo {archivo} ha sido procesado y movido a la carpeta 'Done {categoria}' en el directorio actual.")

    except AttributeError:
        # Si el patrón regex no coincide, ignorar el archivo y pasar al siguiente
        print(f"El archivo {archivo} no tiene el formato esperado y será ignorado.")
        continue

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión a la base de datos
conn.close()

