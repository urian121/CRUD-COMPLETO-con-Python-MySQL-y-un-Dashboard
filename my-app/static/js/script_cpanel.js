window.addEventListener("load", (event) => {
  setTimeout(function () {
    $("#loader-out").fadeOut();
  }, 300);

  //modificandoPaginacion();
});

/**
 * Funcion que modificala la paginacion, quitando algunas cosas
 * colocando ciertos textos en español
 */
function modificandoPaginacion() {
  // Obtener el botón "Previous" de la paginación
  var previousButton = document.querySelector(
    '.page-link[aria-label="Previous"]'
  );

  // Verificar si previousButton no es nulo antes de cambiar su contenido
  if (previousButton !== null) {
    // Cambiar el texto del botón "Anterior" por "Anterior"
    previousButton.innerHTML =
      '<i class="bi bi-arrow-left-circle" style="color: #222;"></i> <span class="sr-only">Anterior</span>';
  }

  // Obtener el botón "Next" de la paginación
  var nextButton = document.querySelector('.page-link[aria-label="Next"]');
  // Verificar si previousButton no es nulo antes de cambiar su contenido
  if (nextButton !== null) {
    // Cambiar el texto del botón "Next" por "Siguiente"
    nextButton.innerHTML =
      '<span class="sr-only">Siguiente <i class="bi bi-arrow-right-circle" style="color: #222;"></i></span>';
  }

  // Quitando el current que sale por defecto en la hoja seleccionada
  var currentElement = document.querySelector(
    ".page-item .active .page-link .sr-only"
  );
  currentElement !== null ? (currentElement.innerHTML = "") : "";
}

/**
 * Ignorar cosignacion desde bandeja entrada
 */
let elem = document.getElementById("ignorarConsignacionBtn");
if (elem) {
  elem.addEventListener("click", function (event) {
    event.preventDefault(); // Evitar el comportamiento predeterminado del enlace

    if (confirm("¿Estas seguro que deseas ignorar esta consignación?")) {
      let url = this.getAttribute("data-href");
      if (url) {
        window.location.href = url;
      }
    }
  });
}

/**
 * Leer consignación desde cualquier bandeja
 */
let tbody_consignaciones = document.querySelector("tbody");
if (tbody_consignaciones) {
  tbody_consignaciones.addEventListener("click", (event) => {
    let target = event.target;
    //let cellIndex = target.cellIndex;

    if (target.tagName === "TD" && target.parentElement.tagName === "TR") {
      let cellIndex = target.cellIndex;
      // console.log("Cell Index:", cellIndex);

      let tableBody = document.querySelector("table").getAttribute("id");
      if (tableBody == "tabla-consignaciones") {
        if (cellIndex === 0 || cellIndex === undefined) {
          //no hacer nada xq se hizo click en el primer td de cualquier fila tr
          return;
        }
      }

      abrilConsignacion(target.parentElement);
    }
  });
}

function abrilConsignacion(info_row) {
  // console.log("mi funcion", info_row);
  let id_consignacion = info_row.dataset.id;
  // console.log(id_consignacion);

  let tableHTML = document.querySelector("table");
  // console.log(tableHTML);
  idTable = tableHTML.getAttribute("id");

  let url_consignacion = "";
  if (idTable == "tabla-consignaciones") {
    url_consignacion = `/read-consignment/${id_consignacion}?from=bandeja_entrada`;
  } else if (idTable == "tabla-consignaciones-leidas") {
    // console.log("tabla ", idTable);
    url_consignacion = `/read-consignment/${id_consignacion}?from=bandeja_leidos`;
  } else if (idTable == "tabla-consig-diarias-recibidas") {
    // console.log(`Tabla ${idTable}`);
    url_consignacion = `/read-consignment/${id_consignacion}?from=bandeja_leidos`;
  }

  if (url_consignacion) {
    window.location.href = url_consignacion;
  }
}
