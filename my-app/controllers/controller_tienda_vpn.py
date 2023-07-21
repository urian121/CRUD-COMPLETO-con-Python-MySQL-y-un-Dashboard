from app import app
from flask import render_template, session, request, flash, redirect, url_for


from conexion.conexionBD import connectionBD  # Conexión a BD

from mysql.connector.errors import Error


PATH_URL = "public/cpanel/tienda_vpn"


# Lista de Consignaciones recibidas
@app.route('/agregar-vpn-tienda', methods=['GET'])
def agregarVPN():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/agregar_vpn.html', dataLogin=dataLoginSesion(), totalConsigSinLeer=totalConsigNoLeidas())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicioCpanel'))


def dataLoginSesion():
    inforLogin = {
        "id": session['id'],
        "name_surname": session['name_surname'],
        "email_user": session['email_user']
    }
    return inforLogin


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
