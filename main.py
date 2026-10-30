from controladores.gestor_tareas import GestorTareasController
from controladores.gestor_usuarios import GestorUsuarios
from persistencia.repositorio import RepositorioJSON
from vistas.app_vista import AppVista


if __name__ == "__main__":
    repositorio = RepositorioJSON()
    try:
        usuarios, tareas = repositorio.cargar_datos()
    except ValueError as error:
        raise SystemExit(f"No se pudieron cargar los datos: {error}") from error

    gestor_usuarios = GestorUsuarios(usuarios, tareas, repositorio)
    gestor_tareas = GestorTareasController(usuarios, tareas, repositorio)

    if not usuarios:
        carlos = gestor_usuarios.agregar_usuario("Carlos Gomez", "carlos@email.com")
        gestor_tareas.agregar_tarea(
            "Alta",
            "Proyecto de POO",
            "Entregar código",
            carlos.id,
            10,
            "2026-10-15",
        )

    app = AppVista(gestor_usuarios, gestor_tareas)
    app.mainloop()
