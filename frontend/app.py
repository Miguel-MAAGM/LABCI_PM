from flask import Flask, render_template
import logging
import os

logging.basicConfig(level=logging.INFO)
logging.disable(logging.DEBUG)
app = Flask(__name__)

@app.route("/")
def index():
    # Acá puedes mostrar datos o configuraciones
    return "<h1>Bienvenido a la configuración de Orange Pi</h1><p>Red no detectada, estás en modo AP.</p>"

@app.route("/config")
def config():
    # Acá podrías mostrar formularios para cambiar Wi-Fi o ver estado
    return "<h2>Configuración Wi-Fi</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
