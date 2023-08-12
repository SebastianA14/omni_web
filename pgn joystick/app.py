from flask import Flask, render_template, request
import logging



app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Cambio realizado aquí

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/control', methods=['POST'])
def control():
    velRobot = 0.3
    thetaRobot = 0.0
    omegaRobot = 0

    comando = request.get_json()['direction']
    app.logger.info('Comando recibido: %s', comando)

    if comando.startswith(':move:'):
        _, _, theta, vel, _ = comando.split(':')
        thetaRobot = float(theta)
        velRobot = float(vel) / 10.0

    if comando.startswith(':ROTATE:'):
        _, _, direction, _ = comando.split(':')
        if direction == 'CCW':
            omegaRobot = -1
        elif direction == 'CW':
            omegaRobot = 1

    # Execute the function
    if thetaRobot == 0 and velRobot == 0:
        print(":00000:0:0;")
    elif round(thetaRobot * 10000) == 7854:
        print(":07854:" + str(round(velRobot * 10)) + ":0;")
    elif thetaRobot == 0 and velRobot != 0 and omegaRobot == 0:
        print(":00000:" + str(round(velRobot * 10)) + ":0;")
    elif velRobot != 0 and omegaRobot != 0 and omegaRobot == 1:
        print(":00000:0:1;")
    elif velRobot != 0 and omegaRobot != 0 and omegaRobot == -1:
        print(":00000:0:2;")
    else:
        print(":" + str(round(thetaRobot * 10000)) + ":" + str(round(velRobot * 10)) + ":0;")

    # Mostrar los valores por terminal
    print("Theta:", thetaRobot)
    print("Velocidad:", velRobot)
    print("Velocidad Angular:", omegaRobot)

    return 'Comando recibido: ' + comando

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
