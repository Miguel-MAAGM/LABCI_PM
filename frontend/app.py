from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess
ws_process = subprocess.Popen(["python", "usbDATA.py"])
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html", active_page="home")

@app.route("/measure")
def measure():
    return render_template("measure.html", active_page="measure")

@app.route("/settings")
def settings():
    return render_template("settings.html", active_page="settings")


if __name__ == "__main__":
    app.run(debug=False)
