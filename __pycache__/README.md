# PROYECTO FINAL SIMULACIÓN COMPUTACIONAL - UNIVERSIDAD DEL VALLE

Este repositorio contiene la implementación en Python de un programa para determinar el número de cajeros requeridos en un banco, considerando diferentes variantes. El objetivo principal es mantener una utilización de los cajeros entre el 85% y el 60%. Durante la implementación, se aplicaron los conceptos y técnicas vistos a lo largo de las clases de la asignatura de Simulación Computacional en la Universidad del Valle.

## Variantes

1. **Clientes que se van por encontrar una cola larga:** Si un cliente llega y encuentra una cola con más de 10 personas, decide irse sin ser atendido. El programa proporcionará el número de personas que no son atendidas debido a esta razón.

2. **Diferentes transacciones de los clientes:** Los clientes pueden realizar tres tipos de transacciones: consignaciones (40% de los clientes), consultas (10%) y retiros (50%). Cada tipo de transacción requiere un tiempo de atención diferente, que sigue una distribución exponencial con medias de 4, 1 y 3 minutos, respectivamente.

3. **Sistema con colas separadas por cada cajero:** En esta variante, se implementa un sistema con una cola de espera separada para cada cajero. Si un cajero se desocupa, ayuda a despachar a los demás cajeros.

4. **Transacciones enviadas por la gerencia:** Los cajeros también deben realizar transacciones enviadas por la gerencia. Estas transacciones llegan en un valor "X" de minutos, dicho valor estará entre 20 y 40 minutos y serán atendidas por el cajero que termine primero la atención con el cliente actual.

5. **Interrupción por transacciones de la gerencia:** Las transacciones enviadas por la gerencia interrumpen el trabajo de uno de los cajeros seleccionado al azar.

6. **Operaciones con tarjeta y cajeros especiales:** El 30% de los clientes realiza operaciones con tarjeta. El tiempo promedio de atención para estos clientes se reduce a 2 minutos. Sin embargo, estos clientes no están dispuestos a esperar más de 5 minutos. Se implementará una estrategia con uno o varios cajeros especialmente para este tipo de cliente.

## Ejecución del programa

1. Clona este repositorio en tu máquina local.

2. Asegúrate de tener Python instalado en tu sistema.

3. Abre una terminal y navega hasta el directorio donde clonaste el repositorio.

4. Ejecuta el programa principal `main.py` usando el siguiente comando:

   ```bash
   python main.py

5. En la ventana ingresa a "Iniciar Simulación"

6. Ingresa el número de cajeros, y presiona "Iniciar simulación"

7. En la parte derecha se visualizan algunos datos. En la última linea se evidencia si cumple o no con la tasa de utilización propuesta en el enunciado del proyecto.
