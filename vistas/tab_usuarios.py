from tkinter import ttk, messagebox

from vistas.widgets import arbol_con_scroll, limpiar_arbol


class TabUsuarios(ttk.Frame):
    def __init__(self, parent, gestor_usuarios, al_cambiar):
        super().__init__(parent)
        self.gestor = gestor_usuarios
        self.al_cambiar = al_cambiar
        self._id_edicion = None
        self._construir()
        self.refrescar()

    def _construir(self):
        formulario = ttk.LabelFrame(self, text="Usuario", padding=12)
        formulario.pack(fill="x", padx=12, pady=(12, 8))
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        ttk.Label(formulario, text="ID").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.lbl_id = ttk.Label(formulario, text="Automático")
        self.lbl_id.grid(row=0, column=1, sticky="w", pady=4)

        ttk.Label(formulario, text="Nombre").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        self.ent_nombre = ttk.Entry(formulario)
        self.ent_nombre.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(formulario, text="Email").grid(row=1, column=2, sticky="e", padx=(16, 8), pady=4)
        self.ent_email = ttk.Entry(formulario)
        self.ent_email.grid(row=1, column=3, sticky="ew", pady=4)

        ttk.Label(
            formulario,
            text="El ID se asigna solo. El email debe ser único y con formato nombre@dominio.cl",
            foreground="#555555",
        ).grid(row=2, column=0, columnspan=4, sticky="w", pady=(4, 0))

        acciones = ttk.Frame(formulario)
        acciones.grid(row=3, column=0, columnspan=4, sticky="w", pady=(10, 0))
        ttk.Button(acciones, text="Nuevo", command=self.limpiar_formulario).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Guardar", command=self.guardar).pack(side="left", padx=6)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar).pack(side="left", padx=6)

        tabla, self.tree = arbol_con_scroll(
            self,
            ("ID", "Nombre", "Email", "Tareas"),
            {"ID": 60, "Nombre": 220, "Email": 280, "Tareas": 80},
        )
        tabla.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tree.bind("<<TreeviewSelect>>", self._cargar_seleccion)

    def refrescar(self):
        limpiar_arbol(self.tree)
        for usuario in self.gestor.usuarios:
            cantidad = self.gestor.cantidad_tareas(usuario.id)
            self.tree.insert("", "end", iid=str(usuario.id), values=(usuario.id, usuario.nombre, usuario.email, cantidad))

    def limpiar_formulario(self):
        self._id_edicion = None
        self.lbl_id.config(text="Automático")
        self.ent_nombre.delete(0, "end")
        self.ent_email.delete(0, "end")
        self.tree.selection_remove(self.tree.selection())
        self.ent_nombre.focus_set()

    def guardar(self):
        try:
            nombre = self.ent_nombre.get()
            email = self.ent_email.get()
            if self._id_edicion is None:
                self.gestor.agregar_usuario(nombre, email)
                mensaje = "Usuario registrado."
            else:
                self.gestor.actualizar_usuario(self._id_edicion, nombre, email)
                mensaje = "Usuario actualizado."
            self.refrescar()
            self.limpiar_formulario()
            self.al_cambiar()
            messagebox.showinfo("Éxito", mensaje, parent=self)
        except ValueError as error:
            messagebox.showerror("Validación", str(error), parent=self)

    def eliminar(self):
        if self._id_edicion is None:
            messagebox.showwarning("Usuarios", "Seleccione un usuario en la tabla.", parent=self)
            return
        usuario = self.gestor.obtener(self._id_edicion)
        if not messagebox.askyesno(
            "Eliminar usuario",
            f"¿Eliminar a {usuario.nombre}? Esta acción no se puede deshacer.",
            parent=self,
        ):
            return
        try:
            self.gestor.eliminar_usuario(self._id_edicion)
            self.refrescar()
            self.limpiar_formulario()
            self.al_cambiar()
            messagebox.showinfo("Éxito", "Usuario eliminado.", parent=self)
        except ValueError as error:
            messagebox.showerror("No se pudo eliminar", str(error), parent=self)

    def _cargar_seleccion(self, _event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        id_usuario = int(seleccion[0])
        usuario = self.gestor.obtener(id_usuario)
        self._id_edicion = usuario.id
        self.lbl_id.config(text=str(usuario.id))
        self.ent_nombre.delete(0, "end")
        self.ent_nombre.insert(0, usuario.nombre)
        self.ent_email.delete(0, "end")
        self.ent_email.insert(0, usuario.email)
