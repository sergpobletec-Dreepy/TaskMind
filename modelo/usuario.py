class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self._id = id_usuario
        self._nombre = nombre
        self._email = email

    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre