from abc import abstractmethod
from modelos.estado_tarea import EstadoTarea
from modelos.cancelable import Cancelable


class Tarea(Cancelable):
    def __init__(self, id_tarea, titulo, descripcion, estado, usuario_asignado):
        self._id = id_tarea
        self._titulo = titulo
        self._descripcion = descripcion
        self._estado = estado if isinstance(estado, EstadoTarea) else EstadoTarea(estado)
        self._usuario_asignado = usuario_asignado

    