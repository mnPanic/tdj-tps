import sys

from typing import List, Tuple, Dict

from dataclasses import dataclass

import collections as col

def main(args: List[str]):
    n1, n2, n3, r1, r2, r3 = parse_args(args)

    calculate_positions(n1, n2, n3, r1, r2, r3)

def calculate_positions(n1, n2, n3, r1, r2, r3):
    initial_game = Game(
        position=[n1, n2, n3],
        moves=[r1, r2, r3]
    )

    sim = Simulator(outcomes={})
    c = sim.mem_outcome(initial_game)

    p_pos, n_pos = sim.positions()

    print(f"p positions: {p_pos}\nn positions: {n_pos}")

OutcomeClass = bool
P: OutcomeClass = False
N: OutcomeClass = True


NimHeap = int
Position = List[NimHeap]

@dataclass
class Game:
    position: Position
    moves: List[int]

    def heap(self, idx: int) -> NimHeap:
        return self.position[idx]

    def positions(self) -> List[int]:
        return range(len(self.position))

    def legal_moves(self, heap_idx) -> List[int]:
        return filter(
            lambda move: self.is_legal_move(heap_idx, move), 
            self.moves,
        )

    def move(self, heap_idx: int, chosen_move: int) -> "Game":
        """Realiza un movimiento en una posición. Asume que es legal"""
        old_heap = self.heap(heap_idx)
        new_heap = old_heap - chosen_move
        
        new_pos = list(self.position)
        new_pos[heap_idx] = new_heap

        return Game(
            position=new_pos,
            moves=self.moves
        )

    def is_legal_move(self, heap_idx: int, chosen_move: int) -> bool:
        return self.heap(heap_idx) >= chosen_move

def outcomes_to_str(outcomes: List[OutcomeClass]) -> str:
    return f"[{', '.join(map(outcome_to_str, outcomes))}]"

def outcome_to_str(outcome_class: OutcomeClass) -> str:
    if outcome_class == P:
        return "P"

    return "N"

@dataclass
class Simulator:
    outcomes: Dict[str, Tuple[Position, OutcomeClass]]

    def key(self, game: Game) -> str:
        return ''.join(map(str, sorted(game.position)))

    def positions(self) -> Tuple[List[Position], List[Position]]:
        p_positions = []
        n_positions = []
        for pos, outcome in self.outcomes.values():
            if outcome == P:
                p_positions.append(pos)
            else:
                n_positions.append(pos)
        
        return p_positions, n_positions

    def store_outcome(self, game: Game, outcome: OutcomeClass):
        self.outcomes[self.key(game)] = (game.position, outcome)

    def find_outcome(self, game: Game) -> OutcomeClass:
        if self.key(game) not in self.outcomes:
            return None
    
        _, outcome = self.outcomes[self.key(game)]
        return outcome

    def mem_outcome(self, game: Game, indent: str="") -> OutcomeClass:
        outcome = self.find_outcome(game)
        if outcome is not None:
            print(f"{indent}outcome memoized for {game.position}: {outcome_to_str(outcome)}")
            return outcome
    
        outcome = self.outcome(game, indent)
        self.store_outcome(game, outcome)

        return outcome

    def outcome(self, game: Game, indent: str) -> OutcomeClass:
        outcomes = []
        print(f"{indent}{game.position}")
        for heap_idx in game.positions():
            # TODO: Poda: si el min move no se puede hacer, cortas
            # guardarlos en orden y que el min sea el primero
            # pedirle los legal moves al juego
            for move in game.legal_moves(heap_idx):
                game_result = game.move(heap_idx, move)
                print(f"{indent}\ttake {move} from {game.heap(heap_idx)} (#{heap_idx})")
                sub_outcome = self.mem_outcome(game_result, indent+"\t\t")
                outcomes.append(sub_outcome)
                
                print(f"{indent}\t-> next player outcome {outcome_to_str(sub_outcome)}")

        game_outcome = self.outcome_from_outcomes(outcomes)
        print(f"{indent}next player outcomes: {outcomes_to_str(outcomes)} -> {outcome_to_str(game_outcome)}")

        return game_outcome

    def outcome_from_outcomes(self, outcomes: List[OutcomeClass]) -> OutcomeClass:
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