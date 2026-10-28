"""
datos.py
========

Archivo de datos común para toda la clase.

IMPORTANTE:
- No contiene la lógica de sincronización.
- No debe utilizar Lock, Semaphore, Condition, Barrier ni RLock.
- Su finalidad es proporcionar un conjunto de datos suficientemente amplio
  para que todos los alumnos trabajen sobre el mismo escenario.

Cada alumno deberá importar estos datos desde su programa.
"""

# -------------------------------------------------------------------
# STOCK INICIAL
# -------------------------------------------------------------------
# Diccionario con las unidades disponibles de cada producto al comenzar.
# Clave   -> nombre del producto.
# Valor   -> número de unidades disponibles.

STOCK_INICIAL = {
    "Teclado mecanico": 18,
    "Teclado inalambrico": 12,
    "Raton gaming": 20,
    "Raton oficina": 25,
    "Monitor 24 pulgadas": 10,
    "Monitor 27 pulgadas": 8,
    "Auriculares USB": 16,
    "Auriculares Bluetooth": 14,
    "Webcam Full HD": 11,
    "Microfono USB": 9,
    "SSD 500 GB": 15,
    "SSD 1 TB": 12,
    "Memoria USB 64 GB": 30,
    "Disco externo 2 TB": 7,
    "Hub USB-C": 13,
    "Cable HDMI": 35,
    "Cable USB-C": 40,
    "Cargador USB-C 65W": 18,
    "Base refrigeradora": 10,
    "Soporte monitor": 9,
    "Router WiFi": 6,
    "Switch 8 puertos": 8,
    "Adaptador USB Ethernet": 12,
    "Impresora laser": 5,
    "Toner negro": 10,
}

# -------------------------------------------------------------------
# PEDIDOS
# -------------------------------------------------------------------
# Lista de pedidos que deberán ser procesados por las cajas.
#
# Cada pedido es una tupla:
# (numero_pedido, producto, unidades)
#
# Hay varios pedidos sobre los mismos productos para provocar accesos
# concurrentes al inventario compartido.

PEDIDOS = [
    ("PED-001", "Teclado mecanico", 4),
    ("PED-002", "Raton gaming", 5),
    ("PED-003", "Monitor 24 pulgadas", 3),
    ("PED-004", "SSD 1 TB", 4),
    ("PED-005", "Cable HDMI", 8),
    ("PED-006", "Auriculares USB", 5),
    ("PED-007", "Teclado mecanico", 6),
    ("PED-008", "Monitor 27 pulgadas", 3),
    ("PED-009", "SSD 500 GB", 5),
    ("PED-010", "Raton oficina", 8),
    ("PED-011", "Webcam Full HD", 4),
    ("PED-012", "Cable USB-C", 10),
    ("PED-013", "Hub USB-C", 5),
    ("PED-014", "Monitor 24 pulgadas", 4),
    ("PED-015", "Auriculares Bluetooth", 6),
    ("PED-016", "Disco externo 2 TB", 3),
    ("PED-017", "Memoria USB 64 GB", 12),
    ("PED-018", "Teclado inalambrico", 5),
    ("PED-019", "Raton gaming", 7),
    ("PED-020", "Cargador USB-C 65W", 6),
    ("PED-021", "SSD 1 TB", 5),
    ("PED-022", "Base refrigeradora", 4),
    ("PED-023", "Monitor 27 pulgadas", 4),
    ("PED-024", "Switch 8 puertos", 4),
    ("PED-025", "Router WiFi", 3),
    ("PED-026", "Toner negro", 4),
    ("PED-027", "Impresora laser", 2),
    ("PED-028", "Adaptador USB Ethernet", 5),
    ("PED-029", "Cable HDMI", 12),
    ("PED-030", "Auriculares USB", 7),
    ("PED-031", "Webcam Full HD", 5),
    ("PED-032", "SSD 500 GB", 7),
    ("PED-033", "Microfono USB", 4),
    ("PED-034", "Soporte monitor", 4),
    ("PED-035", "Cable USB-C", 15),
    ("PED-036", "Teclado mecanico", 7),
    ("PED-037", "Raton oficina", 10),
    ("PED-038", "Hub USB-C", 6),
    ("PED-039", "Disco externo 2 TB", 4),
    ("PED-040", "Router WiFi", 4),
]

# -------------------------------------------------------------------
# REPOSICIONES
# -------------------------------------------------------------------
# Entradas de mercancía previstas durante la ejecución.
#
# Cada reposición es una tupla:
# (numero_albaran, producto, unidades)
#
# Un albarán identifica una entrada concreta de mercancía al almacén.

REPOSICIONES = [
    ("ALB-001", "Monitor 24 pulgadas", 8),
    ("ALB-002", "Monitor 27 pulgadas", 6),
    ("ALB-003", "SSD 1 TB", 10),
    ("ALB-004", "Disco externo 2 TB", 6),
    ("ALB-005", "Router WiFi", 5),
    ("ALB-006", "Impresora laser", 4),
    ("ALB-007", "Auriculares USB", 10),
    ("ALB-008", "Webcam Full HD", 8),
    ("ALB-009", "Raton gaming", 10),
    ("ALB-010", "Teclado mecanico", 12),
    ("ALB-011", "Microfono USB", 6),
    ("ALB-012", "Toner negro", 8),
]

# -------------------------------------------------------------------
# CONFIGURACIÓN DEL SISTEMA
# -------------------------------------------------------------------

# Número máximo de terminales de cobro que pueden utilizarse
# simultáneamente. Deberá utilizarse en la fase de Semaphore.
NUM_TERMINALES = 3

# Número de trabajadores que participarán en la revisión final.
# Deberá utilizarse en la fase de Barrier.
NUM_REVISORES = 4

# Número de cajas que procesarán pedidos concurrentemente.
NUM_CAJAS = 6
