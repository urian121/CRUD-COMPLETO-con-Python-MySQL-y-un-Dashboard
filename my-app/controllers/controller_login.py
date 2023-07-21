
from flask import render_template, request, flash, redirect, url_for
from app import app


from conexion.conexionBD import connectionBD

# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

# Importando funciones para el modulo de login
from funciones.funciones_login import *


@app.route('/admin', methods=['GET'])
def inicioCpanel():
    if 'conectado' in session:
        return render_template('public/cpanel/base_cpanel.html', dataLogin=dataLoginSesion())
    else:
        return render_template('public/login/base_login.html')


@app.route('/mi-perfil', methods=['GET'])
def perfil():
    if 'conectado' in session:
        print('aqui')
        return render_template('public/cpanel/perfil/perfil.html', info_perfil_session=info_perfil_session(), totalConsigSinLeer=totalConsigNoLeidas())
    else:
        return render_template('public/login/base_login.html')


# Crear cuenta de usuario
@app.route('/register-user', methods=['GET'])
def cpanelRegisterUser():
    if 'conectado' in session:
        return redirect(url_for('cpanelListConsignaciones'))
    else:
        return render_template('public/login/auth_register.html')


# Recuperar cuenta de usuario
@app.route('/recovery-password', methods=['GET'])
def cpanelRecoveryPassUser():
    if 'conectado' in session:
        return redirect(url_for('cpanelListConsignaciones'))
    else:
        return render_template('public/login/auth_forgot_password.html')


# Crear cuenta de usuario
@app.route('/saved-register', methods=['POST'])
def cpanelResgisterUserBD():
    if request.method == 'POST' and 'name_surname' in request.form and 'pass_user' in request.form:
        name_surname = request.form['name_surname']
        # name_surname = request.form.get()'name_surname')
        email_user = request.form['email_user']
        pass_user = request.form['pass_user']

        resultData = recibeInsertRegisterUser(
            name_surname, email_user, pass_user)
        if (resultData != 0):
            flash('la cuenta fue creada correctamente.', 'success')
            return render_template('public/login/base_login.html')
        else:
            flash('el registro no fue procesado, por favor verifique.', 'error')
            return render_template('public/login/base_login.html')
    else:
        flash('el método HTTP es incorrecto', 'error')
        return render_template('public/login/base_login.html')


# Actualizar datos de mi perfil
@app.route("/actualizar-datos-perfil", methods=['POST'])
def actualizarPerfil():
    if 'conectado' in session:
        respuesta = procesar_update_perfil(request.form)
        print(respuesta)
        if respuesta == 1:
            flash('Los datos fuerón actualizados correctamente.', 'success')
            return redirect(url_for('cpanelListConsignaciones'))
        elif respuesta == 0:
            flash('La contraseña actual esta incorrecta, por favor verifique.', 'error')
            return redirect(url_for('perfil'))
        elif respuesta == 2:
            flash('Ambas claves deben se igual, por favor verifique.', 'error')
            return redirect(url_for('perfil'))
        elif respuesta == 3:
            flash('La Clave actual es obligatoria.', 'error')
            return redirect(url_for('perfil'))
    else:
        flash('primero debes iniciar sesión.', 'error')
        return render_template('public/login/base_login.html')


# Validar sesión
@app.route('/consignaciones', methods=['GET', 'POST'])
def loginCliente():
    if 'conectado' in session:
        return redirect(url_for('cpanelListConsignaciones'))
    else:
        if request.method == 'POST' and 'email_user' in request.form and 'pass_user' in request.form:

            email_user = str(request.form['email_user'])
            pass_user = str(request.form['pass_user'])

            # Comprobando si existe una cuenta
            conexion_MySQLdb = connectionBD()
            cursor = conexion_MySQLdb.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE email_user = %s", [email_user])
            account = cursor.fetchone()

            if account:
                if check_password_hash(account['pass_user'], pass_user):
                    # Crear datos de sesión, para poder acceder a estos datos en otras rutas
                    session['conectado'] = True
                    session['id'] = account['id']
                    session['name_surname'] = account['name_surname']
                    session['email_user'] = account['email_user']

                    flash('la sesión fue correcta.', 'success')
                    return redirect(url_for('cpanelListConsignaciones'))
                else:
                    # La cuenta no existe o el nombre de usuario/contraseña es incorrecto
                    flash('datos incorrectos por favor revise.', 'error')
                    return render_template('public/login/base_login.html')
            else:
                flash('el usuario no existe, por favor verifique.', 'error')
                return render_template('public/login/base_login.html')
        else:
            flash('primero debes iniciar sesión.', 'error')
            return render_template('public/login/base_login.html')


@app.route('/closed-session',  methods=['GET'])
def cerraSesion():
    if request.method == 'GET':
        if 'conectado' in session:
            # Eliminar datos de sesión, esto cerrará la sesión del usuario
            session.pop('conectado', None)
            session.pop('id', None)
            session.pop('name_surname', None)
            session.pop('email', None)
            flash('tu sesión fue cerrada correctamente.', 'success')
            return render_template('public/login/base_login.html')
        else:
            flash('recuerde debe iniciar sesión.', 'error')
            return render_template('public/login/base_login.html')
