import sys

from typing import List, Tuple, Set

from dataclasses import dataclass

def main(args: List[str]):
    n1, n2, n3, r1, r2, r3 = parse_args(args)

    calculate_positions(n1, n2, n3, r1, r2, r3)

NimHeap = int
Position = Set[NimHeap]

@dataclass
class Memo:
    p_positions: List[Position]
    n_positions: List[Position]

@dataclass
class Game:
    position: Position
    moves: List[int]

    def move(self, heap: NimHeap, chosen_move: int) -> "Game":
        """Realiza un movimiento en una posición. Asume que es legal"""
        new_pos: Position = self.position - {heap}
        new_heap = heap - chosen_move

        new_pos.add(new_heap)

        return Game(
            position=new_pos,
            moves=self.moves
        )

    def is_legal_move(self, heap: NimHeap, chosen_move: int) -> bool:
        return heap >= chosen_move

def calculate_positions(n1, n2, n3, r1, r2, r3) -> Tuple[list, list]:
    # juego base
    #mem = Memo()

    initial_game = Game(
        position={n1, n2, n3},
        moves=[r1, r2, r3]
    )

    c = outcome(initial_game)
    print(class_to_str(c))

OutcomeClass = bool
P: OutcomeClass = False
N: OutcomeClass = True

def class_to_str(outcome_class: OutcomeClass) -> str:
    if outcome_class == P:
        return "P"

    return "N"

def outcome(game: Game) -> OutcomeClass:
    outcomes = []
    for move in game.moves:
        for heap in game.position:
            if game.is_legal_move(heap, move):
                position_result = game.move(heap, move)
                outcomes.append(outcome(position_result))

    if len(outcomes) == 0:
        # Caso base: No tengo movimientos, pierdo
        return P

    # Si tengo al menos una subclase P, quiere decir que puedo forzar
    # un movimiento ganador, por lo que soy N
    p_outcomes = list(filter(lambda s: s == P, outcomes))
    if len(p_outcomes) != 0:
        return N
    
    # Si todas las subclases son N (no hay P) sin importar que haga pierdo.
    # Soy P
    return P

def parse_args(args: List[str]) -> Tuple[int, int, int, int, int, int]:
    if not (len(args) == 7):
        print("usage\n\t main.py n1 n2 n3 r1 r2 r3")
        exit(1)

    args = map(int, args[1:])
    
    n1, n2, n3, r1, r2, r3 = args
    return n1, n2, n3, r1, r2, r3


if __name__ == "__main__":
    main(sys.argv)