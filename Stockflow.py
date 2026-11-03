import threading
import time
from datos import STOCK_INICIAL, PEDIDOS, NUM_CAJAS

inventario = STOCK_INICIAL.copy()
lock_inventario = threading.Lock()

ventas_por_caja = []

for i in range(NUM_CAJAS):
    ventas_por_caja.append([])


def obtener_producto(pedido):
    return pedido[1]


pedidos_ordenados = sorted(PEDIDOS, key=obtener_producto)


def trabajar_caja(numero_caja, pedidos_caja):

    for numero_pedido, producto, cantidad in pedidos_caja:

        with lock_inventario:

            stock_actual = inventario[producto]

            if stock_actual >= cantidad:
                inventario[producto] = stock_actual - cantidad
                venta_aceptada = True
            else:
                venta_aceptada = False

        if venta_aceptada:
            ventas_por_caja[numero_caja].append((producto, cantidad))

            print(
                f"Caja {numero_caja + 1}: vende {numero_pedido} ({cantidad} de {producto})"
            )
        else:
            print(f"Caja {numero_caja + 1}: rechaza {numero_pedido} por falta de stock")


# RESUMEN
def mostrar_resumen():

    print("\n--- RESUMEN FINAL ---")
    print()
    hay_errores = False
    for producto in STOCK_INICIAL:
        vendido = 0

        for ventas_caja in ventas_por_caja:
            for producto_vendido, cantidad in ventas_caja:

                if producto_vendido == producto:
                    vendido += cantidad

        stock_esperado = STOCK_INICIAL[producto] - vendido
        stock_real = inventario[producto]

        print(f"{producto}: real={stock_real}, esperado={stock_esperado}")

        if stock_real != stock_esperado or stock_esperado < 0:
            hay_errores = True
            print(" ERROR: condición de carrera")

    if not hay_errores:
        print("comprobacion correcta: el stock coincide con las ventas")


hilos = []

for numero_caja in range(NUM_CAJAS):
    pedidos_caja = pedidos_ordenados[numero_caja::NUM_CAJAS]

    hilo = threading.Thread(target=trabajar_caja, args=(numero_caja, pedidos_caja))

    hilos.append(hilo)
    hilo.start()


for hilo in hilos:
    hilo.join()

mostrar_resumen()
