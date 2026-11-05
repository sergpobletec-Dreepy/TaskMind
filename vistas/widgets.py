from tkinter import ttk


def arbol_con_scroll(parent, columnas, anchos):
    contenedor = ttk.Frame(parent) #caja vacia
    arbol = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse") #tabla de tareas y usuarios
    scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=arbol.yview) #barra de desplazamiento vertical
    scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=arbol.xview) #barra de desplazamiento horizontal
    arbol.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set) #union de las barras de desplazamiento con la tabla

    for col in columnas: #toma los titulos y los pone en la tabla
        arbol.heading(col, text=col)
        arbol.column(col, width=anchos.get(col, 120), minwidth=60, stretch=True)

    arbol.grid(row=0, column=0, sticky="nsew") #pone la tabla  en la parte superior izquierda
    scroll_y.grid(row=0, column=1, sticky="ns") #pone la barra de desplzamiento vertical a la derecha de la tabla
    scroll_x.grid(row=1, column=0, sticky="ew") #pone la barra de desplazamiento horizontal debajo  de la tabla
    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)
    return contenedor, arbol #deja lista la caja con la tabla dentro para que posteriormente se pueda llenar con los datos


def limpiar_arbol(arbol):
    for item in arbol.get_children():
        arbol.delete(item) #borra todos los elementos de la tabla, para que se pueda actualizar con nuevos datos
