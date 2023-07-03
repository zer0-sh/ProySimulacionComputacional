import simpy
import random
import numpy as np
import csv

tiempo_consignacion = np.maximum(np.random.exponential(scale=4), 1)
tiempo_consulta = np.maximum(np.random.exponential(scale=1), 1)
tiempo_retiro = np.maximum(np.random.exponential(scale=3), 1)

tiempo_max_espera_banco = 5
tiempo_simulacion = 60
media_llegada_clientes = 1
media_tiempo_servicio = {
    'consignacion': tiempo_consignacion,
    'consulta': tiempo_consulta,
    'retiro': tiempo_retiro
}
probabilidad_tarjeta = 0.3
tiempo_atencion_tarjeta = 2
tiempo_max_espera_tarjeta = 5
tiempo_transaccion_gerencia = 30
porcentaje_utilizacion_superior = 85
porcentaje_utilizacion_inferior = 60

class Banco(object):
    def __init__(self, env, num_cajeros, limite_cola):
        self.env = env
        self.cajeros = simpy.Resource(env, num_cajeros)
        self.cola = simpy.Store(env, capacity=limite_cola) ## SE LIMITA LA CAPACIDAD DE LA COLA A UN VALOR QUE SE INGRESA EN LA CREACIÓN DE LA INSTANCIA BANCO
        self.clientes_perdidos = 0
        self.num_clientes_atendidos = 0
        self.num_clientes_con_tarjeta = 0
        self.tiempo_atencion_total = 0

    def llegada_cliente(self):
        while True:
            tiempo_llegada = np.random.poisson(media_llegada_clientes)
            yield self.env.timeout(tiempo_llegada)
            tipo_transaccion = self.get_tipo_transaccion()
            tiempo_servicio = self.get_tiempo_servicio(tipo_transaccion)
            cliente = {
                'tipo_transaccion': tipo_transaccion,
                'tiempo_servicio': tiempo_servicio,
                'con_tarjeta': self.get_con_tarjeta()
            }
            self.env.process(self.proceso_cliente(cliente))

    def proceso_cliente(self, cliente):
        llegada_cliente = self.env.now
        try:
            yield self.cola.put(cliente)  # Intenta poner el cliente en la cola inmediatamente
        except simpy.Interrupt:  # Si no hay lugar en la cola, el cliente se va
            self.clientes_perdidos += 1
            return

        with self.cajeros.request() as request:
            yield request
            espera_banco = self.env.now - llegada_cliente
            if espera_banco > tiempo_max_espera_banco:
                self.clientes_perdidos += 1
                self.cola.get()  # El cliente se va sin ser atendido, se retira de la cola
                return
            espera = self.env.now - llegada_cliente
            if espera > tiempo_max_espera_tarjeta and cliente['con_tarjeta']:
                self.clientes_perdidos += 1
                self.cola.get()  # El cliente se va sin ser atendido, se retira de la cola
            else:
                yield self.env.timeout(cliente['tiempo_servicio'])
                self.num_clientes_atendidos += 1
                if cliente['con_tarjeta']:
                    self.num_clientes_con_tarjeta += 1
                self.tiempo_atencion_total += cliente['tiempo_servicio']
                self.cola.get()  # El cliente ha sido atendido, se retira de la cola

    def get_tipo_transaccion(self):
        prob = random.random()
        if prob < 0.4:
            return 'consignacion'
        elif prob < 0.5:
            return 'consulta'
        else:
            return 'retiro'

    def get_tiempo_servicio(self, tipo_transaccion):
        return random.expovariate(1 / media_tiempo_servicio[tipo_transaccion])

    def get_con_tarjeta(self):
        return random.random() < probabilidad_tarjeta

def guardar_resultados(num_cajeros, num_clientes, porcentaje_utilizacion, num_clientes_perdidos,
                       num_clientes_con_tarjeta, tiempo_atencion_total):
    with open('resultados.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([num_cajeros, num_clientes, porcentaje_utilizacion, num_clientes_perdidos,
                         num_clientes_con_tarjeta, tiempo_atencion_total])

def imprimir_resultados(num_cajeros, num_clientes, porcentaje_utilizacion, num_clientes_perdidos,
                        num_clientes_con_tarjeta, tiempo_atencion_total):
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
    print("----------------------------------------------------------------------------------")

def run_simulacion(num_cajeros, limite_cola):
    env = simpy.Environment()
    banco = Banco(env, num_cajeros, limite_cola)
    env.process(banco.llegada_cliente())
    env.run(until=tiempo_simulacion)

    porcentaje_utilizacion = (banco.tiempo_atencion_total / (num_cajeros * tiempo_simulacion)) * 100

    guardar_resultados(num_cajeros, banco.num_clientes_atendidos, porcentaje_utilizacion, banco.clientes_perdidos,
                       banco.num_clientes_con_tarjeta, banco.tiempo_atencion_total)

    imprimir_resultados(num_cajeros, banco.num_clientes_atendidos, porcentaje_utilizacion, banco.clientes_perdidos,
                        banco.num_clientes_con_tarjeta, banco.tiempo_atencion_total)

