let my_button = document.querySelector("#my-button");
my_button ? my_button.setAttribute("disabled", true) : "";

/**
 * Apenas se cargue la lista de consignaciones, con este script
 * agrego el atributo selected a  la lista de meses seleccionando
 * el mes actual
 */

/*
// Obtener el mes actual en formato de dos dígitos (por ejemplo, "01" para enero)
const mesActual = new Date().toLocaleString("es-ES", { month: "2-digit" });
// Obtener el elemento option correspondiente al mes actual
const optionMesActual = document.querySelector(
  `#filtroPorMes_bandeja_entrada option[value="${mesActual}"]`
);
// Establecer el atributo "selected" en "true" en el elemento option del mes actual
optionMesActual ? (optionMesActual.selected = true) : "";
*/

/**
 * Funcion que recibe el año para filtar por el mismo
 */
const filtraConsigPorYear = () => {
  let mesSelect = document.querySelector("#filtroPorMes_bandeja_entrada").value;
  filtraConsigPorMes(mesSelect);
};
/**
 * Funcion que recibe el mes para realizar el filtro
 * y retorna todas las consignaciones que corresponder al mes seleccionado
 */
async function filtraConsigPorMes(mes) {
  document.querySelector(".capa_informe_general").style.display = "none";
  let valorFiltroPorYear = document.querySelector("#filtroPorYear").value;

  //Limpiando input 'filtrarConsigBandEntrada' y ocultando icono de borrar filtro
  document.querySelector("#filtrarConsigBandEntrada").value = "";
  document.querySelector(".bi-trash3").style.display = "none";

  /*let fechaActual = new Date();
  let mes_actual = ("0" + (fechaActual.getMonth() + 1)).slice(-2);
  mes == "0" ? (mes = mes_actual) : mes;
  */

  if (mes == "0") {
    refresh_bandeja_entrada();
    return;
  }

  /**
   * Llamado la funcion para reiniciar los valor por defecto del boton
   */
  reiniciandoBtnCargarMas();

  const dataPeticion = { mes, valorFiltroPorYear };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(
      "/filtrar-consignacion-mes-bandeja-entrada",
      dataPeticion,
      { headers }
    );
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      // console.log("Se han cargado todos los registros.");
      $("#tabla-consignaciones tbody").html("");
      $("#tabla-consignaciones tbody").html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay consignaciones</td>
      </tr>`);
      //Ocultando el btn cargar más
      document.querySelector(".btnCargarMas").style.display = "none";
      return false;
    }

    if (response.data) {
      //Limpiando el body primero
      $("#tabla-consignaciones tbody").html("");
      let miData = response.data;
      $("#tabla-consignaciones tbody").append(miData);

      document.querySelector(".btnCargarMas").style.display = "block";
    }
  } catch (error) {
    console.error(error);
  } finally {
    // console.log("peticion finalizada");
  }
}

/**
 * Funcion para tomar todos los checkbox seleccionados y moverlos
 * a la bandeja de leidos.
 * cuando se hace clic en el checkbox, el objeto de evento se pasa como argumento a la función selectCheckbox().
 * Luego, dentro de la función, se llama al método stopPropagation()
 * en el objeto de evento para evitar que se propague el evento al elemento <tr>
 * y se ejecute la función abrilConsignacion().
 */
function selectCheckbox(event) {
  event.stopPropagation();
  let checkboxes = document.querySelectorAll('input[type="checkbox"]');
  let conteo = 0;

  checkboxes.forEach((checkbox) => {
    if (checkbox.checked) {
      conteo++;
    }
  });
  if (conteo == "0") {
    document.querySelector("#my-button").setAttribute("disabled", true);
  } else {
    document.querySelector("#my-button").removeAttribute("disabled", true);
  }
  //console.log("Hay " + conteo + " checkboxes seleccionados");
}

/**
 * Procesar todos los checkbox seleccionados para ser movidos a bandeja de leidos
 */
async function procesarConsigLeidas() {
  //Procesando los ids de consignaciones seleccionados
  var checkboxes = document.getElementsByName("checkbox_consignacion[]");
  var ids_seleccionados = []; // Declaración de la variable

  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      // Agregar el valor del checkbox a la variable ids_seleccionados
      ids_seleccionados.push(checkboxes[i].value);
    }
  }

  try {
    const response = await fetch("/procesar-checkbox-consignaciones", {
      method: "POST",
      body: JSON.stringify({ ids: ids_seleccionados }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const jsonResponse = await response.json();
      if (jsonResponse && jsonResponse.idsProcesados) {
        let idsConsig = jsonResponse.idsProcesados;
        idsConsig.forEach((idElement) => {
          document.querySelector("#filaIdConsignacion_" + idElement).remove();
        });
        successfull("la acción fue ejecutada con éxito");
      } else {
        console.log("La respuesta del servidor no es válida.");
      }
    } else {
      console.log("Error al procesar el formulario: " + response.status);
    }
  } catch (error) {
    console.log("Error al procesar el formulario:", error);
  } finally {
    // console.log("peticion finalizada.");
  }
}

/**
 * Funcion para obtener mas consignaciones atraves del boton cargar mas
 */
const cargarMas = async () => {
  let cuerpo = document.body;

  try {
    let tableElement = document.querySelector("#tabla-consignaciones");
    // Obtén el último <tr> dentro de la tabla
    let ultimoTr = tableElement.querySelector("tbody tr:last-child");
    // Obtén el valor del atributo "data-id" del último <tr>
    let ultimoId = ultimoTr.getAttribute("data-id");
    let valorYear = parseInt(document.querySelector("#filtroPorYear").value);
    let valorMes = parseInt(
      document.querySelector("#filtroPorMes_bandeja_entrada").value
    );

    let fechaActual = new Date();
    let mes_actual = ("0" + (fechaActual.getMonth() + 1)).slice(-2);
    valorMes == 0 ? (valorMes = parseInt(mes_actual)) : valorMes;

    const response = await axios.get(
      `/load_more_consignments_bandeja_entrada/${ultimoId}/${valorYear}/${valorMes}`
    );

    if (response.data.fin === 0) {
      // console.log("Se han cargado todos los registros.");
      btnMas = document.querySelector(".btnCargarMas");
      btnMas.classList.remove("btn-primary");
      btnMas.classList.add("btn-warning");
      btnMas.setAttribute("disabled", true);
      btnMas.textContent = "No hay más consignaciones";
      return false;
    }

    // Desplazarse al final del contenedor
    $("html, body").animate(
      { scrollTop: $(".btnCargarMas").offset().top },
      1200
    );

    cuerpo.classList.add("loader");
    setTimeout(function () {
      cuerpo.classList.remove("loader");
    }, 300);

    $("#tabla-consignaciones tbody").append(response.data);
  } catch (error) {
    alert("error petición axios 😭");
  } finally {
    // console.log("Consulta finalizada");
  }
};

/**
 * Validar mostrar el btn de subir
 */
$(window).scroll(function () {
  if ($(this).scrollTop() > 200) {
    $("a.scroll-top").fadeIn("slow");
  } else {
    $("a.scroll-top").fadeOut("slow");
  }
});
$("a.scroll-top").click(function (event) {
  event.preventDefault();
  $("html, body").animate({ scrollTop: 0 }, 600);
});

/**
 * Función que recibe un mensaje y retorna el mensaje en la vista
 */
function successfull(msj) {
  divRespuesta = document.querySelector("#respMsj");
  divRespuesta.innerHTML = "";
  divRespuesta.innerHTML = `
           <div class="alert alert-success alert-dismissible" role="alert" style="font-size: 20px;">
            <strong>Felicitaciones</strong>, ${msj}
          </div>
  `;
  setTimeout(function () {
    divRespuesta.innerHTML = "";
  }, 3000);
}

/**
 *
 */
let f_c_b_e = document.querySelector("#filtrarConsigBandEntrada");
$(f_c_b_e).datepicker({
  locale: "es-es",
  minDate: new Date(new Date().getFullYear(), new Date().getMonth() - 2, 1),
  maxDate: new Date(),
  format: "yyyy-mm-dd",
  showMonthAfterYear: false,
  autoclose: true,
  beforeShowMonth: function (date) {
    var currentDate = new Date();
    var disableMonth = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() - 2,
      1
    );
    return date >= disableMonth ? [true, ""] : [false, ""];
  },
});

/**
 * Aplicando evento change
 */
$(f_c_b_e).on("change", function () {
  let valorOption = f_c_b_e.value;

  // Limpíando select 'filtroPorMes_bandeja_entrada'
  let filtroPorMes_bandeja_entrada = document.getElementById(
    "filtroPorMes_bandeja_entrada"
  );
  // Establece el índice de la opción seleccionada en 0 (primera opción)
  filtroPorMes_bandeja_entrada.selectedIndex = 0;

  /**
   * Agrego la fecha al enlace, para descargar el informe general desde la bandeja de entrada
   */
  document.querySelector(".capa_informe_general").style.display = "block";
  let informe_general = document.querySelector("#informe_general");
  if (informe_general) {
    let url_descarga = `/descargar-reporte-general-bandeja-entrada/${valorOption}`;
    informe_general.href = url_descarga;
  }

  filtrarResumenConsigBandejaEntrada(valorOption);
  document.querySelector(".btnCargarMas").style.display = "none";
});

async function filtrarResumenConsigBandejaEntrada(fechaFitro) {
  document.querySelector(".bi-trash3").style.display = "contents";

  const dataPeticion = { fechaFitro };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(
      "/filtrar-consignaciones-bandeja-entrada-fecha-especifica",
      dataPeticion,
      { headers }
    );
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $("#tabla-consignaciones tbody").html("");
      $("#tabla-consignaciones tbody").html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay consignaciones en este mes</td>
      </tr>`);
      return false;
    }

    if (response.data) {
      //Limpiando el body primero
      $("#tabla-consignaciones tbody").html("");
      let miData = response.data;
      $("#tabla-consignaciones tbody").append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Borrar filtros de la filtro por fechas desde la bandeja de entrada
 */
let borrar_filtro_fecha_bandeja_entrada = document.querySelector(
  "#borrar_filtro_fecha_bandeja_entrada"
);

if (borrar_filtro_fecha_bandeja_entrada) {
  borrar_filtro_fecha_bandeja_entrada.addEventListener("click", (event) => {
    document.querySelector(".capa_informe_general").style.display = "none";
    document.querySelector("#filtrarConsigBandEntrada").value = "";
    //Limpiando el select de filtro por mes
    let selectElement = document.getElementById("filtroPorMes_bandeja_entrada");
    // Establece el índice de la opción seleccionada en 0 (primera opción)
    selectElement.selectedIndex = 0;

    refresh_bandeja_entrada();
    document.querySelector(".bi-trash3").style.display = "none";
  });
}

/**
 * Removiendo el atributo disabled al btn cargar más
 */
const reiniciandoBtnCargarMas = () => {
  const btnCargarMas = document.querySelector(".btnCargarMas ");
  btnCargarMas.disabled = false;
  btnCargarMas.classList.remove("btn-warning");
  btnCargarMas.classList.add("btn-primary");
  btnCargarMas.textContent = "Cargar más consignaciones";
};

/**
 * Resetear -Refrescar Bandeja de entrda
 */
async function refresh_bandeja_entrada() {
  //Limpiando input 'filtrarConsigBandEntrada' y ocultando icono de borrar filtro
  document.querySelector("#filtrarConsigBandEntrada").value = "";
  document.querySelector(".bi-trash3").style.display = "none";

  /**
   * Llamado la funcion para reiniciar los valor por defecto del boton
   */
  reiniciandoBtnCargarMas();

  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post("/reset-refresh-bandeja-entrada", {
      headers,
    });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      // console.log("Se han cargado todos los registros.");
      $("#tabla-consignaciones tbody").html("");
      $("#tabla-consignaciones tbody").html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No hay consignaciones</td>
      </tr>`);
      //Ocultando el btn cargar más
      document.querySelector(".btnCargarMas").style.display = "none";
      return false;
    }

    if (response.data) {
      //Limpiando el body primero
      $("#tabla-consignaciones tbody").html("");
      let miData = response.data;
      $("#tabla-consignaciones tbody").append(miData);

      document.querySelector(".btnCargarMas").style.display = "block";
    }
  } catch (error) {
    console.error(error);
  }
}
