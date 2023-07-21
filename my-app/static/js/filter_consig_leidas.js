const filtraConsigLeidasPorYear = () => {
  let mesSelect = document.querySelector("#filtroPorMes").value;
  filtraConsigLeidasPorMes(mesSelect);
};

/**
 * Funcion que recibe el mes para realizar el filtro
 * y retorna todas las consignaciones que corresponder al mes seleccionado
 */
async function filtraConsigLeidasPorMes(mes) {
  let valorFiltroPorYear = document.querySelector("#filtroPorYear").value;

  //Limpiando input 'filtrarConsigBandEntrada' y ocultando icono de borrar filtro
  document.querySelector("#filtro_resumen_consg_datepicker").value = "";
  document.querySelector(".bi-trash3").style.display = "none";

  /*
  let fechaActual = new Date();
  let mes_actual = ("0" + (fechaActual.getMonth() + 1)).slice(-2);
  mes == "0" ? (mes = mes_actual) : mes;
  */

  let url_api = "";
  if (mes == "0") {
    url_api = "/reset-consignaciones-procesadas";
  } else {
    url_api = "/filtrar-todas-las-consignaciones-leidas-mes-year";
  }

  /**
   * Llamado la funcion para reiniciar los valor por defecto del boton
   */
  reiniciarBtnCargarMasBandejaLeidos();

  const dataPeticion = { mes, valorFiltroPorYear };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url_api, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      document.querySelector(".btnCargarMasConsigLeidas").style.display =
        "none";
      $("#tabla-consignaciones-leidas tbody").html("");
      $("#tabla-consignaciones-leidas tbody").html(`
      <tr>
        <td colspan="4" style="text-align:center;color: red;font-weight: bold;">No hay consignaciones en este mes</td>
      </tr>`);
      return false;
    }

    if (response.data) {
      document.querySelector(".btnCargarMasConsigLeidas").style.display =
        "block";

      //Limpiando el body primero
      $("#tabla-consignaciones-leidas tbody").html("");
      let miData = response.data;
      $("#tabla-consignaciones-leidas tbody").append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}

/*
 * Funcion para manipular le datePicker
 */
