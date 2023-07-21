from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify

from mysql.connector.errors import Error


# Importando cenexión a BD
from funciones.funciones_bandeja_entrada import *

PATH_URL = "public/cpanel/bandeja_entrada"


# Lista de Consignaciones recibidas
@app.route('/consignaciones-recibidas', methods=['GET'])
def cpanelListConsignaciones():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/list_consignaciones.html', miDiccionarioView=listaConsignacionesBandejaEntrada(), totalConsigSinLeer=totalConsigNoLeidas())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


# Acción cargar más consignaciones desde el boton 'cargar más consignaciones'
@app.route("/load_more_consignments_bandeja_entrada/<int:ultimoId>/<int:valorYear>/<int:valorMes>", methods=['GET'])
@app.route("/load_more_consignments_bandeja_entrada", defaults={"ultimoId": 5})
def load_more(ultimoId, valorYear, valorMes):
    resultado_load_more = load_more_bandeja_entrada(
        ultimoId, valorYear, valorMes)
    if (resultado_load_more):
        miDiccionarioConsigBandejaEntrada = {
            'consignacionesTiendaCpanel': resultado_load_more,
            'yearConsignaciones': yearConsignaciones()
        }
        return render_template(f'{PATH_URL}/load_more_consignments.html', miDiccionarioConsigBandejaEntrada=miDiccionarioConsigBandejaEntrada)
    else:
        return jsonify({'fin': 0})


