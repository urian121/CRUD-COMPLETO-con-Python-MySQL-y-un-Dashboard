# PASO 1, Crear mi entorno virtual

`virtualenv env `

# PASO 2, Activar el entorno virtual ejecutando;

`. env/Scripts/activate`

# PASO 3, Ya dentro del entorno virtual instalar flask

`pip install flask`

# Para python 3

`pip3 install Flask`

# PASO 4, Instalar Python MySQL Connector, es una bibliote (Driver) para conectar Python con MySQL

`pip install mysql-connector-python`

# Para desisntalr cualquier paquete, ejemplo

`pip uninstall mysql-connector-python`

## Instalar conector (driver) de conexion entre SQL Server y Python

`pip install pyodbc`

`pip install pandas`
`pip install openpyxl`

# Instalando Flask-SocketIO

`pip install flask-socketio`

# PASO 5, Lista todos mis paquetes

`pip list  o pip freeze`

# Crear/Actualizar el fichero requirements.txt:

`pip freeze > requirements.txt`

# (env)$ deactivate Para desactivar nuestro entono virtual

# IMPORTANTE, para correr el proyecto solo debes ejecutar el archivo

# requirements.txt con el comando;

`pip install -r requirements.txt`

# en el mismo se encuentran todas las dependecias del proyecto.

- sudo apt-get install build-essential
- wget https://download.microsoft.com/download/7/5/6/756E1504-79E7-4DCD-8451-58C93EDF549A/msodbcsql17_17.8.1.1-1_amd64.deb

- sudo dpkg -i msodbcsql17_17.8.1.1-1_amd64.deb

#### Verifica si ya esta instalado usando:

- odbcinst -q -d -n "ODBC Driver 17 for SQL Server"

Ubuntu 22.04
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# IMPORTANTE:

#### Para que funcione el deploy en servidor linux se debe instalar el driver - controlador ODBC de SQL Server

# Nota: cuando valla hacer una actualizacion del archivo requirements.txt debo estar dentro de mi entorno virtual pero no dentro de la carpera app solo en mi entorno.

# Instalar pip install python-dotenv para el control de variables de entorno

#NOTA: CUANDO USO EL METODO FETCH O AXIOS PARA REALIZAR UNA SOLICITUD HTTP, Y LA FUNCION ESTA EN ALGUN ARCHIVO JS, NO FUNCIONA,
HAY QUE AGREGAR LA FUNCION EN EL MISMO ARCHIVO DEBAJO USANDO CUSTOMJS

# Desactivar entorno virtual

`deactivate`

`RECORDAR`
print(f"{respuesta}")
print(f"El valor es: {respuesta}")
Dictionary ={'username':'eduCBA' , 'account':'Premium' , 'validity':'2709 days'}
print(json.dumps(Dictionary))
print(jsonify(Dictionary))
print('Estás en la página {}'.format(page))

`Capturando parametros de una URL`
parametroURL = request.args.get('page')
if parametroURL is not None: # Hacer algo con el valor de page
print('Estás en la página {}'.format(parametroURL))
else: # No se proporcionó un valor para page
print('El parámetro "page" no se encontró en la URL.')

return jsonify(
paises=render_template("public/\_paises.html", paises=paises),
pagination=render_template(
"public/\_pagination.html", pagination=pagination
),
)

Nota: Cuando se registra por primera vez la consignacion
estatus_leido =0 y bandeja=0 esto significa que, la consignación esta en la bandeja de entrada y todavia no ha sido leido.

Cunado la consignacion se lee estatus_leido sera igual a estatus_leido =1 y bandeja seguira en 0 bandeja=0
Si luego de leer la consignacion la mueven a bandeja de consignaciones leidas, obvio no se puede mover una consignacion hasta que sea leida
desde la bandeja de entrada.

Cuando la misma es movida, estatus_leido =1 y bandeja=1, es decir la consignacion ya fue leida y esta en la bandeja de leidos.

querySQL = "SELECT cod_tienda FROM tiendas WHERE ip_vpn_tienda=%s AND nombre_real=%s LIMIT 1"
mycursor.execute(querySQL, (ip_consignacion, 1))
cod_tiendaBD = mycursor.fetchone() # Accede al valor de la columna 'cod_tienda'
codTienda = cod_tiendaBD[0]
