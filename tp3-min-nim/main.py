import sys

from typing import List, Tuple, Dict

from dataclasses import dataclass

def main(args: List[str]):
    n1, n2, n3, r1, r2, r3 = parse_args(args)

    calculate_positions(n1, n2, n3, r1, r2, r3)

def calculate_positions(n1, n2, n3, r1, r2, r3):
    initial_game = Game(
        position=[n1, n2, n3],
        moves=[r1, r2, r3]
    )

    #sim = Simulator(outcomes={})
    #p_pos, n_pos = sim.calculate_positions_for_game(initial_game)

    #print(f"p positions: {p_pos}\nn positions: {n_pos}")
    play_interactive_game(
        playerL=OptimalComputerPlayer(),
        playerR=HumanPlayer(),
        game=initial_game,
    )

OutcomeClass = bool
P: OutcomeClass = False
N: OutcomeClass = True


NimHeap = int
Position = List[NimHeap]
        

@dataclass
class Game:
    """
    Tiene una posición y una lista de movimientos válida,
    permite manualmente avanzar el juego mediante movimientos
    """
    position: Position
    moves: List[int]

    def heap(self, idx: int) -> NimHeap:
        return self.position[idx]

    def positions(self) -> List[int]:
        return range(len(self.position))

    def finished(self) -> bool:
        for heap_idx in self.positions():
            if len(self.legal_moves(heap_idx)) != 0:
                return False
        
        return True

    def legal_moves(self, heap_idx) -> List[int]:
        return list(filter(
            lambda move: self.is_legal_move(heap_idx, move), 
            self.moves,
        ))

    def move(self, heap_idx: int, chosen_move: int) -> "Game":
        """
        Realiza un movimiento en una posición.
        Asume que es legal (ver legal_moves)
        """
        old_heap = self.heap(heap_idx)
        new_heap = old_heap - chosen_move
        
        new_pos = list(self.position)
        new_pos[heap_idx] = new_heap

        return Game(
            position=new_pos,
            moves=self.moves
        )

    def is_legal_move(self, heap_idx: int, chosen_move: int) -> bool:
        return (
            heap_idx < len(self.position) and heap_idx >= 0
            and self.heap(heap_idx) >= chosen_move
        )

def outcomes_to_str(outcomes: List[OutcomeClass]) -> str:
    return f"[{', '.join(map(outcome_to_str, outcomes))}]"

def outcome_to_str(outcome_class: OutcomeClass) -> str:
    if outcome_class == P:
        return "P"

    return "N"

