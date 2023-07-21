# Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
from app import app

# Importando todos mis controllers
from controllers.controller_tienda import *  # Controlador Tienda
from controllers.controller_login import *  # Controlador Login

from controllers.controller_tienda_vpn import *

from controllers.controller_bandeja_entrada import *
from controllers.controller_bandeja_procesadas import *
from controllers.controller_resumen_consignaciones_diarias import *


from controllers.controller_page_not_found import *


# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600)
