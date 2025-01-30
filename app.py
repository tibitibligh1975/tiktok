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
    
    # Lê os dados do body
    body_data = request.get_data().decode('utf-8')
    # Converte os dados do form para um dicionário
    data = parse_qs(body_data)
    
    # Pega o primeiro valor da lista retornada pelo parse_qs
    coins = int(data.get('coins', [1])[0])
    time_a += coins
    
    # Envia o número de coins para determinar quantas animações fazer
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': coins,
        'animacoes_b': 0
    })
    
    return {'status': 'success'}, 200

@app.route('/webhook/timeB', methods=['POST'])
def webhook_time_b():
    global time_b
    
    # Lê os dados do body
    body_data = request.get_data().decode('utf-8')
    # Converte os dados do form para um dicionário
    data = parse_qs(body_data)
    
    # Pega o primeiro valor da lista retornada pelo parse_qs
    coins = int(data.get('coins', [1])[0])
    time_b += coins
    
    # Envia o número de coins para determinar quantas animações fazer
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': 0,
        'animacoes_b': coins
    })
    
    return {'status': 'success'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 