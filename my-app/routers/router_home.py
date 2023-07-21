from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify

from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_bandeja_entrada import *

PATH_URL = "public/cpanel/bandeja_entrada"


# Lista de Consignaciones recibidas
@app.route('/consignaciones-recibidas', methods=['GET'])
def cpanelListConsignaciones():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/list_consignaciones.html', miDiccionarioView=listaConsignacionesBandejaEntrada(), totalConsigSinLeer=totalConsigNoLeidas())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))
