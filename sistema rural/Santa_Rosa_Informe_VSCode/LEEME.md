# SistemaRural-PE con interfaz gráfica

Versión basada en el **código del apartado 1.4** de `Copia de AVANCE_LENGUAJEPROGRAMACION1.1.docx`. El informe usa el Centro de Salud Rural **Santa Rosa, Chugur**, por lo que esta versión conserva ese nombre y no usa el caso Simón Bolívar del proyecto anterior.

## Ejecutar en VS Code

1. Extrae todo el ZIP y conserva los archivos juntos.
2. En VS Code, selecciona **Archivo > Abrir carpeta** y abre `Santa_Rosa_Informe_VSCode`.
3. Abre **Terminal > Nueva terminal**.
4. Ejecuta:

```powershell
python main.py
```

Si tu instalación utiliza el lanzador, ejecuta `py main.py`. También puedes hacer doble clic en `INICIAR.bat` después de extraer todo el ZIP.

**Clave de demostración: `Chugur2026`**

El inicio de sesión permite tres intentos, como el programa del Word. No se necesita un nombre de usuario. Al agotarse los intentos, la aplicación se cierra.

Se requiere Python 3.10 o posterior con Tkinter. No hay paquetes externos que instalar. Puedes comprobar Tkinter con `python -m tkinter`.

## Opciones del Word y sus pantallas

| Opción original | Interfaz gráfica |
|---|---|
| 1. Registrar nuevo paciente | Pacientes > Registrar paciente |
| 2. Registrar nueva cita médica | Citas > Registrar cita |
| 3. Cambiar estado de una cita | Seleccionar cita > escoger estado > Guardar estado |
| 4. Ver citas pendientes (filter) | Pendientes |
| 5. Ver listado protegido (map) | Reportes y tabla de Pacientes |
| 6. Ver edad promedio (reduce) | Reportes y tarjeta de Resumen |
| 7. Salir | Salir del sistema o cerrar ventana |

Se mantienen `Usuario`, `Paciente`, `Cita`, `ValidacionError` y `FuncionalReportes`; sus nombres, propiedades y métodos están en `codigo_informe.py`. El usuario predeterminado, el hash SHA-256, la máscara del DNI, el intervalo de edad de 1 a 120, los códigos P01/C01, las listas en memoria y los estados PROGRAMADA/ATENDIDA/CANCELADA corresponden al código proporcionado.

La interfaz utiliza las clases originales; no es una simulación con datos desconectados. `sistema.py` convierte las operaciones del menú en métodos que los botones pueden llamar. `interfaz.py` contiene las ventanas, eventos, formularios y mensajes.

## Ajustes mínimos de la adaptación

- Se sustituyen `input()` y `print()` por entradas, botones, tablas y avisos de Tkinter.
- Se rechazan nombres vacíos y se limita su longitud a 80 caracteres para mantener legible la interfaz.
- El DNI se escribe oculto en el formulario y las tablas muestran únicamente `*****` más los últimos tres dígitos. El campo se limpia al registrar.
- Se verifica una fecha real con formato `AAAA-MM-DD HH:MM`. El código original aceptaba cualquier texto en ese campo.
- Se comprueba que exista una sesión iniciada antes de ejecutar las operaciones.
- Se pide confirmación antes de cancelar una cita o salir de la sesión con datos.
- Se precisan dos comentarios: SHA-256 es un **hash**, no cifrado; la máscara del DNI es ocultación parcial, no anonimización ni garantía de cumplimiento normativo.

El código original completo extraído del documento, sin esos ajustes, se conserva en `referencia/codigo_word_original.py` para comparar. No es el archivo que debes ejecutar para ver la interfaz.

## Datos y límites

El sistema empieza vacío, igual que el código del Word. Usa nombres y números ficticios. Los registros se mantienen en memoria y se pierden al cerrar. No se implementa una base de datos.

Se conserva la lógica de estados del informe: una cita puede cambiar a cualquiera de los tres estados permitidos. No hay profesionales asignados a las citas, validación de disponibilidad ni bloqueo de citas duplicadas porque esas funciones no están en el código del apartado 1.4.

El Word describe además clases y capacidades que no aparecen en su código: Médico, Recepcionista como subclase, Atención, Historial Clínico, ReporteFactory, exportación PDF y permisos diferenciados por rol. **Esta adaptación no declara implementadas esas capacidades.** El acceso sigue siendo el de un único usuario de demostración.

SHA-256 simple y una clave incluida en el código no constituyen autenticación apta para producción. El DNI completo sigue en memoria dentro del objeto y los nombres aparecen en los listados; por eso se usan solo datos ficticios. No se afirma que este prototipo acredite cumplimiento de la Ley N.º 29733.

## Probar

```powershell
python -m unittest -v test_sistema
```

Resultado esperado: 16 pruebas y `OK`.

Para la exposición: inicia sesión, registra dos pacientes ficticios con edades 25 y 35, programa dos citas, cambia una a ATENDIDA, consulta Pendientes y muestra en Reportes el promedio 30.0 y los DNI parcialmente ocultos. Abre `codigo_informe.py` para señalar `filter`, `map`, `reduce` y las propiedades del modelo.
