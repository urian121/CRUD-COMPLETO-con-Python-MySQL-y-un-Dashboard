function iniciarApp() {
  /*
  // Inicializando SocketIO
  const socket = io();

  //Escuchando connect
  socket.on("connect", function () {
    console.log("Socket Activo Cliente!");
  });

  //Escuchando disconnect
  socket.on("disconnect", function () {
    console.log("Socket Desconectado Cliente!");
  });
*/

  /**
   * Recibir solicitud de envio del formulario enviar consignación
   */
  const form_consignacion = document.querySelector(
    "#formProcesarConsignacionDiaria"
  );
  if (form_consignacion) {
    // verificar si existe el elemento
    form_consignacion.addEventListener("submit", async (event) => {
      // evita que el formulario se envíe de forma predeterminada, recargando la web
      event.preventDefault();

      /**
       * En este ejemplo, inicializamos la variable respuesta_valida como true. Luego,
       * verificamos si cada una de las funciones de validación retorna false.
       * Si alguna de ellas lo hace, actualizamos el valor de respuesta_valida a false.
       * Al final, verificamos el valor de respuesta_valida.
       * Si es true, significa que todas las validaciones fueron exitosas y podemos continuar con el envío del formulario.
       */
      let respuesta_valida = true;

      if (!validar_dia_venta()) {
        respuesta_valida = false;
        // console.log("respuesta1 ", respuesta_valida);
      }

      if (!validar_fechas()) {
        respuesta_valida = false;
        // console.log("respuesta3 ", respuesta_valida);
      }

      if (!validar_inputs()) {
        respuesta_valida = false;
        // console.log("respuesta2 ", respuesta_valida);
      }

      if (!validar_valores_consignados()) {
        respuesta_valida = false;
        // console.log("respuesta 4 ");
      }

      if (!validar_archivo()) {
        respuesta_valida = false;
        // console.log("respuesta 5");
      }

      if (respuesta_valida) {
        document
          .querySelector("#btn_send_consig")
          .setAttribute("disabled", true);

        let bodyHTML = document.body;
        bodyHTML.style.backgroundColor = "#cecece";
        bodyHTML.style.opacity = "0.5";
        bodyHTML.style.position = "fixed";
        bodyHTML.style.width = "100%";
        bodyHTML.style.top = "0";
        bodyHTML.style.bottom = "0";
        bodyHTML.style.left = "0";
        bodyHTML.style.right = "0";
        bodyHTML.style.zIndex = "100000000";

        // crea un objeto FormData con los datos del formulario
        const formData = new FormData(form_consignacion);
        /**
         * Recorriendo toda la informacion que esta llegando desde el formulario
         */
        /*
        for (const [key, value] of formData.entries()) {
          console.log(`${key}: ${value}`);
        }
        */

        try {
          const response = await axios.post(
            "/procesar-consignacion-diaria",
            formData
          ); // envía los datos del formulario al servidor

          if (!response.status) {
            console.log(`HTTP error! status: ${response.status} 😭`);
          }

          // procesa la respuesta del servidor
          if (response.status === 200) {
            // console.log(response.data);
            if (response.data.status_server == 1) {
              alert(response.data.mensaje);
            } else {
              document
                .querySelector("#btn_send_consig")
                .removeAttribute("disabled");
              alert(response.data.mensaje);
              return;
            }
            /**
             * Si la respuesta indica que los datos fueron procesados correctamente,
             * muestra un mensaje de éxito
             */
            //Emitiendo al socket del servidor el evento processConsigOK
            // socket.emit("processConsigOK", "Todo OK");

            let dominio = window.location.href;
            if (dominio) {
              if (dominio != "http://127.0.0.1:5600/admin") {
                window.location.href = "http://controlefectivo.dugotex.com/";
              } else {
                window.location.href = "http://127.0.0.1:5600/admin";
              }
            }

            //Mandar una alerta aqui para notificar que el registro fue un exito.
          } else {
            // Si hubo un error en el servidor, muestra un mensaje de error
            console.log("Hubo un error en el servidor.");
          }
        } catch (error) {
          // Si hubo un error al enviar la petición, muestra un mensaje de error
          console.log("Hubo un error al enviar los datos.");
        } finally {
          // console.log("peticion finalizada");
          //location.href = "/publicar-inmueble";
        }
      }
    });
  }

  /**
   * Validar el input dia de la Venta
   */
  const validar_dia_venta = () => {
    let dia_venta = document.querySelector("#dia_de_la_venta_datepicker");

    /**
     *  La línea "if (!dia_venta.value)"  es una estructura condicional en JavaScript que evalúa si el valor del input
     * Con id "dia_venta" está vacío o es nulo
     */
    if (!dia_venta.value) {
      dia_venta.classList.add("input_vacio");
      mostrar_alert("Debe llenar todos los campos del formulario");
      return false;
    }
    return true;
  };

  /**
   * Funcion para validar inputs vacios
   */
  const validar_inputs = () => {
    //    let inputs = document.querySelectorAll("input[type='text'], textarea");
    let inputs = document.querySelectorAll("input[type='text']");

    let todos_llenos = true;
    //No se puedo usar la función forEach() no se puede interrumpir con return false.
    for (let i = 0; i < inputs.length; i++) {
      if (!inputs[i].value) {
        inputs[i].classList.add("input_vacio");
        console.log(inputs[i]);
        mostrar_alert("Debe llenar todos los campos del formulario");
        todos_llenos = false;
      } else {
        inputs[i].classList.add("input_lleno");
      }
    }
    return todos_llenos;
  };

  /**
   * Validar si existe archivo adjunto
   */
  const validar_archivo = () => {
    let inputs_file = document.querySelectorAll("input[type='file']");
    let valido = true;
    //No se puedo usar la función forEach() no se puede interrumpir con return false.
    for (let i = 0; i < inputs_file.length; i++) {
      if (!inputs_file[i].value) {
        mostrar_alert("Debe adjuntar un archivo de consignación");
        valido = false;
        break;
      } else {
        inputs_file[i].classList.add("input_lleno");
      }
    }

    return valido;
  };

  /**
   * Funcion para validar que todas las fechas sean distintas,
   * obvio aplica cuando el pago corresponde a varios dias.
   * Importante, para esta funcion siempre se ignora el primer elemento del array
   */
  const validar_fechas = () => {
    let f_condi_banco = document.querySelector(
      "#fecha_consignacion_banco_datepicker"
    ).value;

    const inputs_fechas = document.querySelectorAll(
      "input[name='dia_de_la_venta[]']"
    );
    let fechas = [];

    for (let i = 0; i < inputs_fechas.length; i++) {
      const input_f = inputs_fechas[i];

      // Ignorar el primer elemento del array
      if (i === 0) {
        if (
          valida_fecha_banco_mayor_dia_venta([input_f.value], f_condi_banco)
        ) {
          continue;
        }
      }

      const fecha = input_f.value;

      if (fechas.includes(fecha)) {
        input_f.classList.remove("input_lleno");
        input_f.classList.add("input_vacio");
        mostrar_alert("La fecha del día de la venta no puede estar repetida");
        return false;
      }

      fechas.push(fecha);
    }

    if (valida_fecha_banco_mayor_dia_venta(fechas, f_condi_banco)) {
      return true;
    }
  };

  /**
   * Verificando si existe alguna fecha del dia de la venta que es mayor a la fecha de consignacion en el banco
   */
  function valida_fecha_banco_mayor_dia_venta(array_fechas, f_condi_banco) {
    let fechaNueva = new Date(f_condi_banco.split("-").reverse().join("-"));
    let fechas_x = array_fechas.map(
      (fecha) => new Date(fecha.split("-").reverse().join("-"))
    );

    if (fechas_x.some((f) => f > fechaNueva)) {
      console.log(
        "Hay fechas del dia de la venta que es mayor o igual a la fecha de consignacion en el banco."
      );
      mostrar_alert(
        "La fecha del día de la venta no puede ser mayor a la fecha de consignación"
      );
      return false;
    } else {
      console.log(
        "Todas las fechas en el array de fechas son menores que fecha_nueva."
      );
      return true;
    }
  }
  /**
   * Funcion para validar que la suma de todos los valores de pagos sea igual al primer valor
   * del input valor_consignacion[]
   */
  const validar_valores_consignados = () => {
    // Obtener todos los inputs con name="valor_consignacion[]"
    const inputs = document.querySelectorAll(
      'input[name="valor_consignacion[]"]'
    );

    /**
     * Validando si la cantidad de input valor_consignacion es igual a 1, es decir solo esta enviando una sola consignacion
     * pues no proceso a generar las validaciones pues solo retorno true para que avnace en la validación.
     */
    if (inputs.length == 1) {
      return true;
    }

    // Obtener el primer valor del primer input
    const primerValor = parseInt(inputs[0].value.replace(/\D/g, ""));

    // Sumar los valores de los demás inputs, excepto el primer valor del primer input
    let suma = 0;
    for (let i = 0; i < inputs.length; i++) {
      const input = inputs[i];
      if (i === 0) {
        // No sumar el primer valor del primer input
        suma += 0;
      } else {
        // Obtener la cantidad del input y sumarla
        const cantidad = parseInt(input.value.replace(/\D/g, ""));
        suma += cantidad;
      }
    }

    // Validar si la suma es correcta
    if (suma === primerValor) {
      // La suma es correcta
      // console.log(`La suma es Correcta ${suma}`);
      return true;
    } else {
      // console.log(`La suma es Incorrecta ${suma}`);
      mostrar_alert(
        "La suma de todos los valores de la venta debe ser igual al Valor Consignación"
      );
      // La suma es incorrecta
      return false;
    }
  };

  /**
   * Funcion que retorna una alerta
   */
  function mostrar_alert(msj) {
    let existingDiv = document.querySelector("#mini-notification");

    if (existingDiv) {
      existingDiv.remove();
    }

    let div = document.createElement("div");
    div.id = "mini-notification";
    div.classList.add("mini-notification");
    div.style.display = "block";

    let p = document.createElement("p");
    p.textContent = msj;

    let span = document.createElement("span");
    span.style.backgroundColor = "#fff";
    span.style.padding = "12px 17px";
    span.style.textAlign = "center";
    span.style.borderRadius = "50%";
    span.style.marginTop = "-15px";
    span.style.marginRight = "20px";

    span.textContent = "5";
    span.style.float = "right";

    p.appendChild(span);
    div.appendChild(p);

    document.body.insertAdjacentElement("afterbegin", div);

    const intervalo = setInterval(function () {
      let contador = parseInt(span.textContent);
      contador--;
      if (contador < 0) {
        clearInterval(intervalo);
        div.style.display = "none";
      } else {
        span.textContent = contador.toString();
      }
    }, 1000);
  }
}

document.addEventListener("DOMContentLoaded", iniciarApp);
