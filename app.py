from flask import Flask, request, render_template
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Contadores separados para cada time
time_a = 0
time_b = 0

@app.route('/')
def home():
    return render_template('index.html', time_a=time_a, time_b=time_b)

@app.route('/webhook/timeA', methods=['POST'])
def webhook_time_a():
    global time_a
    time_a += 1
    socketio.emit('atualizar_pontos', {'time_a': time_a, 'time_b': time_b})
    return {'status': 'success'}, 200

@app.route('/webhook/timeB', methods=['POST'])
def webhook_time_b():
    global time_b
    time_b += 1
    socketio.emit('atualizar_pontos', {'time_a': time_a, 'time_b': time_b})
    return {'status': 'success'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 