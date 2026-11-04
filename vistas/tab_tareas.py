import tkinter as tk
from tkinter import ttk, messagebox

from vistas.widgets import arbol_con_scroll, limpiar_arbol


class TabTareas(ttk.Frame):
    def __init__(self, parent, gestor_tareas):
        super().__init__(parent)
        self.gestor = gestor_tareas
        self._id_edicion = None
        self._construir()
        self.refrescar_usuarios()
        self.refrescar()

    def _construir(self):
        formulario = ttk.LabelFrame(self, text="Tarea", padding=12)
        formulario.pack(fill="x", padx=12, pady=(12, 8))
        for col in (1, 3):
            formulario.columnconfigure(col, weight=1)

        ttk.Label(formulario, text="ID").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.lbl_id = ttk.Label(formulario, text="Automático")
        self.lbl_id.grid(row=0, column=1, sticky="w")

        ttk.Label(formulario, text="Título").grid(row=0, column=2, sticky="e", padx=(16, 8), pady=4)
        self.ent_titulo = ttk.Entry(formulario)
        self.ent_titulo.grid(row=0, column=3, sticky="ew", pady=4)

        ttk.Label(formulario, text="Descripción").grid(row=1, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.txt_descripcion = tk.Text(formulario, height=3, width=40, wrap="word")
        self.txt_descripcion.grid(row=1, column=1, columnspan=3, sticky="ew", pady=4)

        ttk.Label(formulario, text="Asignar a").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.cmb_usuarios = ttk.Combobox(formulario, state="readonly")
        self.cmb_usuarios.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(formulario, text="Prioridad").grid(row=2, column=2, sticky="e", padx=(16, 8), pady=4)
        self.cmb_tipo = ttk.Combobox(formulario, values=["Alta", "Media", "Baja"], state="readonly")
        self.cmb_tipo.grid(row=2, column=3, sticky="ew", pady=4)
        self.cmb_tipo.set("Alta")
        self.cmb_tipo.bind("<<ComboboxSelected>>", self._mostrar_campos_prioridad)

        self.frame_params = ttk.Frame(formulario)
        self.frame_params.grid(row=3, column=0, columnspan=4, sticky="ew", pady=8)
        self.frame_params.columnconfigure(1, weight=1)
        self.frame_params.columnconfigure(3, weight=1)
        self._crear_campos_prioridad()
        self._mostrar_campos_prioridad()

        acciones = ttk.Frame(formulario)
        acciones.grid(row=4, column=0, columnspan=4, sticky="w")
        ttk.Button(acciones, text="Nueva", command=self.limpiar_formulario).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Guardar", command=self.guardar).pack(side="left", padx=6)
        ttk.Button(acciones, text="Completar", command=self.completar).pack(side="left", padx=6)
        ttk.Button(acciones, text="Cancelar", command=self.cancelar).pack(side="left", padx=6)
        ttk.Button(acciones, text="Eliminar", command=self.eliminar).pack(side="left", padx=6)

        filtros = ttk.Frame(self)
        filtros.pack(fill="x", padx=12, pady=(0, 8))
        ttk.Label(filtros, text="Estado").pack(side="left")
        self.cmb_filtro_estado = ttk.Combobox(
            filtros,
            state="readonly",
            values=["TODAS", "PENDIENTE", "COMPLETADA", "CANCELADA"],
            width=16,
        )
        self.cmb_filtro_estado.set("TODAS")
        self.cmb_filtro_estado.pack(side="left", padx=(6, 16))
        self.cmb_filtro_estado.bind("<<ComboboxSelected>>", lambda _e: self.refrescar())

        ttk.Label(filtros, text="Usuario").pack(side="left")
        self.cmb_filtro_usuario = ttk.Combobox(filtros, state="readonly", width=28)
        self.cmb_filtro_usuario.pack(side="left", padx=6)
        self.cmb_filtro_usuario.bind("<<ComboboxSelected>>", lambda _e: self.refrescar())

        tabla, self.tree = arbol_con_scroll(
            self,
            ("ID", "Título", "Descripción", "Prioridad", "Estado", "Asignado a", "Detalle"),
            {
                "ID": 50,
                "Título": 160,
                "Descripción": 180,
                "Prioridad": 80,
                "Estado": 110,
                "Asignado a": 140,
                "Detalle": 200,
            },
        )
        tabla.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.tree.tag_configure("PENDIENTE", background="#FFF6D8")
        self.tree.tag_configure("COMPLETADA", background="#E4F5EA")
        self.tree.tag_configure("CANCELADA", background="#F8E4E4")
        self.tree.bind("<<TreeviewSelect>>", self._cargar_seleccion)

    def _crear_campos_prioridad(self):
        self.lbl_p1 = ttk.Label(self.frame_params, text="Horas estimadas")
        self.ent_p1 = ttk.Entry(self.frame_params)
        self.lbl_p2 = ttk.Label(self.frame_params, text="Fecha límite")
        self.ent_p2 = ttk.Entry(self.frame_params)
        self.cmb_postergable = ttk.Combobox(self.frame_params, values=["Sí", "No"], state="readonly")
        self.cmb_postergable.set("No")
        self.lbl_ayuda = ttk.Label(self.frame_params, foreground="#555555", text="")

        self.lbl_p1.grid(row=0, column=0, sticky="e", padx=(0, 8), pady=2)
        self.ent_p1.grid(row=0, column=1, sticky="ew", pady=2)
        self.lbl_p2.grid(row=0, column=2, sticky="e", padx=(16, 8), pady=2)
        self.ent_p2.grid(row=0, column=3, sticky="ew", pady=2)
        self.lbl_ayuda.grid(row=1, column=0, columnspan=4, sticky="w")

    def _mostrar_campos_prioridad(self, _event=None):
        tipo = self.cmb_tipo.get() or "Alta"
        self.cmb_postergable.grid_remove()
        self.ent_p1.grid()
        if tipo == "Alta":
            self.lbl_p1.config(text="Horas estimadas")
            self.lbl_p2.config(text="Fecha límite")
            self.lbl_ayuda.config(text="Use fecha AAAA-MM-DD. Las horas deben ser un entero mayor que 0.")
        elif tipo == "Media":
            self.lbl_p1.config(text="Días de vencimiento")
            self.lbl_p2.config(text="Frecuencia")
            self.lbl_ayuda.config(text="Ejemplo de frecuencia: semanal, mensual o cada 15 días.")
        else:
            self.lbl_p1.config(text="¿Es postergable?")
            self.lbl_p2.config(text="Condición")
            self.ent_p1.grid_remove()
            self.cmb_postergable.grid(row=0, column=1, sticky="ew", pady=2)
            self.lbl_ayuda.config(text="Elija Sí o No. La condición describe cuándo se puede posponer.")

    def refrescar_usuarios(self):
        valores = [f"{u.id} - {u.nombre}" for u in self.gestor.usuarios]
        actual = self.cmb_usuarios.get()
        self.cmb_usuarios["values"] = valores
        if actual in valores:
            self.cmb_usuarios.set(actual)
        elif valores:
            self.cmb_usuarios.current(0)
        else:
            self.cmb_usuarios.set("")

        filtro = ["Todos"] + valores
        elegido = self.cmb_filtro_usuario.get()
        self.cmb_filtro_usuario["values"] = filtro
        if elegido in filtro:
            self.cmb_filtro_usuario.set(elegido)
        else:
            self.cmb_filtro_usuario.set("Todos")

    def refrescar(self):
        limpiar_arbol(self.tree)
        estado = self.cmb_filtro_estado.get() or "TODAS"
        id_usuario = self._id_desde_combo(self.cmb_filtro_usuario.get()) if self.cmb_filtro_usuario.get() != "Todos" else None
        for tarea in self.gestor.listar(estado=estado, id_usuario=id_usuario):
            asignado = tarea.usuario_asignado.nombre
            descripcion = tarea.descripcion or "—"
            self.tree.insert(
                "",
                "end",
                iid=str(tarea.id),
                values=(
                    tarea.id,
                    tarea.titulo,
                    descripcion,
                    tarea.tipo_prioridad,
                    tarea.estado.value,
                    asignado,
                    tarea.detalle(),
                ),
                tags=(tarea.estado.value,),
            )

    def limpiar_formulario(self):
        self._id_edicion = None
        self.lbl_id.config(text="Automático")
        self.ent_titulo.delete(0, "end")
        self.txt_descripcion.delete("1.0", "end")
        self.ent_p1.delete(0, "end")
        self.ent_p2.delete(0, "end")
        self.cmb_tipo.set("Alta")
        self.cmb_postergable.set("No")
        self._mostrar_campos_prioridad()
        if self.cmb_usuarios["values"]:
            self.cmb_usuarios.current(0)
        self.tree.selection_remove(self.tree.selection())
        self.ent_titulo.focus_set()

    def guardar(self):
        try:
            titulo = self.ent_titulo.get()
            descripcion = self.txt_descripcion.get("1.0", "end").strip()
            tipo = self.cmb_tipo.get()
            id_usuario = self._id_desde_combo(self.cmb_usuarios.get())
            if id_usuario is None:
                raise ValueError("Debe existir al menos un usuario para asignar la tarea.")
            p1, p2 = self._parametros()
            if self._id_edicion is None:
                self.gestor.agregar_tarea(tipo, titulo, descripcion, id_usuario, p1, p2)
                mensaje = "Tarea creada."
            else:
                self.gestor.actualizar_tarea(self._id_edicion, tipo, titulo, descripcion, id_usuario, p1, p2)
                mensaje = "Tarea actualizada."
            self.refrescar()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", mensaje, parent=self)
        except ValueError as error:
            messagebox.showerror("Validación", str(error), parent=self)

    def completar(self):
        id_tarea = self._id_seleccionado("complete")
        if id_tarea is None:
            return
        try:
            self.gestor.completar_tarea(id_tarea)
            self.refrescar()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Tarea completada.", parent=self)
        except ValueError as error:
            messagebox.showerror("Estado no válido", str(error), parent=self)

    def cancelar(self):
        id_tarea = self._id_seleccionado("cancele")
        if id_tarea is None:
            return
        if not messagebox.askyesno("Cancelar tarea", "¿Cancelar la tarea seleccionada?", parent=self):
            return
        try:
            self.gestor.cancelar_tarea(id_tarea)
            self.refrescar()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Tarea cancelada.", parent=self)
        except ValueError as error:
            messagebox.showerror("Estado no válido", str(error), parent=self)

    def eliminar(self):
        id_tarea = self._id_seleccionado("elimine")
        if id_tarea is None:
            return
        if not messagebox.askyesno(
            "Eliminar tarea",
            "¿Eliminar la tarea de forma permanente?",
            parent=self,
        ):
            return
        try:
            self.gestor.eliminar_tarea(id_tarea)
            self.refrescar()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Tarea eliminada.", parent=self)
        except ValueError as error:
            messagebox.showerror("No se pudo eliminar", str(error), parent=self)

    def _parametros(self):
        tipo = self.cmb_tipo.get()
        if tipo == "Baja":
            return self.cmb_postergable.get(), self.ent_p2.get()
        return self.ent_p1.get(), self.ent_p2.get()

    def _id_seleccionado(self, verbo):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Tareas", f"Seleccione una tarea para {verbo}.", parent=self)
            return None
        return int(seleccion[0])

    def _id_desde_combo(self, texto):
        if not texto or texto == "Todos":
            return None
        return int(texto.split(" - ", 1)[0])

    def _cargar_seleccion(self, _event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        tarea = self.gestor.obtener(int(seleccion[0]))
        self._id_edicion = tarea.id
        self.lbl_id.config(text=str(tarea.id))
        self.ent_titulo.delete(0, "end")
        self.ent_titulo.insert(0, tarea.titulo)
        self.txt_descripcion.delete("1.0", "end")
        self.txt_descripcion.insert("1.0", tarea.descripcion)
        self.cmb_tipo.set(tarea.tipo_prioridad)
        self._mostrar_campos_prioridad()
        self.cmb_usuarios.set(f"{tarea.usuario_asignado.id} - {tarea.usuario_asignado.nombre}")
        self.ent_p1.delete(0, "end")
        self.ent_p2.delete(0, "end")
        if tarea.tipo_prioridad == "Alta":
            self.ent_p1.insert(0, str(tarea.horas_estimadas))
            self.ent_p2.insert(0, tarea.fecha_limite)
        elif tarea.tipo_prioridad == "Media":
            self.ent_p1.insert(0, str(tarea.dias_vencimiento))
            self.ent_p2.insert(0, tarea.frecuencia)
        else:
            self.cmb_postergable.set("Sí" if tarea.es_postergable else "No")
            self.ent_p2.insert(0, tarea.condicion)
