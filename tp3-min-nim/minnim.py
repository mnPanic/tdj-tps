import sys

from typing import List, Tuple, Dict

from dataclasses import dataclass

def main(raw_args: List[str]):
    args = parse_args(raw_args)
    validate_args(args)

    initial_game = Game(
        position=[args.n1, args.n2, args.n3],
        moves=[args.r1, args.r2, args.r3]
    )

    if args.mode == MODE_PLAY:
        play_interactive_game(
            playerL=OptimalComputerPlayer("Computadora"),
            playerR=HumanPlayer("Humano"),
            game=initial_game,
        )
    else:
        sim = Simulator(debug=True, outcomes={})
        p_positions, n_positions = sim.calculate_positions_for_game(initial_game)

        print(f"P-posiciones:\n{p_positions}\n\nN-posiciones:\n{n_positions}")

@dataclass
class Args:
    n1: int
    n2: int
    n3: int
    r1: int
    r2: int
    r3: int

    mode: str # calculate | play

MODE_CALCULATE = "calc"
MODE_PLAY = "play"

def parse_args(args: List[str]) -> Args:
    if not (len(args) == 8):
        print("usage\n\t main.py {calculate|play} n1 n2 n3 r1 r2 r3")
        exit(1)

    mode = args[1]
    args = map(int, args[2:])
    
    n1, n2, n3, r1, r2, r3 = args
    return Args(
        n1 = n1,
        n2 = n2,
        n3 = n3,
        r1 = r1,
        r2 = r2,
        r3 = r3,
        mode = mode,
    )

def validate_args(args: Args):
    if args.mode not in {MODE_CALCULATE, MODE_PLAY}:
        print(f"Modo inválido '{args.mode}', debe ser {MODE_CALCULATE} o {MODE_PLAY}")
        exit(1)
    
    if not (args.n1 <= args.n2 and args.n2 <= args.n3):
        print(f"Pilas inválidas, deben satisfacer n1 <= n2 <= n3")
        exit(1)
    
    if not(args.r1 < args.r2 and args.r2 < args.r3):
        print(f"Movimientos inválidos, deben satisfacer r1 < r2 < r3")
        exit(1)

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
    debug: bool

    def calculate_positions_for_game(
            self, 
            initial_game: Game,
        ) -> Tuple[List[Position], List[Position]]:
        self._mem_outcome(initial_game)
        return self._positions()

    def _positions(self) -> Tuple[List[Position], List[Position]]:
        """
        Calcula las p-posiciones y n-posiciones.
        Ordena las posiciones para devolver una representación canónica. Es útil
        si se quiere hacer "trampa" y jugar contra la máquina con el
        conocimiento de cuales son N posiciones y P posiciones (alcanza con
        buscarlas en su representación canónica)
        """
        p_positions = []
        n_positions = []
        print("Calculando P y N posiciones")
        for pos, outcome, _ in self.outcomes.values():
            if outcome == P:
                p_positions.append(sorted(pos))
            else:
                n_positions.append(sorted(pos))
        
        return p_positions, n_positions

    def print(self, s: str):
        if self.debug:
            print(s)

    def _mem_outcome(self, game: Game, indent: str="") -> OutcomeClass:
        outcome = self._find_outcome(game)
        if outcome is not None:
            self.print(f"{indent}outcome memoized for {game.position}: {outcome_to_str(outcome)}")
            return outcome
    
        outcome, value = self._outcome(game, indent)
        self._store_outcome(game, outcome, value)

        return outcome

    def _outcome(self, game: Game, indent: str) -> Tuple[OutcomeClass, float]:
        # Posible poda: si el min move no se puede hacer, cortas guardarlos en
        # orden y que el min sea el primero pedirle los legal moves al juego
    
        outcomes = []
        self.print(f"{indent}{game.position}")
        for heap_idx in game.positions():
            for move in game.legal_moves(heap_idx):
                game_result = game.move(heap_idx, move)

                self.print(f"{indent}  ┌─ take {move} from #{heap_idx} ({game.heap(heap_idx)})")

                sub_outcome = self._mem_outcome(game_result, indent+"  │  ")
                outcomes.append(sub_outcome)
                
                self.print(f"{indent}  └─> next player outcome {outcome_to_str(sub_outcome)}")

        game_outcome, game_value = self._outcome_from_outcomes(outcomes)
        self.print(f"{indent}next player outcomes: {outcomes_to_str(outcomes)} -> this game outcome: {outcome_to_str(game_outcome)}, val {game_value:.2f}")

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

    def __str__(self):
        return f"heap #{self.heap_idx + 1} take {self.take}"

class Player:
    """Jugador de min nim"""
    def __init__(self, name: str):
        self.name = name

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
    def __init__(self, name: str):
        super().__init__(name)
        self.simulator = Simulator(outcomes={}, debug=False)

    def choose_move(self, game: Game) -> PlayerMove:
        # Si tengo un outcome para el juego, es porque ya precalculé todo su
        # árbol. Sino, lo precalculo. No se puede hacer en init porque todavía
        # no se sabe qué juego se juega.
        if self.simulator._find_outcome(game) is None:
            self.simulator._mem_outcome(game)

        # (value, move)
        values: List[Tuple[float, PlayerMove]] = []

        print(f"Calculando mejor movimiento para\n{game.position}")
        print("Opciones:")
        for heap_idx in game.positions():
            for move in game.legal_moves(heap_idx):
                game_result = game.move(heap_idx, move)
                val = self.simulator.find_value(game_result)

                move = PlayerMove(heap_idx=heap_idx, take=move)
                values.append((val, move))

                print(f"{move} -> {game_result.position} ({val:.2f})")

        # Argmin
        move_to_min_value = min(values, key=lambda t: t[0])[1]

        return move_to_min_value

def play_interactive_game(
    playerL: Player,
    playerR: Player,
    game: Game,
):
    playerL: Tuple[str, Player] = (f"L ({playerL.name})", playerL)
    playerR: Tuple[str, Player] = (f"R ({playerR.name})", playerR)

    player = playerL
    next_player = playerR
    while not game.finished():
        print(f"Turno de {player[0]}")
        move = player[1].choose_move(game)

        while not game.is_legal_move(move.heap_idx, move.take):
            print("Movimiento ilegal, elegí de vuelta")
            move = player[1].choose_move(game)

        print(f"Movimiento elegido {move}")

        game = game.move(move.heap_idx, move.take)

        player, next_player = next_player, player
        print("-" * 20)
    
    print(f"Gana {next_player[0]}!")

if __name__ == "__main__":
    main(sys.argv)