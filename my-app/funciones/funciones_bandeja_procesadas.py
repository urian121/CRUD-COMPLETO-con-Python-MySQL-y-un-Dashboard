from conexion.conexionBD import connectionBD  # Conexión a BD

from mysql.connector.errors import Error


# Funcion que retorna un diccionario de consignaciones leidas
def listaConsignacionesLeidasTiendaCpanel():
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)
    querySQL = ("""
                SELECT 
                    c.id, c.nombre_tienda, c.nota_consignacion, 
                    c.ip_consignacion, c.estatus_leido,
                    DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                    DATE_FORMAT(MIN(d.dia_venta), '%d de %b %Y') AS dia_de_la_ventaBD
                FROM consignaciones AS c
                INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                WHERE 
                c.bandeja = %s 
                AND estatus_leido = %s
                AND c.status_consignacion_ignorada=%s
                GROUP BY c.id, c.nombre_tienda, d.fecha_consignacion_banco
                ORDER BY c.id DESC
                LIMIT 15
                """)
    cursor.execute(querySQL, (1, 1, 0))
    consignacionesLeidasBD = cursor.fetchall()
    conexion_MySQLdb.commit()

    miDiccionarioConsigLeidas = {
        'consignacionesLeidasBD': consignacionesLeidasBD,
        'yearConsignaciones': yearConsignaciones(),
        'totalConsigSinLeer': totalConsigNoLeidas()
    }
    return miDiccionarioConsigLeidas


def load_more_consignaciones_procesadas(ultimoId, valorYear, valorMes):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        c.id, c.code_tienda, c.ip_consignacion,
                        c.nombre_tienda, c.nota_consignacion, 
                        DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                        DATE_FORMAT(d.dia_venta, '%d de %b %Y') AS dia_de_la_ventaBD
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                    WHERE c.id < %s
                    AND YEAR(d.fecha_consignacion_banco)=%s
                    AND MONTH(d.fecha_consignacion_banco)=%s
                    AND c.bandeja=%s
                    AND c.status_consignacion_ignorada=%s
                    ORDER BY c.id DESC LIMIT 15
                """
                cursor.execute(querySQL, (ultimoId, valorYear, valorMes, 1, 0))
                consignaciones = cursor.fetchall()
        return consignaciones or []

    except Exception as e:
        print(f"Ocurrió un load more consignaciones: {e}")
        return {}


# Obtener todas las consignaciones procesadas por una fecha en especifico
def getAll_consignaciones_por_fecha_especifica(fechaFitro):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                    SELECT 
                        c.id, c.nombre_tienda, c.nota_consignacion, 
                        c.ip_consignacion, c.estatus_leido,
                        DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                        DATE_FORMAT(d.dia_venta, '%d de %b %Y') AS dia_de_la_ventaBD
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                    WHERE d.dia_venta = %s AND c.bandeja = %s AND c.estatus_leido = %s
                    ORDER BY c.id DESC
                """
                mycursor.execute(querySQL, (fechaFitro, 1, 1))
                consignacionesProcesadasBD = mycursor.fetchall()
                conexion_MySQLdb.commit()
                return consignacionesProcesadasBD or []
    except Exception as e:
        print(
            f"Ocurrió un error en  getAll_consignaciones_por_fecha_especifica: {e}")
        return []


# Resetear la lista de consignaciones Procesadas
def process_reset_consignaciones_procesadas():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                            SELECT 
                                c.id, c.nombre_tienda, c.nota_consignacion, 
                                c.ip_consignacion, c.estatus_leido,
                                DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                                DATE_FORMAT(MIN(d.dia_venta), '%d de %b %Y') AS dia_de_la_ventaBD
                            FROM consignaciones AS c
                            INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                            WHERE 
                            c.bandeja = %s 
                            AND estatus_leido = %s
                            AND c.status_consignacion_ignorada=%s
                            GROUP BY c.id, c.nombre_tienda, d.fecha_consignacion_banco
                            ORDER BY c.id DESC
                            LIMIT 15
                    """)
                mycursor.execute(querySQL, (1, 1, 0))
                consignacionesBD = mycursor.fetchall()
                return consignacionesBD or []

    except Exception as e:
        print(
            f"Ocurrió en la funcion process_reset_consignaciones_procesadas: {e}")
        return []


def process_filtro_procesadas_por_mes(mes, yearFiltro):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = (f"""
                        SELECT 
                            c.id, c.code_tienda, 
                            c.nombre_tienda, c.nota_consignacion, 
                            c.ip_consignacion, c.estatus_leido,
                            DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                            DATE_FORMAT(d.dia_venta, '%d de %b %Y') AS dia_de_la_ventaBD
                        FROM consignaciones AS c
                        INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                        WHERE YEAR(d.fecha_consignacion_banco) = CASE WHEN '{yearFiltro}' = '' THEN YEAR(CURDATE()) ELSE '{yearFiltro}' END 
                        AND MONTH(d.fecha_consignacion_banco) = '{mes}'
                        AND c.bandeja ='{1}' AND c.estatus_leido ='{1}'  ORDER BY c.id DESC
                        """)
                mycursor.execute(querySQL,)
                consignacionesProcesadasBD = mycursor.fetchall()
                return consignacionesProcesadasBD or []

    except Exception as e:
        print(f"Ocurrió un error en process_filtro_procesadas_por_mesn: {e}")
        return {}


# funcion mejorada para obtener el total de consignaciones no leidas y en bandejas de entrada
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


def yearConsignaciones():
    conexion_MySQLdb = connectionBD()  # Hago instancia a mi conexion desde la funcion
    mycursor = conexion_MySQLdb.cursor(dictionary=True)
    querySQL = (
        "SELECT DISTINCT YEAR(dia_venta) anio FROM detalles_consignaciones")
    mycursor.execute(querySQL)
    listaYearConsignaciones = mycursor.fetchall()
    mycursor.close()  # cerrrando conexion SQL
    conexion_MySQLdb.close()  # cerrando conexion de la BD
    return listaYearConsignaciones
