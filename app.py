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
@app.route('/habitacion/<id_hab>', methods=['GET'])
def mostrar_detalle_habitacion(id_hab):
    habitacion_db = db.habitacion.find_one({'id_hab': id_hab})
    return render_template('detalle_habitaciones.html', habitacion=habitacion_db)

#RESERVAS
@app.route('/reservas')
def reservar():
    habitaciones_db = list(db.habitacion.find())
    return render_template('reservas.html', habitaciones=habitaciones_db, datetime=datetime, timedelta=timedelta) 

#LOGIN
@app.route("/login")
def login():
    return render_template('login.html')



#RESERVAS: post
@app.route('/reservas/agregar', methods=['POST'])
def agregar_reserva():
    reservaciones = db.reservas
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], '%Y-%m-%d')
    fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d')
    ciudad = request.form['ciudad']
    correo = request.form['correo']
    fono = request.form['fono']
    habitaciones_db = list(db.habitacion.find())
    habitaciones = []

    id_res = len(list(db.reservas.find()))+1

    if fecha_salida <= fecha_ingreso:
        error_message = "Error: La fecha de salida debe ser posterior a la fecha de ingreso."
        return render_template('reservas.html', error_message=error_message, habitaciones=habitaciones_db)

    if (fecha_salida - fecha_ingreso).days < 1:
        error_message = "Error: La reserva debe ser de al menos un día."
        return render_template('reservas.html', error_message=error_message, habitaciones=habitaciones_db)

    habitacion_cantidad = False
    total=0
    for habitacion in habitaciones_db:
        cantidad = request.form.get(f"cantidad_{habitacion['nombre']}")
        if cantidad and 1 <= int(cantidad) <= 10:
            habitacion_cantidad = True
            total=total+(int(habitacion['precio'])*int(cantidad))
            habitaciones.append({
                "nombre": habitacion['nombre'],
                "valor": int(habitacion['precio']),
                "cantidad": int(cantidad)
            })

    if not habitacion_cantidad:
        error_message = "Error: Debe ingresar al menos una cantidad de habitación válida (entre 1 y 10)."
        return render_template('reservas.html', error_message=error_message, habitaciones=habitaciones_db)

    dias = (fecha_salida - fecha_ingreso).days
    total_reserva=total*dias
    reserva = Reserva(nombre, apellido, fecha_ingreso, fecha_salida, ciudad, habitaciones, "Reservado", total, dias, total_reserva, correo, fono, id_res)
    reservaciones.insert_one(reserva.to_db_collection())
    flash('Reserva realizada con éxito', 'success')
    return redirect(url_for('reservar'))

"""
#RUTAS DE ADMINISTRADOR

#GESTION RESERVA
@app.route('/gestion_reservas')
def gestion_reservas():
    user_info = session.get('user_info')
    if user_info:
        reservas_db=list (db.reservas.find())
        return render_template('/admin/gestion_reservas.html', reservas =reservas_db)
    else:
        return redirect(url_for('login'))
# GESTION CONTACTO
@app.route('/gestion_contacto')
def gestion_contacto():
    user_info = session.get('user_info')
    if user_info:
        mensajes_db = list(db.mensajes.find())
        return render_template('admin/gestion_contacto.html', mensajes=mensajes_db)
    else:
        return redirect(url_for('login'))

#INTERACCION CON BASE DE DATOS

#CONTACTO: POST
@app.route('/mensaje/agregar', methods=['POST'])
def agregar_mensaje():
    mensajes = db.mensajes
    asunto = request.form['asunto']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    mensaje = request.form['mensaje']
    estado = "Recibido"
    mensaje = Mensaje(asunto, nombre, apellido, correo, mensaje, estado)
    mensajes.insert_one(mensaje.to_db_collection())
    return redirect(url_for('home'))



#RESERVAS: CAMBIAR ESTADO -> POST
@app.route('/estado_reserva/<reserva_id>', methods=['POST'])
def cambiar_estado_reserva(reserva_id):
    reservas = db.reservas
    id_obj = ObjectId(reserva_id)
    estado_actual = request.form['estado']

    if estado_actual != "Anulado":
        if estado_actual == "Reservado":
            nuevo_estado = 'Confirmado'
        elif estado_actual == "Confirmado":
            nuevo_estado = 'Realizado'
        elif estado_actual == "Realizado":
            nuevo_estado = 'Anulado'
    
        reservas.update_one({'_id': id_obj}, {'$set': {'estado': nuevo_estado}})
    return redirect(url_for('gestion_reservas'))

#MENSAJES: CAMBIAR ESTADO -> POST
@app.route('/estado_msj/<mensaje_id>', methods=['POST'])
def cambiar_estado_msj(mensaje_id):
    nuevo_estado = 'c'
    mensajes = db.mensajes
    mensaje_id_obj = ObjectId(request.form['_id'])

    mensajes.update_one({'_id': mensaje_id_obj}, {'$set': {'estado': nuevo_estado}})
    return redirect(url_for('gestion_contacto'))

#LOGIN: POST
@app.route('/admin/login', methods=['POST'])
def validar_usuario():
    usuario = request.form['usuario']
    password = request.form['password']
    usuarios = personal_login()
    for us in usuarios:
        if us["user"] == usuario and us["clave"] == password:
            session['user_info'] = {"user": us["user"]}
            return redirect(url_for('gestion_reservas'))
    error_message = 'error: Usuario no registrado'
    return render_template('login.html', error_message=error_message)


#CERRAR SESIÓN
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_info', None)
    return redirect(url_for('login'))
"""
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'mesage': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code=404
    return response

#lanzar la app
if __name__ == "__main__":
    app.run(debug=True)