from flask import Flask, render_template, redirect, url_for, jsonify, session, request, flash

app = Flask(__name__)
app.secret_key ="dfghjkl"
import database as dbase
from models.reserva import Reserva
from models.mensaje import Mensaje
db = dbase.dbConnection()

from bson import ObjectId

from datetime import datetime, timedelta 

#Datos para hoja NOSOTROS
from data.data_general import personal_data
#Datos para validar usuario
from data.data_general import personal_login

#RUTAS USUARIOS NO REGISTRADOS
@app.route("/")
def home():
    return render_template("index.html")

#NOSOTROS
@app.route('/nosotros')
def nosotros():
    data_array = personal_data()
    return render_template('nosotros.html', data_array=data_array)

#CONTACTO
@app.route("/contacto")
def contacto():
    return render_template('contacto.html')


#HABITACIONES
@app.route('/habitaciones')
def ver_habitaciones():
    habitaciones_db = list(db.habitacion.find())
    return render_template('habitaciones.html', habitaciones=habitaciones_db)

#HABITACIONES POR ID
@app.route('/habitacion/<habitacion_id>', methods=['GET'])
def mostrar_detalle_habitacion(habitacion_id):
    habitacion_db = db.habitacion.find_one({'_id': ObjectId(habitacion_id)})
    return render_template('detalle_habitaciones.html', habitacion=habitacion_db)


@app.errorhandler(404)
def notFound(error=None):
    message = {
        'mesage': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code=404
    return response

@app.errorhandler(Exception)
def handle_error(error):
    message = {
        'message': 'Ocurrió un error inesperado en la aplicación.',
        'error': str(error)
    }
    return render_template('error.html', error=message), 500


#lanzar la app
if __name__ == "__main__":
    app.run(debug=True)