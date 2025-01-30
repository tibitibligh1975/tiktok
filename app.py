from flask import Flask, request, render_template
from flask_socketio import SocketIO
import os
from urllib.parse import parse_qs

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
    
    # Processa os dados do form
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        data = request.get_json()
    
    # Calcula pontos baseado em coins e repeatCount
    coins = int(data.get('coins', 1))
    repeat_count = int(data.get('repeatCount', 1))
    total_points = coins * repeat_count
    
    time_a += total_points
    
    # Envia o número total de pontos e quantas animações fazer
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': total_points,
        'animacoes_b': 0
    })
    
    return {'status': 'success'}, 200

@app.route('/webhook/timeB', methods=['POST'])
def webhook_time_b():
    global time_b
    
    # Processa os dados do form
    if request.content_type == 'application/x-www-form-urlencoded':
        data = request.form
    else:
        data = request.get_json()
    
    # Calcula pontos baseado em coins e repeatCount
    coins = int(data.get('coins', 1))
    repeat_count = int(data.get('repeatCount', 1))
    total_points = coins * repeat_count
    
    time_b += total_points
    
    # Envia o número total de pontos e quantas animações fazer
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': 0,
        'animacoes_b': total_points
    })
    
    return {'status': 'success'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 