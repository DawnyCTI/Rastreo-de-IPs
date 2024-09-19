from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import geoip2.database

app = Flask(__name__)

# Crear la base de datos si no existe
def crear_bd():
    con = sqlite3.connect("ip_database.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ips (id INTEGER PRIMARY KEY, ip TEXT NOT NULL)")
    con.commit()
    con.close()

# Función para convertir coordenadas decimales a DMS
def decimal_a_dms(latitud_decimal, longitud_decimal):
    def convertir_dms(coordenada_decimal):
        grados = int(coordenada_decimal)
        minutos = int((coordenada_decimal - grados) * 60)
        segundos = (coordenada_decimal - grados - minutos / 60) * 3600
        return grados, minutos, segundos

    lat_grados, lat_minutos, lat_segundos = convertir_dms(abs(latitud_decimal))
    lon_grados, lon_minutos, lon_segundos = convertir_dms(abs(longitud_decimal))

    lat_dir = 'N' if latitud_decimal >= 0 else 'S'
    lon_dir = 'E' if longitud_decimal >= 0 else 'W'

    return {
        'latitud': f"{lat_grados}°{lat_minutos}'{lat_segundos:.1f}\"{lat_dir}",
        'longitud': f"{lon_grados}°{lon_minutos}'{lon_segundos:.1f}\"{lon_dir}"
    }

# Función para rastrear IP usando GeoIP2
def rastrear_ip(ip):
    ruta_db = 'GeoLite2-City.mmdb'
    try:
        reader = geoip2.database.Reader(ruta_db)
        response = reader.city(ip)
        
        coordenadas_dms = decimal_a_dms(response.location.latitude, response.location.longitude)
        return {
            "IP": ip,
            "Ciudad": response.city.name,
            "Región": response.subdivisions.most_specific.name,
            "País": response.country.name,
            "Latitud": response.location.latitude,
            "Longitud": response.location.longitude
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"No se pudo rastrear la IP: {e}"}

# Página principal para mostrar las IPs guardadas
@app.route('/')
def index():
    con = sqlite3.connect("ip_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ips")
    ips = cur.fetchall()
    con.close()
    return render_template('index.html', ips=ips)

# Ruta para guardar una nueva IP
@app.route('/guardar', methods=['POST'])
def guardar():
    ip = request.form['ip']
    con = sqlite3.connect("ip_database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO ips (ip) VALUES (?)", (ip,))
    con.commit()
    con.close()
    return redirect(url_for('index'))

# Ruta para buscar información de una IP
@app.route('/buscar', methods=['POST'])
def buscar():
    ip = request.form['ip_buscar']
    datos = rastrear_ip(ip)
    
    # Verificar los datos en la consola
    print("Datos de búsqueda:", datos)
    
    con = sqlite3.connect("ip_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ips")
    ips = cur.fetchall()
    con.close()

    return render_template('index.html', datos=datos, ips=ips)

# Ruta para editar una IP existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nueva_ip = request.form['ip']
        con = sqlite3.connect("ip_database.db")
        cur = con.cursor()
        cur.execute("UPDATE ips SET ip = ? WHERE id = ?", (nueva_ip, id))
        con.commit()
        con.close()
        return redirect(url_for('index'))
    
    con = sqlite3.connect("ip_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ips WHERE id = ?", (id,))
    ip = cur.fetchone()
    con.close()
    return render_template('editar.html', ip=ip)

# Ruta para borrar una IP
@app.route('/borrar/<int:id>', methods=['GET'])
def borrar(id):
    con = sqlite3.connect("ip_database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM ips WHERE id = ?", (id,))
    con.commit()
    con.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    crear_bd()
    app.run(debug=True)
