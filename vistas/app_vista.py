import tkinter as tk
from tkinter import ttk

from vistas.tab_tareas import TabTareas
from vistas.tab_usuarios import TabUsuarios


class AppVista(tk.Tk):
    def __init__(self, gestor_usuarios, gestor_tareas):
        super().__init__()
        self.gestor_usuarios = gestor_usuarios
        self.gestor_tareas = gestor_tareas
        self.title("TaskMind — Gestor de tareas")
        self.geometry("1100x720")
        self.minsize(960, 640)
        self._aplicar_estilo()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_tareas = TabTareas(self.notebook, gestor_tareas)
        self.tab_usuarios = TabUsuarios(self.notebook, gestor_usuarios, al_cambiar=self._al_cambiar_usuarios)

        self.notebook.add(self.tab_tareas, text="Tareas")
        self.notebook.add(self.tab_usuarios, text="Usuarios")

    def _al_cambiar_usuarios(self):
        self.tab_tareas.refrescar_usuarios()
        self.tab_tareas.refrescar()

    def _aplicar_estilo(self):
        estilo = ttk.Style(self)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("TNotebook.Tab", padding=(16, 8))
        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        estilo.configure("TButton", padding=(10, 4))
