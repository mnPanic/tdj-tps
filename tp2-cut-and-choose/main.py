"""
Argumentos:
- T: Tamaño de la torta
- N: Cantidad de iteraciones
"""

import sys
import random

from typing import List, Tuple, Dict

Cake = List[str]

def cake_to_str(cake: Cake) -> str:
    return ''.join(cake)

cake_parts = ["1", "2", "3", "4"]

# Identidades
f1: Dict[str, float] = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
}

f2: Dict[str, float] = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
}

def utility(f: Dict[str, float], cake: Cake, cake_part: Cake) -> float:
    """Función de valoración de un jugador, normalizada a 1"""
    max_value = 0
    for part in cake:
        max_value += f[part]

    value = 0
    for part in cake_part:
        value += f[part]
    
    return value/max_value

def main(args: List[str]):
    # T, N
    cake_size, num_iters = parse_args(args)

    player1_total = 0
    player2_total = 0
    for i in range(num_iters):
        print(f"(#{i})")
        u1, u2 = simulate(cake_size)
        player1_total += u1
        player2_total += u2
        print()
    
    print(f"totals: 1: {player1_total:.3f}, 2: {player2_total:.3f}")


def simulate(cake_size: int):
    cake = generate_cake(cake_size)
    cut_index = player1_cut(cake)

    first_half, second_half = cake[:cut_index], cake[cut_index:]
    choice = player2_choose(cake, first_half, second_half)
    if choice:
        player1_half = first_half
        player2_half = second_half
    else:
        player1_half = second_half
        player2_half = first_half

    player1_profit = utility(f1, cake, player1_half)
    player2_profit = utility(f2, cake, player2_half)

    # Output de la iter
    output = f"cake: {cake_to_str(cake)}, cut index: {cut_index}\n"

    # Debug printeamos valores de mitades
    p1fh = utility(f1, cake, first_half)
    p1sh = utility(f1, cake, second_half)

    p2fh = utility(f2, cake, first_half)
    p2sh = utility(f2, cake, second_half)
    output += f"{cake_to_str(first_half)} -> 1: {p1fh:.3f}, 2: {p2fh:.3f}\n"
    output += f"{cake_to_str(second_half)} -> 1: {p1sh:.3f}, 2: {p2sh:.3f}\n"

    # Cortes y profits
    output += f" cut: {cake_to_str(player1_half)} (1) {cake_to_str(player2_half)} (2)\n"
    output += f"profits: 1: {player1_profit:.3f}, 2: {player2_profit:.3f}"
    print(output)

    return player1_profit, player2_profit

def parse_args(args: List[str]) -> Tuple[int, int]:
    if len(args) != 3:
        print("usage\n\t main.py <T> <N>")
    
    return int(args[1]), int(args[2])
    
def generate_cake(size: int) -> Cake:
    """Genera una torta aleatoria de tamaño size"""
    # TODO: Las cantidades deberían ser aleatorias, tal vez no uniformes?
    # Generar weights cuya suma sea 1, aleatorios.

    # Genera una aleatoria lista de tamaño k con una distribución uniforme de 
    # los elementos de population
    # https://docs.python.org/3/library/random.html#random.choices
    return random.choices(population=cake_parts, k=size)


def player1_cut(cake: Cake) -> int:
    """
    Jugador 1. Devuelve el índice en el cual cortar la torta, no inclusivo.
    Parte en [0, cut) y [cut, T].
    """
    # Dummy por ahora
    return int(len(cake) / 2)

CHOOSE_FIRST = False
CHOOSE_SECOND = True
def player2_choose(cake: Cake, first: Cake, second: Cake) -> bool:
    """Jugador 2. Elige la primera o segunda mitad. True si second"""
    if utility(f2, cake, first) >= utility(f2, cake, second):
        return CHOOSE_FIRST

    return CHOOSE_SECOND

if __name__ == "__main__":
    main(sys.argv)