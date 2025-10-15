from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

# Cargar mensajes desde JSON
with open('mensajes.json', 'r', encoding='utf-8') as f:
    mensajes = json.load(f)

def procesar_mensaje(texto):
    texto = texto.lower().strip()
    
    # Detectar intención
    if any(palabra in texto for palabra in ['hola', 'buenas', 'info', 'hello']):
        return mensajes['saludo']
    elif any(palabra in texto for palabra in ['1', 'precio', 'tarifa', 'cuanto', 'cuesta']):
        return mensajes['precios']
    elif any(palabra in texto for palabra in ['2', 'reservar', 'reserva', 'booking', 'quiero reservar']):
        return mensajes['reservar']
    elif any(palabra in texto for palabra in ['3', 'ubicacion', 'direccion', 'mapa', 'donde', 'llegar']):
        return mensajes['ubicacion']
    elif any(palabra in texto for palabra in ['4', 'servicio', 'incluye', 'que hay', 'facilidades']):
        return mensajes['servicios']
    elif any(palabra in texto for palabra in ['5', 'wifi', 'internet', 'contraseña', 'password', 'red']):
        return mensajes['wifi']
    else:
        return mensajes['default']

# Ruta principal - solo para mantener activo
@app.route('/')
def home():
    return "✅ Bot del Hostel Activo - Listo para recibir mensajes"

# Ruta para probar respuestas
@app.route('/probar/<tipo>')
def probar_respuesta(tipo):
    respuesta = procesar_mensaje(tipo)
    return f"<pre>{respuesta}</pre>"

# Ruta para webhook (futuras integraciones)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        mensaje_usuario = data.get('mensaje', '')
        respuesta = procesar_mensaje(mensaje_usuario)
        
        return jsonify({
            'exito': True,
            'respuesta': respuesta
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)