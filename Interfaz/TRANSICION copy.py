import glob
import re
import os
import mysql.connector
from datetime import datetime

# Conexión a la base de datos con usuario y contraseña
conn = mysql.connector.connect(
    host='195.235.211.197',
    database='pc2ishealther',
    user='pc2is_healther',
    password='pssihealthers'
)

import mysql.connector

# Obtener la lista de conexiones activas
active_connections = conn.cmd_refresh()


# Cerrar la conexión principal
conn.close()
