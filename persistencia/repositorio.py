import json
from pathlib import Path

from modelos import TareaFactory, Usuario


class RepositorioJSON:
    def __init__(self, directorio_base=None):
        raiz = Path(directorio_base) if directorio_base else Path(__file__).resolve().parent.parent
        self.archivo_usuarios = raiz / "usuarios.json"
        self.archivo_tareas = raiz / "tareas.json"

    def guardar_datos(self, usuarios, tareas):
        self._escribir(self.archivo_usuarios, [u.to_dict() for u in usuarios])
        self._escribir(self.archivo_tareas, [t.to_dict() for t in tareas])

    def cargar_datos(self):
        usuarios = []
        for data in self._leer(self.archivo_usuarios):
            usuarios.append(Usuario.from_dict(data))

        por_id = {u.id: u for u in usuarios}
        tareas = []
        for data in self._leer(self.archivo_tareas):
            usuario = por_id.get(data.get("usuario_id"))
            if usuario is None:
                raise ValueError(
                    f"La tarea {data.get('id')} referencia un usuario inexistente ({data.get('usuario_id')})."
                )
            tareas.append(TareaFactory.desde_dict(data, usuario))
        return usuarios, tareas

    def _leer(self, ruta):
        if not ruta.exists():
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = archivo.read().strip()
                if not contenido:
                    return []
                datos = json.loads(contenido)
        except json.JSONDecodeError as error:
            raise ValueError(f"No se pudo leer {ruta.name}: JSON inválido ({error.msg}).") from error
        if not isinstance(datos, list):
            raise ValueError(f"{ruta.name} debe contener una lista.")
        return datos

    def _escribir(self, ruta, datos):
        temporal = ruta.with_suffix(ruta.suffix + ".tmp")
        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        temporal.replace(ruta)
