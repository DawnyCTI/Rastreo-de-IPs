document.addEventListener('DOMContentLoaded', function() {
    // Obtener datos de las coordenadas directamente desde el DOM
    const datosElement = document.getElementById('datos-json');
    let datos = {};

    if (datosElement) {
        try {
            datos = JSON.parse(datosElement.textContent);
        } catch (e) {
            console.error('Error al parsear los datos JSON:', e);
        }

        // Verificar si los datos están presentes
        if (datos.Latitud && datos.Longitud) {
            const latitud = datos.Latitud;
            const longitud = datos.Longitud;
            mostrarMapa(latitud, longitud);
        } else {
            console.error('No se proporcionaron coordenadas válidas.');
        }
    } else {
        console.error('No se encontraron datos.');
    }
});

function mostrarMapa(latitud, longitud) {
    // Inicializa el mapa y lo centra en las coordenadas proporcionadas
    var map = L.map('map').setView([latitud, longitud], 13);

    // Agrega el mapa base de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Agrega un marcador en las coordenadas y muestra un popup
    L.marker([latitud, longitud]).addTo(map)
        .bindPopup('Ubicación de la IP: ' + latitud + ', ' + longitud)
        .openPopup();
}
