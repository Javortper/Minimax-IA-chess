import chess
import chess.svg
import math
import copy

DEPTH_OF_ENEMY = 3 #Number of moves that enemy can see in the future

class Tablero():
    #Clase que maneja el engine del tablero. Aqui aplicamos los movimientos,reseteamos el juego,
    #obtenemos información del estado actual de la partida...
    #Basicamente es un wrapper del python-chess
    def __init__(self):
        self.board = chess.Board()
        self.square = chess.Square()
        self.enemy = Opponent(self)

    def render_image(self):
        board_image = chess.svg.board(board=self.board)
        return board_image

    def get_turn(self):
        if self.board.turn == True:
            return 'w'
        else:
            return 'b'

    def move_piece_uci(self, movement:str):
        #Receive a move in form of characters
        move = chess.Move.from_uci(movement)
        if move in self.board.legal_moves:
            self.board.push(move)

    def move_piece_san(self, movement:str):
        #Receive a move in form of characters
        self.board.push_san(movement)

    def possible_movements(self):
        return self.board.legal_moves

    def undo_move(self):
        self.board.pop()

    def reset_game(self):
        self.board.reset_board()
        
    def enemy_movement(self, depth = DEPTH_OF_ENEMY):
        _, enemy_move = self.enemy.minimax(self, depth, True)
        print(enemy_move)
        self.move_piece_uci(enemy_move)


class Opponent():
    #Esta clase aplica el algoritmo MiniMax para elegir el mejor posible estado siguientwes 
    #entre todas las posibilidades.
    def __init__(self, tablero:Tablero):
        self.pieces_values={chess.PAWN:1,
                            chess.KNIGHT:3,
                            chess.BISHOP:3,
                            chess.ROOK:5,
                            chess.QUEEN:9}
        self.colour = chess.BLACK
    
    def evaluation(self, state):
        #Basic heuristic. Sum of (nº of pieces * value) for BLACK pieces.
        #IA try to maximice BLACK pieces and Player try to minimice it.
        state_value = 0
        for piece_type in self.pieces_values.keys():
            n_pieces = len(list(state.board.pieces(piece_type, self.colour)))
            state_value += n_pieces * self.pieces_values[piece_type]
        return state_value

    def generate_next_states(self, tablero):
        #Return list of possible boards for every move.
        possible_next_states = []
        for move in tablero.possible_movements():
            move = str(move)
            state_copy = copy.deepcopy(tablero)
            state_copy.move_piece_uci(move)
            possible_next_states.append(state_copy)
        return possible_next_states

    def minimax(self, state:Tablero, depth:int, maximice_player:bool):
        #IA -> Maximice(True); Human -> Minimice  (False)
        #IA will watch 3 nexts generations of possible boards
        possible_moves = state.possible_movements()
        if maximice_player:
            value = float('-inf')
            for next_state, choosed_move in zip(self.generate_next_states(state), list(possible_moves)):
                next_state_value, move = self.minimax_aux(next_state, depth-1, False, choosed_move)
                value = max(value, next_state_value)
            return value, str(move)
        else:
            value = float('inf')
            for next_state, choosed_move in zip(self.generate_next_states(state), list(possible_moves)):
                next_state_value, move = self.minimax_aux(next_state, depth-1, True, choosed_move)
                value = min(value, next_state_value)
            return value, str(move)

    def minimax_aux(self, state:Tablero, depth:int, maximice_player:bool, choosed_move:str):
        if depth == 0:
            return self.evaluation(state), choosed_move
        else:
            if maximice_player:
                value = float('-inf')
                for next_state in self.generate_next_states(state):
                    next_state_value, move = self.minimax_aux(next_state, depth-1, False, choosed_move)
                    value = max(value, next_state_value)
                return value, move
            else:
                value = float('inf')
                for next_state in self.generate_next_states(state):
                    next_state_value, move  = self.minimax_aux(next_state, depth-1, True, choosed_move)
                    value = min(value, next_state_value)
                return value, move

#tablero = Tablero()
#print(list(tablero.possible_movements))
#ia = Opponent(tablero)
#tablero.move_piece_uci('a2a4')
#ia.generate_next_states(tablero)

#tablero.enemy_movement()
#ia = Opponent(tablero)
#print(ia.minimax(tablero, 2, True))