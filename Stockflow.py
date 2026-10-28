# Fase 1 · Condición de carrera
# ● Crear el inventario a partir de STOCK_INICIAL.
# ● Crear NUM_CAJAS hilos que representen las cajas.
# ● Repartir y procesar los pedidos de PEDIDOS concurrentemente.
# ● Cada venta deberá comprobar si existe stock suficiente y, si existe, descontar las unidades.
# ● Provocar una situación en la que varias cajas compitan por las últimas unidades de un mismo
# producto.
# ● Ejecutar varias veces la aplicación y comprobar si aparecen resultados inconsistentes.
# ● Identificar la sección crítica y documentarla en el README.

import requests
import time
from threading import Thread

from datos import (STOCK_INICIAL, PEDIDOS, NUM_CAJAS)

stock = STOCK_INICIAL
pedidos = []

for     in PEDIDOS:
    if pedido[1] == 'Router WiFi':
            pedidos.append(pedido)

for pedido in PEDIDOS:
    if pedido[1] == 'Router WiFi':
            pedidos.append(pedido)



          
          
hilos = []

for numero in range(NUM_CAJAS):
      hilo = Thread(target=pedidos, args=(numero,))
      hilos.apend(hilo)
      hilo.start()


for hilo in hilo:
      hilo.join()


print(f'Inventario inicial: {STOCK_INICIAL} ')
print(f'Inventario final: {}')