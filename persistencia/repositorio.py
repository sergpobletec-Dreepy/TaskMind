import json
import os
from modelos import Usuario, Tarea, AltaPrioridad, MediaPrioridad, BajaPrioridad, EstadoTarea

class RepositorioJSON:
    FILE_USUARIOS = "usuarios.json"
    FILE_TAREAS = "tareas.json"