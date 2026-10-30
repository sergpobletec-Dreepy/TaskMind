from modelos.validaciones import texto_obligatorio, validar_email


class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self._id = id_usuario
        self._nombre = texto_obligatorio(nombre, "Nombre")
        self._email = validar_email(email)

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = texto_obligatorio(valor, "Nombre")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = validar_email(valor)

    def actualizar(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def to_dict(self):
        return {"id": self._id, "nombre": self._nombre, "email": self._email}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["nombre"], data["email"])
