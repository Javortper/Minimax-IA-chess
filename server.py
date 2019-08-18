from flask import Flask, render_template, request, Markup
import chess_engine

app = Flask(__name__)
game = chess_engine.Tablero()

@app.route('/')
def mostrar_tablero():
    return render_template('index.html', board_image=Markup(game.render_image()))

@app.route('/handleAction', methods=['POST'])
def actualiza_tablero():
        if request.method == 'POST':
                if 'move' in request.form:
                        move = request.form["move"]
                        game.move_piece_san(move)
                        board_image = game.render_image()
                        return render_template('handleAction.html', board_image=Markup(board_image))

                #TODO: NO FUNCIONAN
                elif request.form['back'] == 'Deshacer movimiento':
                        game.undo_move()
                        board_image = game.render_image()
                        return render_template('handleAction.html', board_image=Markup(board_image))

                elif request.form['reset'] == 'Reiniciar tablero':
                        game.reset_game()
                        board_image = game.render_image()
                        return render_template('index.html', board_image=Markup(board_image))



if __name__ == "__main__":
        app.run(debug=True)