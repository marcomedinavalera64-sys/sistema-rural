"""En VS Code: abrir esta carpeta y ejecutar python main.py."""
import tkinter as tk
from sistema import Sistema
from interfaz import Aplicacion


if __name__ == "__main__":
    ventana = tk.Tk()
    app = Aplicacion(ventana, Sistema())
    ventana.mainloop()