# Leer consignación desde la bandeja de entrada, mi decorador recibe el id de la consignación
@app.route('/read-consignment/<int:idConsignacion>', methods=['GET'])
def viewLeerConsignacion(idConsignacion):
    if 'conectado' in session:
        fromView = request.args.get('from')

        # Importante, la función detallesConsignacionCpanel() retorna mas de un parametro
        resultData = detallesConsignacionCpanel(idConsignacion)

        # Asignando los valores retornados a dos variables distintas
        # utilizando la sintaxis de desempaquetado de tuplas,
        # los valores de listaConsignaciones y respuesta_server_sql se asignan a dos variables distintas.
        listaConsignaciones, respuesta_server_sql, dataDetallesBD = resultData

        diferencias = {}
        total_venta_pos = 0
        total_consig_pos = 0
        total_consig_tienda = 0
        total_diferencia = 0
        valor_venta_bd = 0
        valor_venta_bd_pendiente = 0

        for detalleBD in dataDetallesBD:
            fecha_venta_str = detalleBD['dia_venta'].strftime('%Y-%m-%d')
            # Bandera para verificar si se encontró una coincidencia (registro) en el POS
            registro_no_encontado = False
            valor_venta_bd_pendiente = int(detalleBD['valor_venta'])

            for consignacion in respuesta_server_sql:
                if str(fecha_venta_str) == str(consignacion['FechaVenta']):
                    # Establecer la bandera para indicar que se encontró una coincidencia
                    registro_no_encontado = True
                    valor_venta = int(detalleBD['valor_venta'])
                    valor_total = int(consignacion['ValorTotal'])
                    ValorDeposito = int(consignacion['ValorDeposito'])
                    ValorVenta = int(consignacion['ValorVenta'])
                    ValorRecaudo = int(consignacion['ValorRecaudo'])
                    ValorBonos = int(consignacion['ValorBonos'])

                    total_venta_pos += valor_total
                    total_consig_pos += ValorDeposito
                    total_consig_tienda += valor_venta

                    diferencia = (valor_venta - valor_total)
                    total_diferencia += diferencia

                    diferencias[detalleBD['dia_venta']] = {
                        'ValorTotal': valor_total,
                        'valor_venta': valor_venta,
                        'ValorDeposito': ValorDeposito,
                        'ValorRecaudo': ValorRecaudo,
                        'ValorBonos': ValorBonos,
                        'ValorVenta': ValorVenta,
                        'diferencia': diferencia
                    }

            if not registro_no_encontado:
                # Agregar datos vacíos para las fechas sin coincidencia
                diferencias[detalleBD['dia_venta']] = {
                    'ValorTotal': 0,
                    'valor_venta': valor_venta_bd_pendiente,
                    'ValorDeposito': 0,
                    'ValorRecaudo': 0,
                    'ValorBonos': 0,
                    'ValorVenta': 0,
                    'diferencia': 1
                }
                # print("Fecha no igual, esta fecha no esta en el POS")
                # print(f"Dia Venta:{fecha_venta_str} - Valor venta:{(detalleBD['valor_venta'])}")

                valor_venta_bd = detalleBD['valor_venta']

        # print(f"Diferencias: {diferencias}")

        resultados_totales = {
            'total_venta_pos': total_venta_pos,
            'total_consig_pos': total_consig_pos,
            'total_consig_tienda': total_consig_tienda + valor_venta_bd,
            'total_diferencia': total_diferencia
        }
        data_final_pos_vs_BD = {
            'diferencias': diferencias,
            'resultados_totales': resultados_totales
        }
        # print(f"probando {valor_venta_bd}")

        if resultData:
            return render_template(f'{PATH_URL}/read_consignment.html', data_final_pos_vs_BD=data_final_pos_vs_BD, desde_bandeja=fromView, totalConsigSinLeer=totalConsigNoLeidas(), detailsConsignment=listaConsignaciones)
        else:
            flash('No existe la consignación', 'error')
            return redirect(url_for('cpanelListConsignaciones'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


# Descargar imagen de la consignación
@app.route('/download-file/<int:idFileBD>', methods=['GET'])
def downloadConsignmentFile(idFileBD):
    if request.method == 'GET':
        return process_descarga_imagen_consignacion(idFileBD)


# Mover consignación a 'consignaciones procesadas'
@app.route('/mover-consignacion/<string:idConsignacion>', methods=['GET'])
def moverConsignacionLeidaCpanel(idConsignacion):
    if 'conectado' in session:
        result_mover_consignacion = process_mover_consignacion(idConsignacion)
        if (result_mover_consignacion):
            flash('la consignación fue movida correctamente.', 'success')
            return redirect(url_for('cpanelListConsignaciones'))
        else:
            flash('La consignación no fue movida a consignaciones procesadas.', 'error')
            return redirect(url_for('cpanelListConsignaciones'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


# Ignorar una consignación
@app.route('/ignorar-consignacion/<string:idConsignacion>', methods=['GET'])
def ignorarConsignacion(idConsignacion):
    if 'conectado' in session:
        result_ignorar_consignacion = process_ignorar_consignacion(
            idConsignacion)
        if (result_ignorar_consignacion):
            flash('la consignación fue ignorada correctamente.', 'success')
            return redirect(url_for('cpanelListConsignaciones'))
        else:
            flash('La consignación no fue ignorada.', 'error')
            return redirect(url_for('cpanelListConsignaciones'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


# Resetear - Refescar Bandeja de entrada
@app.route('/reset-refresh-bandeja-entrada', methods=['POST'])
def resetBandejaEntrada():
    result_resetBandejaEntrada = process_resetBandejaEntrada()
    if result_resetBandejaEntrada:
        return render_template(f'{PATH_URL}/filtro_consignaciones_mes.html', resultFiltro=result_resetBandejaEntrada)
    else:
        return jsonify({'fin': 0})


# Filtra consignacion desde el mes
@app.route('/filtrar-consignacion-mes-bandeja-entrada', methods=['POST'])
def filtrandoConsignacionPorMes():
    # Recibiendo request.json y no request.form
    mes = request.json['mes']
    yearFiltro = request.json['valorFiltroPorYear']

    result_filtro_consignacion_por_mes = process_filtro_consignacion_por_mes(
        mes, yearFiltro)

    if (result_filtro_consignacion_por_mes):
        return render_template(f'{PATH_URL}/filtro_consignaciones_mes.html', resultFiltro=result_filtro_consignacion_por_mes)
    else:
        return jsonify({'fin': 0})


# Filtando consignacion de acuerdo a una fecha en especifica
@app.route('/filtrar-consignaciones-bandeja-entrada-fecha-especifica', methods=['POST'])
def filtrandoConsignacionBandejaEntradaFechaEspecifica():
    fechaFitro = request.json.get('fechaFitro', '')
    result_filtro = process_filtrar_consignacion_por_fecha_especifica(
        fechaFitro)
    if result_filtro:
        return render_template(f'{PATH_URL}/result_filtro_bandeja_entrada_date.html', resultFiltroBandjEntrada=result_filtro)
    else:
        return jsonify({'fin': 0})


# Procesar consignaciones desde los checkbox
@app.route('/procesar-checkbox-consignaciones', methods=['POST'])
def procesarCheckboxConsignacion():
    if 'conectado' in session:
        idsConsigChecked = request.json.get('ids')
        result_consignaciones_checkbox = process_consignaciones_checkbox(
            idsConsigChecked)
        if (result_consignaciones_checkbox):
            return jsonify({"idsProcesados": idsConsigChecked})
    else:
        flash('primero debes iniciar sesión.', 'error')
    return redirect(url_for('inicioCpanel'))


# Forzar descargar del reporte General desde la bandeja de entrdada, debe ser método GET
@app.route('/descargar-reporte-general-bandeja-entrada/<string:fecha>', methods=['GET'])
def procesarDescargarInformeGeneral(fecha):
    if 'conectado' in session:
        resultData = creando_consultas_para_descarga_informe_general(fecha)

        # utilizando la sintaxis de desempaquetado de tuplas,
        dataDetallesBD, respuesta_server_sql = resultData

        diferencias = {}
        total_venta_pos = 0
        total_consig_pos = 0
        total_consig_tienda = 0
        total_diferencia = 0
        valor_venta_bd_pendiente = 0

        for detalleBD in dataDetallesBD:
            fecha_venta_str = detalleBD['dia_venta'].strftime('%Y-%m-%d')
            registro_no_encontrado = True
            valor_venta_bd_pendiente = int(detalleBD['valor_venta'])
            diferencias[detalleBD['dia_venta']] = []

            for consignacion in respuesta_server_sql:
                if str(fecha_venta_str) == str(consignacion['FechaVenta']):
                    registro_no_encontrado = False
                    valor_venta = int(detalleBD['valor_venta'])

                    tienda = consignacion['Tienda']
                    valor_total = int(consignacion['ValorTotal'])
                    ValorDeposito = int(consignacion['ValorDeposito'])
                    ValorVenta = int(consignacion['ValorVenta'])
                    ValorRecaudo = int(consignacion['ValorRecaudo'])
                    ValorBonos = int(consignacion['ValorBonos'])

                    total_venta_pos += valor_total
                    total_consig_pos += ValorDeposito
                    total_consig_tienda += valor_venta

                    diferencia = (valor_venta - valor_total)
                    total_diferencia += diferencia

                    diferencias[detalleBD['dia_venta']].append({
                        'Tienda': tienda,
                        'ValorTotal': valor_total,
                        'valor_venta': valor_venta,
                        'ValorDeposito': ValorDeposito,
                        'ValorRecaudo': ValorRecaudo,
                        'ValorBonos': ValorBonos,
                        'ValorVenta': ValorVenta,
                        'diferencia': diferencia
                    })

            if registro_no_encontrado:
                diferencias[detalleBD['dia_venta']].append({
                    'Tienda': '',
                    'ValorTotal': 0,
                    'valor_venta': valor_venta_bd_pendiente,
                    'ValorDeposito': 0,
                    'ValorRecaudo': 0,
                    'ValorBonos': 0,
                    'ValorVenta': 0,
                    'diferencia': 1
                })
        print(f"Diferencias: {diferencias}")

        return reporte_informe_general(diferencias)
    else:
        return redirect(url_for('inicioCpanel'))
