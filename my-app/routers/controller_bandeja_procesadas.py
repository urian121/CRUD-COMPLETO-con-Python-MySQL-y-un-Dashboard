from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify, session

import os
from mysql.connector.errors import Error
from datetime import datetime


# Importando cenexión a BD
from funciones.funciones_bandeja_procesadas import *

PATH_URL = "public/cpanel/bandeja_procesadas"


# Mostrar lista de consignaciones procesadas
@app.route('/consignaciones-procesadas', methods=['GET'])
def cpanelListConsignacionesLeidas():
    if 'conectado' in session and request.method == 'GET':
        return render_template(f'{PATH_URL}/list_consignaciones_leidas.html', consignacionesLeidasTiendaCpanel=listaConsignacionesLeidasTiendaCpanel(), totalConsigSinLeer=totalConsigNoLeidas())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


# cargar mas consignaciones desde la bandeja de leidos
@app.route("/load_more_consignments_bandeja_leidas/<int:ultimoId>/<int:valorYear>/<int:valorMes>", methods=['GET'])
@app.route("/load_more_consignments_bandeja_leidas", defaults={"ultimoId": 5})
def load_more_procesada(ultimoId, valorYear, valorMes):
    resultado_load_more = load_more_consignaciones_procesadas(
        ultimoId, valorYear, valorMes)
    if (resultado_load_more):
        miDiccionarioConsigBandejaLeidos = {
            'consignacionesTiendaCpanel': resultado_load_more,
            'yearConsignaciones': yearConsignaciones()
        }
        return render_template(f'{PATH_URL}/load_more_consignments_leidas.html', miDiccionarioConsigBandejaLeido=miDiccionarioConsigBandejaLeidos)
    else:
        return jsonify({'fin': 0})


# Reset reset-consignaciones-procesadas
@app.route('/reset-consignaciones-procesadas', methods=['POST'])
def resetConsignacionesProcesadas():
    result_process = process_reset_consignaciones_procesadas()
    if result_process:
        return render_template(f'{PATH_URL}/reset_bandeja_leidos.html', resultFiltro=result_process)
    else:
        return jsonify({'fin': 0})


# Mostrar todas las consignaciones procesadas desde el filtro mes-year
@app.route('/filtrar-todas-las-consignaciones-leidas-mes-year', methods=['POST'])
def filtrandoConsignacionProcesadasPorMes():
    if 'conectado' in session:
        mes = request.json['mes']
        yearFiltro = request.json['valorFiltroPorYear']

        resultado = process_filtro_procesadas_por_mes(mes, yearFiltro)
        if resultado:
            return render_template(f'{PATH_URL}/resultado_filtro_consg_leidas.html', resultFiltroCongLeidas=resultado)
        else:
            return jsonify({'fin': 0})


# Cargar las consignaciones de acuerdo a una fecha en especifica
@app.route('/filtrar-consignaciones-procesadas-fecha-especifica', methods=['POST'])
def filtrandoConsignacionLeidasFechaEspecifica():
    fechaFitro = request.json.get('fechaFitro', '')
    resultado = getAll_consignaciones_por_fecha_especifica(fechaFitro)
    if resultado:
        return render_template(f'{PATH_URL}/resultado_filtro_consg_leidas.html', resultFiltroCongLeidas=resultado)
    else:
        return jsonify({'fin': 0})
