from flask import session
from flask import send_file  # biblioteca o modulo send_file para forzar la descarga
from os import path  # Modulo para obtener la ruta o directorio
import datetime


from conexion.conexionBD import connectionBD  # Conexión a BD


from mysql.connector.errors import Error

import os
import openpyxl


def listaConsignacionesBandejaEntrada():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                        SELECT 
                            c.id, c.code_tienda, 
                            c.nombre_tienda, c.nota_consignacion, 
                            c.ip_consignacion, c.estatus_leido,
                            DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                            DATE_FORMAT(MIN(d.dia_venta), '%d de %b %Y') AS dia_de_la_ventaBD
                        FROM consignaciones AS c
                        INNER JOIN detalles_consignaciones AS d 
                        ON c.id = d.id_consignacion
                        WHERE c.bandeja =%s
                        AND c.status_consignacion_ignorada=%s
                        GROUP BY c.id, c.nombre_tienda, d.fecha_consignacion_banco
                        ORDER BY c.id DESC
                        LIMIT 10
                """)
                cursor.execute(querySQL, (0, 0))
                consignacionesBD = cursor.fetchall()

        fecha_actual = datetime.datetime.now().strftime('%d-%m-%Y')
        miDiccionarioConsigBandejaEntrada = {
            'hoy': fecha_actual,
            'consignacionesTiendaCpanel': consignacionesBD,
            'yearConsignaciones': yearConsignaciones()
        }

        return miDiccionarioConsigBandejaEntrada

    except Exception as e:
        print(f"Ocurrió un error al obtener las consignaciones: {e}")
        return {}


def load_more_bandeja_entrada(ultimoId, valorYear, valorMes):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        c.id, c.code_tienda, c.ip_consignacion,
                        c.nombre_tienda, c.nota_consignacion, c.estatus_leido,
                        DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco, 
                        DATE_FORMAT(d.dia_venta, '%d de %b %Y') AS dia_de_la_ventaBD
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d ON c.id = d.id_consignacion
                    WHERE c.id < %s
                    AND YEAR(d.fecha_consignacion_banco)=%s 
                    AND MONTH(d.fecha_consignacion_banco)=%s
                    AND c.bandeja=%s
                    AND c.status_consignacion_ignorada=%s
                    ORDER BY c.id DESC LIMIT 20
                """
                cursor.execute(querySQL, (ultimoId, valorYear, valorMes, 0, 0))
                consignaciones = cursor.fetchall()
        return consignaciones or []

    except Exception as e:
        print(f"Ocurrió un load more consignaciones: {e}")
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
