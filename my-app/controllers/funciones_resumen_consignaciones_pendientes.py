from conexion.conexionBD import connectionBD  # Conexión a BD

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


# Filtrando las tiendas que no han realizado la consignacion con respecto a las que ya lo han hecho.
def encontrar_tiendas_no_ok(tiendas, tienda_OK):
    tiendas_no_ok = []  # Declarando una lista vacia
    tiendas_ok_ids = [tienda['code_tienda'] for tienda in tienda_OK]

    for tienda in tiendas:
        if tienda[0] not in tiendas_ok_ids:
            tiendas_no_ok.append(tienda)
    return tiendas_no_ok


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
