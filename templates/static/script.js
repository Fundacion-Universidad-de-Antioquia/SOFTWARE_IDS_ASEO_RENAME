document.addEventListener("DOMContentLoaded", function() {
  // Obtener el mensaje de error del contenido de la modal
  const errorMessageElement = document.querySelector('#errorModal .modal-body');
  const errorMessage = errorMessageElement ? errorMessageElement.textContent.trim() : '';

  // Depuración: Verifica qué contiene errorMessage
  console.log("Mensaje de error:", errorMessage);

  // Mostrar el modal solo si hay un mensaje de error válido
  if (errorMessage && errorMessage !== "None") {
      const modal = new bootstrap.Modal(document.getElementById('errorModal'));
      modal.show();
  }

  // Redireccionar al hacer clic en el botón de iniciar sesión
  document.getElementById('loginButton').addEventListener('click', function() {
      window.location.href = 'http://localhost:8000/azure_auth/login';
  });

  document.querySelector('.btn-close').addEventListener('click', function() {
    const modalElement = document.getElementById('errorModal');
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    modalInstance.hide();
  });

});
