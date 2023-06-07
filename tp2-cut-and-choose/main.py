"""
Argumentos:
- T: Tamaño de la torta
- N: Cantidad de iteraciones
"""

import sys
import random

from dataclasses import dataclass

from typing import List, Tuple, Dict

Cake = str
FlavorValuation = Dict[str, float]

cake_flavors = ["1", "2", "3", "4"]

CHOOSE_FIRST = False
CHOOSE_SECOND = True

# Información completa, sabe los gustos del otro jugador
P1_INFO_COMPLETE = "complete"

# Información incompleta, no sabe los gustos del otro jugador e intenta
# garantizar 0.5
P1_INFO_INCOMPLETE = "incomplete"

def main(args: List[str]):
    # T, N
    cake_size, num_iters, debug = parse_args(args)

    game = CutAndChoose(
        debug=debug, 
        vals=flavor_valuation_inverse(), 
        p1_info=P1_INFO_COMPLETE,
    )

    game.play(cake_size, num_iters)

def parse_args(args: List[str]) -> Tuple[int, int, bool]:
    if not (len(args) == 3 or len(args) == 4):
        print("usage\n\t main.py <T> <N> {--debug}")
        exit(1)
    
    T = int(args[1])
    N = int(args[2])
    debug = False

    if len(args) == 4 and args[3] == "--debug":
        debug=True

    return T, N, debug


@dataclass
class PlayersValuation():
    name: str
    f1: FlavorValuation
    f2: FlavorValuation

class CutAndChoose():
    def __init__(self, debug: bool, quiet: bool, vals: PlayersValuation, p1_info: str) -> None:
        self.debug = debug
        self.quiet = quiet
        self.vals = vals
        self.p1_info = p1_info
        self.debug_print("Printing debug information")

    def play(self, cake_size: int, num_iters: int) -> Tuple[List[int], Dict[str, List[str]]]:
        self.print(f"Running Cut and choose with {num_iters} iterations, cakes of size {cake_size} and valuations of kind '{self.vals.name}'")

        records = []
        player1_total = 0
        player2_total = 0
        for i in range(num_iters):
            self.print(f"(#{i})")
            u1, u2, cut = self.simulate(cake_size)
            player1_total += u1
            player2_total += u2

            records.append({
                "p1": u1,
                "p2": u2,
                "val": self.vals.name,
                "p1_info": self.p1_info,
                "cut": cut,
                "iter": i,
                "p1_total": player1_total,
                "p2_total": player2_total,
            })
            
            self.print()
    
        self.print(f"totals: 1: {player1_total:.3f}, 2: {player2_total:.3f}")

        return records
        
    def simulate(self, cake_size: int) -> Tuple[int, int, int]: # u1, u2, cut
        cake = self.generate_cake(cake_size)
        self.debug_print(f"cake: {cake}")

        cut_index = self.player1_cut(cake)

        first_half, second_half = cake[:cut_index], cake[cut_index:]
        choice = self.player2_choose(cake, first_half, second_half)
        if choice == CHOOSE_SECOND:
            p1_cake = first_half
            p2_cake = second_half
        else:
            p1_cake = second_half
            p2_cake = first_half

        p1_profit = utility(self.vals.f1, cake, p1_cake)
        p2_profit = utility(self.vals.f2, cake, p2_cake)

        # Output de la iter
        output = f"cake: {cake}, cut index: {cut_index}\n"

        # Debug agregamos valores de mitades
        if self.debug:
            p1_fh = utility(self.vals.f1, cake, first_half)
            p1_sh = utility(self.vals.f1, cake, second_half)

            p2_fh = utility(self.vals.f2, cake, first_half)
            p2_sh = utility(self.vals.f2, cake, second_half)
            output += f"{first_half} -> 1: {p1_fh:.3f}, 2: {p2_fh:.3f}\n"
            output += f"{second_half} -> 1: {p1_sh:.3f}, 2: {p2_sh:.3f}\n"

        # Cortes y profits
        output += f" cut: {p1_cake} (1) {p2_cake} (2)\n"
        output += f"profits: 1: {p1_profit:.3f}, 2: {p2_profit:.3f}"
        self.print(output)

        return p1_profit, p2_profit, cut_index

    def generate_cake(self, size: int) -> Cake:
        """Genera una torta aleatoria de tamaño size"""
        # Genera una aleatoria lista de tamaño k con una distribución uniforme de 
        # los elementos de population
        # https://docs.python.org/3/library/random.html#random.choices
        return ''.join(random.choices(population=cake_flavors, k=size))

    def player1_cut(self, cake: Cake) -> int:
        """Jugador 1. Devuelve el índice en el cual cortar la torta"""
        if self.p1_info == P1_INFO_COMPLETE:
            return self.player1_cut_complete(cake)
        
        elif self.p1_info == P1_INFO_INCOMPLETE:
            return self.player1_cut_incomplete(cake)
    
        return -1

    def player1_cut_half(self, cake: Cake) -> int:
        """Parte en [0, cut) y [cut, T]."""
        return int(len(cake) / 2)

    def player1_cut_incomplete(self, cake: Cake) -> int:
        """Intenta de garantizarse 0.5"""
        # Se queda con el corte que minimiza la diferencia entre las dos partes

        # Lista de corte, diferencia
        cuts: List[Tuple[int, float]] = []

        for cut in range(1, len(cake)):
            first_half = cake[:cut]

            # Como los valores están normalizados, sabemos que la segunda mitad
            # es 1 - el primero
            first_value = utility(self.vals.f1, cake, first_half)
            second_value = 1 - first_value

            dif = abs(first_value - second_value)
            cuts.append((cut, dif))

        return min(cuts, key=lambda t: t[1])[0]


    def player1_cut_complete(self, cake: Cake) -> int:
        """
        Prueba todos los cortes posibles y se queda con el que le de un valor máximo
        """
        # listas de (corte, valor corte)
        cuts: List[Tuple[int, float]] = []

        for cut in range(1, len(cake)):
            self.debug_print(f"\ncut {cut}")
            
            value = self.cut_value(cake, cut)

            self.debug_print(f"{value:.3f}")

            cuts.append((cut, value))

        max_cut_value = max(cuts, key=lambda t: t[1])
        self.debug_print(f"predicted value: {max_cut_value[1]}")
        return max_cut_value[0]

    def cut_value(self, cake: Cake, cut_index: int) -> float:
        """
        Dada una torta y un corte, devuelve el valor esperado considerando que el
        jugador 2 va a elegir la mitad que más le conviene.

        Ejemplo, dada

            cake = 1234, cuts:
            1       1: 0.3 2: 0.6
            234     1: 0.7 2: 0.4

        Asume que 2 va a elegir mitad 1, porque paga 0.6 (max) entonces a vos te
        queda la mitad 234, con paga 0.7. Entonces el valor del corte es 0.7
        """

        first_half, second_half = cake[:cut_index], cake[cut_index:]
        p1_first_half_profit = utility(self.vals.f1, cake, first_half)
        p2_first_half_profit = utility(self.vals.f2, cake, first_half)

        p1_second_half_profit = utility(self.vals.f1, cake, second_half)
        p2_second_half_profit = utility(self.vals.f2, cake, second_half)

        output = f"{first_half} -> 1: {p1_first_half_profit:.3f}, 2: {p2_first_half_profit:.3f}\n"
        output += f"{second_half} -> 1: {p1_second_half_profit:.3f}, 2: {p2_second_half_profit:.3f}"
        self.debug_print(output)

        # Si al p2 le da igual, asumimos que elije la que nos perjudica
        if p2_first_half_profit == p2_second_half_profit:
            return min(p1_first_half_profit, p1_second_half_profit)

        if p2_first_half_profit > p2_second_half_profit:
            # Elige el primero, nos toca el segundo
            return p1_second_half_profit

        return p1_first_half_profit


    def player2_choose(self, cake: Cake, first: Cake, second: Cake) -> bool:
        """Jugador 2. Elige la primera o segunda mitad. True si second"""
        if utility(self.vals.f2, cake, first) >= utility(self.vals.f2, cake, second):
            return CHOOSE_FIRST

        return CHOOSE_SECOND

    def print(self, s: str=""):
        if not self.quiet:
            print(s)

    def debug_print(self, s: str):
        if self.debug:
            self.print(s)

