from controladores.gestor_tareas import GestorTareasController
from controladores.gestor_usuarios import GestorUsuarios
from persistencia.repositorio import RepositorioJSON
from vistas.app_vista import AppVista


def cargar_datos_prueba(gestor_usuarios, gestor_tareas):
    """Genera registros iniciales si el sistema no tiene usuarios cargados."""
    carlos = gestor_usuarios.agregar_usuario("Carlos Gomez", "carlos@email.com")
    gestor_tareas.agregar_tarea(
        prioridad="Alta",
        titulo="Proyecto de POO",
        descripcion="Entregar código",
        usuario_id=carlos.id,
        estimacion_horas=10,
        fecha_entrega="2026-10-15",
    )


def main():
    repositorio = RepositorioJSON()

    # Carga de datos con captura amplia de errores de archivo o formato JSON
    try:
        usuarios, tareas = repositorio.cargar_datos()
    except (ValueError, FileNotFoundError, KeyError) as error:
        raise SystemExit(f"Error crítico al inicializar la base de datos: {error}") from error

    # Inicialización de controladores
    gestor_usuarios = GestorUsuarios(usuarios, tareas, repositorio)
    gestor_tareas = GestorTareasController(usuarios, tareas, repositorio)

    # Poblar base de datos vacía
    if not usuarios:
        cargar_datos_prueba(gestor_usuarios, gestor_tareas)

    # Lanzamiento de la interfaz gráfica
    app = AppVista(gestor_usuarios, gestor_tareas)
    app.mainloop()


if __name__ == "__main__":
    main()
