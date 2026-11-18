import unittest
from codigo_informe import Usuario, Paciente, Cita, FuncionalReportes, ValidacionError
from sistema import Sistema


class PruebasInforme(unittest.TestCase):
    def setUp(self):
        self.s = Sistema()
        self.s.iniciar_sesion("Chugur2026")

    def paciente(self):
        return self.s.registrar_paciente("Paciente ficticio Alfa", "00000123", "25")

    def test_autenticacion_original(self):
        u = Usuario("U01", "Demo", "Chugur2026")
        self.assertTrue(u.autenticar("Chugur2026"))
        self.assertFalse(u.autenticar("otra"))
        self.assertNotIn("Chugur2026", vars(u).values())

    def test_tres_intentos(self):
        s = Sistema()
        for _ in range(3):
            self.assertFalse(s.iniciar_sesion("incorrecta"))
        with self.assertRaises(ValidacionError):
            s.iniciar_sesion("Chugur2026")
        self.assertFalse(s.autenticado)

    def test_acierto_en_tercer_intento(self):
        s = Sistema()
        s.iniciar_sesion("x"); s.iniciar_sesion("x")
        self.assertTrue(s.iniciar_sesion("Chugur2026"))

    def test_operaciones_sin_sesion(self):
        s = Sistema()
        for accion in (lambda: s.registrar_paciente("Demo", "00000123", "25"),
                       lambda: s.registrar_cita("P01", "2026-11-18 09:00"),
                       lambda: s.cambiar_estado("C01", "ATENDIDA"), s.pendientes,
                       s.resumen_pacientes, s.promedio):
            with self.assertRaises(ValidacionError):
                accion()

    def test_paciente_y_mascara(self):
        p = self.paciente()
        self.assertEqual(p.id_p, "P01")
        self.assertEqual(p.dni_protegido, "*****123")
        self.assertEqual(p.dni_real, "00000123")

    def test_dni_invalido(self):
        for dni in ("abc", "123", "123456789", "1234 678", "²²²²²²²²"):
            with self.subTest(dni=dni), self.assertRaises(ValidacionError):
                self.s.registrar_paciente("Demo", dni, "20")
        self.assertEqual(self.s.pacientes_db, [])

    def test_edad_y_nombre(self):
        for edad in ("0", "-1", "121", "hola", "2.5", ""):
            with self.subTest(edad=edad), self.assertRaises(ValidacionError):
                self.s.registrar_paciente("Demo", "00000123", edad)
        with self.assertRaises(ValidacionError):
            self.s.registrar_paciente(" ", "00000123", "20")
        self.assertEqual(self.s.pacientes_db, [])

    def test_cita_referencia(self):
        p = self.paciente()
        c = self.s.registrar_cita(p.id_p, "2026-11-18 09:00")
        self.assertEqual(c.id_c, "C01")
        self.assertIs(c.paciente, p)
        self.assertEqual(c.estado, "PROGRAMADA")

    def test_cita_sin_paciente(self):
        with self.assertRaises(ValidacionError):
            self.s.registrar_cita("P99", "2026-11-18 09:00")
        self.assertEqual(self.s.citas_db, [])

    def test_fecha_invalida(self):
        p = self.paciente()
        for fecha in ("", "mañana", "2026-02-30 09:00", "2026-11-18 25:00", "2026-1-1 9:0"):
            with self.subTest(fecha=fecha), self.assertRaises(ValidacionError):
                self.s.registrar_cita(p.id_p, fecha)
        self.assertEqual(self.s.citas_db, [])

    def test_estados_originales(self):
        p = self.paciente()
        c = self.s.registrar_cita(p.id_p, "2026-11-18 09:00")
        for estado in ("atendida", "cancelada", "programada"):
            self.s.cambiar_estado(c.id_c, estado)
            self.assertEqual(c.estado, estado.upper())
        with self.assertRaises(ValidacionError):
            self.s.cambiar_estado(c.id_c, "OTRA")
        self.assertEqual(c.estado, "PROGRAMADA")

    def test_estado_cita_inexistente(self):
        with self.assertRaises(ValidacionError):
            self.s.cambiar_estado("C99", "ATENDIDA")

    def test_filter(self):
        p = self.paciente()
        for hora in ("09:00", "10:00", "11:00"):
            self.s.registrar_cita(p.id_p, "2026-11-18 " + hora)
        self.s.cambiar_estado("C02", "ATENDIDA")
        self.s.cambiar_estado("C03", "CANCELADA")
        self.assertEqual([c.id_c for c in self.s.pendientes()], ["C01"])
        self.assertEqual(len(self.s.citas_db), 3)

    def test_map_y_reduce(self):
        self.paciente()
        self.s.registrar_paciente("Paciente ficticio Beta", "00000456", "35")
        resumen = self.s.resumen_pacientes()
        self.assertEqual(resumen[0]["DNI_Protegido"], "*****123")
        self.assertNotIn("00000123", str(resumen))
        self.assertEqual(self.s.promedio(), 30.0)
        resumen[0]["Nombre"] = "Cambio externo"
        self.assertEqual(self.s.pacientes_db[0].nombre, "Paciente ficticio Alfa")

    def test_reportes_vacios(self):
        self.assertEqual(self.s.pendientes(), [])
        self.assertEqual(self.s.resumen_pacientes(), [])
        self.assertEqual(self.s.promedio(), 0.0)

    def test_clases_originales_directas(self):
        p = Paciente("P01", "Demo", "00000123", 25)
        c = Cita("C01", p, "fecha del ejemplo original")
        c.estado = "atendida"
        self.assertEqual(FuncionalReportes.filtrar_programadas([c]), [])
        self.assertEqual(FuncionalReportes.promedio_edad([p]), 25.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
