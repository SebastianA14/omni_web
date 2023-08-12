from flask import Flask, render_template, request
import logging
import spidev
import math

# Configuración SPI
spi_bus = 0  # Cambiar el número de bus SPI si es necesario
spi_device = 0  # Cambiar el número de dispositivo SPI si es necesario
spi_speed_hz = 1000000  # Cambiar la velocidad del reloj SPI si es necesario

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Cambio realizado aquí

@app.route('/')
def index():
    return render_template('index.html')

# Función para enviar los datos a través de SPI
def enviar_datos_spi(mensaje):
    try:
        spi = spidev.SpiDev()
        spi.open(spi_bus, spi_device)
        spi.max_speed_hz = spi_speed_hz
        
        spi.writebytes(list(mensaje.encode()))
        print("Datos enviados:", mensaje)
    except IOError as e:
        print("Error SPI:", e)
    finally:
        spi.close()

@app.route('/control', methods=['POST'])
def control():
    velRobot = 0.3
    thetaRobot = 0.0000
    omegaRobot = 0

    comando = request.get_json()['direction']
    app.logger.info('Comando recibido: %s', comando)

    if comando == ':move:LF;':
        thetaRobot = math.pi/4
        print("1")
        app.logger.info('Hola')
    if comando == ':move:FORWARD;':
        thetaRobot = 0.0000
        print("2")
    if comando == ':move:RF;':
        thetaRobot = 7*math.pi/4
        print("3")
    if comando == ':move:LEFT;':
        thetaRobot = math.pi/2
        print("4")
    if comando == ':move:STOP;':
        thetaRobot = 0.0000
        velRobot = 0.0
        print("5")
    if comando == ':move:RIGHT;':
        thetaRobot = 3*math.pi/2
        print("6")
    if comando == ':move:LB;':
        thetaRobot = 3*math.pi/4
        print("7")
    if comando == ':move:BACKWARD;':
        thetaRobot = math.pi
        print("8")
    if comando == ':move:RB;':
        thetaRobot = 5*math.pi/4
        print("9")
    if comando == ':ROTATE:CCW;':
        omegaRobot = -1
        print("14")
    if comando == ':ROTATE:CW;':
        omegaRobot = 1
        print("16")

    # Execute the function
    if(thetaRobot == 0 and velRobot == 0): 
        enviar_datos_spi(":00000:0:0;")
    elif(round(thetaRobot*10000) == 7854):
        enviar_datos_spi(":07854:" + str(round(velRobot*10)) + ":0;")
    elif(thetaRobot == 0 and velRobot != 0 and omegaRobot == 0):
        enviar_datos_spi(":00000:" + str(round(velRobot*10)) + ":0;")
    elif(velRobot != 0 and omegaRobot != 0 and omegaRobot == 1):
        enviar_datos_spi(":00000:0:1;")
    elif(velRobot != 0 and omegaRobot != 0 and omegaRobot == -1):
        enviar_datos_spi(":00000:0:2;")
    else:
        enviar_datos_spi((":" + str(round(thetaRobot*10000)) + ":" + str(round(velRobot*10)) + ":0;"))
        
    print("Direction: ", thetaRobot)

    return 'Comando recibido:' + comando

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

