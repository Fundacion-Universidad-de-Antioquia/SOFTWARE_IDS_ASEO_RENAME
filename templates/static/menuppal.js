$(document).ready(function() {
    $('#justificacion-textarea').closest('.form-group').hide();
    $('#validarZonaBtn').prop('disabled', true);

    // Función para cargar zonas
    cargarZonas();

    function cargarZonas() {
        $.ajax({
            url: '/api/zonas/',
            type: 'GET',
            success: function(data) {
                var $select = $('#id_zona');
                $select.empty();
                $select.append($('<option>', {
                    value: '',
                    text: 'Seleccione una zona'
                }));
                data.forEach(function(zona) {
                    if (zona) {
                        $select.append($('<option>', { 
                            value: zona, 
                            text: zona 
                        }));
                    }
                });

                // Validación de formulario al cambiar la selección
                $select.change(function() {
                    validarFormulario();
                });

                // Obtener el correo de la tabla
                const selectedRow = document.querySelector('tbody tr');
                const correo = selectedRow ? selectedRow.cells[4].innerText : '';

                // Verificar si existe el correo y habilitar/deshabilitar campos
                if (correo) {
                    sendLogUpdateRequest(correo);
                } else {
                    mostrarAlertaCorreoFaltante();
                    bloquearCampos();
                }
            },
            error: function() {
                console.error('Error loading zones');
            }
        });
    }

    // Función para mostrar una alerta si no hay correo
    function mostrarAlertaCorreoFaltante() {
        Swal.fire({
            title: 'Advertencia',
            text: 'No se encontró un correo válido para el usuario. Por favor, comuniquese con su jefe inmediato he informe sobre este inconveniente.',
            icon: 'warning'
        });
    }

    // Función para bloquear campos
    function bloquearCampos() {
        $('#id_zona').prop('disabled', true);
        $('#justificacion-textarea').prop('disabled', true);
        $('#validarZonaBtn').prop('disabled', true);
    }

    // Función para desbloquear campos cuando se obtiene el correo
    function desbloquearCampos() {
        $('#id_zona').prop('disabled', false);
        $('#justificacion-textarea').prop('disabled', false);
        validarFormulario();
    }

    // Validar el formulario basado en la entrada de usuario
    function validarFormulario() {
        const selectedZona = $('#id_zona').val();
        const fecha = $('#id_fecha').val();
        const justificacionVisible = $('#justificacion-textarea').closest('.form-group').is(':visible');
        const justificacion = $('#justificacion-textarea').val();

        if (selectedZona && fecha && (!justificacionVisible || justificacion)) {
            $('#validarZonaBtn').prop('disabled', false);
        } else {
            $('#validarZonaBtn').prop('disabled', true);
        }
    }

    // Validación de zona y otros campos
    function validarZona() {
        const selectedZona = document.getElementById('id_zona').value;
        const selectedRow = document.querySelector('tbody tr');
        const selectedNombre = selectedRow ? selectedRow.cells[1].innerText : '';
        const selectedDepartamento = selectedRow ? selectedRow.cells[3].innerText : '';
        const correo = $('#userEmail').val();  // Capturar el correo desde un campo oculto

        if (!selectedZona || !selectedNombre || !selectedDepartamento) {
            Swal.fire({
                title: 'Advertencia',
                text: 'Por favor, seleccione una zona y asegúrese de que el nombre y el departamento estén disponibles.',
                icon: 'warning'
            });
            return;
        }

        const capturedZona = selectedRow ? selectedRow.cells[2].innerText : '';

        if (selectedZona !== capturedZona) {
            Swal.fire({
                title: 'Confirmación',
                text: 'La zona seleccionada es diferente a la zona capturada. ¿Está seguro que desea continuar?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Sí',
                cancelButtonText: 'No',
                customClass: {
                    confirmButton: 'btn-confirm', // Clase personalizada para el botón "Sí"
                    cancelButton: 'btn-cancel'    // Clase personalizada para el botón "No"
                },
                buttonsStyling: false  // Necesario para aplicar las clases personalizadas
            }).then((result) => {
                if (result.isConfirmed) {
                    continuarValidacion(selectedZona, selectedNombre, selectedDepartamento);
                }
            });
        } else {
            continuarValidacion(selectedZona, selectedNombre, selectedDepartamento);
        }
    }

    // Continuar con la validación
    function continuarValidacion(selectedZona, selectedNombre, selectedDepartamento) {
        const fecha = $('#id_fecha').val();
        const justificacion = $('#justificacion-textarea').val();
        const correo = $('#userEmail').val();  // Obtener el correo desde el input oculto
        // Guardar justificación en sessionStorage
        if (justificacion) {
            sessionStorage.setItem('justificacion', justificacion);
        }
        // Guardar justificación en sessionStorage
        if (fecha) {
            sessionStorage.setItem('fecha', fecha);
        }
        $.ajax({
            url: '/api/guardar_fecha/',
            type: 'POST',
            data: {
                'fecha': fecha,
                'justificacion': justificacion,
                'correo': correo,  // Pasar el correo
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function() {
                window.location.href = `/azure_auth/novedades/?zona=${selectedZona}&nombre=${selectedNombre}&departamento=${selectedDepartamento}`;
            },
            error: function() {
                Swal.fire({
                    title: 'Error',
                    text: 'Error al guardar la fecha y justificación en la sesión.',
                    icon: 'error'
                });
            }
        });
    }

    $('#validarZonaBtn').click(validarZona);

    // Solicitud de actualización de log
    function sendLogUpdateRequest(correo) {
        fetch(`https://app-conexionerp-prod-001.azurewebsites.net/logs/consultar/?correo=${encodeURIComponent(correo)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            updateFormDate(data.new_date, data.requires_justification);
            desbloquearCampos();  // Desbloquear campos una vez se recibe la respuesta y hay correo
        })
        .catch(err => {
            console.error('Error updating log:', err);
        });
    }

    // Actualización de la fecha del formulario
    function updateFormDate(newDate, requiresJustification) {
        const dateField = document.getElementById('id_fecha');
        dateField.value = newDate;

        if (requiresJustification) {
            $('#justificacion-textarea').closest('.form-group').show();
        } else {
            $('#justificacion-textarea').closest('.form-group').hide();
        }

        validarFormulario();
    }

    $('#justificacion-textarea').on('input', function() {
        validarFormulario();
    });

    $('#id_fecha').on('input', function() {
        validarFormulario();
    });
});
