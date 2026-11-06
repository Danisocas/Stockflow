# StockFlow

## 1. ¿De qué trata la práctica?

En esta práctica he hecho un programa en Python que simula una tienda. Hay varias cajas vendiendo productos al mismo tiempo y un almacén que va reponiendo el stock

El programa trabaja con 6 cajas, 3 terminales de cobro, 4 revisores, 25 productos, 40 pedidos y 12 reposiciones

## 2. Archivos del proyecto

- `datos.py`: tiene el stock inicial, los pedidos, las reposiciones y los números de cajas, terminales y revisores. No lo he modificado
- `Stockflow.py`: es el programa principal, con los hilos y los mecanismos de sincronización

## 3. ¿Cómo se ejecuta?

Abro la terminal en la carpeta del proyecto y ejecuto:

`python3 Stockflow.py`


## 4. Condición de carrera (Feature 1)

Al principio no utilizábamos ningún `Lock`. Como varias cajas trabajan a la vez, dos de ellas podían consultar el mismo stock antes de que ninguna lo descontara.


## 5. Mecanismos de sincronización utilizados

### Lock (Feature 2)

Sirve para que solo una caja pueda comprobar y modificar el inventario a la vez. Así otra caja no puede cambiar el stock mientras se está realizando una venta  

### Semaphore (Feature 3)

Hay 6 cajas, pero solo 3 terminales de cobro. Con `Semaphore(NUM_TERMINALES)` hacemos que como máximo 3 cajas utilicen un terminal al mismo tiempo. Las demás tienen que esperar a que quede uno libre.

### Condition (Feature 4)

Si una caja quiere vender un producto y no hay suficiente stock, utiliza `wait()` para esperar sin estar comprobando continuamente el inventario

Cuando el almacén repone, utiliza `notify_all()` para avisar a las cajas. Luego, cada caja vuelve a comprobar el stock con un `while`, porque puede que todavía no haya suficiente

### Barrier (Feature 5)

Se crean 4 revisores y se reparten los 25 productos. Cada uno comprueba su parte y llega a `barrera.wait()`


### RLock (Feature 6)

He creado la clase `GestorInventario`, que se encarga de consultar, vender y reponer los productos

Utilizo `RLock` porque el método `vender()` llama a `consultar_stock()`, y los dos necesitan el mismo cerrojo. `RLock` permite que un hilo vuelva a adquirir un bloqueo que ya tiene


## 6. Cómo evitamos los deadlocks

Un deadlock ocurre cuando unos hilos se quedan esperando recursos que no se liberan y ninguno puede continuar

Un posible problema sería que una caja mantuviera bloqueado el inventario mientras espera un terminal y otro hilo necesitara ese bloqueo para poder liberar un recurso que la caja está esperando

En nuestro código lo evitamos de esta manera:

- Primero se comprueba y descuenta el stock dentro de `gestor.vender()`, y al terminar se libera el `RLock`.
- Después, y ya sin tener bloqueado el inventario, la caja utiliza el terminal con `Semaphore`.
- El `time.sleep(0.2)` del cobro no se hace mientras está bloqueado el inventario.
- Cuando una caja hace `Condition.wait()`, libera temporalmente el cerrojo para que el almacén pueda reponer.
- El almacén no necesita utilizar los terminales de cobro.
- Los revisores empiezan después de terminar las cajas y el almacén, y los cuatro llegan a la barrera.

## 7. Pruebas y resultados

### Pruebas que he comprobado

- He ejecutado la versión final de `Stockflow.py` y ha terminado correctamente
- En la ejecución aparecen las ventas de las cajas y las reposiciones del almacén
- Se muestran las cajas obteniendo y liberando los terminales
- Aparecen los 4 revisores, que esperan en la barrera antes de completar la revisión
- Al final aparece el mensaje `Comprobación correcta: el stock coincide con las ventas`


## 8. Git y ramas

- `main`: versión completa de la develop
- `develop`: donde se juntan las features terminadas
- `feature/race-condition`: condición de carrera
- `feature/lock-inventario`: protección con Lock
- `feature/semaphore-terminales`: terminales de cobro
- `feature/condition-reposicion`: reposiciones y espera
- `feature/barrier-inventario`: revisión de stock
- `feature/rlock-gestor`: clase GestorInventario
- `feature/documentacion`: prevención de deadlocks y README