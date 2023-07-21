from conexion.conexionBD import connectionBD  # Conexión a BD
from conexion.conn_server import connBigData  # Conexion al servidor externo
# Conexion al servidor externo para consultar todas las tiendas activas
from conexion.conexionTiendaBD import connBDAdminitracionFE

from mysql.connector.errors import Error


# Función que retorna las tiendas que ya han consignado a la fecha actual.
def resumenConsignacionesRecibidas():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                    SELECT 
                        c.id, c.code_tienda,
                        c.valor_consignacion,
                        c.nombre_tienda,
                        MIN(d.dia_venta) AS dia_de_la_ventaBD
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                    WHERE 
                        d.dia_venta = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                        AND c.status_consignacion_ignorada = %s
                    GROUP BY c.id, c.code_tienda, c.valor_consignacion, c.nombre_tienda, d.dia_venta
                    ORDER BY c.id DESC
                """
                mycursor.execute(querySQL, (0,))
                resumen_consignaciones_diarias = mycursor.fetchall()
                if resumen_consignaciones_diarias:
                    return (resumen_consignaciones_diarias)
                else:
                    return {}

    except Exception as e:
        print(f"Ocurrió un error leyendo la consignación: {e}")
        return {}


# Funcion que retorna las tiendas con consignaciones pendientes a la fecha actual
def resumenConsignacionesPendientes():
    try:
        # Asegúrate de llamar a la función con paréntesis
        conexion_SQL_Server = connBDAdminitracionFE()
        if conexion_SQL_Server:
            with conexion_SQL_Server.cursor() as mycursor:
                querySQL = """
                    SELECT T.Codigo, REPLACE(S.serv_nombre, '\\SQLEXPRESS', '') VPN, T.Descripcion Tienda
                        FROM dbo.tbServidores S
                        INNER JOIN BD_BODEGAOLAP.dbo.tbDimTiendas T ON T.tien_id = S.tien_id
                        WHERE T.Activa=1
                    """
                mycursor.execute(querySQL)
                tiendas_activas = mycursor.fetchall()

                respuesta = encontrar_tiendas_no_ok(
                    tiendas_activas, resumenConsignacionesRecibidas())
            return respuesta

    except Exception as e:
        print(f"Ocurrió un error al buscar la tienda: {e}")
        return None


def resumenFiltroConsignacionesRecibidasDiariaBD(fechaFiltro):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                    SELECT
                        c.id, c.nombre_tienda, c.code_tienda,
                        d.id_consignacion, d.valor_venta, d.dia_venta
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                    WHERE d.dia_venta = %s
                    ORDER BY d.id_detalles_consignaciones DESC
                    """
                mycursor.execute(querySQL, (fechaFiltro,))
                resumen_consignaciones_diarias = mycursor.fetchall()

                return resumen_consignaciones_diarias or []

    except Exception as e:
        print(f"Ocurrió un error leyendo la consignación: {e}")
        return {}


# Funcion que retorna las tiendas con consignaciones pendientes a la fecha actual
def resumenFiltroConsignacionesPendientesDiarias(fechaFiltro):
    try:
        # Asegúrate de llamar a la función con paréntesis
        conexion_SQL_Server = connBDAdminitracionFE()
        if conexion_SQL_Server:
            with conexion_SQL_Server.cursor() as mycursor:
                '''
                querySQL = f"""
                   SELECT RES.Tienda
                        FROM(
                        SELECT T.dimid_tienda,T.Descripcion Tienda
                        FROM BD_BODEGAOLAP.dbo.tbDimTiendas T
                        LEFT JOIN (SELECT DISTINCT dimid_tienda 
                                    FROM BD_BIGDATA.dbo.DepositoTiendas 
                                    WHERE FechaDeposito='{fechaFiltro}'
                                    ) DT ON DT.dimid_tienda = T.dimid_tienda
                        WHERE T.Activa=1
                        AND DT.dimid_tienda IS NULL
                        )RES
                        WHERE RES.dimid_tienda NOT IN (399,392,388,309,312,378,260,57)
                    '''
                querySQL = """
                    SELECT T.Codigo, REPLACE(S.serv_nombre, '\\SQLEXPRESS', '') VPN, T.Descripcion Tienda
                        FROM dbo.tbServidores S
                        INNER JOIN BD_BODEGAOLAP.dbo.tbDimTiendas T ON T.tien_id = S.tien_id
                        WHERE T.Activa=1
                    """
                mycursor.execute(querySQL)
                tiendas_activas = mycursor.fetchall()

                respuesta = encontrar_tiendas_no_ok(
                    tiendas_activas, resumenFiltroConsignacionesRecibidasDiariaBD(fechaFiltro))
            return respuesta

    except Exception as e:
        print(
            f"Ocurrió un error resumenFiltroConsignacionesPendientesDiarias: {e}")
        return None


# Filtrando las tiendas que no han realizado la consignacion con respecto a las que ya lo han hecho.
def encontrar_tiendas_no_ok(tiendas, tienda_OK):
    tiendas_no_ok = []  # Declarando una lista vacia
    tiendas_ok_ids = [tienda['code_tienda'] for tienda in tienda_OK]

    for tienda in tiendas:
        if tienda[0] not in tiendas_ok_ids:
            tiendas_no_ok.append(tienda)
    return tiendas_no_ok


# Consultando API_BIGDATA *
def API_BIGDATA(codTienda, fechaConsig):
    try:
        conexion_SQL_Server = connBigData()
        if conexion_SQL_Server:
            with conexion_SQL_Server.cursor() as mycursor:
                # Convertir la lista de fechas en una cadena separada por comas ['2023-06-05', '2023-06-05']
                fechas = ', '.join(f"'{fecha}'" for fecha in fechaConsig)

                # Usar la cadena de fechas en la cláusula IN de la consulta SQL
                querySQL = f"""
                    SELECT 
                        IdDep, Tienda, ValorDeposito,
                        FechaDeposito, ValorVenta, Fecha as FechaVenta, 
                        ValorRecaudo, ValorBonos, ValorTotal
                    FROM DepositoTiendas 
                    WHERE Codigo = '{codTienda}'
                    AND FechaDeposito IN ({fechas})
                    """
                mycursor.execute(querySQL,)

                result = mycursor.fetchall()
                # Convirtiendo esta data en un diccionario
                # Obtiene los nombres de las columnas
                columns = [desc[0] for desc in mycursor.description]
                infoConsigTienda = [dict(zip(columns, row)) for row in result]

                return infoConsigTienda

        else:
            print("No se pudo conectar con la base de datos Big_data.")
            return []
    except Exception as e:
        print(
            f"Ocurrió un error al buscar las consignaciones en BIGDATA: {e}")
        return []


def totalConsigNoLeidas():
    conexion_MySQLdb = connectionBD()
    mycursor = conexion_MySQLdb.cursor()

    querySQL = (
        "SELECT COUNT(*) FROM consignaciones WHERE bandeja =%s AND status_consignacion_ignorada=%s")
    mycursor.execute(querySQL, (0, 0))
    total = mycursor.fetchone()[0]

    mycursor.close()
    conexion_MySQLdb.close()
    return total
