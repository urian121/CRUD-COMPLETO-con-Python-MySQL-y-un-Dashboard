window.addEventListener("load", (event) => {
  //Eliminando la variable clicks si existe
  localStorage.removeItem("clicks");

  setTimeout(function () {
    $("#loader-out").fadeOut();
  }, 300);
});

$("#fecha_consignacion_banco_datepicker").datepicker({
  //uiLibrary: "bootstrap4",
  locale: "es-es",
  minDate: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1),
  maxDate: new Date(),
  format: "dd-mm-yyyy",
  showMonthAfterYear: false,
  autoclose: true,
  beforeShowMonth: function (date) {
    var currentDate = new Date();
    var disableMonth = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() - 1,
      1
    );
    var monthToShow = date >= disableMonth ? [true, ""] : [false, ""];
    return monthToShow;
  },
});
let fechaRegistro = document.querySelector(
  "#fecha_consignacion_banco_datepicker"
);
fechaRegistro ? (fechaRegistro.value = miFechaActual()) : "";

function activarDatePickerTwo() {
  $("#datepicker_1").datepicker({
    //uiLibrary: "bootstrap4",
    locale: "es-es",
    minDate: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1),
    maxDate: new Date(),
    format: "dd-mm-yyyy",
    showMonthAfterYear: false,
    autoclose: true,
    beforeShowMonth: function (date) {
      var currentDate = new Date();
      var disableMonth = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth() - 1,
        1
      );
      var monthToShow = date >= disableMonth ? [true, ""] : [false, ""];
      return monthToShow;
    },
  });
  let f_datepicker_1 = document.querySelector("#datepicker_1");
  f_datepicker_1 ? (f_datepicker_1.value = miFechaActual()) : "";

  document
    .querySelector("#valor_consignacion_varios_pagos")
    .addEventListener("input", (inputClick) => {
      let cantidad = inputClick.target.value.replace(/\D/g, ""); // Eliminar caracteres no numéricos
      cantidad = parseInt(cantidad, 10); // Convertir a número entero
      if (isNaN(cantidad)) {
        cantidad = 0; // Si no se puede convertir a número, se establece en 0
      }
      // Formatear la cantidad y asignarla al campo de entrada
      inputClick.target.value =
        "$ " +
        cantidad.toLocaleString("es-CO", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        });
    });
}
/*
 * Obtener la fecha actual
 */
function miFechaActual() {
  let fechaActual = new Date();
  let anio = fechaActual.getFullYear();
  let mes = ("0" + (fechaActual.getMonth() + 1)).slice(-2);
  let dia = ("0" + fechaActual.getDate()).slice(-2);
  return `${dia}-${mes}-${anio}`;
}

/**
 * Capturar el valor de la consignacion para ser formateado
 */
/*const valorConsig = document.querySelector("#valor_consignacion_diaria");
if (valorConsig != null) {*/
let valorConsigDiaria = document.querySelector("#valor_consignacion_diaria");
if (valorConsigDiaria) {
  valorConsigDiaria.addEventListener("input", (inputClick) => {
    let cantidad = inputClick.target.value.replace(/\D/g, ""); // Eliminar caracteres no numéricos
    cantidad = parseInt(cantidad, 10); // Convertir a número entero
    if (isNaN(cantidad)) {
      cantidad = 0; // Si no se puede convertir a número, se establece en 0
    }
    // Formatear la cantidad y asignarla al campo de entrada
    inputClick.target.value =
      "$ " +
      cantidad.toLocaleString("es-CO", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      });
  });
}

//Funcion para formatear cantidades a Pesos Colombianos
function formatearCantidad(valor_inic) {
  //Formatear cantidades a pesos Colombianos
  const inputCantidadList = document.querySelectorAll(
    "#valor_consignacion_grupal_" + valor_inic
  );

  inputCantidadList.forEach((inputCantidad) => {
    inputCantidad.addEventListener("input", (input) => {
      let cantidad = input.target.value.replace(/\D/g, ""); // Eliminar caracteres no numéricos
      cantidad = parseInt(cantidad, 10); // Convertir a número entero
      if (isNaN(cantidad)) {
        cantidad = 0; // Si no se puede convertir a número, se establece en 0
      }
      // Formatear la cantidad y asignarla al campo de entrada
      input.target.value =
        "$ " +
        cantidad.toLocaleString("es-CO", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        });
    });
  });
}

