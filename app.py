from flask import Flask, request, render_template
from flask_socketio import SocketIO
import matplotlib.pyplot as plt
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Contadores separados para cada time
time_a = 0
time_b = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook/timeA', methods=['POST'])
def webhook_time_a():
    global time_a
    time_a += 1
    socketio.emit('novo_comentario')
    return {'status': 'success'}, 200

@app.route('/webhook/timeB', methods=['POST'])
def webhook_time_b():
    global time_b
    time_b += 1
    socketio.emit('novo_comentario')
    return {'status': 'success'}, 200

@app.route('/grafico')
def gerar_grafico():
    plt.clf()
    plt.figure(figsize=(10, 6))
    
    # Criar barras lado a lado
    times = ['Time A', 'Time B']
    valores = [time_a, time_b]
    
    plt.bar(times, valores)
    plt.title('Placar')
    plt.ylabel('Pontos')
    
    # Adicionar os valores em cima das barras
    for i, v in enumerate(valores):
        plt.text(i, v, str(v), ha='center')

    # Converte o gráfico para base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return plot_url

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 