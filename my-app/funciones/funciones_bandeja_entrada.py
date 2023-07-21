from flask import session
from flask import send_file  # biblioteca o modulo send_file para forzar la descarga
from os import path  # Modulo para obtener la ruta o directorio
import datetime


from conexion.conexionBD import connectionBD  # Conexión a BD
from conexion.conn_server import connBigData  # Conexion al servidor externo


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


# Función que busca los detalles de la consignación seleccionada desde la bandeja de entrada.
def detallesConsignacionCpanel(idConsignacion):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        c.id, c.code_tienda, c.nombre_tienda, 
                        c.valor_consignacion, c.nota_consignacion, 
                        c.name_archivo, c.url_archivo,
                        d.dia_venta, d.fecha_consignacion_banco, 
                        DATE(d.fecha_registro) AS fecha_registro
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d
                        ON c.id = d.id_consignacion
                    WHERE c.id = %s
                    AND c.status_consignacion_ignorada = %s
                    LIMIT 1
                """
                cursor.execute(querySQL, (idConsignacion, 0))
                listaConsignaciones = cursor.fetchone()

                if listaConsignaciones:
                    # Obtener el código de la tienda
                    codTienda = listaConsignaciones['code_tienda']

                    # Consulta y Verifico si existen mas de 1 consignacion para obtener detalles de la consignación
                    fechas_consignaciones = (
                        consignaciones_grupales_por_fecha_BD(idConsignacion))
                    # print(fechas_consignaciones) # Ejemplo ['2023-6-1', '2023-6-8']

                    # Llamar a la función API_BIGDATA
                    resp_server_sql = API_BIGDATA(
                        codTienda, fechas_consignaciones)

                    # Actualizar el estatus de la consignación
                    updateStatusConsignacion(idConsignacion)

                    # Consulta para obtener detalles deo las consignaciones
                    detalleConsignaciones = detalles_consignacionesBD(
                        idConsignacion)

                    # Validar si alguna de estas variables (listaConsignaciones, resp_server_sql, detalleConsignaciones) está vacía
                    # Retornar una lista vacía en ese caso, de lo contrario, retornar el valor de la variable.
                    return (
                        listaConsignaciones or [],
                        resp_server_sql or [],
                        detalleConsignaciones or []
                    )
                else:
                    # Retornar listas vacías
                    return [], [], []

    except Exception as e:
        print(f"Ocurrió un error al leer la consignación: {e}")
        return None


'''
 Buscar todas las fechas (dia_venta) a la cuál pertenece el 'idConsignacion', esto retornará:
 una ['2023-6-1'] o más de una fecha ['2023-6-1', '2023-6-8', '2023-6-8'], cuando retorna más de una fecha indica que 
 dicha consignación es grupal, es decir pertenece a varios dias.
 Estas fecha se deben envia al POS para extraer la información de la consignación de acuerdo al POST
'''


def consignaciones_grupales_por_fecha_BD(idConsignacion):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT DATE_FORMAT(dia_venta, '%Y-%c-%e') AS dia_de_la_venta 
                FROM detalles_consignaciones 
                WHERE id_consignacion = %s
                """
                cursor.execute(querySQL, (idConsignacion,))
                dataDetallesBD = cursor.fetchall()
                if dataDetallesBD is not None:
                    fechas = list(row['dia_de_la_venta']
                                  for row in dataDetallesBD)
                    return fechas  # ['2023-6-1', '2023-6-8']
                else:
                    print(
                        "No se encontraron detalles de consignaciones para el id especificado")
                    return []
    except Exception as e:
        print(
            f"Ocurrió un error al leer los detalles de la consignación: {e}")
        return None


# Detalles de consignaciones grupales
def detalles_consignacionesBD(idConsignacion):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT dia_venta, valor_venta FROM detalles_consignaciones WHERE id_consignacion = %s"
                cursor.execute(querySQL, (idConsignacion,))
                dataDetallesBD = cursor.fetchall()
        return dataDetallesBD or []
    except Exception as e:
        print(
            f"Ocurrió un error al leer los detalles de la consignación: {e}")
        return None


# Actualizando el estado de la consignación ha 'leida'
def updateStatusConsignacion(idConsignacion):
    conexion_MySQLdb = connectionBD()  # Hago instancia a mi conexion desde la funcion
    mycursor = conexion_MySQLdb.cursor(dictionary=True)
    mycursor.execute("""
            UPDATE consignaciones
            SET
                estatus_leido = %s
            WHERE id = %s
            """, (1, idConsignacion))
    conexion_MySQLdb.commit()
    mycursor.close()  # cerrando conexion de la consulta sql
    conexion_MySQLdb.close()  # cerrando conexion de la BD
    resultado_update = mycursor.rowcount  # retorna 1 o 0
    return resultado_update


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


