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

/**
 * Verificar si existe alerta para ocultarla
 */
// encontrar el elemento con la clase "alert"
var alertElement = document.querySelector(".alert");

// verificar si el elemento existe
if (alertElement) {
  // esperar 5 segundos antes de hacer que el elemento desaparezca
  setTimeout(function () {
    alertElement.style.opacity = "0"; // establecer la opacidad a 0 para hacer que el elemento desaparezca
    alertElement.style.transition = "opacity 1s ease"; // establecer la transición para que el elemento desaparezca gradualmente
    setTimeout(function () {
      alertElement.remove(); // eliminar el elemento del DOM después de la transición
    }, 1000);
  }, 5000);
}

let i = document.querySelector(".bx-hide");
i.addEventListener("click", (e) => {
  var tipoinput = document.querySelector("#pass_user");
  tipoinput.type === "password"
    ? (tipoinput.type = "text")
    : (tipoinput.type = "password");
});
