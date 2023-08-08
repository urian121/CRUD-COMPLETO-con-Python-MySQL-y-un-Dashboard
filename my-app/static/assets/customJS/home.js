const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);

function eliminarEmpleado(id_empleado) {
  if (confirm("¿Estas seguro que deseas ELIMINAR el empleado?")) {
    let tr = document.querySelector(`#empleado_${id_empleado}`);

    const urlForm = "/borrar-empleado";
    const requestData = { id_empleado };

    axios
      .post(urlForm, requestData)
      .then((resp) => {
        console.log(resp.data);
        if (resp.data === 1) {
          tr.remove(); //remuevo el registro desde la lista
          mensajeAlerta((msg = "Registro Eliminado con éxito."), (tipo = 1));
        } else {
          console.log("Error al intentar borrar el carro");
        }
      })
      .catch((error) => {
        console.error("Error en la solicitud:", error);
      });
  }
}
