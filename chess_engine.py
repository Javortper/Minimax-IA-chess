import chess
import chess.svg
import math

class Tablero():
    #Clase que maneja el engine del tablero. Aqui aplicamos los movimientos,reseteamos el juego,
    #obtenemos información del estado actual de la partida...
    #Basicamente es un wrapper del python-chess
    def __init__(self):
        self.board = chess.Board()
        self.square = chess.Square()

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

    #def pieces(self, piece_type:str):
        #list of all white pieces
        #piece_type; 'w'->white, 'b'->black
        #pass

    def undo_move(self):
        self.board.pop()

    def reset_game(self):
        self.board.reset_board()
        

class ArticialOpponent():
    #Esta clase aplica el algoritmo MiniMax para elegir el mejor posible estado siguientwes 
    #entre todas las posibilidades.
    def __init__(self, tablero):
        self.pieces_values={'P':1,
                            'K':3,
                            'B':3,
                            'R':5,
                            'Q':9}
        self.tablero = tablero
        self.colour = chess.BLACK
    
    def evaluation(self, state):
        #Basic heuristic. Sum of (nº of pieces * value)
        state_value = 0
        for piece_type in self.pieces_values.values():
            n_pieces = len(list(tablero.board.pieces(piece_type, self.colour)))
            state_value += n_pieces * self.pieces_values[piece_type]
        return state_value

    def generate_next_states(self, depth):
        #Return list of possible boards for every move. Index 0 = first generation, index 1 = second generation...
        possible_next_states = []
        while depth == 0:
            j = []
            for move in self.tablero.possible_movements():
                actual_state = self.tablero
                possible_next_state = actual_state.move_piece_uci(move)
                j.append(possible_next_state)
            possible_next_states.append(j)
        return possible_next_states

    def minimax(self, state:Tablero, depth:int):
        #IA -> Maximice; Human -> Minimice  
        #IA will watch 3 nexts generations of possible boards
        if depth == 0:
            return self.evaluation(state)
        else:
            

        


tablero = Tablero()
for mov in tablero.possible_movements():
    print(mov)

ia = ArticialOpponent(tablero)