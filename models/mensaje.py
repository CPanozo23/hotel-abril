class Mensaje:
    def __init__(self, asunto, nombre, apellido, correo, mensaje, estado, id_men):
        self.asunto = asunto
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.mensaje = mensaje
        self.estado = estado
        self.id_men = id_men
    
    def to_db_collection(self):
        return {
            'asunto': self.asunto,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'mensaje': self.mensaje,
            'estado': self.estado,
            'id_men': self.id_men
        }