# Forzar descarga de la imagen consignación
def process_descarga_imagen_consignacion(idFileBD):
    basepath = path.dirname(__file__)
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)

    cursor.execute(
        "SELECT url_archivo FROM consignaciones WHERE id = %s", (idFileBD,))
    resultadoQuery = cursor.fetchone()
    # es una expresión condicional que se utiliza para asignar un valor a la variable "rutaFileBD"
    # dependiendo del resultado de la consulta a la base de datos
    ''' 
        Si el resultado de la consulta no es nulo y contiene el campo "url_archivo".
        En caso contrario, se asigna el valor "None" a "rutaFileBD". La expresión condicional se utiliza para manejar 
        los casos en los que el resultado de la consulta puede ser nulo o no contener el campo "url_archivo".
        '''
    rutaFileBD = resultadoQuery['url_archivo'] if resultadoQuery and 'url_archivo' in resultadoQuery else None

    url_File = path.join(
        basepath, '../static/' + rutaFileBD)
    return send_file(url_File, as_attachment=True)


# Mover una consignación desde la bandeja de entrda a consignaciones procesadas
def process_mover_consignacion(idConsignacion):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                        UPDATE consignaciones
                        SET 
                            bandeja = %s
                        WHERE id=%s
                    """
                cursor.execute(querySQL, (1, idConsignacion,))
                conexion_MySQLdb.commit()
        return cursor.rowcount or []
    except Exception as e:
        print(
            f"Ocurrió un error al leer los detalles de la consignación: {e}")
        return None


# Ingnorar consignación
def process_ignorar_consignacion(idConsignacion):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    UPDATE consignaciones
                    SET 
                        status_consignacion_ignorada = %s
                    WHERE id=%s
                    """
                cursor.execute(querySQL, (1, idConsignacion,))
                conexion_MySQLdb.commit()
        return cursor.rowcount or []

    except Exception as e:
        print(
            f"Ocurrió un error al ignorar la consignación: {e}")
        return None


def process_resetBandejaEntrada():
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
        return consignacionesBD or []
    except Exception as e:
        print(
            f"Errro en la funcion process_resetBandejaEntrada: {e}")
        return None


def process_filtro_consignacion_por_mes(mes, yearFiltro):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
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
                    AND c.bandeja ='{0}'
                    AND c.status_consignacion_ignorada = '{0}'
                    ORDER BY id DESC LIMIT 10
                    """)
                cursor.execute(querySQL,)
                consignacionesBD = cursor.fetchall()
        return consignacionesBD or []
    except Exception as e:
        print(
            f"Errro en la funcion process_filtro_consignacion_por_mes: {e}")
        return None


def process_filtrar_consignacion_por_fecha_especifica(fechaFitro):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT 
                        c.id, c.nombre_tienda, c.nota_consignacion, 
                        c.ip_consignacion, c.estatus_leido,
                        DATE_FORMAT((d.fecha_consignacion_banco), '%d de %b %Y') AS fecha_consignacion_banco,
                        DATE_FORMAT(d.dia_venta, '%d de %b %Y') AS dia_de_la_ventaBD
                    FROM consignaciones AS c
                    INNER JOIN detalles_consignaciones AS d 
                        ON c.id = d.id_consignacion
                    WHERE d.dia_venta = %s 
                        AND c.bandeja = %s
                    ORDER BY id DESC
                """
                cursor.execute(querySQL, (fechaFitro, 0))
                consignacionesBandejaEntrada = cursor.fetchall()
        return consignacionesBandejaEntrada or []
    except Exception as e:
        print(
            f"Errro en la funcion process_filtrar_consignacion_por_fecha_especifica: {e}")
        return None


def process_consignaciones_checkbox(idsConsigChecked):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                for idconsignacion in idsConsigChecked:
                    querySQL = """
                        UPDATE consignaciones
                        SET 
                            bandeja = %s
                        WHERE id=%s
                        """
                    cursor.execute(querySQL, (1, idconsignacion,))
                    conexion_MySQLdb.commit()
        return cursor.rowcount or []

    except Exception as e:
        print(
            f"Ocurrió en la funcion process_consignaciones_checkbox: {e}")
        return None


# Procesar las consultas para crear el informe general desde la bandeja de entrada
def creando_consultas_para_descarga_informe_general(fecha_dia_venta):
    if fecha_dia_venta:
        # Consulta para obtener detalles de todas las consignaciones de acuerdo a una fecha en especifico
        detalleConsignaciones = detalles_consignaciones_informeGeneral(
            fecha_dia_venta)
        # print(f"Caso 2: {detalleConsignaciones}")

        # Llamar a la función API_BIGDATA_INFORME_GENERAL
        resp_server_sql = API_BIGDATA_INFORME_GENERAL(fecha_dia_venta)
        # print(f"Caso 1: {resp_server_sql}")

        return detalleConsignaciones or [], resp_server_sql or []


