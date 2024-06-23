import tkinter as tk
from tkinter import ttk

class Equipo:
    def __init__(self, nombre, entrenador):
        self.nombre = nombre
        self.entrenador = entrenador

class Partido:
    def __init__(self, equipo_local, equipo_visitante):
        self.equipo_local = equipo_local
        self.equipo_visitante = equipo_visitante
        self.resultado = None

    def jugar_partido(self, resultado):
        self.resultado = resultado
        return f"Partido entre {self.equipo_local.nombre} y {self.equipo_visitante.nombre} jugado. Resultado: {self.resultado}\n"

class Grupo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.equipos = []

    def agregar_equipo(self, equipo):
        self.equipos.append(equipo)

class Mundial:
    def __init__(self, info_text):
        self.grupos = []
        self.info_text = info_text

    def registrar_grupo(self, grupo):
        self.grupos.append(grupo)
        self.info_text.insert(tk.END, f"Grupo {grupo.nombre} registrado en el Mundial\n")

class GestionMundial:
    def __init__(self, root):
        self.mundial = Mundial(None)

        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Pestaña de equipos
        self.equipo_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.equipo_tab, text="Equipos")

        self.equipo_frame = tk.LabelFrame(self.equipo_tab, text="Agregar Equipo", padx=10, pady=10)
        self.equipo_frame.pack(fill="x", padx=10, pady=10)

        self.equipo_nombre_entry = self.crear_entrada(self.equipo_frame, "Nombre del Equipo:", 0, 0)
        self.entrenador_nombre_entry = self.crear_entrada(self.equipo_frame, "Nombre del Entrenador:", 1, 0)

        self.agregar_equipo_button = tk.Button(self.equipo_frame, text="Agregar Equipo", command=self.agregar_equipo)
        self.agregar_equipo_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Pestaña de grupos
        self.grupo_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.grupo_tab, text="Grupos")

        self.grupo_frame = tk.LabelFrame(self.grupo_tab, text="Registrar Grupo", padx=10, pady=10)
        self.grupo_frame.pack(fill="x", padx=10, pady=10)

        self.grupo_nombre_entry = self.crear_entrada(self.grupo_frame, "Nombre del Grupo:", 0, 0)
        
        self.agregar_grupo_button = tk.Button(self.grupo_frame, text="Registrar Grupo", command=self.registrar_grupo)
        self.agregar_grupo_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Pestaña de partidos
        self.partido_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.partido_tab, text="Partidos")

        self.partido_frame = tk.LabelFrame(self.partido_tab, text="Registrar Partido", padx=10, pady=10)
        self.partido_frame.pack(fill="x", padx=10, pady=10)

        self.equipo_local_entry = self.crear_entrada(self.partido_frame, "Equipo Local:", 0, 0)
        self.equipo_visitante_entry = self.crear_entrada(self.partido_frame, "Equipo Visitante:", 1, 0)
        self.resultado_entry = self.crear_entrada(self.partido_frame, "Resultado:", 2, 0)

        self.jugar_partido_button = tk.Button(self.partido_frame, text="Jugar Partido", command=self.jugar_partido)
        self.jugar_partido_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Pestaña de información
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text="Información")

        self.info_text = tk.Text(self.info_tab, height=20, width=50)
        self.info_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Asociar info_text con Mundial
        self.mundial.info_text = self.info_text

    def crear_entrada(self, parent, texto, fila, columna):
        label = tk.Label(parent, text=texto)
        label.grid(row=fila, column=columna, sticky="w", padx=5, pady=5)
        entry = tk.Entry(parent)
        entry.grid(row=fila, column=columna+1, sticky="w", padx=5, pady=5)
        return entry

    def agregar_equipo(self):
        nombre_equipo = self.equipo_nombre_entry.get()
        nombre_entrenador = self.entrenador_nombre_entry.get()

        equipo = Equipo(nombre_equipo, nombre_entrenador)
        grupo_seleccionado = self.obtener_grupo_seleccionado()

        if grupo_seleccionado:
            grupo_seleccionado.agregar_equipo(equipo)
            self.info_text.insert(tk.END, f"Equipo '{nombre_equipo}' agregado al grupo '{grupo_seleccionado.nombre}'\n")
        else:
            self.info_text.insert(tk.END, "Error: No hay grupo seleccionado\n")

        self.equipo_nombre_entry.delete(0, tk.END)
        self.entrenador_nombre_entry.delete(0, tk.END)

    def registrar_grupo(self):
        nombre_grupo = self.grupo_nombre_entry.get()
        grupo = Grupo(nombre_grupo)
        self.mundial.registrar_grupo(grupo)

        self.grupo_nombre_entry.delete(0, tk.END)

    def jugar_partido(self):
        nombre_equipo_local = self.equipo_local_entry.get()
        nombre_equipo_visitante = self.equipo_visitante_entry.get()
        resultado = self.resultado_entry.get()

        equipo_local = self.buscar_equipo(nombre_equipo_local)
        equipo_visitante = self.buscar_equipo(nombre_equipo_visitante)

        if equipo_local and equipo_visitante:
            partido = Partido(equipo_local, equipo_visitante)
            self.info_text.insert(tk.END, partido.jugar_partido(resultado))
        else:
            self.info_text.insert(tk.END, "Error: Equipos no encontrados\n")

        self.equipo_local_entry.delete(0, tk.END)
        self.equipo_visitante_entry.delete(0, tk.END)
        self.resultado_entry.delete(0, tk.END)

    def buscar_equipo(self, nombre):
        for grupo in self.mundial.grupos:
            for equipo in grupo.equipos:
                if equipo.nombre == nombre:
                    return equipo
        return None

    def obtener_grupo_seleccionado(self):
        grupos = self.mundial.grupos
        if grupos:
            return grupos[-1]  
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión del Mundial")
    root.geometry("800x600")
    gestion_mundial = GestionMundial(root)
    root.mainloop()
