"""Clases y funciones extraídas del apartado 1.4 del informe.
Lógica original conservada; se precisaron dos comentarios de seguridad.
Solo para demostración con datos ficticios.
"""
import hashlib
from functools import reduce

# ==========================================
# 1. EXCEPCIONES Y MODELO DE OBJETOS (POO)
# ==========================================
class ValidacionError(Exception): 
    pass

class Usuario:
    """Usuario del sistema con hash SHA-256; hash no es cifrado."""
    def __init__(self, id_u: str, nombre: str, clave: str):
        self.id_u = id_u
        self.nombre = nombre
        self.__hash = hashlib.sha256(clave.encode()).hexdigest()

    def autenticar(self, clave_ingresada: str) -> bool:
        return self.__hash == hashlib.sha256(clave_ingresada.encode()).hexdigest()

class Paciente:
    """Paciente con DNI parcialmente oculto en las salidas."""
    def __init__(self, id_p: str, nombre: str, dni: str, edad: int):
        self.id_p = id_p
        self.nombre = nombre
        self.dni = dni  # Usa el setter con validación
        self.edad = edad

    @property
    def dni_protegido(self) -> str:
        """Muestra solo los últimos 3 dígitos para proteger la privacidad."""
        return f"*****{self.__dni[-3:]}"

    @property
    def dni_real(self) -> str:
        return self.__dni

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, valor: str):
        if not valor.isdigit() or len(valor) != 8:
            raise ValidacionError("El DNI debe tener exactamente 8 dígitos numéricos.")
        self.__dni = valor

class Cita:
    """Cita médica con control de estados."""
    ESTADOS = ["PROGRAMADA", "ATENDIDA", "CANCELADA"]

    def __init__(self, id_c: str, paciente: Paciente, fecha: str):
        self.id_c = id_c
        self.paciente = paciente
        self.fecha = fecha
        self.__estado = "PROGRAMADA"

    @property
    def estado(self) -> str: 
        return self.__estado

    @estado.setter
    def estado(self, valor: str):
        if valor.upper() not in self.ESTADOS:
            raise ValidacionError(f"Estado no válido. Use: {self.ESTADOS}")
        self.__estado = valor.upper()

# ==========================================
# 2. PARADIGMA FUNCIONAL (PROCESAMIENTO)
# ==========================================
class FuncionalReportes:
    @staticmethod
    def filtrar_programadas(citas: list[Cita]) -> list[Cita]:
        """filter(): Filtra citas en estado PROGRAMADA."""
        return list(filter(lambda c: c.estado == "PROGRAMADA", citas))

    @staticmethod
    def mapear_resumen(pacientes: list[Paciente]) -> list[dict]:
        """map(): Transforma la lista a un resumen seguro con DNI protegido."""
        return list(map(lambda p: {
            "ID": p.id_p,
            "Nombre": p.nombre, 
            "DNI_Protegido": p.dni_protegido, 
            "Edad": p.edad
        }, pacientes))

    @staticmethod
    def promedio_edad(pacientes: list[Paciente]) -> float:
        """reduce(): Calcula la edad promedio acumulada."""
        if not pacientes: 
            return 0.0
        return reduce(lambda acc, p: acc + p.edad, pacientes, 0) / len(pacientes)