# Detalles consignaciones para el informe general, de acuerdo a una fecha en especifico
def detalles_consignaciones_informeGeneral(fecha_dia_venta):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT dia_venta, valor_venta FROM detalles_consignaciones WHERE dia_venta = %s"
                cursor.execute(querySQL, (fecha_dia_venta,))
                dataDetallesBD = cursor.fetchall()
        return dataDetallesBD or []
    except Exception as e:
        print(f"Error buscando consignaciones para Inf.Genral: {e}")
        return []


# Consultando API_BIGDATA para general un infome general de todas las consignaciones por una fecha unica *
def API_BIGDATA_INFORME_GENERAL(fechaConsig):
    try:
        conexion_SQL_Server = connBigData()
        if conexion_SQL_Server:
            with conexion_SQL_Server.cursor() as mycursor:
                querySQL = f"""
                    SELECT 
                        IdDep, Tienda, ValorDeposito,
                        FechaDeposito, ValorVenta, Fecha as FechaVenta, 
                        ValorRecaudo, ValorBonos, ValorTotal
                    FROM DepositoTiendas 
                    WHERE FechaDeposito = ('{fechaConsig}')
                    """
                mycursor.execute(querySQL,)
                result = mycursor.fetchall()

                # Convirtiendo esta data en un diccionario
                # Obtiene los nombres de las columnas
                columns = [desc[0] for desc in mycursor.description]
                infoConsigTienda = [dict(zip(columns, row)) for row in result]
                return infoConsigTienda
        else:
            print("No se pudo conectar con la base de datos Big_data reporteGeneral.")
            return []
    except Exception as e:
        print(f"Ocurrió un error en Big_data reporteGeneral: {e}")
        return []


# Descargar Informe general desde la bandeja entrada
def reporte_informe_general(data):
    resultado = []  # Definiendo una lista vacia
    # Iterando sobre un diccionario
    for fecha, registros in data.items():
        for registro in registros:
            datos = {}  # Definiendo un diccionario vacio
            datos['Fecha'] = fecha
            for clave, valor in registro.items():
                datos[clave] = valor
            resultado.append(datos)

    # Crear el libro de Excel
    wb = openpyxl.Workbook()
    hoja = wb.active

    # Agregar la fila de encabezado con los títulos
    hoja.append(('NOMBRE DE LA TIENDA', 'FECHA VENTA', 'VENTA POST', 'CONSIGNACIÓN POS', 'VALOR VENTA', 'VALOR RECAUDOS', 'VALOR BONOS',
                'CONSIGNACIÓN TIENDA', 'DIFERENCIA'))

    # Agregar los registros a la hoja
    # for registro in registros:  Itero sobre una Lista
    for registro in resultado:
        # print(f"aqui {registro}")
        tienda = registro['Tienda']
        fecha_venta = registro['Fecha']

        venta_post = "{:,.0f}".format(
            registro['ValorTotal']).replace(",", ".")  # Venta Pos ValorTotal
        ValorDeposito = "{:,.0f}".format(
            registro['ValorDeposito']).replace(",", ".")  # Consignación Pos

        valor_venta = registro['valor_venta']  # Consignación Tienda

        ValorVenta = "{:,.0f}".format(
            registro['ValorVenta']).replace(",", ".")  # Valor Venta
        ValorRecaudo = "{:,.0f}".format(
            registro['ValorRecaudo']).replace(",", ".")  # Valor Recaudo
        ValorBonos = "{:,.0f}".format(
            registro['ValorBonos']).replace(",", ".")  # Valor Bono

        diferencia = registro['diferencia']  # Diferencia

        hoja.append((tienda, fecha_venta, venta_post, ValorDeposito, ValorVenta, ValorRecaudo, ValorBonos,
                    valor_venta, diferencia))

    fecha_actual = datetime.datetime.now()
    archivoExcel = f"informe_consignaciones_{fecha_actual.strftime('%Y_%m_%d')}.xlsx"
    carpeta_descarga = "../static/downloads-excel"
    ruta_descarga = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), carpeta_descarga)

    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)
        # Dando permisos a la carpeta
        os.chmod(ruta_descarga, 0o755)

    ruta_archivo = os.path.join(ruta_descarga, archivoExcel)
    wb.save(ruta_archivo)

    # Enviar el archivo como respuesta HTTP
    return send_file(ruta_archivo, as_attachment=True)
