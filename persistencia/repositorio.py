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