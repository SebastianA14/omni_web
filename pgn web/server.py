from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/control', methods=['POST'])
def control():
    comando = request.form['comando']
    # Aquí debes implementar la lógica para controlar el carrito según el comando recibido
    return 'Comando recibido: ' + comando
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