$("#filtro_resumen_consg_datepicker").datepicker({
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

/*
 *  Funcion que esta pendiente de la lista o datepicker
 */
$("#filtro_resumen_consg_datepicker").on("change", function () {
  // Limpíando select 'filtroPorMes'
  let filtroPorMes = document.getElementById("filtroPorMes");
  filtroPorMes.selectedIndex = 0;

  let fechaSeleccionada = $(this).val();
  filtrarResumenConsig(fechaSeleccionada);
});

/*
 * Realizar filtro por fecha, para el resumen de consignaciones diaria
 */
async function filtrarResumenConsig(fechaFitro) {
  document.querySelector(".bi-trash3").style.display = "contents";

  const dataPeticion = { fechaFitro };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(
      "/filtrar-consignaciones-procesadas-fecha-especifica",
      dataPeticion,
      { headers }
    );
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    let btnLoaderMoreLeidas = document.querySelector(
      ".btnCargarMasConsigLeidas"
    );
    if (response.data.fin === 0) {
      btnLoaderMoreLeidas.style.display = "none";

      console.log("No hay consignaciones para esta fecha.");
      $("#tabla-consignaciones-leidas tbody").html("");
      $("#tabla-consignaciones-leidas tbody").html(`
      <tr>
        <td colspan="4" style="text-align:center;color: red;font-weight: bold;">No hay consignaciones para esta fecha</td>
      </tr>`);
      return false;
    }

    if (response.data) {
      btnLoaderMoreLeidas.style.display = "none";

      //Limpiando el body primero
      $("#tabla-consignaciones-leidas tbody").html("");
      let miData = response.data;
      $("#tabla-consignaciones-leidas tbody").append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * funcion para el boton cargar mas consiginaciones desde consignaciones Leidas
 */
const cargarMasConsignacionesLeidas = async () => {
  let cuerpo = document.body;

  try {
    let tableElement = document.querySelector("#tabla-consignaciones-leidas");
    // Obtén el último <tr> dentro de la tabla
    let ultimoTr = tableElement.querySelector("tbody tr:last-child");
    // Obtén el valor del atributo "data-id" del último <tr>
    let ultimoId = ultimoTr.getAttribute("data-id");
    let valorYear = parseInt(document.querySelector("#filtroPorYear").value);
    let valorMes = parseInt(document.querySelector("#filtroPorMes").value);

    let fechaActual = new Date();
    let mes_actual = ("0" + (fechaActual.getMonth() + 1)).slice(-2);
    valorMes == 0 ? (valorMes = parseInt(mes_actual)) : valorMes;

    const response = await axios.get(
      `/load_more_consignments_bandeja_leidas/${ultimoId}/${valorYear}/${valorMes}`
    );

    if (response.data.fin === 0) {
      btnMas = document.querySelector(".btnCargarMasConsigLeidas");
      btnMas.classList.remove("btn-primary");
      btnMas.classList.add("btn-warning");
      btnMas.setAttribute("disabled", true);
      btnMas.textContent = "No hay más consignaciones";
      return false;
    }

    // Desplazarse al final del contenedor
    $("html, body").animate(
      { scrollTop: $(".btnCargarMasConsigLeidas").offset().top },
      1200
    );

    cuerpo.classList.add("loader");
    setTimeout(function () {
      cuerpo.classList.remove("loader");
    }, 300);

    $("#tabla-consignaciones-leidas tbody").append(response.data);
  } catch (error) {
    alert("error petición axios 😭");
  } finally {
    console.log("Consulta finalizada");
  }
};

/**
 * Borrar filtros de la filtro por fechas desde la bandeja de leidos
 */
let borrar_filtro_fecha_bandeja_leidos = document.querySelector(
  "#borrar_filtro_fecha_bandeja_leidos"
);

if (borrar_filtro_fecha_bandeja_leidos) {
  borrar_filtro_fecha_bandeja_leidos.addEventListener("click", (event) => {
    document.querySelector("#filtro_resumen_consg_datepicker").value = "";

    let selectElement = document.getElementById("filtroPorMes");
    selectElement.selectedIndex = 0;

    reset_bandeja_leidos();
    document.querySelector(".bi-trash3").style.display = "none";
  });
}

/**
 *  Resetear bandeja de Leidos
 */
async function reset_bandeja_leidos() {
  console.log("lleguee");
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  /**
   * Llamado la funcion para reiniciar los valor por defecto del boton
   */
  reiniciarBtnCargarMasBandejaLeidos();

  try {
    const response = await axios.post("/reset-consignaciones-procesadas", {
      headers,
    });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      $("#tabla-consignaciones-leidas tbody").html("");
      $("#tabla-consignaciones-leidas tbody").html(`
      <tr>
        <td colspan="4" style="text-align:center;color: red;font-weight: bold;">No hay consignaciones</td>
      </tr>`);
      //Ocultando el btn cargar más
      document.querySelector(".btnCargarMasConsigLeidas").style.display =
        "none";
      return false;
    }

    if (response.data) {
      //Limpiando el body primero
      $("#tabla-consignaciones-leidas tbody").html("");
      let miData = response.data;
      $("#tabla-consignaciones-leidas tbody").append(miData);
      document.querySelector(".btnCargarMasConsigLeidas").style.display =
        "block";
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Removiendo el atributo disabled al btn cargar más
 */
const reiniciarBtnCargarMasBandejaLeidos = () => {
  const btnCargarMasConsigLeidas = document.querySelector(
    ".btnCargarMasConsigLeidas "
  );
  btnCargarMasConsigLeidas.disabled = false;
  btnCargarMasConsigLeidas.classList.remove("btn-warning");
  btnCargarMasConsigLeidas.classList.add("btn-primary");
  btnCargarMasConsigLeidas.textContent = "Cargar más consignaciones";
};
