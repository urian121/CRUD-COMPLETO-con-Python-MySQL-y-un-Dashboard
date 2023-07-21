import pyodbc


def connBigData():
    server = 'SRVDATA\SQLDATA'  # Reemplace la dirección IP con la suya
    database = 'BD_BIGDATA'  # Reemplace el nombre de la base de datos con la suya
    username = 'Aplicacion'  # Reemplace el nombre de usuario con el suyo si es necesario
    password = 'AppData.90212023*'
    statusEncrypt = 'no'
    ODBC = 'SQL Server'
    # Producccion
    # ODBC = 'ODBC Driver 17 for SQL Server'

    try:
        conn_string = f'DRIVER={ODBC};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt={statusEncrypt};'
        connection = pyodbc.connect(conn_string)
        # print("Conexión exitosa a las TIENDAS connBigData.")

        return connection

    except pyodbc.Error as e:
        print("Error al conectarse al servidor connBigData:", e)
        return None
