from abc import abstractmethod
from modelos.estado_tarea import EstadoTarea
from modelos.cancelable import Cancelable


class Tarea(Cancelable): #clase tarea que
    def __init__(self, id_tarea, titulo, descripcion, estado, usuario_asignado): 
        self._id = id_tarea
        self._titulo = titulo
        self._descripcion = descripcion
        self._estado = estado if isinstance(estado, EstadoTarea) else EstadoTarea(estado)
        self._usuario_asignado = usuario_asignado

    @property #getters
    def id(self): return self._id
    
    @property
    def titulo(self): return self._titulo
    
    @property
    def estado(self): return self._estado

    @estado.setter #cambiar el estado de una tarea
    def estado(self, nuevo_estado):
        self._estado = nuevo_estado

    @property
    def usuario_asignado(self): return self._usuario_asignado

    def es_cancelable(self):
        return self._estado != EstadoTarea.COMPLETADA

    def cancelar(self):
        if not self.es_cancelable():
            raise ValueError(f"No se puede cancelar '{self._titulo}'. Ya está COMPLETADA.")
        self._estado = EstadoTarea.CANCELADA

    @abstractmethod
    def to_dict(self):
        pass

    class AltaPrioridad(Tarea):
        def __init__(self, id_tarea, titulo, descripcion, estado, usuario, horas_estimadas, fecha_limite):
            super().__init__(id_tarea, titulo, descripcion, estado, usuario)
            self.horas_estimadas = horas_estimadas
            self.fecha_limite = fecha_limite

    def to_dict(self):
        return {
            "tipo": "AltaPrioridad", "id": self.id, "titulo": self._titulo, "descripcion": self._descripcion,
            "estado": self.estado.value, "usuario_id": self.usuario_asignado.id if self.usuario_asignado else None,
            "horas_estimadas": self.horas_estimadas, "fecha_limite": self.fecha_limite
        }

    class MediaPrioridad(Tarea):
        def __init__(self, id_tarea, titulo, descripcion, estado, usuario, dias_vencimiento, frecuencia):
            super().__init__(id_tarea, titulo, descripcion, estado, usuario)
            self.dias_vencimiento = dias_vencimiento
            self.frecuencia = frecuencia

    def to_dict(self):
        return {
            "tipo": "MediaPrioridad", "id": self.id, "titulo": self._titulo, "descripcion": self._descripcion,
            "estado": self.estado.value, "usuario_id": self.usuario_asignado.id if self.usuario_asignado else None,
            "dias_vencimiento": self.dias_vencimiento, "frecuencia": self.frecuencia
        }