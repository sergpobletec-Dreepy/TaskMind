from abc import ABC, abstractmethod

from modelos.cancelable import Cancelable
from modelos.estado_tarea import EstadoTarea
from modelos.validaciones import (
    entero_positivo,
    parsear_bool,
    parsear_fecha,
    texto_obligatorio,
    texto_opcional,
)


class Tarea(Cancelable, ABC):
    def __init__(self, id_tarea, titulo, descripcion, estado, usuario_asignado):
        if usuario_asignado is None:
            raise ValueError("La tarea debe tener un usuario asignado.")
        self._id = id_tarea
        self._titulo = texto_obligatorio(titulo, "Título")
        self._descripcion = texto_opcional(descripcion, "Descripción")
        self._estado = estado if isinstance(estado, EstadoTarea) else EstadoTarea(estado)
        self._usuario_asignado = usuario_asignado

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._titulo = texto_obligatorio(valor, "Título")

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = texto_opcional(valor, "Descripción")

    @property
    def estado(self):
        return self._estado

    @property
    def usuario_asignado(self):
        return self._usuario_asignado

    @usuario_asignado.setter
    def usuario_asignado(self, usuario):
        if usuario is None:
            raise ValueError("La tarea debe tener un usuario asignado.")
        self._usuario_asignado = usuario

    @property
    @abstractmethod
    def tipo_prioridad(self):
        pass

    def es_pendiente(self):
        return self._estado == EstadoTarea.PENDIENTE

    def es_cancelable(self):
        return self._estado == EstadoTarea.PENDIENTE

    def cancelar(self):
        if self._estado == EstadoTarea.COMPLETADA:
            raise ValueError(f"No se puede cancelar '{self._titulo}'. Ya está completada.")
        if self._estado == EstadoTarea.CANCELADA:
            raise ValueError(f"'{self._titulo}' ya está cancelada.")
        self._estado = EstadoTarea.CANCELADA

    def completar(self):
        if self._estado == EstadoTarea.CANCELADA:
            raise ValueError(f"No se puede completar '{self._titulo}'. Está cancelada.")
        if self._estado == EstadoTarea.COMPLETADA:
            raise ValueError(f"'{self._titulo}' ya está completada.")
        self._estado = EstadoTarea.COMPLETADA

    def _datos_base(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado.value,
            "usuario_id": self.usuario_asignado.id,
        }

    @abstractmethod
    def detalle(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


class AltaPrioridad(Tarea):
    def __init__(self, id_tarea, titulo, descripcion, estado, usuario, horas_estimadas, fecha_limite):
        super().__init__(id_tarea, titulo, descripcion, estado, usuario)
        self._horas_estimadas = entero_positivo(horas_estimadas, "Horas estimadas")
        self._fecha_limite = parsear_fecha(fecha_limite, "Fecha límite")

    @property
    def tipo_prioridad(self):
        return "Alta"

    @property
    def horas_estimadas(self):
        return self._horas_estimadas

    @property
    def fecha_limite(self):
        return self._fecha_limite

    def detalle(self):
        return f"{self._horas_estimadas} h · límite {self._fecha_limite}"

    def to_dict(self):
        datos = self._datos_base()
        datos.update({
            "tipo": "AltaPrioridad",
            "horas_estimadas": self._horas_estimadas,
            "fecha_limite": self._fecha_limite,
        })
        return datos


class MediaPrioridad(Tarea):
    def __init__(self, id_tarea, titulo, descripcion, estado, usuario, dias_vencimiento, frecuencia):
        super().__init__(id_tarea, titulo, descripcion, estado, usuario)
        self._dias_vencimiento = entero_positivo(dias_vencimiento, "Días de vencimiento")
        self._frecuencia = texto_obligatorio(frecuencia, "Frecuencia", minimo=2, maximo=40)

    @property
    def tipo_prioridad(self):
        return "Media"

    @property
    def dias_vencimiento(self):
        return self._dias_vencimiento

    @property
    def frecuencia(self):
        return self._frecuencia

    def detalle(self):
        return f"{self._dias_vencimiento} días · {self._frecuencia}"

    def to_dict(self):
        datos = self._datos_base()
        datos.update({
            "tipo": "MediaPrioridad",
            "dias_vencimiento": self._dias_vencimiento,
            "frecuencia": self._frecuencia,
        })
        return datos


class BajaPrioridad(Tarea):
    def __init__(self, id_tarea, titulo, descripcion, estado, usuario, es_postergable, condicion):
        super().__init__(id_tarea, titulo, descripcion, estado, usuario)
        self._es_postergable = parsear_bool(es_postergable, "Postergable")
        self._condicion = texto_obligatorio(condicion, "Condición", minimo=2, maximo=80)

    @property
    def tipo_prioridad(self):
        return "Baja"

    @property
    def es_postergable(self):
        return self._es_postergable

    @property
    def condicion(self):
        return self._condicion

    def detalle(self):
        postergable = "Sí" if self._es_postergable else "No"
        return f"Postergable: {postergable} · {self._condicion}"

    def to_dict(self):
        datos = self._datos_base()
        datos.update({
            "tipo": "BajaPrioridad",
            "es_postergable": self._es_postergable,
            "condicion": self._condicion,
        })
        return datos
