// Inicializando SocketIO
const socket = io();

//Escuchando connect
socket.on("connect", function () {
  console.log("Socket Activo.!");
});

//Escuchando disconnect
socket.on("disconnect", function () {
  console.log("Socket Desconectado.!");
});

// Escuchando por processConsigOKBD
socket.on("processConsigOKBD", (ultima_consignacion) => {
  let tabla_consignaciones = document.querySelector("#tabla-consignaciones");

  // Convertir el resultado en un objeto JavaScript
  let resultado = JSON.parse(ultima_consignacion);

  // Obtener el tbody de la tabla
  let tbody = tabla_consignaciones.querySelector("tbody");

  // Crear una nueva fila tr
  let fila = document.createElement("tr");
  fila.setAttribute("data-bs-toggle", "tooltip");
  fila.setAttribute("data-bs-offset", "0,4");
  fila.setAttribute("data-bs-placement", "top");
  fila.setAttribute("data-bs-html", "true");
  fila.setAttribute("title", "");
  fila.setAttribute("style", "color: #333 !important");
  fila.setAttribute(
    "data-href",
    `/read-consignment/${resultado.id}?from=bandeja_entrada`
  );
  fila.setAttribute("onclick", "abrilConsignacion(this)");
  fila.setAttribute("id", `filaIdConsignacion_${resultado.id}`);
  fila.setAttribute("data-id", resultado.id);
  fila.classList.add("noLeido");
  fila.setAttribute("data-bs-original-title", "<span>Leer consignación</span>");

  // Crear el primer td
  let td1 = document.createElement("td");

  // Crear el div dentro del primer td
  let divCheckbox = document.createElement("div");
  divCheckbox.classList.add("form-group");

  // Crear la etiqueta label dentro del div
  let label = document.createElement("label");
  label.classList.add("form-check-label");
  label.setAttribute("for", resultado.id);

  // Crear el icono dentro de la etiqueta label
  let icono = document.createElement("i");
  icono.classList.add("bi", "bi-arrow-right");
  icono.style.padding = "0px 40px 0px 5px";
  label.appendChild(icono);

  // Agregar el nombre de la tienda al label
  label.appendChild(document.createTextNode(resultado.nombre_tienda));

  // Agregar el checkbox y el label al div
  //divCheckbox.appendChild(checkbox);
  divCheckbox.appendChild(label);

  // Agregar el div al primer td
  td1.appendChild(divCheckbox);

  // Agregar el primer td a la fila
  fila.appendChild(td1);

  // Crear el segundo td con el valor de nota_consignacion
  let td2 = document.createElement("td");
  td2.appendChild(document.createTextNode(resultado.nota_consignacion));
  fila.appendChild(td2);

  // Crear el icono de consignación no leída
  let iconoNoLeida = document.createElement("i");
  iconoNoLeida.classList.add("bi", "bi-check2");
  iconoNoLeida.setAttribute("style", "color: #fa5c7c");
  iconoNoLeida.setAttribute("data-bs-toggle", "tooltip");
  iconoNoLeida.setAttribute("data-bs-offset", "0,4");
  iconoNoLeida.setAttribute("data-bs-placement", "top");
  iconoNoLeida.setAttribute("data-bs-html", "true");
  iconoNoLeida.setAttribute("title", "");
  iconoNoLeida.setAttribute(
    "data-bs-original-title",
    "<span>Consignación no leída</span>"
  );

  // Crear el enlace desactivado para mover a leídos
  let enlaceLeidos = document.createElement("a");
  enlaceLeidos.setAttribute("style", "pointer-events: none; cursor: default");
  enlaceLeidos.setAttribute("disabled", "disabled");
  enlaceLeidos.setAttribute("href", "#");

  // Agregar el icono de consignación no leída y el enlace a la celda
  let td3 = document.createElement("td");
  td3.appendChild(iconoNoLeida);
  fila.appendChild(td3);

  // Crear el cuarto td con el valor de dia_de_la_ventaBD
  let td4 = document.createElement("td");
  td4.appendChild(enlaceLeidos);
  // let fecha_f_c_b = new Date(resultado.fecha_consignacion_banco);
  // let formatoDeseado = fecha_f_c_b.toISOString().split("T")[0];
  td4.appendChild(document.createTextNode(resultado.fecha_consignacion_banco));

  fila.appendChild(td4);

  let td5 = document.createElement("td");
  td5.appendChild(document.createTextNode(resultado.dia_de_la_ventaBD));
  fila.appendChild(td5);

  // Insertar la fila en la primera posición del tbody
  tbody.insertBefore(fila, tbody.firstChild);

  //console.log(fila);
});
