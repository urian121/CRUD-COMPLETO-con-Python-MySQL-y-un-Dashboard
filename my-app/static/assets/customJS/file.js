/**
 *
 * General vista previa de imagen perfil cargada
 */
function readURL(input) {
  if (input.files && input.files[0]) {
    var imageUrl = URL.createObjectURL(input.files[0]);
    $("#imagePreview").css("background-image", "url(" + imageUrl + ")");
    $("#imagePreview").hide();
    $("#imagePreview").fadeIn(650);
  }
}

$("#imageUpload").change(function () {
  readURL(this);
});

/**
 * Formatear cantidad en salario
 */
let salario = document.querySelector("#salario_empleado");
if (salario) {
  salario.addEventListener("input", (inputClick) => {
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