//Vista previa del archivo imagen
let fileD = document.getElementById("archivo");
if (fileD) {
  fileD.addEventListener("change", function (event) {
    const archivo = event.target.files[0]; // Obtener el archivo cargado
    const tamanoMaximoBytes = 10 * 1024 * 1024; // 10 megabytes en bytes

    let divMensaje = document.querySelector(".mensaje");
    if (archivo.size > tamanoMaximoBytes) {
      divMensaje.style.display = "block";
      divMensaje.textContent =
        "La imagen supera el tamaño máximo permitido de 10 megabytes.";
      event.target.value = ""; // Limpiar el campo de archivo cargado

      document.querySelector("#preview").src = "";
      return;
    } else {
      divMensaje.textContent = "";
      divMensaje.style.display = "none";

      var reader = new FileReader();
      reader.onload = function () {
        document.getElementById("preview").src = reader.result;
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  });
}

/**
 * Funcion para generar una vista previa de la imagen
 */
// JavaScript
function viewPrevioFotos() {
  const archivoInput = document.getElementById("archivo");
  const previewsContainer = document.getElementById("previews-container");

  archivoInput.addEventListener("change", function () {
    const archivos = this.files;
    previewsContainer.innerHTML = ""; // Clear previous previews

    let totalSize = 0;

    // Loop through all selected files
    for (let i = 0; i < archivos.length; i++) {
      const archivo = archivos[i];
      const reader = new FileReader();

      // Validate file type (image/*)
      if (!archivo.type.startsWith("image/")) {
        // Show an error message for invalid file types
        document.querySelector(".mensaje").innerText =
          "Por favor, seleccione solo imágenes (JPG o PNG).";
        document.querySelector(".mensaje").style.display = "block";
        return;
      }

      // Validate file size (not more than 8 MB)
      if (archivo.size > 8 * 1024 * 1024) {
        // Show an error message for oversized files
        document.querySelector(".mensaje").innerText =
          "El tamaño máximo permitido para cada imagen es de 8 MB.";
        document.querySelector(".mensaje").style.display = "block";
        return;
      }

      // Calculate total size of all images
      totalSize += archivo.size;

      // Generate preview for each image
      reader.addEventListener("load", function () {
        const previewImagen = document.createElement("img");
        previewImagen.classList.add("img-fluid");
        previewImagen.src = this.result;
        previewsContainer.appendChild(previewImagen);
      });

      reader.readAsDataURL(archivo);
    }

    // Validate total size of all images (not more than 10 MB)
    if (totalSize > 10 * 1024 * 1024) {
      // Show an error message for oversized total size
      document.querySelector(".mensaje").innerText =
        "El peso total de las imágenes no debe superar los 10 MB.";
      document.querySelector(".mensaje").style.display = "block";
      return;
    }

    // If everything is valid, clear the error message
    document.querySelector(".mensaje").innerText = "";
    document.querySelector(".mensaje").style.display = "none";
  });
}

// Call the function to initialize the image previews and validation
viewPrevioFotos();

/*Toggle switch, cuando esta oculto estos inputs,
 * les aplico el atributo disabled, para evitar que se envien
 */
/*
const toggleConsignacionDiaria = () => {
  //Luego activo mi consignacion diaria
  let respConsig = document.querySelector("#capaConsignacionDiaria");
  if (respConsig.style.display === "none") {
    respConsig.style.display = "block";
    console.log("a");
  } else {
    respConsig.style.display = "none";
  }
};
*/

//Otra forma de negar un valor
/*let miVariable = false;
const variasConsignaciones = () => {
  miVariable = !miVariable;
  if (miVariable) {
    fetch("/form-varios-pagos")
      .then((response) => response.text())
      .then((data) => {
        // Hacer algo con el contenido del archivo cargado
        document.querySelector("#capa_formularios").innerHTML = data;
        activarDatePickerTwo();
        viewPrevioFoto();
      })
      .catch((error) => {
        console.error(error);
      });
  } else {
    fetch("/form-pago-diario")
      .then((response) => response.text())
      .then((data) => {
        // Hacer algo con el contenido del archivo cargado
        document.querySelector("#capa_formularios").innerHTML = data;
      })
      .catch((error) => {
        console.error(error);
      });
  }
};
*/

/**
 * Funcion para crear campos de forma dinamica.
 */
let inic = 1;
let count = 0;
const agregarMasConsignaciones = () => {
  document.querySelector("#btnAddConsig").style.display = "none";

  inic++;
  count++; // Incrementar el contador en cada clic

  if (inic >= 0) {
    eliminarBTNagregarMasConsig();
  }

  // console.log("clicks ", inic, count);
  // console.log("total clics " + count);
  // Verificar si la variable existe en el localStorage
  if (!localStorage.getItem("clicks")) {
    // Si no existe, crearla y asignarle un valor inicial
    localStorage.setItem("clicks", parseInt(count));
  } else {
    // Si existe, actualizar su valor
    localStorage.setItem("clicks", parseInt(count));
  }

  $("#resultCreatedMore").append(`
  <div class="form-group row" id="newRow_${inic}">
      <div class="col-md-4 mb-3">
        <label for="valor_consignacion_${inic}" class="form-label">Valor Venta</label>
        <input type="text" name="valor_consignacion[]" id="valor_consignacion_grupal_${inic}" class="form-control" required>
      </div>
      <div class="col-md-3 mb-3">
        <label for="fechaConsignacion_${inic}" class="form-label" style="color:#566a7f !important;">Día de la Venta</label>
        <input type="text" name="dia_de_la_venta[]"  id="datepicker_${inic}" style="max-width: 80%" class="form-control" readonly required>
      </div>
      <div class="col-md-5 mb-3 mt-4">
        <button type="button" class="btn btn-warning mb-2" onclick="borrarConsig('${inic}');">
          <i class="bi bi-dash"></i> Eliminar 
        </button>
        <button type="button" class="btn btn-primary mb-2 createBTNAddConsig" id="btnCreate_${inic}" onclick="agregarMasConsignaciones();">
          <i class="bi bi-plus"></i> Agregar
        </button>
      </div>
    </div>`);

  $("#datepicker_" + inic).datepicker({
    //uiLibrary: "bootstrap4",
    locale: "es-es",
    minDate: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1),
    maxDate: new Date(),
    format: "dd-mm-yyyy",
    showMonthAfterYear: false,
    autoclose: true,
    beforeShowMonth: function (date) {
      var currentDate = new Date();
      var disableMonth = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth() - 1,
        1
      );
      var monthToShow = date >= disableMonth ? [true, ""] : [false, ""];
      return monthToShow;
    },
  });
  let datepicker_x = document.querySelector("#datepicker_" + inic);
  datepicker_x ? (datepicker_x.value = miFechaActual()) : "";

  formatearCantidad(inic);
  mostrarOcultarCorteConsignacion(inic);
};

