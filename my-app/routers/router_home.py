from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify

from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/cpanel"


# Lista de Consignaciones recibidas
@app.route('/home', methods=['GET'])
def cpanelListConsignaciones():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/list_consignaciones.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/empleados/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        if 'foto_empleado' in request.files:
            foto_perfil = request.files['foto_empleado']
            resultado = procesar_form_empleado(request.form, foto_perfil)
            if resultado:
                return render_template(f'{PATH_URL}/empleados/form_empleado.html')
            else:
                flash('El empleado NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/empleados/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/empleados/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))
