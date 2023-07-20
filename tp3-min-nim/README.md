<!-- omit in toc -->
# Teoría de Juegos - TP3 - Min Nim

Este programa implementa el juego **Min Nim** para los jugadores L y R. Hay 3
pilas, de n1, n2 y n3 objetos, respectivamente. Cada jugador en su turno debe
quitar r1, r2 o r3 objetos de una misma pila (que puede ser cualquiera).
Comienza el jugador L. Gana el que juega último.

Para ejecutar el programa,

```bash
python3 minnim.py {calc|play} {n1} {n2} {n3} {r1} {r2} {r3}
```

Tiene dos modos: `calc` (calcular conjuntos de P-posiciones y N-posiciones)
y `play` (jugar contra la computadora)

- [Calculate (`calc`)](#calculate-calc)
- [Play (`play`)](#play-play)
- [Índice del código](#índice-del-código)

## Calculate (`calc`)

Calcula los conjuntos de P-posiciones y N-posiciones. Imprime el árbol de juego
en forma tabulada junto con el análisis.

> Para detalles de la implementación consultar el [informe](informe.pdf).

Ejemplo de uso:

```bash
$ python3 minnim.py calc 0 0 3 1 2 3
[0, 0, 3]
  ┌─ take 1 from #2 (3)
  │  [0, 0, 2]
  │    ┌─ take 1 from #2 (2)
  │    │  [0, 0, 1]
  │    │    ┌─ take 1 from #2 (1)
  │    │    │  [0, 0, 0]
  │    │    │  next player outcomes: [] -> this game outcome: P, val 0.00
  │    │    └─> next player outcome P
  │    │  next player outcomes: [P] -> this game outcome: N, val 1.00
  │    └─> next player outcome N
  │    ┌─ take 2 from #2 (2)
  │    │  outcome memoized for [0, 0, 0]: P
  │    └─> next player outcome P
  │  next player outcomes: [N, P] -> this game outcome: N, val 0.50
  └─> next player outcome N
  ┌─ take 2 from #2 (3)
  │  outcome memoized for [0, 0, 1]: N
  └─> next player outcome N
  ┌─ take 3 from #2 (3)
  │  outcome memoized for [0, 0, 0]: P
  └─> next player outcome P
next player outcomes: [N, N, P] -> this game outcome: N, val 0.33
Calculando P y N posiciones
P-posiciones:
[[0, 0, 0]]

N-posiciones:
[[0, 0, 1], [0, 0, 2], [0, 0, 3]]
```

Se imprime para cada posición todos los movimientos legales y para cada uno el
juego resultante y su correspondiente análisis recursivo. Al final de cada
movimiento imprime la *outcome class* del juego resultante. Por ejemplo,

```text
[0, 0, 3]
  ┌─ take 1 from #2 (3)
  │  [0, 0, 2]
  │  ... análisis recursivo ...
  └─> next player outcome N
```

La *outcome class* de una posición se calcula a partir las *outcome classes* de
los juegos resultantes para cada movimiento.

```text
[0, 0, 3]
  ┌─ take 1 from #2 (3)
  │  ...
  └─> next player outcome N
  ┌─ take 2 from #2 (3)
  │  ...
  └─> next player outcome N
  ┌─ take 3 from #2 (3)
  │  ...
  └─> next player outcome P
next player outcomes: [N, N, P] -> this game outcome: N, val 0.33
```

Además se calcula el *valor* (usado por el jugador óptimo, ver [play](#play)).

Como hacemos programación dinámica y guardamos el *outcome class* de cada juego,
cuando nos encontramos con uno que ya tenemos calculado lo notificamos.

```text
[0, 0, 3]
  ...
  ┌─ take 3 from #2 (3)
  │  outcome memoized for [0, 0, 0]: P
  └─> next player outcome P
```

## Play (`play`)

Juega contra la computadora (como L). El IA implementado conoce los conjuntos de
P-posiciones y N-posiciones y funciona de la siguiente manera:

- Si se encuentra en una posición ganadora, juega el movimiento ganador
- Si se encuentra en una posición perdedora, juega el movimiento que *dificulta*
  la decisión al jugador R (humano) lo máximo posible.

  Para encontrarlo, ve a que posición lo lleva cada movimiento legal y se queda
  con el que lleve a la posición que tenga el **mínimo valor**.

  Definimos el valor como la proporción de jugadas ganadoras. De esa forma, lo
  que hace es hacer la jugada que hace que el humano tenga la menor cantidad de
  jugadas ganadoras posibles.

> Para más detalles consultar el [informe](informe.pdf).

Por lo tanto, solo tiene sentido jugar con la computadora partiendo desde una
posición perdedora (P). Dos ejemplos son `play 2 3 5 1 2 3` (n1, n2, n3, r1, r2,
r3) y `play 11 15 20 3 5 9` (en este es todo un desafío ganarle).

Se juega por turnos, y el programa le pide al usuario que vaya ingresando sus
movimientos de a dos partes, primero que elija la pila y luego cuanto va a
tomar.

Ejemplo de juego:

```bash
$ python3 minnim.py play 2 3 5 1 2 3
Turno de L (Computadora)
Calculando mejor movimiento para
[2, 3, 5]
Opciones:
heap #1 take 1 -> [1, 3, 5] (0.29)
heap #1 take 2 -> [0, 3, 5] (0.33)
heap #2 take 1 -> [2, 2, 5] (0.14)
heap #2 take 2 -> [2, 1, 5] (0.33)
heap #2 take 3 -> [2, 0, 5] (0.40)
heap #3 take 1 -> [2, 3, 4] (0.25)
heap #3 take 2 -> [2, 3, 3] (0.38)
heap #3 take 3 -> [2, 3, 2] (0.43)
Movimiento elegido heap #2 take 1
--------------------
Turno de R (Humano)
Estado del juego: [2, 2, 5]
pila # ([1, 2, 3]): 3  
tomar ([1, 2, 3]): 1
Movimiento elegido heap #3 take 1
--------------------
Turno de L (Computadora)
Calculando mejor movimiento para
[2, 2, 4]
Opciones:
heap #1 take 1 -> [1, 2, 4] (0.33)
heap #1 take 2 -> [0, 2, 4] (0.40)
heap #2 take 1 -> [2, 1, 4] (0.33)
heap #2 take 2 -> [2, 0, 4] (0.40)
heap #3 take 1 -> [2, 2, 3] (0.43)
heap #3 take 2 -> [2, 2, 2] (0.50)
heap #3 take 3 -> [2, 2, 1] (0.20)
Movimiento elegido heap #3 take 3
--------------------
Turno de R (Humano)
Estado del juego: [2, 2, 1]
pila # ([1, 2, 3]): 3
tomar ([1, 2, 3]): 1
Movimiento elegido heap #3 take 1
--------------------
Turno de L (Computadora)
Calculando mejor movimiento para
[2, 2, 0]
Opciones:
heap #1 take 1 -> [1, 2, 0] (0.33)
heap #1 take 2 -> [0, 2, 0] (0.50)
heap #2 take 1 -> [2, 1, 0] (0.33)
heap #2 take 2 -> [2, 0, 0] (0.50)
Movimiento elegido heap #1 take 1
--------------------
Turno de R (Humano)
Estado del juego: [1, 2, 0]
pila # ([1, 2, 3]): 2
tomar ([1, 2, 3]): 1
Movimiento elegido heap #2 take 1
--------------------
Turno de L (Computadora)
Calculando mejor movimiento para
[1, 1, 0]
Opciones:
heap #1 take 1 -> [0, 1, 0] (1.00)
heap #2 take 1 -> [1, 0, 0] (1.00)
Movimiento elegido heap #1 take 1
--------------------
Turno de R (Humano)
Estado del juego: [0, 1, 0]
pila # ([1, 2, 3]): 2
tomar ([1, 2, 3]): 1
Movimiento elegido heap #2 take 1
--------------------
Gana R (Humano)!
```

El jugador computadora imprime en su turno su análisis: cada movimiento posible,
su juego resultante y su valor. Esto permite saber si su posición y
cada posición resultante (en particular la que le quedó al humano) son N o P

- Si alguna posición resultante tiene valor 0 entonces es P. Y el bot, al elegir
  el mínimo, lo va a elegir. Por lo que vamos a encontrarnos en una posición P
  (y perdimos).
- El resto de las posiciones resultantes son N.
- Si todas las posiciones resultantes son N, entonces la posición del bot es P,
  y por lo tanto a nosotros nos garantiza una posición N. ¡Venimos bien! Pero
  todavía nos podemos equivocar.

Por ejemplo, en

```text
Turno de L (Computadora)
Calculando mejor movimiento para
[2, 2, 4]
Opciones:
heap #1 take 1 -> [1, 2, 4] (0.33)
heap #1 take 2 -> [0, 2, 4] (0.40)
heap #2 take 1 -> [2, 1, 4] (0.33)
heap #2 take 2 -> [2, 0, 4] (0.40)
heap #3 take 1 -> [2, 2, 3] (0.43)
heap #3 take 2 -> [2, 2, 2] (0.50)
heap #3 take 3 -> [2, 2, 1] (0.20)
Movimiento elegido heap #3 take 3
```

Como todas las posiciones tienen valores diferentes de 0, sabemos que son N y
por lo tanto `[2, 2, 4]` es P. Por lo que le seguimos ganando al bot.

Si en cambio hubiéramos elegido una jugada perdedora,

```text
Turno de R (Humano)
Estado del juego: [2, 2, 5]
pila # ([1, 2, 3]): 1
tomar ([1, 2, 3]): 2
Movimiento elegido heap #1 take 2
--------------------
Turno de L (Computadora)
Calculando mejor movimiento para
[0, 2, 5]
Opciones:
heap #2 take 1 -> [0, 1, 5] (0.00)
heap #2 take 2 -> [0, 0, 5] (0.33)
heap #3 take 1 -> [0, 2, 4] (0.40)
heap #3 take 2 -> [0, 2, 3] (0.20)
heap #3 take 3 -> [0, 2, 2] (0.00)
Movimiento elegido heap #2 take 1
```

se puede ver que para `[0, 2, 5]` hay varios movimientos que llevan a posiciones
con valor 0 (que son P), por lo que es N, y esencialmente ya perdimos.

## Índice del código

- `Game` es la clase que representa un juego y permite realizar movimientos
- `Simulator` simula todos los juegos posibles, generando el
  *game tree*. Permite calcular las P posiciones y N posiciones.
- `Player` es una clase abstracta para jugadores, usada por
  `play_interactive_game`. Implementa dos sub-jugadores:
  - `HumanPlayer` es un jugador humano, que pide movimientos interactivamente
  - `OptimalComputerPlayer` es el jugador que implementa la función que juega de
    forma óptima y cuando está en una posición perdedora dificulta la elección
    del otro jugador.

    Para obtener los valores de las posiciones aprovecha que son pre-calculados
    por el `Simulator`.