class Mensaje:
    def __init__(self, asunto, nombre, apellido, correo, mensaje, estado):
        self.asunto = asunto
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.mensaje = mensaje
        self.estado = estado
    
    def to_db_collection(self):
        return {
            'asunto': self.asunto,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'mensaje': self.mensaje,
            'estado': self.estado
        }