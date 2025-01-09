from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time

from query import query_latest_prometheus_value, get_window_opening_time

app = Flask(__name__)
socketio = SocketIO(app)

temperature = 0
window_time = 0

def update_data():
    global temperature, window_time
    while True:
        temperature = query_latest_prometheus_value("raspberry_pi", "temperature")
        temperature_outside = query_latest_prometheus_value("openweathermap", "temperature")
        window_time = get_window_opening_time(float(temperature), float(temperature_outside))
        socketio.emit('update', {'temperature': temperature, 'window_time': window_time, 'temperature_outside': temperature_outside})
        time.sleep(30)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    threading.Thread(target=update_data, daemon=True).start()
    socketio.run(app, debug=True)
