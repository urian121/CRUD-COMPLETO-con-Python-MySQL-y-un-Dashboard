import os
import re
from datetime import datetime
from flask import request
from os import path  # Modulo para obtener la ruta o directorio
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD
from conexion.conn_server import connBigData  # Conexion al servidor externo


# Funcion que retorna la validacion del peso del archivo
def procesarPesoArchivo(archivo):
    if archivo:
        # Validar el peso del archivo
        tam_max = 10 * 1024 * 1024  # 10 megabytes
        tam_archivo = len(archivo.read())
        archivo.seek(0)  # Regresar al inicio del archivo
        if tam_archivo > tam_max:
            return False
        else:
            return True


def procesarFile(file, mes_actual):
    try:
        # Nombre original del archivo
        filename = secure_filename(file.filename)

        extension = path.splitext(filename)[1]
        # Generando string de 60 ipico de caracteres
        # nuevoNameFile = uuid.uuid4().hex + uuid.uuid1().hex
        # Por defecto genera un string de 128 caracteres
        # nuevoNameFile = uuid.uuid4().hex + uuid.uuid4().hex + uuid.uuid4().hex + uuid.uuid4().hex

        # Creando un string de 100 caracteres
        nuevoNameFile = (uuid.uuid4().hex + uuid.uuid4().hex +
                         uuid.uuid4().hex + uuid.uuid4().hex)[:100]

        nombreFile = nuevoNameFile + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(
            basepath, '../static/consignment_files', mes_actual)

        # Validar si existe la ruta y crearla si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            # Dando permiso a la carpeta
            os.chmod(upload_dir, 0o755)

        # Construir la ruta completa de subida del archivo
        upload_path = os.path.join(upload_dir, nombreFile)
        file.save(upload_path)

        return nombreFile
    except Exception as e:
        print("Error al procesar archivo:", e)
        return None


