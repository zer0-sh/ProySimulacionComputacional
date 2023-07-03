import simpy
import random
import numpy as np

### GENERACION DEL TIEMPO DE SERVICIO ALEATORIAMENTE

tiempo_consignacion = np.maximum(np.random.exponential(scale=4), 1)
tiempo_consulta = np.maximum(np.random.exponential(scale=1), 1)
tiempo_retiro = np.maximum(np.random.exponential(scale=3), 1)

# Variables globales
tiempo_max_espera_banco = 5  # Tiempo máximo de espera en el banco (minutos)

tiempo_simulacion = 60  # Tiempo de simulación en minutos
media_llegada_clientes = 1  # Media de llegada de clientes (clientes por minuto)
media_tiempo_servicio = {
    'consignacion': tiempo_consignacion,  # Media de tiempo de servicio para consignaciones (con media de 4 minutos)
    'consulta': tiempo_consulta,  # Media de tiempo de servicio para consultas (con media de 1 minutos)
    'retiro': tiempo_retiro  # Media de tiempo de servicio para retiros (con media de 3 minutos)
}
probabilidad_tarjeta = 0.3  # Probabilidad de que un cliente realice una operación con tarjeta
tiempo_atencion_tarjeta = 2  # Tiempo de atención promedio para clientes con tarjeta (minutos)
tiempo_max_espera_tarjeta = 5  # Tiempo máximo de espera para clientes con tarjeta (minutos)
tiempo_transaccion_gerencia = 30  # Tiempo entre transacciones de gerencia (minutos)
porcentaje_utilizacion_superior = 85 # Valor porcentaje de utilizacion superior
porcentaje_utilizacion_inferior = 60 # Valor porcentaje de utilizacion inferior

class Banco(object):
    def __init__(self, env, num_cajeros):
        self.env = env
        self.cajeros = simpy.Resource(env, num_cajeros)  # Recurso compartido para representar los cajeros automáticos
        self.cola = simpy.Store(env)  # Almacén utilizado para manejar la cola de clientes
        self.clientes_perdidos = 0  # Número de clientes que abandonaron el banco debido a la espera excesiva
        self.num_clientes_atendidos = 0  # Número de clientes que fueron atendidos correctamente
        self.num_clientes_con_tarjeta = 0  # Número de clientes que realizaron una operación con tarjeta
        self.tiempo_atencion_total = 0  # Tiempo total utilizado para atender a los clientes

    def llegada_cliente(self):
        while True:
            tiempo_llegada = np.random.poisson(media_llegada_clientes)  # Genera el tiempo entre llegadas de clientes con distribución de Poisson
            yield self.env.timeout(tiempo_llegada)
            tipo_transaccion = self.get_tipo_transaccion()  # Obtiene el tipo de transacción aleatoriamente
            tiempo_servicio = self.get_tiempo_servicio(tipo_transaccion)  # Obtiene el tiempo de servicio para el tipo de transacción
            cliente = {
                'tipo_transaccion': tipo_transaccion,
                'tiempo_servicio': tiempo_servicio,
                'con_tarjeta': self.get_con_tarjeta()
            }
            self.env.process(self.proceso_cliente(cliente))  # Inicia el proceso del cliente

    def proceso_cliente(self, cliente):
        llegada_cliente = self.env.now
        with self.cajeros.request() as request:
            yield request
            espera_banco = self.env.now - llegada_cliente
            if espera_banco > tiempo_max_espera_banco:
                self.clientes_perdidos += 1  # Registra un cliente perdido si la espera en el banco excede el límite
                return  # El cliente se va sin ser atendido
            espera = self.env.now - llegada_cliente
            if espera > tiempo_max_espera_tarjeta and cliente['con_tarjeta']:
                self.clientes_perdidos += 1  # Registra un cliente perdido si la espera en el cajero excede el límite para clientes con tarjeta
            else:
                yield self.env.timeout(cliente['tiempo_servicio'])  # Simula el tiempo de atención al cliente
                self.num_clientes_atendidos += 1  # Incrementa el contador de clientes atendidos
                if cliente['con_tarjeta']:
                    self.num_clientes_con_tarjeta += 1  # Incrementa el contador de clientes con tarjeta
                self.tiempo_atencion_total += cliente['tiempo_servicio']  # Actualiza el tiempo total de atención

    def get_tipo_transaccion(self):
        prob = random.random()
        if prob < 0.4:
            return 'consignacion'  # Retorna 'consignacion' con una probabilidad del 40%
        elif prob < 0.5:
            return 'consulta'  # Retorna 'consulta' con una probabilidad del 10%
        else:
            return 'retiro'  # Retorna 'retiro' con una probabilidad del 50%

    def get_tiempo_servicio(self, tipo_transaccion):
        return random.expovariate(1 / media_tiempo_servicio[tipo_transaccion])  # Genera el tiempo de servicio basado en la media correspondiente

    def get_con_tarjeta(self):
        return random.random() < probabilidad_tarjeta  # Retorna True si el número aleatorio generado es menor a la probabilidad de tener tarjeta

def imprimir_resultados(num_cajeros, num_clientes, porcentaje_utilizacion, num_clientes_perdidos, num_clientes_con_tarjeta, tiempo_atencion_total):
    print("Resultados de la simulación:")
    print(f"Número de cajeros: {num_cajeros}")
    print(f"Número de clientes atendidos: {num_clientes}")
    print(f"Porcentaje de utilización del banco: {format(porcentaje_utilizacion, '.5f')}%")
    print(f"Número de clientes perdidos: {num_clientes_perdidos}")
    print(f"Número de clientes con tarjeta: {num_clientes_con_tarjeta}")
    print(f"Tiempo de atención total: {format(tiempo_atencion_total, '.0f')} minutos")

    if porcentaje_utilizacion_inferior <= porcentaje_utilizacion <= porcentaje_utilizacion_superior:
        print("Cumple con la tasa de utilización")
    else:
        print("No cumple con la tasa de utilización")

def run_simulacion(num_cajeros):
    env = simpy.Environment()  # Crea el entorno de simulación
    banco = Banco(env, num_cajeros)  # Crea una instancia del banco
    env.process(banco.llegada_cliente())  # Inicia el proceso de llegada de clientes
    env.run(until=tiempo_simulacion)  # Ejecuta la simulación hasta el tiempo especificado

    # Cálculo del porcentaje de utilización del banco
    porcentaje_utilizacion = (banco.tiempo_atencion_total / (num_cajeros * tiempo_simulacion)) * 100

    # Imprimir resultados
    imprimir_resultados(num_cajeros, banco.num_clientes_atendidos, porcentaje_utilizacion, banco.clientes_perdidos,
                        banco.num_clientes_con_tarjeta, banco.tiempo_atencion_total)

# Ejecutar simulación con 1 cajero
run_simulacion(1)
