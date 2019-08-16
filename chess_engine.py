import chess
import chess.svg

class Tablero():
    def __init__(self):
        self.board = chess.Board()
        self.square = chess.Square()

    def render_image(self):
        board_image = chess.svg.board(board=self.board)
        return board_image

    def move_piece(self, movement):
        #Receive a move in form of characters
        move = chess.Move.from_uci(movement)
        if move in self.board.legal_moves:
            self.board.push(move)
        else:
            return "Movimiento inválido"

    def possible_movements(self):
        return self.board.legal_moves

    def undo_move(self):
        self.board.pop()

    def reset_game(self):
        self.board.reset_board()
        

class Oponent():
    def __init__(self, tablero):
        self.value = 0
        self.tablero = tablero

    def legal_moves(self):
        return self.tablero.possible_movements()


tab = Tablero()
moves = tab.board.legal_moves
for square in chess.SquareSet():
    print(square)

#tab.move_piece("b2b3")
#print(tab.board)
#tab.undo_move()
#print(tab.board)