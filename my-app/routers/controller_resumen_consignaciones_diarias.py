from flask import render_template, request, flash, jsonify, session
from app import app

import os
from mysql.connector.errors import Error
from flask import send_file  # biblioteca o modulo send_file para forzar la descarga

import datetime
import openpyxl

# Importando cenexión a BD
from conexion.conexionBD import connectionBD
from funciones.funciones_resumen_consignaciones_pendientes import *

PATH_URL = "public/cpanel/consignaciones_diarias"


# funcion para obtener la lista de tienda pendiente por consignar a la fecha actual.
@app.route('/resumen-consignaciones-diarias', methods=['GET'])
def cpanelListResumenConsignaciones():
    if 'conectado' in session and request.method == 'GET':
        return render_template(f'{PATH_URL}/resumen_consignaciones.html', consigRecibidasDiarias=resumenConsignacionesRecibidas(), consigPendienteDiarias=resumenConsignacionesPendientes(), totalConsigSinLeer=totalConsigNoLeidas())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return render_template('public/login/base_login.html')


# Filtar resumen de consignaciones por fecha especifica
@app.route('/filtrar-resumen-consignaciones-diarias-fecha-especifica', methods=['POST'])
def filtrandoResumenConsignacionesDiarias():
    fechaFiltro = request.json.get('fechaFitroResumen')
    resp1 = resumenFiltroConsignacionesRecibidasDiariaBD(fechaFiltro)
    resp2 = resumenFiltroConsignacionesPendientesDiarias(fechaFiltro)

    if resp1 or resp2:
        return render_template(f'{PATH_URL}/result_filtro_resumen_consig_diaria.html', consigRecibidasDiarias=resp1, consigPendienteDiarias=resp2)
    else:
        return jsonify({'fin': 0})


# Funcion para realizar la consulta a BD y generar el reporte en Excel
@app.route('/informe-excel-consignaciones-recibidas/<string:fecha>', methods=['GET'])
def reporteExcelBD(fecha):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                        SELECT 
                            c.nombre_tienda,
                            c.valor_consignacion,
                            d.dia_venta
                        FROM consignaciones AS c
                        INNER JOIN detalles_consignaciones AS d 
                        ON c.id = d.id_consignacion
                        WHERE DATE(d.dia_venta) = %s
                        ORDER BY c.id DESC
                    """
                mycursor.execute(querySQL, (fecha,))
                dataBD = mycursor.fetchall()

                # creando un nuevo objeto de libro de trabajo de Excel usando la biblioteca de Python openpyxl
                wb = openpyxl.Workbook()
                hoja = wb.active
                # Crea la fila del encabezado con los títulos
                hoja.append(
                    ('TIENDA', 'VALOR CONSIGNACIÓN', 'FECHA CONSIGNACIÓN'))
                for filaPersona in dataBD:

                    formato_valor_consignacion = "{:,.0f}".format(
                        filaPersona['valor_consignacion']).replace(",", ".")

                    # Agrega una tupla con los valores de la consignación
                    hoja.append((filaPersona['nombre_tienda'], formato_valor_consignacion,
                                filaPersona['dia_venta']))

                fecha_actual = datetime.datetime.now()
                archivoExcel = f"consignaciones_recibidas_{fecha_actual.strftime('%Y_%m_%d')}.xlsx"
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
                return send_file(ruta_archivo, as_attachment=False)

    except Exception as e:
        print(f"Ocurrió un error al descargar las consignaciones diarias: {e}")
        return []


@app.route('/informe-excel-consignaciones-pendientes/<string:fecha>', methods=['GET'])
def reporteExcelBDPendientes(fecha):
    dataDB = resumenFiltroConsignacionesPendientesDiarias(fecha)

    # Abre el archivo Excel y la hoja activa
    wb = openpyxl.Workbook()
    hoja = wb.active

    # Crea la fila del encabezado con los títulos
    hoja.append(('TIENDA', 'FECHA CONSIGNACIÓN PENDIENTE'))

    for data in dataDB:
        # Agrega una tupla con los valores de la consignación
        hoja.append((data[2], fecha))

    fecha_actual = datetime.datetime.now()
    archivoExcel = f"consignaciones_pendientes_{fecha_actual.strftime('%Y_%m_%d')}.xlsx"
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
    return send_file(ruta_archivo, as_attachment=False)
