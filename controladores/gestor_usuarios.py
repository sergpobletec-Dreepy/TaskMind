from modelos import Usuario
from modelos.validaciones import siguiente_id, validar_email


class GestorUsuarios:
    def __init__(self, usuarios, tareas, repositorio):
        self.usuarios = usuarios
        self.tareas = tareas
        self._repositorio = repositorio

    def agregar_usuario(self, nombre, email):
        self._validar_email_unico(email)
        usuario = Usuario(siguiente_id(self.usuarios), nombre, email)
        self.usuarios.append(usuario)
        self._guardar()
        return usuario

    def actualizar_usuario(self, id_usuario, nombre, email):
        usuario = self.obtener(id_usuario)
        self._validar_email_unico(email, excluir_id=id_usuario)
        usuario.actualizar(nombre, email)
        self._guardar()
        return usuario

    def eliminar_usuario(self, id_usuario):
        usuario = self.obtener(id_usuario)
        asignadas = [t for t in self.tareas if t.usuario_asignado.id == id_usuario]
        if asignadas:
            raise ValueError(
                f"No se puede eliminar a {usuario.nombre}: tiene {len(asignadas)} tarea(s) asignada(s)."
            )
        self.usuarios.remove(usuario)
        self._guardar()

    def obtener(self, id_usuario):
        usuario = next((u for u in self.usuarios if u.id == id_usuario), None)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return usuario

    def cantidad_tareas(self, id_usuario):
        return sum(1 for t in self.tareas if t.usuario_asignado.id == id_usuario)

    def _validar_email_unico(self, email, excluir_id=None):
        normalizado = validar_email(email)
        if any(u.email == normalizado and u.id != excluir_id for u in self.usuarios):
            raise ValueError("Ya existe un usuario con ese email.")

    def _guardar(self):
        self._repositorio.guardar_datos(self.usuarios, self.tareas)
