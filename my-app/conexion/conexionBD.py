

# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector
from mysql.connector.errors import Error


def connectionBD():
    try:
        # connection = mysql.connector.connect(
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="bd_consignaciones",

            # host="localhost",
            # user="root",
            # passwd="Pass23.-.*",
            # database="bd_consignaciones",

            # auth_plugin='mysql_native_password',
            # charset='utf8mb4',
            # collation='utf8mb4_unicode_ci'
            raise_on_warnings=True

        )
        if connection.is_connected():
            # print("Conexión exitosa a la BD")
            return connection

    # except mysql.connector.errors.InterfaceError:
        # Si se produce un error de conexión, significa que el servidor no está en línea
        # print("El servidor de MySQL está apagado")

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
