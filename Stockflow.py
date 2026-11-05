
import threading
import time
from datos import STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_CAJAS, NUM_TERMINALES, NUM_REVISORES


# VARIABLES COMPARTIDAS

inventario = STOCK_INICIAL.copy()

lock_inventario = threading.Lock()
terminales = threading.Semaphore(NUM_TERMINALES)
condicion = threading.Condition(lock_inventario)
barrera = threading.Barrier(NUM_REVISORES)

reposiciones_terminadas = False

ventas_por_caja = []

for i in range(NUM_CAJAS):
    ventas_por_caja.append([])


# ORDENAR LOS PEDIDOS

def obtener_producto(pedido):
    return pedido[1]


pedidos_ordenados = sorted(PEDIDOS, key=obtener_producto)


# FUNCION DE LAS CAJAS

def trabajar_caja(numero_caja, pedidos_caja):

    for numero_pedido, producto, cantidad in pedidos_caja:

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

            with terminales:

                print(f"Caja {numero_caja + 1}: obtiene terminal")

                time.sleep(0.2)

                print(f"Caja {numero_caja + 1}: libera terminal")

            ventas_por_caja[numero_caja].append((producto, cantidad))

            print(
                f"Caja {numero_caja + 1}: vende pedido {numero_pedido} "
                f"({cantidad} de {producto})"
            )

        else:

            print(
                f"Caja {numero_caja + 1}: rechaza pedido {numero_pedido} "
                f"por falta de stock"
            )


# FUNCION DEL ALMACEN

def trabajar_almacen():

    global reposiciones_terminadas

    for albaran, producto, cantidad in REPOSICIONES:

        with condicion:

            inventario[producto] += cantidad

            condicion.notify_all()

        print(f"Almacén repone {cantidad} unidades de {producto}")

        time.sleep(0.1)

    with condicion:

        reposiciones_terminadas = True

        condicion.notify_all()

    print("Almacén: reposiciones terminadas")


# FEATURE 5 - REVISION DEL INVENTARIO

def revisar_inventario(numero_revisor, productos_revisor):

    print(f"Revisor {numero_revisor + 1}: comienza la revisión")

    for producto in productos_revisor:

        with lock_inventario:

            stock_actual = inventario[producto]

        if stock_actual < 0:

            print(
                f"Revisor {numero_revisor + 1}: ERROR en {producto}"
            )

        else:

            print(
                f"Revisor {numero_revisor + 1}: "
                f"{producto} tiene {stock_actual} unidades"
            )

    print(f"Revisor {numero_revisor + 1}: esperando a los demás")

    barrera.wait()

    print(f"Revisor {numero_revisor + 1}: revisión completada")


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

        for albaran, producto_repuesto, cantidad in REPOSICIONES:

            if producto_repuesto == producto:
                repuesto += cantidad

        stock_esperado = STOCK_INICIAL[producto] + repuesto - vendido

        stock_real = inventario[producto]

        print(f"{producto}: real={stock_real}, esperado={stock_esperado}")

        if stock_real != stock_esperado or stock_esperado < 0:

            hay_errores = True

            print("ERROR: el stock no es correcto")

    if not hay_errores:

        print("Comprobación correcta: el stock coincide con las ventas")


# INICIAR LAS CAJAS

hilos = []

for numero_caja in range(NUM_CAJAS):

    pedidos_caja = pedidos_ordenados[numero_caja::NUM_CAJAS]

    hilo = threading.Thread(
        target=trabajar_caja,
        args=(numero_caja, pedidos_caja)
    )

    hilos.append(hilo)
    hilo.start()


# INICIAR EL ALMACEN

hilo_almacen = threading.Thread(target=trabajar_almacen)

hilo_almacen.start()


# ESPERAR A QUE TERMINEN LAS CAJAS Y EL ALMACEN

for hilo in hilos:
    hilo.join()

hilo_almacen.join()


# FEATURE 5 - INICIAR LOS REVISORES

productos = list(STOCK_INICIAL.keys())

hilos_revisores = []

for numero_revisor in range(NUM_REVISORES):

    productos_revisor = productos[numero_revisor::NUM_REVISORES]

    hilo = threading.Thread(
        target=revisar_inventario,
        args=(numero_revisor, productos_revisor)
    )

    hilos_revisores.append(hilo)
    hilo.start()


for hilo in hilos_revisores:
    hilo.join()


# MOSTRAR EL RESUMEN FINAL

mostrar_resumen()
