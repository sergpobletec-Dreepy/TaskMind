from tkinter import ttk


def arbol_con_scroll(parent, columnas, anchos):
    contenedor = ttk.Frame(parent)
    arbol = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse")
    scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=arbol.yview)
    scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=arbol.xview)
    arbol.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    for col in columnas:
        arbol.heading(col, text=col)
        arbol.column(col, width=anchos.get(col, 120), minwidth=60, stretch=True)

    arbol.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)
    return contenedor, arbol


def limpiar_arbol(arbol):
    for item in arbol.get_children():
        arbol.delete(item)
