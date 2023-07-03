import implementacion as impl
import tkinter as tk
import sys
from tkinter import messagebox

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

class VentanaSimulacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana de Simulación")
        self.geometry("850x300")
        self.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

        self.frame_datos = tk.Frame(self, bg="#403e4d")
        self.frame_datos.pack(fill=tk.BOTH, expand=True)

        self.frame_izquierda = tk.Frame(self.frame_datos, bg="#403e4d")
        self.frame_izquierda.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_derecha = tk.Frame(self.frame_datos, bg="#403e4d")
        self.frame_derecha.pack(side=tk.LEFT, padx=10, pady=10)

        self.label_cajeros = tk.Label(self.frame_izquierda, text="Número de Cajeros:", font=("Times New Roman", 12), bg="#403e4d", fg="white")
        self.label_cajeros.pack(side=tk.TOP, padx=10, pady=10)

        self.entry_cajeros = tk.Entry(self.frame_izquierda, font=("Times New Roman", 12))
        self.entry_cajeros.pack(side=tk.TOP, padx=10, pady=10)
        self.entry_cajeros.insert(tk.END, "1")  # Valor predeterminado

        self.label_simulaciones = tk.Label(self.frame_izquierda, text="Número de Simulaciones:", font=("Times New Roman", 12), bg="#403e4d", fg="white")
        self.label_simulaciones.pack(side=tk.TOP, padx=10, pady=10)

        self.entry_simulaciones = tk.Entry(self.frame_izquierda, font=("Times New Roman", 12))
        self.entry_simulaciones.pack(side=tk.TOP, padx=10, pady=10)
        self.entry_simulaciones.insert(tk.END, "1")  # Valor predeterminado

        self.button_ejecutar_simulacion = tk.Button(self.frame_izquierda, text="Ejecutar Simulación individual", command=self.ejecutar_simulacion)
        self.button_ejecutar_simulacion.pack(side=tk.TOP, padx=10, pady=10)

        self.button_ejecutar_simulaciones = tk.Button(self.frame_izquierda, text="Ejecutar Simulaciones en bloque", command=self.ejecutar_simulaciones)
        self.button_ejecutar_simulaciones.pack(side=tk.TOP, padx=10, pady=10)

        self.text_area = tk.Text(self.frame_derecha, font=("Times New Roman", 12), bg="#403e4d", fg="white")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Redirigir la salida estándar a la Text Area
        sys.stdout = RedirectText(self.text_area)

    def ejecutar_simulacion(self):
        # Obtener el número de cajeros ingresado
        num_cajeros_str = self.entry_cajeros.get()

        if not num_cajeros_str:
            # El campo está vacío
            messagebox.showerror("Error", "Ingrese un valor para el número de cajeros.")
            return

        try:
            num_cajeros = int(num_cajeros_str)
            if num_cajeros <= 0 or num_cajeros > 50:
                # El número de cajeros no cumple con los requisitos
                messagebox.showerror("Error", "Ingrese un valor entero positivo entre 1 y 50 para el número de cajeros.")
                return
        except ValueError:
            # El valor ingresado no es un entero válido
            messagebox.showerror("Error", "Ingrese un valor entero válido para el número de cajeros.")
            return

        # Ejecutar la simulación una vez
        impl.run_simulacion(num_cajeros=num_cajeros)

        # Mostrar mensaje de ejecución exitosa
        messagebox.showinfo("Simulación completada", "La simulación se ha completado y los resultados se han guardado.")

    def ejecutar_simulaciones(self):
        # Obtener el número de cajeros ingresado
        num_cajeros_str = self.entry_cajeros.get()

        if not num_cajeros_str:
            # El campo está vacío
            messagebox.showerror("Error", "Ingrese un valor para el número de cajeros.")
            return

        try:
            num_cajeros = int(num_cajeros_str)
            if num_cajeros <= 0 or num_cajeros > 50:
                # El número de cajeros no cumple con los requisitos
                messagebox.showerror("Error", "Ingrese un valor entero positivo entre 1 y 50 para el número de cajeros.")
                return
        except ValueError:
            # El valor ingresado no es un entero válido
            messagebox.showerror("Error", "Ingrese un valor entero válido para el número de cajeros.")
            return

        # Obtener el número de simulaciones ingresado
        num_simulaciones_str = self.entry_simulaciones.get()

        if not num_simulaciones_str:
            # El campo está vacío
            messagebox.showerror("Error", "Ingrese un valor para el número de simulaciones.")
            return

        try:
            num_simulaciones = int(num_simulaciones_str)
            if num_simulaciones <= 0:
                # El número de simulaciones no cumple con los requisitos
                messagebox.showerror("Error", "Ingrese un valor entero positivo mayor a cero para el número de simulaciones.")
                return
        except ValueError:
            # El valor ingresado no es un entero válido
            messagebox.showerror("Error", "Ingrese un valor entero válido para el número de simulaciones.")
            return

        # Ejecutar las simulaciones
        for _ in range(num_simulaciones):
            impl.run_simulacion(num_cajeros=num_cajeros)

        # Mostrar mensaje de ejecución exitosa
        messagebox.showinfo("Simulaciones completadas", f"Se han ejecutado {num_simulaciones} simulaciones y los resultados se han guardado.")

    def cerrar_programa(self):
        self.destroy()

if __name__ == "__main__":
    ventana = VentanaSimulacion()
    ventana.mainloop()
 