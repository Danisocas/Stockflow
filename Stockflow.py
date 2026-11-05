import threading
import time
from datos import STOCK_INICIAL, PEDIDOS, NUM_CAJAS, NUM_TERMINALES, REPOSICIONES

inventario = STOCK_INICIAL.copy()

lock_inventario = threading.Lock()
terminales = threading.Semaphore(NUM_TERMINALES)
condicion = threading.Condition(lock_inventario)

reposiciones_terminadas = False

ventas_por_caja = []

for i in range(NUM_CAJAS):
    ventas_por_caja.append([])


def obtener_producto(pedido):
    return pedido[1]


pedidos_ordenados = sorted(PEDIDOS, key=obtener_producto)


def trabajar_caja(numero_caja, pedidos_caja):

    for numero_pedido, producto, cantidad in pedidos_caja:

        # Comprobar y descontar el stock
        with condicion:
            while inventario[producto] < cantidad and not reposiciones_terminadas:
                print(f"Caja {numero_caja + 1}: esperando stock de {producto}")
                condicion.wait()

            if inventario[producto] >= cantidad:
                inventario[producto] -= cantidad
                venta_aceptada = True
            else:
                venta_aceptada = False

        if venta_aceptada:

            # Utilizar un terminal de cobro
            with terminales:
                print(f"Caja {numero_caja + 1}: obtiene terminal")

                time.sleep(0.2)

                print(f"Caja {numero_caja + 1}: libera terminal")

            ventas_por_caja[numero_caja].append((producto, cantidad))

            print(
                f"Caja {numero_caja + 1}: vende {numero_pedido} ({cantidad} de {producto})"
            )

        else:
            print(f"Caja {numero_caja + 1}: rechaza {numero_pedido} por falta de stock")



def trabajar_almacen():
    global reposiciones_terminadas

    for alb, producto, cantidad in REPOSICIONES:
        with condicion:
            inventario[producto] += cantidad
            condicion.notify_all()

        print(f"Almcen repone {cantidad} unidades de {producto}")

    with condicion:
        reposiciones_terminadas = True
        condicion.notify_all()

    print("Almacén: reposiciones terminadas")



# RESUMEN FINAL
def mostrar_resumen():

    print("\n--- RESUMEN FINAL ---")
    print()
    hay_errores = False

    for producto in STOCK_INICIAL:
        vendido = 0
        repuesto = 0

        for ventas_caja in ventas_por_caja:
            for producto_vendido, cantidad in ventas_caja:

                if producto_vendido == producto:
                    vendido += cantidad


        for alb, producto_repuesto, cantidad in REPOSICIONES:
            if producto_repuesto == producto:
                repuesto += cantidad
        
        stock_esperado = STOCK_INICIAL[producto] + repuesto - vendido
        stock_real = inventario[producto]

        print(f"{producto}: real={stock_real}, esperado={stock_esperado}")

        if stock_real != stock_esperado or stock_esperado < 0:
            hay_errores = True
            print("ERROR: el stock no es correcto")

    if not hay_errores:
        print("comprobación correcta: el stock coincide con las ventas")


hilos = []

for numero_caja in range(NUM_CAJAS):

    pedidos_caja = pedidos_ordenados[numero_caja::NUM_CAJAS]

    hilo = threading.Thread(target=trabajar_caja, args=(numero_caja, pedidos_caja))

    hilos.append(hilo)
    hilo.start()



# Crear e iniciar el hilo

hilo_almacen = threading.Thread(target=trabajar_almacen)
hilo_almacen.start()

for hilo in hilos:
    hilo.join()

hilo_almacen.join()


mostrar_resumen()
