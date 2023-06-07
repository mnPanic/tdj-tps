# TDJ TP2 - Cut and choose

Teoría de juegos, TP2 - Cut and choose iterado con información perfecta.

Archivos:

- Enunciado: [`enunciado.txt`](enunciado.txt)
- Implementación: [`main.py`](main.py)
  - Ver [uso del programa](#uso-del-programa) para correrlo
- Experimentos: [`experimentos.ipynb`](experimentos.ipynb)
  - Para correrlos usar cualquier programa que permita ver *notebooks* de
    python, como `jupyter lab`, `jupyter notebook`, etc.

## Uso del programa

Requerimientos:

- Python 3.8 o superior
- Para correr el programa principal no hace falta ninguna dependencia externa.
- Para experimentos: `seaborn`, `pandas`, `matplotlib` y `tqdm`

Para correr el programa,

```bash
main.py <T> <N> {--debug}
```

Argumentos:

- `T`: Tamaño de la torta
- `N`: Cantidad de iteraciones
- `--debug`: Opción para correr con modo debug, que tiene más prints (no recomendable)

Ejecuta el programa para **información completa** y tablas de valuación
**inversas**. Si se desea cambiar, hay que configurarlo desde el código (y
no desde línea de comandos)

Ejemplo de output:

```bash
$ python3 main.py 10 10
Running Cut and choose with 10 iterations, cakes of size 10 and valuations of kind 'opuesto'
(#0)
cake: 3221423141, cut index: 5
 cut: 23141 (1) 32214 (2)
profits: 1: 0.519, 2: 0.522

(#1)
cake: 2214323211, cut index: 5
 cut: 23211 (1) 22143 (2)
profits: 1: 0.552, 2: 0.571

(#2)
cake: 1413332143, cut index: 5
 cut: 14133 (1) 32143 (2)
profits: 1: 0.520, 2: 0.520

(#3)
cake: 4442142143, cut index: 5
 cut: 42143 (1) 44421 (2)
profits: 1: 0.524, 2: 0.517

(#4)
cake: 4432114141, cut index: 4
 cut: 114141 (1) 4432 (2)
profits: 1: 0.720, 2: 0.520

(#5)
cake: 4234311433, cut index: 5
 cut: 11433 (1) 42343 (2)
profits: 1: 0.591, 2: 0.571

(#6)
cake: 2432244244, cut index: 5
 cut: 24322 (1) 44244 (2)
profits: 1: 0.632, 2: 0.581

(#7)
cake: 3334321123, cut index: 4
 cut: 321123 (1) 3334 (2)
profits: 1: 0.720, 2: 0.520

(#8)
cake: 2412423223, cut index: 5
 cut: 23223 (1) 24124 (2)
profits: 1: 0.520, 2: 0.520

(#9)
cake: 2323113132, cut index: 5
 cut: 13132 (1) 23231 (2)
profits: 1: 0.517, 2: 0.524

totals: 1: 5.814, 2: 5.366
```

en cada iteración, muestra la torta generada, el índice del corte, la mitad
elegida por cada jugador y la ganancia de cada uno. Al final muestra las
ganancias totales.
No hace ningún gráfico, hay que hacerlos programáticamente (como hacemos en los
experimentos)
