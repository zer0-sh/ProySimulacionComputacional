import tkinter as tk
from tkinter import messagebox
import subprocess


def iniciar_simulacion():
    subprocess.Popen(["python", "ventana_simulacion.py"])
    # messagebox.showinfo("Todo bien","Ejecutando simulación...")
    ventana.destroy()


def mostrar_enunciado():
    enunciado = """Determinar el número de cajeros que requiere un banco teniendo como objetivo mantener una utilización entre 85 y 60%.
Los clientes llegan de acuerdo con una distribución Poisson con media de 1 cliente por minuto. Hay una sola línea de espera. El tiempo de servicio sigue una distribución exponencial con media de 3 minutos.

Variantes:
1. Un cliente que llega y encuentra una cola con más de 10 personas se va. Se quiere saber también el número de personas que no se atiende por esta razón, serían clientes perdidos por no haber sido atendidos.
2. Hay diferentes transacciones que pueden realizar los clientes: consignaciones (el 40% de los clientes), consultas (10%) y retiros (50%), que requieren diferentes tiempos de atención (exponencial con media 4, 1 y 3 minutos respectivamente).
3. Compara con un sistema donde hay una cola de espera separada por cada cajero. Sin embargo, si se desocupa un cajero, ayuda a despachar a los demás.
4. Los cajeros deben realizar además transacciones enviadas por la gerencia. Estas transacciones llegan cada 30 minutos y están atendidas por el cajero que termina primero la atención con el cliente actual.
5. Las transacciones de la gerencia interrumpen el trabajo de uno de los cajeros (seleccionado al azar).
6. El 30% de los clientes realiza las operaciones con tarjeta. El tiempo promedio de atención de ellos se reduce a 2 minutos, sin embargo, estos clientes no están dispuestos a esperar más de 5 minutos. Ensayar una estrategia con uno o varios cajeros especialmente para este tipo de cliente."""

    messagebox.showinfo("Enunciado del Proyecto", enunciado)


def acerca_de():
    info = "Proyecto realizado por:\n\n- Steven Muñoz \n- Estefany Castro \n- Valentina Hurtado \n- Camilo Azcarate \n\n Universidad del Valle \n Simulación Computacional \n 2023-1"
    messagebox.showinfo("Acerca de", info)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Proyecto Simulación Computacional")
ventana.geometry("500x500")
ventana.configure(bg="#403e4d")

# Fuente para los botones
fuente = ("Times New Roman", 18, "bold")

# Frame para contener los botones y centrarlos
frame_botones = tk.Frame(ventana, bg="#403e4d")
frame_botones.pack(expand=True)

# Función para abrir una nueva ventana de simulación
boton_simulacion = tk.Button(frame_botones, text="Iniciar Simulación",
                             font=fuente, bg="#e8e8e8", command=iniciar_simulacion)
boton_simulacion.pack(pady=10)

# Función para mostrar el enunciado del proyecto
boton_enunciado = tk.Button(frame_botones, text="Mostrar Enunciado",
                            font=fuente, bg="#e8e8e8", command=mostrar_enunciado)
boton_enunciado.pack(pady=10)

# Función para mostrar información sobre el proyecto
boton_acerca_de = tk.Button(
    frame_botones, text="Acerca de", font=fuente, bg="#e8e8e8", command=acerca_de)
boton_acerca_de.pack(pady=10)

# Centrar el frame de los botones en la ventana
frame_botones.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Ejecutar la aplicación
ventana.mainloop()
