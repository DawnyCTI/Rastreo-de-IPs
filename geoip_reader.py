# geoip_reader.py
import geoip2.database
from flask import render_template

# Carga de la base de datos GeoIP
reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')

def buscar_ip(ip):
    ip = ip.strip()  # Limpia espacios en blanco
    try:
        response = reader.city(ip)
        datos = {
            'IP': ip,
            'Ciudad': response.city.name,
            'Región': response.subdivisions.most_specific.name,
            'País': response.country.name,
            'Latitud': response.location.latitude,
            'Longitud': response.location.longitude
        }
        return datos, None
    except geoip2.errors.AddressNotFoundError:
        return None, 'Dirección IP no encontrada'
    except Exception as e:
        return None, str(e)