@dataclass
class Simulator:
    """
    Simula todas las partidas posibles para obtener los conjuntos de
    P-posiciones y N-posiciones.
    """
    outcomes: Dict[str, Tuple[Position, OutcomeClass, float]]

    def calculate_positions_for_game(
            self, 
            initial_game: Game,
        ) -> Tuple[List[Position], List[Position]]:
        self._mem_outcome(initial_game)
        return self._positions()

    def _positions(self) -> Tuple[List[Position], List[Position]]:
        """Calcula las p-posiciones y n-posiciones."""
        p_positions = []
        n_positions = []
        for pos, outcome in self.outcomes.values():
            if outcome == P:
                p_positions.append(pos)
            else:
                n_positions.append(pos)
        
        return p_positions, n_positions

    def _mem_outcome(self, game: Game, indent: str="") -> OutcomeClass:
        outcome = self._find_outcome(game)
        if outcome is not None:
            print(f"{indent}outcome memoized for {game.position}: {outcome_to_str(outcome)}")
            return outcome
    
        outcome, value = self._outcome(game, indent)
        self._store_outcome(game, outcome, value)

        return outcome

    def _outcome(self, game: Game, indent: str) -> Tuple[OutcomeClass, float]:

        # TODO: Poda: si el min move no se puede hacer, cortas guardarlos en
        # orden y que el min sea el primero pedirle los legal moves al juego
        outcomes = []
        print(f"{indent}{game.position}")
        for heap_idx in game.positions():
            for move in game.legal_moves(heap_idx):
                game_result = game.move(heap_idx, move)

                print(f"{indent}\ttake {move} from {game.heap(heap_idx)} (#{heap_idx})")

                sub_outcome = self._mem_outcome(game_result, indent+"\t\t")
                outcomes.append(sub_outcome)
                
                print(f"{indent}\t-> next player outcome {outcome_to_str(sub_outcome)}")

        game_outcome, game_value = self._outcome_from_outcomes(outcomes)
        print(f"{indent}next player outcomes: {outcomes_to_str(outcomes)} -> {outcome_to_str(game_outcome)}, val {game_value}")

        return game_outcome, game_value

    def _outcome_from_outcomes(self, outcomes: List[OutcomeClass]) -> Tuple[OutcomeClass, float]:
        """
        Calcula el outcome class de una posición en base a los outcome
        classes de las posiciones resultantes de hacer todos los movimientos
        legales.
        Además, calcula el valor de la posición como la proporción de jugadas ganadoras.
        """
        if len(outcomes) == 0:
            # Caso base: No tengo movimientos, pierdo
            return P, 0

        # Si tengo al menos una subclase P, quiere decir que puedo forzar
        # un movimiento ganador, por lo que soy N
        p_outcomes = list(filter(lambda s: s == P, outcomes))
        if len(p_outcomes) != 0:
            return N, len(p_outcomes) / len(outcomes)
        
        # Si todas las subclases son N (no hay P) sin importar que haga pierdo.
        # Soy P
        return P, 0

    def _store_outcome(self, game: Game, outcome: OutcomeClass, value: float):
        self.outcomes[self._key(game)] = (game.position, outcome, value)

    def _find_outcome(self, game: Game) -> OutcomeClass:
        if self._key(game) not in self.outcomes:
            return None
    
        _, outcome, _ = self.outcomes[self._key(game)]
        return outcome

    def find_value(self, game: Game) -> float:
        if self._key(game) not in self.outcomes:
            return None
        
        _, _, value = self.outcomes[self._key(game)]
        return value

    def _key(self, game: Game) -> str:
        """
        Esto es necesario porque las Position (listas) no son hasheables.
        Además permite tomar como equivalentes permutaciones de juegos, evitando
        re-computar simetrías.
        """
        return ''.join(map(str, sorted(game.position)))


@dataclass
class PlayerMove:
    heap_idx: int
    take: int

class Player:
    """Jugador de min nim"""
    def choose_move(self, game: Game) -> PlayerMove:
        raise NotImplementedError

class HumanPlayer(Player):
    def choose_move(self, game: Game) -> PlayerMove:
        print(f"Estado del juego: {game.position}")
        positions = list(map(lambda p: p+1, game.positions()))
        heap = input(f"pila # ({positions}): ")
        take = input(f"tomar ({game.moves}): ")

        return PlayerMove(
            heap_idx=int(heap) - 1,
            take=int(take),
        )

class OptimalComputerPlayer(Player):
    def __init__(self):
        self.simulator = Simulator(outcomes={})

    def choose_move(self, game: Game) -> PlayerMove:
        if self.simulator._find_outcome(game) is None:
            self.simulator._mem_outcome(game)
    
        # (value, move)
        values: List[Tuple[float, PlayerMove]] = []

        for heap_idx in game.positions():
            for move in game.legal_moves(heap_idx):
                game_result = game.move(heap_idx, move)
                val = self.simulator.find_value(game_result)

                values.append((val, PlayerMove(heap_idx=heap_idx, take=move)))

        # return argmin values
        return min(values, key=lambda t: t[0])[1]

def play_interactive_game(
    playerL: Player,
    playerR: Player,
    game: Game,
):
    playerL: Tuple[str, Player] = ("L", playerL)
    playerR: Tuple[str, Player] = ("R", playerR)

    player = playerL
    next_player = playerR
    while not game.finished():
        print(f"Turno de {player[0]}")
        move = player[1].choose_move(game)

        while not game.is_legal_move(move.heap_idx, move.take):
            print("Movimiento ilegal, elegí de vuelta")
            move = player[1].choose_move(game)
        
        print("Movimiento elegido")

        game = game.move(move.heap_idx, move.take)

        player, next_player = next_player, player
        print("-" * 20)
    
    print(f"Gana {next_player[0]}!")

def parse_args(args: List[str]) -> Tuple[int, int, int, int, int, int]:
    if not (len(args) == 7):
        print("usage\n\t main.py n1 n2 n3 r1 r2 r3")
        exit(1)

    args = map(int, args[1:])
    
    n1, n2, n3, r1, r2, r3 = args
    return n1, n2, n3, r1, r2, r3


if __name__ == "__main__":
    main(sys.argv)