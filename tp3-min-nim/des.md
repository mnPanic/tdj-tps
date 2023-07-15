Pregunta Lucas y aclaración Cami

Lucas: Buenas, nose si alguno ya arranco con el TP de Min-nim, pero que
entendieron por r1,r2,r3. que podes quitar ese numero en su respectiva fila, o
que el jugador puede decidir quitar alguna de esas cantidades de cualquier fila?

Cami: Ahora ya no me acuerdo que decía pero creo que yo había entendido que vos
de la fila que elijas podes sacar o r1 o r2 o r3 (así como en el nim que
habíamos visto podías sacar 1, 2, 3,.... o cuántas quieras de una misma fila,
pero acá en lugar de cuántas quieras es una de esas 3 cantidades que te dan)

---

N: Next player can force a win. Gana el que juega

P: Previous player who played (or the second to play) wins. Pierde el que juega

- conjunto de pilas para que no tenga orden, porque 3 2 1 es eq a 1 2 3

- memo aprovechando simetrias


una posición es N si al menos un juego resultante es P
una posición es P si todas las resultantes son N

estrategia optima:

- si estoy en una N posicion, la jugada óptima es cualquiera que me lleva a una
  P pos
- Si estoy en una P posicion, la jugada óptima es la que me lleva a la posición
  N de mínimo valor

si el valor de P es 0 -> elegis siempre el de mínimo valor

valor de una posición N

intuición: no es lo mismo que haya 1 jugada ganadora sobre 3 a que las 3 sean
ganadoras.


N

  N 0.1
  N 0.2
  P 0
  N 1

P

  N 0.1
  N 0.2
  N 0.5
  N 1

valor de N = la proporción de jugadas ganadoras
