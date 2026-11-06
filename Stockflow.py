import threading
import time
from datos import STOCK_INICIAL, PEDIDOS, REPOSICIONES, NUM_CAJAS, NUM_TERMINALES, NUM_REVISORES

class GestorInventario:

    def __init__(self):
        self.stock = STOCK_INICIAL.copy()
        self.cerrojo = threading.RLock()
        self.condicion = threading.Condition(self.cerrojo)
        self.reposiciones_terminadas = False

    def consultar_stock(self, producto):
        with self.cerrojo:
            return self.stock[producto]

    def vender(self, producto, cantidad):

        with self.condicion:

            while (self.consultar_stock(producto) < cantidad and not self.reposiciones_terminadas):
                print(f"Esperando stock de {producto}")
                self.condicion.wait()

            if self.consultar_stock(producto) >= cantidad:
                self.stock[producto] -= cantidad
                return True
            else:
                return False

    def reponer(self, producto, cantidad):

        with self.condicion:
            self.stock[producto] += cantidad
            self.condicion.notify_all()

    def terminar_reposiciones(self):

        with self.condicion:
            self.reposiciones_terminadas = True
            self.condicion.notify_all()



gestor = GestorInventario()

terminales = threading.Semaphore(NUM_TERMINALES)
barrera = threading.Barrier(NUM_REVISORES)

ventas_por_caja = []

for i in range(NUM_CAJAS):
    ventas_por_caja.append([])


def obtener_producto(pedido):
    return pedido[1]


pedidos_ordenados = sorted(PEDIDOS, key=obtener_producto)


# CAJAS
def trabajar_caja(numero_caja, pedidos_caja):

    for numero_pedido, producto, cantidad in pedidos_caja:

        venta_aceptada = gestor.vender(producto, cantidad)

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
                f"Caja {numero_caja + 1}: rechaza pedido "
                f"{numero_pedido} por falta de stock"
            )

# ALMACEN

def trabajar_almacen():

    for albaran, producto, cantidad in REPOSICIONES:

        gestor.reponer(producto, cantidad)

        print(f"Almacén repone {cantidad} unidades de {producto}")

        time.sleep(0.1)

    gestor.terminar_reposiciones()

    print("Almacén: reposiciones terminadas")



def revisar_inventario(numero_revisor, productos_revisor):

    print(f"Revisor {numero_revisor + 1}: comienza la revisión")

    for producto in productos_revisor:

        stock_actual = gestor.consultar_stock(producto)

        if stock_actual < 0:
            print(f"Revisor {numero_revisor + 1}: ERROR en {producto}")

        else:
            print(
                f"Revisor {numero_revisor + 1}: "
                f"{producto} tiene {stock_actual} unidades"
            )

    print(f"Revisor {numero_revisor + 1}: esperando a los demás")

    barrera.wait()

    print(f"Revisor {numero_revisor + 1}: revisión completada")


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

        stock_real = gestor.consultar_stock(producto)

        print(f"{producto}: real={stock_real}, esperado={stock_esperado}")

        if stock_real != stock_esperado or stock_esperado < 0:
            hay_errores = True
            print("ERROR: el stock no es correcto")

    if not hay_errores:
        print()
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


# Iniciar el amacen
hilo_almacen = threading.Thread(target=trabajar_almacen)
hilo_almacen.start()



for hilo in hilos:
    hilo.join()

hilo_almacen.join()


# iniciar los cuatro revisores

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


# ESPERAR A LOS REVISORES
for hilo in hilos_revisores:
    hilo.join()


# ver los resultados
mostrar_resumen()