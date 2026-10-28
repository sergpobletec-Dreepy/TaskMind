import json
import os
from modelos import Usuario, Tarea, AltaPrioridad, MediaPrioridad, BajaPrioridad, EstadoTarea

class RepositorioJSON:
    FILE_USUARIOS = "usuarios.json"
    FILE_TAREAS = "tareas.json"

    @classmethod
    def guardar_datos(cls, usuarios, tareas):
        with open(cls.FILE_USUARIOS, "w") as f:
            json.dump([u.to_dict() for u in usuarios], f, indent=4)
        
        with open(cls.FILE_TAREAS, "w") as f:
            json.dump([t.to_dict() for t in tareas], f, indent=4)

    @classmethod
    def cargar_datos(cls):
        usuarios = []
        tareas = []
        if os.path.exists(cls.FILE_USUARIOS):
            with open(cls.FILE_USUARIOS, "r") as f:
                usuarios = [Usuario.from_dict(d) for d in json.load(f)]
                
        dic_usuarios = {u.id: u for u in usuarios}

        if os.path.exists(cls.FILE_TAREAS):
            with open(cls.FILE_TAREAS, "r") as f:
                for d in json.load(f):
                    u = dic_usuarios.get(d["usuario_id"])
                    if d["tipo"] == "AltaPrioridad":
                        tareas.append(AltaPrioridad(d["id"], d["titulo"], d["descripcion"], d["estado"], u, d["horas_estimadas"], d["fecha_limite"]))
                    elif d["tipo"] == "MediaPrioridad":
                        tareas.append(MediaPrioridad(d["id"], d["titulo"], d["descripcion"], d["estado"], u, d["dias_vencimiento"], d["frecuencia"]))
                    elif d["tipo"] == "BajaPrioridad":
                        tareas.append(BajaPrioridad(d["id"], d["titulo"], d["descripcion"], d["estado"], u, d["es_postergable"], d["condicion"]))
        return usuarios, tareas