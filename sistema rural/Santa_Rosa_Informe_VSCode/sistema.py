"""Operaciones del menú del informe, reutilizadas por la interfaz gráfica."""
from datetime import datetime
from codigo_informe import Usuario, Paciente, Cita, FuncionalReportes, ValidacionError


class Sistema:
    def __init__(self):
        # Mismas listas en memoria y usuario de demostración que en el Word.
        self.pacientes_db = []
        self.citas_db = []
        self.admin = Usuario("U01", "Recepcionista Santa Rosa", "Chugur2026")
        self.intentos = 0
        self.autenticado = False

    def iniciar_sesion(self, clave):
        if self.intentos >= 3:
            raise ValidacionError("Se agotaron los tres intentos. Reinicia el programa.")
        if self.admin.autenticar(clave):
            self.autenticado = True
            return True
        self.intentos += 1
        return False

    def verificar_sesion(self):
        if not self.autenticado:
            raise ValidacionError("Primero debes iniciar sesión.")

    def registrar_paciente(self, nombre, dni, edad_texto):
        self.verificar_sesion()
        nombre, dni = nombre.strip(), dni.strip()
        if not nombre:
            raise ValidacionError("Escribe el nombre ficticio del paciente.")
        if len(nombre) > 80:
            raise ValidacionError("El nombre puede tener hasta 80 caracteres.")
        try:
            edad = int(edad_texto)
        except (ValueError, TypeError):
            raise ValidacionError("La edad debe ser un número entero.") from None
        # Se conserva el intervalo del menú original: de 1 a 120 años.
        if edad <= 0 or edad > 120:
            raise ValidacionError("La edad ingresada no es válida. Usa de 1 a 120 años.")
        if not dni.isascii():
            raise ValidacionError("El DNI debe contener 8 dígitos del 0 al 9.")
        paciente = Paciente(f"P{len(self.pacientes_db) + 1:02d}", nombre, dni, edad)
        self.pacientes_db.append(paciente)
        return paciente

    def registrar_cita(self, id_p, fecha):
        self.verificar_sesion()
        paciente = next((p for p in self.pacientes_db if p.id_p == id_p), None)
        if paciente is None:
            raise ValidacionError("Registra y selecciona un paciente antes de programar la cita.")
        fecha = fecha.strip()
        try:
            momento = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValidacionError("Usa una fecha real con el formato AAAA-MM-DD HH:MM.") from None
        if momento.strftime("%Y-%m-%d %H:%M") != fecha:
            raise ValidacionError("Usa el formato AAAA-MM-DD HH:MM, por ejemplo 2026-11-18 09:00.")
        cita = Cita(f"C{len(self.citas_db) + 1:02d}", paciente, fecha)
        self.citas_db.append(cita)
        return cita

    def cambiar_estado(self, id_c, nuevo_estado):
        self.verificar_sesion()
        cita = next((c for c in self.citas_db if c.id_c == id_c), None)
        if cita is None:
            raise ValidacionError("Selecciona una cita en la tabla.")
        # Usa el setter original; admite los tres estados del informe.
        cita.estado = nuevo_estado.strip()
        return cita

    def pendientes(self):
        self.verificar_sesion()
        return FuncionalReportes.filtrar_programadas(self.citas_db)

    def resumen_pacientes(self):
        self.verificar_sesion()
        return FuncionalReportes.mapear_resumen(self.pacientes_db)

    def promedio(self):
        self.verificar_sesion()
        return FuncionalReportes.promedio_edad(self.pacientes_db)
