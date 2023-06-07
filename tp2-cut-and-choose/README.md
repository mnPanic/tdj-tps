# TDJ TP2 - Cut and choose

Teoría de juegos, TP2 - Cut and choose iterado con información perfecta.

[Link al campus](https://campus.exactas.uba.ar/mod/assign/view.php?id=319058)

## Uso del programa

TODO

## TODOs

- Está bien la torta?
- Informe
- Gráficos
  - Comparar con jugador 1
  - Gráfico over iterations de la ganancia
  - Histograma de los cortes
    - habla de la tabla
  - Histograma de lo que se puede garantizar o boxplot?
    - habla de si cambia conocer la función
- Probar diferentes opciones en tablas de gustos
- Refinar output

ambivalente vs prefiere 1, puede sacar más diferencia

o prefieren 1 cada uno pero son diferentes

con un par de valuaciones la diferencia en la evolución, cuanto se aleja el 1
del 2.

## Exp

- ver para cada tabla de valoración, como se comportan las estrategias del p1
  - la strat de información incompleta en la teoría siempre te garantiza 0.5 +-
    epsilon. La idea sería mostrar que la nuestra funciona mejor para algunas
    tablas (pero no para otras)

clases de equivalencia de valuaciones?

- iguales (identity ambos, o igual a 1 todos son la misma)
- inversos
- cambia con algunos en cero? se puede probar con la anterior

## Enunciado

Se trata de escribir un programa que simule el proceso Cut & Choose iterado con información completa.

A partir de 4 componentes comestibles (1, 2, 3 y 4) que formarán parte de una "torta unidimensional", se tiene una función f1 (o tabla) a valores reales no negativos que indica cuánto le gusta cada componente al primer jugador, y otra f2 con lo mismo para el segundo jugador.

Leer enteros T y N. A partir de un arreglo de T elementos todos del conjunto {1,2,3,4} que representa la torta, la función de valoración ui de un jugador se calcula simplemente en proporción a la cantidad de 1, de 2, de 3 y de 4 que contiene el arreglo, sumando los "gustos" del jugador, normalizado a 1. Es decir, para i=1,2,

    ui (p1...pt)   =   1/factor  Sumatoria j=1,...,t  fi (pj).

Conociendo las u1 y u2, el primer jugador divide la torta con un solo corte, y el segundo elige una de las dos mitades. Así, se pide hacer una simulación que consiste en el Cut & Choose para arreglos de tamaño T creados aleatoriamente con las componentes mencionadas (cantidades cualesquiera). El procedimiento debe ser “estratégico”, esto es, el primer jugador al conocer u2 divide teniendo en cuenta esta información. Debe dividir el arreglo en 2 mitades conexas (ambas de entre 0 y T elementos), luego el segundo jugador elegirá la mitad que le convenga, quedando la otra para el primero. Y así ambos van sumando las ganancias dadas por las ui a lo largo de N iteraciones.

Tener en cuenta que en cada paso el primer jugador, una vez vista la torta, debe cortarla pensando en su propio beneficio, pero suponiendo cómo será la elección del segundo, de quien conoce sus "gustos". De ser necesario, explicar el criterio usado para esto.

Hacer la simulación N veces para los mismos parámetros, imprimiendo los datos relevantes en cada paso. (Opcionalmente, graficar.)

Concluir comentando los resultados para distintas opciones en las tablas de gustos, observando las ganancias de los participantes.

Lenguaje: a elección. Entregar el programa y un informe de 1 a 3 páginas.