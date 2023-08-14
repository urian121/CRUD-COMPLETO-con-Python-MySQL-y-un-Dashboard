
from flask import session, flash

from conexion.conexionBD import connectionBD
# Para encriptar contraseña generate_password_hash
from werkzeug.security import check_password_hash

import re
# Para encriptar contraseña generate_password_hash
from werkzeug.security import generate_password_hash


def recibeInsertRegisterUser(name_surname, email_user, pass_user):
    conexion_MySQLdb = connectionBD()
    cursor = conexion_MySQLdb.cursor(dictionary=True)

    # Comprobando si existe una cuenta
    cursor.execute("SELECT * FROM users WHERE email_user = %s", (email_user,))
    result = cursor.fetchone()  # Obtener la primera fila de resultados
    cursor.close()  # cerrando conexión SQL

    if result is not None:
        flash('ya existe la cuenta', 'error')
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_user):
        flash('correo invalido', 'error')
    elif not name_surname or not email_user or not pass_user:
        flash('por favor llene los campos del formulario.', 'error')
    else:
        # La cuenta no existe y los datos del formulario son válidos,
        # ahora inserte una nueva cuenta en la tabla de cuentas
        nueva_password = generate_password_hash(pass_user, method='scrypt')

        conexion_MySQLdb = connectionBD()
        cursor = conexion_MySQLdb.cursor(dictionary=True)
        sql = (
            "INSERT INTO users(name_surname, email_user, pass_user) VALUES (%s, %s, %s)")
        valores = (name_surname, email_user, nueva_password)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()

        cursor.close()  # Cerrando conexion SQL
        conexion_MySQLdb.close()  # cerrando conexion de la BD

        resultado_insert = cursor.rowcount  # retorna 1 o 0
    return resultado_insert


def info_perfil_session():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT name_surname, email_user FROM users WHERE id = %s"
                cursor.execute(querySQL, (session['id'],))
                info_perfil = cursor.fetchall()
        return info_perfil
    except Exception as e:
        print(f"Error en info_perfil_session : {e}")
        return []


def procesar_update_perfil(data_form):
    # Extraer datos del diccionario data_form
    id_user = session['id']
    name_surname = data_form['name_surname']
    email_user = data_form['email_user']
    pass_actual = data_form['pass_actual']
    new_pass_user = data_form['new_pass_user']
    repetir_pass_user = data_form['repetir_pass_user']

    if not pass_actual or not email_user:
        return 3

    with connectionBD() as conexion_MySQLdb:
        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = """SELECT * FROM users WHERE email_user = %s LIMIT 1"""
            cursor.execute(querySQL, (email_user,))
            account = cursor.fetchone()
            if account:
                if check_password_hash(account['pass_user'], pass_actual):
                    # Verificar si new_pass_user y repetir_pass_user están vacías
                    if not new_pass_user or not repetir_pass_user:
                        # if len(new_pass_user) == 0 or len(repetir_pass_user) == 0:
                        return updatePefilSinPass(id_user, name_surname)
                    else:
                        if new_pass_user != repetir_pass_user:
                            return 2
                        else:
                            try:
                                nueva_password = generate_password_hash(
                                    new_pass_user, method='scrypt')
                                with connectionBD() as conexion_MySQLdb:
                                    with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                                        querySQL = """
                                            UPDATE users
                                            SET 
                                                name_surname = %s,
                                                pass_user = %s
                                            WHERE id = %s
                                        """
                                        params = (name_surname,
                                                  nueva_password, id_user)
                                        cursor.execute(querySQL, params)
                                        conexion_MySQLdb.commit()
                                return cursor.rowcount or []
                            except Exception as e:
                                print(
                                    f"Ocurrió en procesar_update_perfil: {e}")
                                return []
            else:
                return 0


def updatePefilSinPass(id_user, name_surname):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    UPDATE users
                    SET 
                        name_surname = %s
                    WHERE id = %s
                """
                params = (name_surname, id_user)
                cursor.execute(querySQL, params)
                conexion_MySQLdb.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Ocurrió un error en la funcion updatePefilSinPass: {e}")
        return []


def dataLoginSesion():
    inforLogin = {
        "id": session['id'],
        "name_surname": session['name_surname'],
        "email_user": session['email_user']
    }
    return inforLogin
