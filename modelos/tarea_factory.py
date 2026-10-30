from modelos.estado_tarea import EstadoTarea
from modelos.tarea import AltaPrioridad, BajaPrioridad, MediaPrioridad


class TareaFactory:
    @staticmethod
    def normalizar_tipo(tipo):
        clave = str(tipo).strip().lower().replace("prioridad", "")
        if clave in ("alta", "altaprioridad"):
            return "Alta"
        if clave in ("media", "mediaprioridad"):
            return "Media"
        if clave in ("baja", "bajaprioridad"):
            return "Baja"
        raise ValueError("La prioridad debe ser Alta, Media o Baja.")

    @classmethod
    def crear(cls, tipo, id_tarea, titulo, descripcion, estado, usuario, p1, p2):
        tipo_norm = cls.normalizar_tipo(tipo)
        if tipo_norm == "Alta":
            return AltaPrioridad(id_tarea, titulo, descripcion, estado, usuario, p1, p2)
        if tipo_norm == "Media":
            return MediaPrioridad(id_tarea, titulo, descripcion, estado, usuario, p1, p2)
        return BajaPrioridad(id_tarea, titulo, descripcion, estado, usuario, p1, p2)

    @classmethod
    def desde_dict(cls, data, usuario):
        tipo = data.get("tipo")
        if tipo == "AltaPrioridad":
            p1, p2 = data.get("horas_estimadas"), data.get("fecha_limite")
        elif tipo == "MediaPrioridad":
            p1, p2 = data.get("dias_vencimiento"), data.get("frecuencia")
        elif tipo == "BajaPrioridad":
            p1, p2 = data.get("es_postergable"), data.get("condicion")
        else:
            raise ValueError(f"Tipo de tarea desconocido: {tipo}")

        return cls.crear(
            tipo,
            data["id"],
            data["titulo"],
            data.get("descripcion", ""),
            data.get("estado", EstadoTarea.PENDIENTE),
            usuario,
            p1,
            p2,
        )
