class Reserva:
    def __init__(self, nombre, apellido, fecha_ingreso, fecha_salida, ciudad, habitaciones, estado, total, dias, total_reserva, correo, fono):
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.ciudad = ciudad
        self.habitaciones = habitaciones
        self.estado = estado
        self.total = total
        self.dias = dias
        self.total_reserva = total_reserva
        self.correo = correo
        self.fono = fono

    def to_db_collection(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_ingreso': self.fecha_ingreso,
            'fecha_salida': self.fecha_salida,
            'ciudad': self.ciudad,
            'habitaciones': self.habitaciones,
            'estado': self.estado,
            'total': self.total,
            'dias': self.dias,
            'total_reserva': self.total_reserva,
            'correo': self.correo,
            'fono': self.fono
        }
    
