const form = document.getElementById("form-confirmacion");

form.addEventListener("submit", function (event) {
  event.preventDefault(); // Evita el envío tradicional

  const input = this.codigo_descuento;
  const codigo = input.value;
  const url = this.action + '?codigo=' + codigo; // URL de la API
  const cont_total = document.getElementById("orden_total");
  const cont_success = document.getElementById("codigo_success");

  console.log(url)  // Verifica la URL generada
  // Realiza la solicitud GET a la API

  fetch(url)
    .then(response => response.json())
    .then(response => {
      
      if (response.status === true) {
        let total = Number(response.total);
        let formateado = total.toLocaleString('es-AR', {
          style: 'currency',
          currency: 'ARS',
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });

        cont_total.innerHTML = formateado;




        cont_success.classList.remove('text-danger');
        cont_success.classList.add('text-success');
        cont_success.innerHTML = 'Código de descuento aplicado correctamente.';
        
      
      } else {
        cont_success.innerHTML = 'Código de descuento inválido.';
        input.value = ""; // Limpia el campo de entrada
        cont_success.classList.remove('text-success');
        cont_success.classList.add('text-danger');
      }







      
    })    
});
