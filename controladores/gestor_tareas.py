from modelos import EstadoTarea, TareaFactory
from modelos.validaciones import siguiente_id


class GestorTareasController:
    """Controlador encargado de gestionar el ciclo de vida, persistencia 
    y reglas de negocio de las tareas.
    """

    def __init__(self, usuarios: list, tareas: list, repositorio):
        self.usuarios = usuarios
        self.tareas = tareas
        self._repositorio = repositorio

    def agregar_tarea(self, tipo: str, titulo: str, descripcion: str, id_usuario: int, p1=None, p2=None, **kwargs):
        """Crea una nueva tarea a través de la fábrica, la añade a la lista y la guarda."""
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
            **kwargs,
        )
        self.tareas.append(tarea)
        self._guardar()
        return tarea

    def actualizar_tarea(self, id_tarea: int, tipo: str, titulo: str, descripcion: str, id_usuario: int, p1=None, p2=None, **kwargs):
        """Actualiza una tarea existente. Solo se permiten modificaciones en estado PENDIENTE."""
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
            **kwargs,
        )
        indice = self.tareas.index(tarea)
        self.tareas[indice] = reemplazo
        self._guardar()
        return reemplazo

    def eliminar_tarea(self, id_tarea: int):
        """Remueve una tarea del sistema y guarda los cambios."""
        tarea = self.obtener(id_tarea)
        self.tareas.remove(tarea)
        self._guardar()

    def cancelar_tarea(self, id_tarea: int):
        """Marca una tarea como CANCELADA y actualiza la persistencia."""
        tarea = self.obtener(id_tarea)
        tarea.cancelar()
        self._guardar()

    def completar_tarea(self, id_tarea: int):
        """Marca una tarea como COMPLETADA y actualiza la persistencia."""
        tarea = self.obtener(id_tarea)
        tarea.completar()
        self._guardar()

    def obtener(self, id_tarea: int):
        """Busca una tarea por ID. Lanza ValueError si no existe."""
        tarea = next((t for t in self.tareas if t.id == id_tarea), None)
        if not tarea:
            raise ValueError(f"Tarea con ID {id_tarea} no encontrada.")
        return tarea

    def listar(self, estado: str = None, id_usuario: int = None):
        """Filtra la lista de tareas por estado (PENDIENTE, COMPLETADA, CANCELADA) y/o por usuario."""
        resultado = list(self.tareas)
        if estado and estado != "TODAS":
            resultado = [
                t for t in resultado 
                if (hasattr(t.estado, "value") and t.estado.value == estado) or t.estado == estado
            ]
        if id_usuario is not None:
            resultado = [
                t for t in resultado 
                if t.usuario_asignado and getattr(t.usuario_asignado, "id", None) == id_usuario
            ]
        return resultado

    def _obtener_usuario(self, id_usuario: int):
        """Busca un usuario por ID o lanza una excepción si no existe."""
        usuario = next((u for u in self.usuarios if u.id == id_usuario), None)
        if not usuario:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado.")
        return usuario

    def _guardar(self):
        """Sincroniza el estado actual en el repositorio JSON."""
        self._repositorio.guardar_datos(self.usuarios, self.tareas)
