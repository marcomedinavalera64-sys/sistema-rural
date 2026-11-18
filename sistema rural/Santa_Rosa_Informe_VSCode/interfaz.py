"""Interfaz Tkinter del código del informe. Los handlers sustituyen input/print."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from codigo_informe import Cita, ValidacionError

FONDO = "#F3F6FA"
TINTA = "#173247"
SUAVE = "#647789"
AZUL = "#102E43"
VERDE = "#087E86"
BORDE = "#DDE5EB"


class Aplicacion:
    def __init__(self, raiz, sistema):
        self.raiz, self.sistema = raiz, sistema
        self.raiz.title("Santa Rosa · SistemaRural-PE | Grupo 6")
        self.raiz.geometry("1180x780")
        self.raiz.minsize(1040, 720)
        self.raiz.configure(bg=FONDO)
        self.estilos()
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)
        self.mostrar_login()

    def mostrar_login(self):
        self.login = tk.Frame(self.raiz, bg=FONDO)
        self.login.pack(fill="both", expand=True)
        presentacion = tk.Frame(self.login, bg=AZUL, width=425, padx=46)
        presentacion.pack(side="left", fill="y")
        presentacion.pack_propagate(False)
        self.etiqueta(presentacion, "+", 50, "#84DFCE", True).pack(anchor="w", pady=(100, 22))
        self.etiqueta(presentacion, "SANTA\nROSA", 37, "white", True, justify="left").pack(anchor="w")
        self.etiqueta(presentacion, "Centro de Salud Rural\nChugur · Cajamarca", 13, "#BBD1DD", justify="left").pack(anchor="w", pady=20)
        self.etiqueta(presentacion, "SistemaRural-PE\nGestión de pacientes y citas", 11, "white", justify="left").pack(anchor="w", pady=18)
        self.etiqueta(presentacion, "LENGUAJE DE PROGRAMACIÓN\nGRUPO 6 · DEMOSTRACIÓN ACADÉMICA", 9,
                      "#BBD1DD", justify="left").pack(side="bottom", anchor="w", pady=35)
        lado = tk.Frame(self.login, bg=FONDO)
        lado.pack(side="left", fill="both", expand=True)
        tarjeta = tk.Frame(lado, bg="white", padx=36, pady=34,
                            highlightbackground=BORDE, highlightthickness=1)
        tarjeta.place(relx=.5, rely=.5, anchor="center", relwidth=.84)
        self.etiqueta(tarjeta, "Bienvenido", 27, TINTA, True).pack(anchor="w")
        self.etiqueta(tarjeta, "Ingresa para comenzar la demostración.", 11, SUAVE).pack(anchor="w", pady=(8, 24))
        self.etiqueta(tarjeta, "Recepcionista Santa Rosa", 11, TINTA, True).pack(anchor="w", pady=(0, 18))
        self.etiqueta(tarjeta, "Contraseña", 9, SUAVE, True).pack(anchor="w", pady=(0, 6))
        self.clave = tk.StringVar()
        self.entrada_clave = ttk.Entry(tarjeta, textvariable=self.clave, show="•")
        self.entrada_clave.pack(fill="x")
        mostrar = tk.BooleanVar()
        tk.Checkbutton(tarjeta, text="Mostrar contraseña", variable=mostrar,
                       command=lambda: self.entrada_clave.configure(show="" if mostrar.get() else "•"),
                       bg="white", fg=SUAVE, activebackground="white", relief="flat").pack(anchor="w", pady=8)
        self.btn_ingresar = self.boton(tarjeta, "Ingresar al sistema", self.ingresar)
        self.btn_ingresar.pack(fill="x", pady=(6, 15))
        self.aviso_login = tk.StringVar(value="Tienes 3 intentos para ingresar.")
        tk.Label(tarjeta, textvariable=self.aviso_login, bg="white", fg=SUAVE,
                 font=("Segoe UI", 9), wraplength=360, justify="left").pack(anchor="w")
        self.etiqueta(tarjeta, "Clave de demostración: Chugur2026", 10, VERDE, True).pack(anchor="w", pady=(18, 5))
        self.etiqueta(tarjeta, "Usa datos ficticios. Los registros duran esta sesión.", 9, SUAVE,
                      wraplength=360, justify="left").pack(anchor="w")
        self.entrada_clave.bind("<Return>", lambda evento: self.ingresar())
        self.entrada_clave.focus_set()

    def ingresar(self):
        try:
            correcto = self.sistema.iniciar_sesion(self.clave.get())
        except ValidacionError as error:
            self.aviso_login.set(str(error))
            return
        if correcto:
            self.login.destroy()
            self.construir_marco()
            self.navegar("Resumen")
        else:
            restantes = 3 - self.sistema.intentos
            self.clave.set("")
            self.aviso_login.set(f"Contraseña incorrecta. Intentos restantes: {restantes}.")
            if restantes == 0:
                self.btn_ingresar.configure(state="disabled")
                self.entrada_clave.configure(state="disabled")
                messagebox.showerror("Acceso denegado", "Se agotaron los tres intentos. El sistema se cerrará.", parent=self.raiz)
                self.raiz.destroy()

    def construir_marco(self):
        lateral = tk.Frame(self.raiz, bg=AZUL, width=205)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)
        self.etiqueta(lateral, "+  SANTA ROSA", 17, "white", True).pack(anchor="w", padx=20, pady=(30, 8))
        self.etiqueta(lateral, "Chugur · Cajamarca", 10, "#BBD1DD").pack(anchor="w", padx=20)
        self.etiqueta(lateral, "SISTEMARURAL-PE", 8, "#A4BECD", True).pack(anchor="w", padx=20, pady=(35, 12))
        self.menu = {}
        for numero, nombre in enumerate(("Resumen", "Pacientes", "Citas", "Pendientes", "Reportes"), 1):
            boton = tk.Button(lateral, text=f"{numero:02}    {nombre}", anchor="w",
                               command=lambda n=nombre: self.navegar(n), bg=AZUL, fg="#CDDFE8",
                               activebackground="#245165", activeforeground="white", relief="flat", bd=0,
                               cursor="hand2", font=("Segoe UI", 11), padx=16, pady=14)
            boton.pack(fill="x", padx=10, pady=4)
            self.menu[nombre] = boton
        self.boton(lateral, "Salir del sistema", self.salir, True).pack(side="bottom", fill="x", padx=20, pady=(15, 25))
        self.etiqueta(lateral, "Grupo 6\nDemostración académica\nDatos en memoria", 9, "#BBD1DD",
                      justify="left").pack(side="bottom", anchor="w", padx=20)
        derecha = tk.Frame(self.raiz, bg=FONDO)
        derecha.pack(side="left", fill="both", expand=True)
        cabecera = tk.Frame(derecha, bg="white", padx=26, pady=14)
        cabecera.pack(fill="x")
        self.etiqueta(cabecera, "Recepcionista Santa Rosa", 10, SUAVE).pack(side="left")
        self.etiqueta(cabecera, "SESIÓN ACTIVA  /  " + date.today().strftime("%d.%m.%Y"), 9, VERDE, True).pack(side="right")
        self.estado = tk.StringVar(value="Acceso concedido. Comienza registrando un paciente ficticio.")
        tk.Label(derecha, textvariable=self.estado, bg="#E8F0F4", fg=TINTA, anchor="w",
                 font=("Segoe UI", 9), padx=24, pady=10).pack(side="bottom", fill="x")
        self.contenido = tk.Frame(derecha, bg=FONDO, padx=25, pady=20)
        self.contenido.pack(fill="both", expand=True)

    def navegar(self, nombre):
        if not self.sistema.autenticado:
            return
        for hijo in self.contenido.winfo_children():
            hijo.destroy()
        for clave, boton in self.menu.items():
            boton.configure(bg="#245165" if clave == nombre else AZUL)
        vistas = {"Resumen": self.resumen, "Pacientes": self.pacientes,
                  "Citas": self.citas, "Pendientes": self.pendientes, "Reportes": self.reportes}
        vistas[nombre]()

    def titulo(self, titulo, subtitulo):
        self.etiqueta(self.contenido, titulo, 25, TINTA, True).pack(anchor="w")
        self.etiqueta(self.contenido, subtitulo, 10, SUAVE).pack(anchor="w", pady=(5, 18))

    def ejecutar(self, accion, mensaje):
        try:
            resultado = accion()
        except (ValidacionError, ValueError) as error:
            self.estado.set(str(error))
            messagebox.showwarning("Revisa los datos", str(error), parent=self.raiz)
            return False
        self.estado.set(mensaje(resultado) if callable(mensaje) else mensaje)
        return True

    def tarjetas(self, datos):
        fila = tk.Frame(self.contenido, bg=FONDO)
        fila.pack(fill="x", pady=(0, 16))
        for i, (titulo, valor) in enumerate(datos):
            fila.columnconfigure(i, weight=1)
            tarjeta = self.panel(fila)
            tarjeta.grid(row=0, column=i, sticky="ew", padx=(0, 10 if i < len(datos)-1 else 0))
            self.etiqueta(tarjeta, titulo, 8, SUAVE, True).pack(anchor="w")
            self.etiqueta(tarjeta, str(valor), 28, VERDE, True).pack(anchor="w", pady=(8, 0))

    def tabla_citas(self, padre, datos):
        arbol = self.tabla(padre, [("id", "Cita", 65), ("pac", "Paciente", 230),
                                  ("fecha", "Fecha y hora", 180), ("estado", "Estado", 130)], 6)
        self.llenar(arbol, [(c.id_c, c.paciente.nombre, c.fecha, c.estado) for c in datos])
        return arbol

    def resumen(self):
        self.titulo("Gestión de pacientes y citas", "El módulo operativo de tu informe, ahora con interfaz gráfica.")
        self.tarjetas((("PACIENTES", len(self.sistema.pacientes_db)), ("CITAS", len(self.sistema.citas_db)),
                       ("PROGRAMADAS", len(self.sistema.pendientes())), ("EDAD PROMEDIO", f"{self.sistema.promedio():.1f}")))
        acciones = tk.Frame(self.contenido, bg=FONDO)
        acciones.pack(fill="x", pady=(0, 15))
        self.boton(acciones, "+ Registrar paciente", lambda: self.navegar("Pacientes")).pack(side="left")
        self.boton(acciones, "+ Registrar cita", lambda: self.navegar("Citas"), True).pack(side="left", padx=10)
        panel = self.panel()
        panel.pack(fill="both", expand=True)
        self.etiqueta(panel, "Últimas citas registradas", 14, TINTA, True).pack(anchor="w")
        if not self.sistema.citas_db:
            self.etiqueta(panel, "Aún no hay citas. Registra un paciente y programa su primera cita.", 10, SUAVE,
                          wraplength=650, justify="left").pack(anchor="w", pady=(16, 5))
        self.tabla_citas(panel, self.sistema.citas_db[-10:])

    def pacientes(self):
        self.titulo("Registro de pacientes", "Datos ficticios para la exposición · DNI de 8 dígitos · Edad de 1 a 120 años.")
        panel = self.panel()
        panel.pack(fill="x")
        campos = tk.Frame(panel, bg="white")
        campos.pack(fill="x")
        self.p_nombre, _ = self.campo(campos, "Nombre y apellido ficticios", 0, ancho=25)
        self.p_dni, entrada_dni = self.campo(campos, "DNI ficticio", 1, ancho=15)
        entrada_dni.configure(show="•")
        self.p_edad, _ = self.campo(campos, "Edad", 2, ancho=10)
        barra = tk.Frame(panel, bg="white")
        barra.pack(fill="x", pady=(14, 0))
        listado = self.panel()
        listado.pack(fill="both", expand=True, pady=(16, 0))
        self.etiqueta(listado, "Pacientes registrados", 14, TINTA, True).pack(anchor="w")
        self.etiqueta(listado, "El listado muestra únicamente los últimos tres dígitos del DNI.", 9, SUAVE).pack(anchor="w", pady=4)
        self.tabla_p = self.tabla(listado, [("id", "Código", 70), ("nombre", "Nombre", 280),
                                          ("dni", "DNI protegido", 130), ("edad", "Edad", 80)], 6)
        def actualizar():
            self.llenar(self.tabla_p, [(p["ID"], p["Nombre"], p["DNI_Protegido"], p["Edad"])
                                      for p in self.sistema.resumen_pacientes()])
        def limpiar():
            self.p_nombre.set(""); self.p_dni.set(""); self.p_edad.set("")
        def registrar():
            if self.ejecutar(lambda: self.sistema.registrar_paciente(self.p_nombre.get(), self.p_dni.get(), self.p_edad.get()),
                             lambda p: f"Paciente {p.id_p} registrado correctamente."):
                limpiar()
                actualizar()
        self.btn_registrar = self.boton(barra, "Registrar paciente", registrar)
        self.btn_registrar.pack(side="left")
        self.boton(barra, "Limpiar", limpiar, True).pack(side="left", padx=10)
        actualizar()

    def citas(self):
        self.titulo("Citas médicas", "Programa una cita y actualiza su estado como en el código del informe.")
        panel = self.panel()
        panel.pack(fill="x")
        campos = tk.Frame(panel, bg="white")
        campos.pack(fill="x")
        opciones = [f"{p.id_p} · {p.nombre}" for p in self.sistema.pacientes_db]
        self.c_paciente, _ = self.campo(campos, "Paciente registrado", 0, opciones=opciones, ancho=27)
        self.c_fecha, _ = self.campo(campos, "Fecha AAAA-MM-DD", 1, date.today().isoformat(), ancho=15)
        self.c_hora, _ = self.campo(campos, "Hora HH:MM", 2, "09:00", ancho=9)
        lista = self.panel()
        lista.pack(fill="both", expand=True, pady=(16, 0))
        self.etiqueta(lista, "Citas registradas", 14, TINTA, True).pack(anchor="w")
        self.tabla_c = self.tabla_citas(lista, self.sistema.citas_db)
        def registrar():
            if self.ejecutar(lambda: self.sistema.registrar_cita(self.c_paciente.get().split(" · ")[0],
                               self.c_fecha.get().strip()+" "+self.c_hora.get().strip()),
                             lambda c: f"Cita {c.id_c} registrada en estado PROGRAMADA."):
                actualizar()
        self.btn_cita = self.boton(panel, "Registrar cita", registrar)
        self.btn_cita.pack(anchor="w", pady=(14, 0))
        barra = tk.Frame(lista, bg="white")
        barra.pack(side="bottom", fill="x", pady=(13, 0), before=self.tabla_c.master)
        self.etiqueta(barra, "Nuevo estado", 9, SUAVE).pack(side="left", padx=(0, 10))
        self.c_estado = tk.StringVar(value="PROGRAMADA")
        ttk.Combobox(barra, values=Cita.ESTADOS, textvariable=self.c_estado,
                     state="readonly", width=17).pack(side="left")
        def cambiar():
            codigo = self.seleccionado(self.tabla_c)
            if codigo and self.c_estado.get() == "CANCELADA":
                if not messagebox.askyesno("Cancelar cita", f"¿Cambiar {codigo} a CANCELADA?", parent=self.raiz):
                    return
            if self.ejecutar(lambda: self.sistema.cambiar_estado(codigo, self.c_estado.get()),
                             lambda c: f"Cita {c.id_c}: estado actualizado a {c.estado}."):
                actualizar()
        self.btn_estado = self.boton(barra, "Guardar estado", cambiar)
        self.btn_estado.pack(side="right")
        def actualizar():
            self.llenar(self.tabla_c, [(c.id_c, c.paciente.nombre, c.fecha, c.estado) for c in self.sistema.citas_db])
        def seleccionar(event=None):
            codigo = self.seleccionado(self.tabla_c)
            cita = next((c for c in self.sistema.citas_db if c.id_c == codigo), None)
            if cita:
                self.c_estado.set(cita.estado)
        self.tabla_c.bind("<<TreeviewSelect>>", seleccionar)

    def pendientes(self):
        self.titulo("Citas pendientes", "Consulta las citas que conservan el estado PROGRAMADA.")
        datos = self.sistema.pendientes()
        self.tarjetas((("CITAS PROGRAMADAS", len(datos)), ("TOTAL DE CITAS", len(self.sistema.citas_db))))
        panel = self.panel()
        panel.pack(fill="both", expand=True)
        self.etiqueta(panel, "Próximas atenciones registradas", 14, TINTA, True).pack(anchor="w")
        self.tabla_pendientes = self.tabla_citas(panel, datos)
        barra = tk.Frame(panel, bg="white")
        barra.pack(side="bottom", fill="x", pady=(12, 0), before=self.tabla_pendientes.master)
        self.etiqueta(barra, "Consulta mediante FuncionalReportes.filtrar_programadas", 9, SUAVE).pack(side="left")
        self.boton(barra, "Actualizar", lambda: self.navegar("Pendientes"), True).pack(side="right")

    def reportes(self):
        self.titulo("Reportes de pacientes", "Listado con DNI parcialmente oculto y cálculo de la edad promedio.")
        self.tarjetas((("PACIENTES REGISTRADOS", len(self.sistema.pacientes_db)),
                       ("EDAD PROMEDIO", f"{self.sistema.promedio():.1f} años")))
        panel = self.panel()
        panel.pack(fill="both", expand=True)
        self.etiqueta(panel, "Listado protegido", 14, TINTA, True).pack(anchor="w")
        self.etiqueta(panel, "Incluye nombres; ocultar parte del DNI no convierte el listado en anónimo.", 9, SUAVE,
                      wraplength=700, justify="left").pack(anchor="w", pady=6)
        self.tabla_r = self.tabla(panel, [("id", "Código", 70), ("nombre", "Nombre", 260),
                                         ("dni", "DNI protegido", 130), ("edad", "Edad", 85)], 7)
        self.llenar(self.tabla_r, [(p["ID"], p["Nombre"], p["DNI_Protegido"], p["Edad"])
                                  for p in self.sistema.resumen_pacientes()])
        pie = tk.Frame(panel, bg="white")
        pie.pack(side="bottom", fill="x", pady=(12, 0), before=self.tabla_r.master)
        self.etiqueta(pie, "map: listado protegido  ·  reduce: promedio de edades", 9, SUAVE).pack(side="left")
        self.boton(pie, "Actualizar reportes", lambda: self.navegar("Reportes"), True).pack(side="right")

    def salir(self):
        if not self.sistema.autenticado or messagebox.askyesno("Salir del sistema",
            "Los datos están en memoria y se perderán al cerrar. ¿Deseas salir?", parent=self.raiz):
            self.raiz.destroy()


    def estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TEntry", padding=8, fieldbackground="white", bordercolor=BORDE)
        estilo.configure("TCombobox", padding=7, fieldbackground="white", arrowsize=14)
        estilo.map("TCombobox", fieldbackground=[("readonly", "white")],
                   foreground=[("readonly", TINTA)])
        estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=34,
                         background="white", fieldbackground="white", foreground=TINTA,
                         borderwidth=0)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                         background="#EAF0F5", foreground=TINTA, padding=(8, 10), relief="flat")
        estilo.map("Treeview", background=[("selected", "#D3ECEE")],
                   foreground=[("selected", TINTA)])
        estilo.configure("Vertical.TScrollbar", troughcolor=FONDO, background=BORDE)
        self.raiz.option_add("*Font", ("Segoe UI", 10))

    def etiqueta(self, padre, texto, tam=10, color=TINTA, negrita=False, **opciones):
        return tk.Label(padre, text=texto, font=("Segoe UI", tam, "bold" if negrita else "normal"),
                        fg=color, bg=padre.cget("bg"), **opciones)

    def boton(self, padre, texto, accion, secundario=False):
        boton = tk.Button(padre, text=texto, command=accion, cursor="hand2",
                          font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                          bg="#EAF0F5" if secundario else VERDE,
                          fg=TINTA if secundario else "white", activebackground="#CDE7E9",
                          activeforeground=TINTA, padx=13, pady=10)
        return boton

    def panel(self, padre=None):
        return tk.Frame(padre or self.contenido, bg="white", padx=16, pady=15,
                        highlightbackground=BORDE, highlightthickness=1)

    def campo(self, padre, titulo, columna, valor="", opciones=None, ancho=22):
        marco = tk.Frame(padre, bg=padre.cget("bg"))
        marco.grid(row=0, column=columna, sticky="ew", padx=(0, 12))
        padre.columnconfigure(columna, weight=1)
        self.etiqueta(marco, titulo, 9, SUAVE, True).pack(anchor="w", pady=(0, 6))
        variable = tk.StringVar(value=valor)
        if opciones is None:
            widget = ttk.Entry(marco, textvariable=variable, width=ancho)
        else:
            widget = ttk.Combobox(marco, textvariable=variable, values=opciones,
                                  state="readonly", width=ancho)
        widget.pack(fill="x")
        return variable, widget

    def tabla(self, padre, columnas, altura=8):
        marco = tk.Frame(padre, bg="white")
        marco.pack(fill="both", expand=True, pady=(10, 0))
        arbol = ttk.Treeview(marco, columns=[c[0] for c in columnas], show="headings",
                             height=altura, selectmode="browse")
        for clave, titulo, ancho in columnas:
            arbol.heading(clave, text=titulo, anchor="w")
            arbol.column(clave, width=ancho, minwidth=55, anchor="w")
        vertical = ttk.Scrollbar(marco, orient="vertical", command=arbol.yview)
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=arbol.xview)
        arbol.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        arbol.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)
        arbol.tag_configure("par", background="#F5F8FB")
        arbol.tag_configure("alerta", foreground="#A35D10")
        return arbol

    def llenar(self, arbol, filas):
        seleccion = arbol.selection()
        arbol.delete(*arbol.get_children())
        for i, fila in enumerate(filas):
            arbol.insert("", "end", iid=str(fila[0]), values=fila,
                         tags=("par",) if i % 2 else ())
        if seleccion and arbol.exists(seleccion[0]):
            arbol.selection_set(seleccion[0])

    def seleccionado(self, arbol):
        return arbol.selection()[0] if arbol.selection() else ""
