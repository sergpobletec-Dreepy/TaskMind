from modelos import EstadoTarea, TareaFactory
from modelos.validaciones import siguiente_id


class GestorTareasController:
    def __init__(self, usuarios, tareas, repositorio):
        self.usuarios = usuarios
        self.tareas = tareas
        self._repositorio = repositorio

    def agregar_tarea(self, tipo, titulo, descripcion, id_usuario, p1, p2):
        usuario = self._obtener_usuario(id_usuario)
        tarea = TareaFactory.crear(
            tipo,
            siguiente_id(self.tareas),
            titulo,
            descripcion,
            EstadoTarea.PENDIENTE,
            usuario,
            p1,
            p2,
        )
        self.tareas.append(tarea)
        self._guardar()
        return tarea

    def actualizar_tarea(self, id_tarea, tipo, titulo, descripcion, id_usuario, p1, p2):
        tarea = self.obtener(id_tarea)
        if not tarea.es_pendiente():
            raise ValueError("Solo se pueden editar tareas en estado PENDIENTE.")
        usuario = self._obtener_usuario(id_usuario)
        reemplazo = TareaFactory.crear(
            tipo,
            tarea.id,
            titulo,
            descripcion,
            tarea.estado,
            usuario,
            p1,
            p2,
        )
        indice = self.tareas.index(tarea)
        self.tareas[indice] = reemplazo
        self._guardar()
        return reemplazo

    def eliminar_tarea(self, id_tarea):
        tarea = self.obtener(id_tarea)
        self.tareas.remove(tarea)
        self._guardar()

    def cancelar_tarea(self, id_tarea):
        tarea = self.obtener(id_tarea)
        tarea.cancelar()
        self._guardar()

    def completar_tarea(self, id_tarea):
        tarea = self.obtener(id_tarea)
        tarea.completar()
        self._guardar()

    def obtener(self, id_tarea):
        tarea = next((t for t in self.tareas if t.id == id_tarea), None)
        if not tarea:
            raise ValueError("Tarea no encontrada.")
        return tarea

    def listar(self, estado=None, id_usuario=None):
        resultado = list(self.tareas)
        if estado and estado != "TODAS":
            resultado = [t for t in resultado if t.estado.value == estado]
        if id_usuario is not None:
            resultado = [t for t in resultado if t.usuario_asignado.id == id_usuario]
        return resultado

    def _obtener_usuario(self, id_usuario):
        usuario = next((u for u in self.usuarios if u.id == id_usuario), None)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return usuario

    def _guardar(self):
        self._repositorio.guardar_datos(self.usuarios, self.tareas)