def flavor_valuation_identity() -> PlayersValuation:
    identity_valuation = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
    }

    return PlayersValuation(
        name="identidad",
        f1=identity_valuation,
        f2=identity_valuation,
    )

def flavor_valuation_inverse() -> PlayersValuation:
    return PlayersValuation(
        name="opuesto",
        f1 = {
            "1": 4,
            "2": 3,
            "3": 2,
            "4": 1,
        },
        f2 ={
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
        }
    )


def flavor_valuation_inverse_disjoint() -> PlayersValuation:
    return PlayersValuation(
        name="opuesto_disjunto",
        f1 = {
            "1": 1,
            "2": 1,
            "3": 0,
            "4": 0,
        },
        f2 ={
            "1": 0,
            "2": 0,
            "3": 1,
            "4": 1,
        }
    )

def flavor_valuation_igual_picky() -> PlayersValuation:
    return PlayersValuation(
        name="igual_vs_picky",
        f1 = {
            "1": 1,
            "2": 1,
            "3": 1,
            "4": 1,
        },
        f2 ={
            "1": 1,
            "2": 0,
            "3": 0,
            "4": 0,
        }
    )

def utility(f: FlavorValuation, cake: Cake, cake_part: Cake) -> float:
    """Función de valoración de un jugador, normalizada a 1"""
    max_value = 0
    for part in cake:
        max_value += f[part]
    
    # Necesario por si hay gustos que aportan 0
    if max_value == 0:
        return 0

    value = 0
    for part in cake_part:
        value += f[part]
    
    return value/max_value



if __name__ == "__main__":
    main(sys.argv)
