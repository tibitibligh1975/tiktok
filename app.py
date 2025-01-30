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
    
    body_data = request.get_data().decode('utf-8')
    data = parse_qs(body_data)
    
    gift_name = data.get('giftName', [''])[0]
    coins = int(data.get('coins', [1])[0])
    
    # Verifica qual presente foi enviado
    if gift_name == 'Coração':  # Ajuste o nome conforme aparecer no webhook
        pontos = coins * 10  # Coração vale 10
    else:
        pontos = coins  # Rosa vale 1
    
    time_a += pontos
    
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': pontos,
        'animacoes_b': 0
    })
    
    return {'status': 'success'}, 200

@app.route('/webhook/timeB', methods=['POST'])
def webhook_time_b():
    global time_b
    
    body_data = request.get_data().decode('utf-8')
    data = parse_qs(body_data)
    
    gift_name = data.get('giftName', [''])[0]
    coins = int(data.get('coins', [1])[0])
    
    # Verifica qual presente foi enviado
    if gift_name == 'Dino':  # Ajuste o nome conforme aparecer no webhook
        pontos = coins * 10  # Dino vale 10
    else:
        pontos = coins  # Flor vale 1
    
    time_b += pontos
    
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': 0,
        'animacoes_b': pontos
    })
    
    return {'status': 'success'}, 200

@app.route('/comando/timeA', methods=['POST'])
def comando_time_a():
    global time_a
    
    # Simplesmente adiciona 1 ponto
    time_a += 1
    
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': 1,
        'animacoes_b': 0
    })
    
    return {'status': 'success'}, 200

@app.route('/comando/timeB', methods=['POST'])
def comando_time_b():
    global time_b
    
    # Simplesmente adiciona 1 ponto
    time_b += 1
    
    socketio.emit('atualizar_pontos', {
        'time_a': time_a, 
        'time_b': time_b,
        'animacoes_a': 0,
        'animacoes_b': 1
    })
    
    return {'status': 'success'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 