# Detalles de consignación, desde la vista deTienda
def detallesConsignaciones(idConsignacion):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                  SELECT 
                      c.nombre_tienda, c.nota_consignacion,
                      c.url_archivo,
                      d.fecha_consignacion_banco,
                      SUM(d.valor_venta) AS total_valor_venta
                  FROM consignaciones AS c
                  INNER JOIN detalles_consignaciones AS d
                      ON c.id = d.id_consignacion
                  WHERE c.id = %s
                  AND c.status_consignacion_ignorada = %s
                  GROUP BY c.nombre_tienda, d.fecha_consignacion_banco
                  LIMIT 1
                """
                params = (idConsignacion, 0)
                cursor.execute(querySQL, params)
                resultadoQuery = cursor.fetchone()
        return resultadoQuery or []

    except Exception as e:
        print(f"Ocurrió un error, consignación no encontrada: {e}")
        return []


# Recibiendo varias consignaciones diarias y procesandolas.
def recibeInsertConsignacion(valor_consignacion, fechas_consig, fecha_consignacion_banco, name_archivo, miFile, nota_consignacion, code_tienda, ip_consignacion, nombre_tienda):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)

    # Concatenando la Fecha actual con Hora-Minutos-Segundos
    """
    hora_actual = datetime.now().strftime('%H:%M:%S')
    fecha_hora = '{} {}'.format(fecha_consignacion_banco, hora_actual)
    fecha_hora_formateada = datetime.strptime(
        fecha_hora, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    """
    fecha_objeto = datetime.strptime(fecha_consignacion_banco, "%d-%m-%Y")
    fecha_hora_formateada = fecha_objeto.strftime("%Y-%m-%d")

    # Obtener la lista de valores y fechas
    valores_enteros = []
    for valor in valor_consignacion:
        # eliminar los puntos y otros caracteres no numéricos
        cantidad_sin_puntos = re.sub('[^0-9]+', '', valor)
        # convertir a un número entero
        valor_entero = int(cantidad_sin_puntos)
        valores_enteros.append(valor_entero)

    fechas_consignacion = []
    for fecha in fechas_consig:
        # formatear la fecha
        fecha_consig = datetime.strptime(
            fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
        fechas_consignacion.append(fecha_consig)

    # Si es el primer Registro
    if len(valores_enteros) > 0:
        try:
            consignacion = valores_enteros[0]
            fecha_consig = fechas_consignacion[0]
            sql = ("INSERT INTO consignaciones(valor_consignacion, name_archivo, url_archivo, nota_consignacion, code_tienda, ip_consignacion, nombre_tienda) VALUES (%s, %s, %s, %s, %s, %s, %s)")
            valores = (consignacion,
                       name_archivo, miFile, nota_consignacion, code_tienda, ip_consignacion, nombre_tienda)
            cursor.execute(sql, valores)
            conexion_MySQLdb.commit()
            # Obtener el ultimo id del registro que fue insertado
            ultimo_id_consignacion = cursor.lastrowid

            # Si len(valores_enteros) > 1 es decir son varias consignaciones, no registro la primera consignacione la tabla de detalles_consignaciones la cual es es total de la consiginacion
            # pues esa se guarda en la tabla de consignaciones
            if (len(valores_enteros) > 1):
                for i in range(1, len(valores_enteros)):
                    consignacion = valores_enteros[i]
                    fecha_consig = fechas_consignacion[i]
                    sqlDetalles = (
                        "INSERT INTO detalles_consignaciones(id_consignacion, valor_venta, dia_venta, fecha_consignacion_banco) VALUES (%s, %s, %s, %s)")
                    valoresConsignaciones = (
                        ultimo_id_consignacion, consignacion, fecha_consig, fecha_hora_formateada)
                    cursor.execute(sqlDetalles, valoresConsignaciones)
                    conexion_MySQLdb.commit()
            else:
                # Si es una sola consignacion pues la guarda en la tabla de detalles_consignaciones
                for i in range(len(valores_enteros)):
                    consignacion = valores_enteros[i]
                    fecha_consig = fechas_consignacion[i]
                    sqlDetalles = (
                        "INSERT INTO detalles_consignaciones(id_consignacion, valor_venta, dia_venta, fecha_consignacion_banco) VALUES (%s, %s, %s, %s)")
                    valoresConsignaciones = (
                        ultimo_id_consignacion, consignacion, fecha_consig, fecha_hora_formateada)
                    cursor.execute(sqlDetalles, valoresConsignaciones)
                    conexion_MySQLdb.commit()

            # resultado_insert representa cualquier insert de alguna de las 2 tablas
            resultado_insert = cursor.rowcount  # retorna 1 o 0
            return resultado_insert

        finally:
            cursor.close()  # Cerrando conexion SQL
            conexion_MySQLdb.close()  # cerrando conexion de la BD


# Total de consignaciones no leidas
def totalConsigNoLeidas():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT * FROM consignaciones
                    WHERE estatus_leido =%s
                    AND bandeja= %s
                    AND status_consignacion_ignorada = %s
                """
                params = (0, 0, 0)
                cursor.execute(querySQL, params)
                data = cursor.fetchall()
                total = len(data)
        return total or []

    except Exception as e:
        print(f"Ocurrió un error, consignación no encontrada: {e}")
        return []


# Lista de consignaciones
def listaConsignacionesPorTienda():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                result_info_code = INFO_TIENDA_API_BIGDATA()

                ip_vpn_tienda = get_ip_address()
                if ip_vpn_tienda == "192.168.2.18":  # Don Jorge
                    ip_vpn_tienda = "10.0.8.152"
                if ip_vpn_tienda == "192.168.2.89":  # Urian
                    ip_vpn_tienda = "10.0.8.38"
                if ip_vpn_tienda == "127.0.0.1":  # Urian Local
                    ip_vpn_tienda = "10.0.8.159"
                if ip_vpn_tienda == "192.168.2.19":  # Deivis
                    ip_vpn_tienda = "10.0.8.145"

                querySQL = """
                    SELECT 
                        c.id, c.estatus_leido,
                        c.nombre_tienda,
                        d.fecha_consignacion_banco,
                        SUM(d.valor_venta) AS total_valor_venta
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d
                        ON c.id = d.id_consignacion
                    WHERE c.code_tienda = %s
                    AND c.status_consignacion_ignorada=%s
                    GROUP BY c.id, c.estatus_leido, c.nombre_tienda, d.fecha_consignacion_banco
                    ORDER BY c.id DESC
                    LIMIT 120
                """
                params = (result_info_code[0], 0)
                # print("Consulta SQL:", querySQL)
                # print("Parámetros:", params)
                cursor.execute(querySQL, params)
                listaConsignaciones = cursor.fetchall()
        return listaConsignaciones or []

    except Exception as e:
        print(f"Ocurrió un error al lista las consignacion por tienda: {e}")
        return {}


# Informacion tienda
def INFO_TIENDA_API_BIGDATA():
    try:
        conexion_SQL_Server = connBigData()
        if conexion_SQL_Server:
            with conexion_SQL_Server.cursor() as mycursor:

                ip_vpn_tienda = get_ip_address()
                if ip_vpn_tienda == "192.168.2.18":  # Don Jorge
                    ip_vpn_tienda = "10.0.8.152"
                if ip_vpn_tienda == "192.168.2.89":  # Urian
                    ip_vpn_tienda = "10.0.8.38"
                if ip_vpn_tienda == "127.0.0.1":  # Urian Local
                    ip_vpn_tienda = "10.0.8.159"
                if ip_vpn_tienda == "192.168.2.19":  # Deivis
                    ip_vpn_tienda = "10.0.8.145"

                querySQL = f"""
                    SELECT 
                        distinct
                        V.CodigoTienda,
                        T.Descripcion descripcion_tienda,
                        V.VPN
                    FROM BD_Administracion_FE.dbo.tbVPNTiendas V
                    INNER JOIN BD_BODEGAOLAP.dbo.tbDimTiendas T ON T.dimid_tienda = V.dimid_tienda
                    WHERE T.Activa=1
                    AND V.VPN='{ip_vpn_tienda}'
                    """
                mycursor.execute(querySQL, )
                result = mycursor.fetchone()
                return result or []
        else:
            print("No se encontro la Tienda.")
            return []
    except Exception as e:
        print(
            f"Error en consulta, tienda no encontrada: {e}")
        return []


# Lista de consignaciones grupales
def listaConsignacionesGrupales(idConsig):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT * FROM detalles_consignaciones 
                    WHERE id_consignacion =%s 
                    ORDER BY dia_venta DESC
                """
                cursor.execute(querySQL, (idConsig,))
                listaConsignacionesGrupales = cursor.fetchall()
        return listaConsignacionesGrupales or []

    except Exception as e:
        print(f"Ocurrió un load more consignaciones: {e}")
        return []


def get_ip_address():
    client_ip = request.remote_addr
    return client_ip
