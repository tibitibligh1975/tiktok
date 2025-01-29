from flask import Flask, request, render_template
from flask_socketio import SocketIO
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Contador global de comentários
comentarios = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe o webhook do TikTok
    data = request.json
    
    # Adiciona timestamp do comentário
    comentarios.append(datetime.now())
    
    # Emite evento para atualizar o gráfico
    socketio.emit('novo_comentario')
    
    return {'status': 'success'}, 200

@app.route('/grafico')
def gerar_grafico():
    # Limpa o gráfico anterior
    plt.clf()
    
    # Cria o gráfico
    plt.figure(figsize=(10, 6))
    plt.hist([c.timestamp() for c in comentarios], bins=20)
    plt.title('Comentários ao Longo do Tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Quantidade de Comentários')
    
    # Converte o gráfico para base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return plot_url

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 