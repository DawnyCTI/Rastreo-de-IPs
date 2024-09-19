# Rastreo de IPs

Este proyecto es una aplicación web desarrollada con Flask que permite rastrear direcciones IP para obtener información sobre su ubicación geográfica. Utiliza la base de datos GeoLite2 de MaxMind para proporcionar detalles como ciudad, región, país y coordenadas geográficas. La aplicación también permite visualizar la ubicación en un mapa.

## Características

- **Interfaz de Usuario:**
  - **Agregar IPs:** Permite al usuario añadir nuevas direcciones IP a la base de datos.
  - **Mostrar IPs:** Muestra una lista de todas las IPs almacenadas en la base de datos.
  - **Editar IPs:** Permite al usuario actualizar una dirección IP existente.
  - **Eliminar IPs:** Permite al usuario eliminar una dirección IP de la base de datos.
  - **Buscar IP:** Permite al usuario buscar información sobre una IP específica, incluyendo su ubicación en un mapa.

- **Geolocalización:**
  - Utiliza la base de datos GeoLite2 de MaxMind para obtener información de localización basada en IP.
  - Convierte las coordenadas geográficas en formato decimal a formato DMS (grados, minutos, segundos).

- **Base de Datos:**
  - Utiliza SQLite para almacenar las direcciones IP.

## Instalación

### Clonar el Repositorio

```bash
git clone https://github.com/DawnyCTI/Rastreo-de-IPs
cd rastreo-de-ips


