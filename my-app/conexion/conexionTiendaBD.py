
""" 
Conexión a nueva BD para consultar todas las tiendas activas
"""
import pyodbc


def connBDAdminitracionFE():
    server = 'SRVDATA\SQLDATA'
    # server = '192.168.10.10\SQLDATA'
    database = 'BD_Administracion_FE'
    username = 'Aplicacion'
    password = 'AppData.90212023*'
    statusEncrypt = 'no'
    ODBC = 'SQL Server'
    # Producccion
    # ODBC = 'ODBC Driver 17 for SQL Server'

    try:
        conn_string = f'DRIVER={ODBC};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt={statusEncrypt};'
        connection = pyodbc.connect(conn_string)
        # print("Conexión exitosa a las TIENDAS connBDAdminitracionFE.")

        return connection

    except pyodbc.Error as e:
        print("Error al conectarse al servidor connBDAdminitracionFE:", e)
        return None