/**
 * Funcion que recibe el numero de filas por consignaciones a crear
 */
function eliminarBTNagregarMasConsig() {
  let btns = document.querySelectorAll(".createBTNAddConsig");
  btns.forEach((element) => {
    // console.log(element);
    element.style.display = "none";
  });
}

const borrarConsig = (valor) => {
  // console.log("*** ", inic);
  // console.log("valor a eliminar ", valor);
  // Verificar si la variable existe en el localStorage
  if (localStorage.getItem("clicks")) {
    let valorClick = localStorage.getItem("clicks");
    //console.log("total click del LocalStorage " + valorClick);

    localStorage.setItem("clicks", valorClick - 1);

    if (localStorage.getItem("clicks") == 0) {
      document.querySelector("#btnAddConsig").style.display = "block";

      inic = 1;
      count = 0;

      // console.log("No hay elemento");
      // console.log(`Valores reiniciados inic =${inic} y count= ${count}`);
      document.querySelector("#volver_datepicker").style.display = "none";
      document.querySelector("#dia_de_la_venta_datepicker").value = "";
      document.querySelector("#cuerpo_datepicker").style.display = "block";
    } else {
      console.log("Hay elementos");
    }

    $("#newRow_" + valor).remove();

    if (inic == valor || inic != valor) {
      //console.log("inic = ", inic);
      //console.log("valor = " + valor);
      let btn = document.querySelectorAll(".createBTNAddConsig");
      if (btn.length > 0) {
        let ultimoBtn = btn[btn.length - 1];
        //console.log(ultimoBtn);
        document.querySelector(`#${ultimoBtn.id}`).style.display =
          "inline-block";
      }
    }
  }
};

/**
 * Funcion para  mostrar/ocultar el input dia_de_la_venta_datepicker de acuerdo si tengo varias consignaciones lo oculto
 * de lo contrario lo muestro
 */
function mostrarOcultarCorteConsignacion(click) {
  let cuerpo_datepicker = document.querySelector("#cuerpo_datepicker");
  cuerpo_datepicker.style.display = "none";

  let date_picker = document.querySelector("#dia_de_la_venta_datepicker");
  date_picker.value = "01-01-1900";

  let volver_datepicker = document.querySelector("#volver_datepicker");
  volver_datepicker.style.display = "block";
  volver_datepicker.addEventListener("click", (e) => {
    document.querySelector("#btnAddConsig").style.display = "block";

    //Eliminando la variable clicks si existe
    localStorage.removeItem("clicks");
    inic = 1;
    count = 0;

    document.querySelector("#resultCreatedMore").innerHTML = "";
    cuerpo_datepicker.style.display = "block";
    volver_datepicker.style.display = "none";
    date_picker.value = "";
  });
}

$("#dia_de_la_venta_datepicker").datepicker({
  //uiLibrary: "bootstrap4",
  locale: "es-es",
  minDate: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 1),
  maxDate: new Date(),
  format: "dd-mm-yyyy",
  showMonthAfterYear: false,
  autoclose: true,
  beforeShowMonth: function (date) {
    var currentDate = new Date();
    var disableMonth = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() - 1,
      1
    );
    var monthToShow = date >= disableMonth ? [true, ""] : [false, ""];
    return monthToShow;
  },
});

/*
FUNCIONA CON AJAX, el dilema esta en formatear los datos antes de enviarlo
$.ajax({
  type: "POST",
  url: "/procesar-filtro-consign-diaria",
  data: JSON.stringify({ lista1, lista2 }),
  contentType: "application/json",
  success: function (data) {
    console.log(data);
    // Aquí puedes hacer algo si la solicitud AJAX fue exitosa
  },
  error: function () {
    console.log("Error en la solicitud");
    // Aquí puedes hacer algo si la solicitud AJAX falló
  },
});
*/
