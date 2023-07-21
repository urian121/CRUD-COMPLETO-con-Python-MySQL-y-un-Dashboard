from app import app

# Importando el objeto app de mi app
from flask import render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime

# Importando funciones para la tienda
from funciones.funciones_tienda import *

PATH_URL_TIENDA = "public/tienda"


@app.route('/', methods=['GET'])
def inicio():
    if INFO_TIENDA_API_BIGDATA():
        return render_template(f'{PATH_URL_TIENDA}/base_tienda.html', informacion_tienda=INFO_TIENDA_API_BIGDATA(), lista_consignaciones=listaConsignacionesPorTienda() or [])
    else:
        return render_template('public/NotFound/tienda_no_sincronizada.html')


@app.route('/procesar-consignacion-diaria', methods=['POST'])
def procesarFormConsignacionDiaria():
    # print(f"Data request: {request.form}")
    # Recibiendo formulario de Pago diario
    valor_consignacion = request.form.getlist('valor_consignacion[]')
    fechas_consig = request.form.getlist('dia_de_la_venta[]')
    fecha_consignacion_banco = request.form['fecha_consignacion_banco']

    code_tienda = request.form['code_tienda']
    ip_consignacion = request.form['ip_consignacion']
    nombre_tienda = request.form['nombre_tienda']

    # Mes actual
    # mes_actual = datetime.now().strftime("%B")
    mes_actual = datetime.now().strftime("%B_%Y")
    nota_consignacion = request.form['nota_consignacion']

    if (request.files['archivo']):
        # Script para archivo
        file = request.files['archivo']  # recibiendo el archivo

        # validar tamaño del archivo
        pesoArchivo = procesarPesoArchivo(file)
        if (pesoArchivo != False):
            # Procesando todo el archivo recibido
            miFile = procesarFile(file, mes_actual)
            if (miFile != False):
                urlFile = f"consignment_files/{mes_actual}/{miFile}"

                resultData = recibeInsertConsignacion(
                    valor_consignacion, fechas_consig, fecha_consignacion_banco, miFile, urlFile, nota_consignacion, code_tienda, ip_consignacion, nombre_tienda)
                if (resultData == 1):
                    return jsonify({'status_server': 1, 'mensaje': 'La consignación fue registrada con correctamente.', 'status_mensaje': 'success'})
                else:
                    return jsonify({'status_server': 0, 'mensaje': 'Ocurrio un error en el registro', 'status_mensaje': 'error'})
        else:
            return jsonify({'status_server': 0, 'mensaje': 'El archivo supera el peso establecido, recuerda maximo 2 MB', 'status_mensaje': 'error'})
    else:
        return jsonify({'status_server': 0, 'mensaje': 'Debe cargar un archivo', 'status_mensaje': 'error'})


# Deetalles de una consignación
@app.route('/details-consignment/<string:idConsignacion>', methods=['GET'])
def viewDetallesConsignacion(idConsignacion):
    if request.method == 'GET':
        resultData = detallesConsignaciones(idConsignacion)
        # Mostrando si esta consignacion es mas de 1 dia
        consignacionGrupales = (
            listaConsignacionesGrupales(idConsignacion) or [])

        if resultData:
            return render_template(f'{PATH_URL_TIENDA}/detalles_consignacion.html', infoDetalles=resultData, consignacionGrupales=consignacionGrupales, informacion_tienda=INFO_TIENDA_API_BIGDATA())
        else:
            flash('No existe la consignación', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Método HTTP incorrecto', 'error')
        return redirect(url_for('inicio'))


# Formulario para un solo pago
@app.route('/form-pago-diario', methods=['GET'])
def cargarFormPagoDiario():
    if request.method == 'GET':
        return render_template(f'{PATH_URL_TIENDA}/form_pago_diario.html')
