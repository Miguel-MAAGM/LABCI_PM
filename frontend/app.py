from flask import Flask, render_template

app = Flask(__name__)
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No se envía nada realmente, solo se resuelve la IP local
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Configura tu IP y puerto aquí

WS_IP = get_local_ip()
WS_PORT = 8765

@app.route("/")
def index():
    print(f"Conectando a WebSocket en ws://{WS_IP}:{WS_PORT}")
    return render_template("index.html", ws_ip=WS_IP, ws_port=WS_PORT)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
