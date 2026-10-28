class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self._id = id_usuario
        self._nombre = nombre
        self._email = email

    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def email(self): return self._email

    def to_dict(self):
        return {"id": self._id, "nombre": self._nombre, "email": self._email}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["nombre"], data["email"])

    