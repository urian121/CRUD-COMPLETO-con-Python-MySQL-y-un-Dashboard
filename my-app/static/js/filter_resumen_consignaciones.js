/*
 * Función para manipular le datePicker (resumenFechaConsignacion)
 */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#resumenFechaConsignacion").value = date_actual();
});

let r_f_c = document.querySelector("#resumenFechaConsignacion");
$(r_f_c).datepicker({
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
 *  Funcion que esta pendiente del datepicker
 */
$(r_f_c).on("change", function () {
  let fechaSeleccionada = $(this).val();
  filtrarResumenConsig(fechaSeleccionada);
});

/*
 * Realizar filtro por fecha, para el resumen de consignaciones diaria
 */
async function filtrarResumenConsig(fechaFitroResumen) {
  try {
    const response = await axios.post(
      "/filtrar-resumen-consignaciones-diarias-fecha-especifica",
      { fechaFitroResumen },
      {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      }
    );
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status} 😭`);
    }

    if (response.data.fin === 0) {
      // console.log("No hay consignaciones para esta fecha.");
      $("#respuesta_filtro_diario").html("");
      $("#respuesta_filtro_diario").html(`
      <p style="text-align:center;color: red;font-weight: bold;">No hay consignaciones para esta fecha</p>`);
      return false;
    }

    if (response.data) {
      //Limpiando el body primero
      $("#respuesta_filtro_diario").html("");
      $("#respuesta_filtro_diario").append(response.data);
      let linkDownloader = document.querySelector(
        "#linkDescargarConsigRecibidas"
      );
      linkDownloader.href =
        "/informe-excel-consignaciones-recibidas/" + fechaFitroResumen;

      document.querySelector(
        "#linkDescargarConsigPendientesFiltro"
      ).href = `/informe-excel-consignaciones-pendientes/${fechaFitroResumen}`;
    }
  } catch (error) {
    console.error(error);
  }
}

function date_actual() {
  let fechaActual = new Date();
  let anio = fechaActual.getFullYear();
  let mes = ("0" + (fechaActual.getMonth() + 1)).slice(-2);
  let dia = ("0" + fechaActual.getDate()).slice(-2);
  let dia_anterior = parseInt(dia - 1);
  //  return `${anio}-${mes}-${dia}`;
  return `${anio}-${mes}-${dia_anterior}`;
}
