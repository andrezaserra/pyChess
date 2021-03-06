import chess
import checker


def translate(entry):
    try:
        row = int(entry[0])
        col = entry[1]
        if row < 1 or row > 8:
            print(entry[0] + "is not in the range from 1 - 8")
            return None
        if col < 'a' or col > 'h':
            print(entry[1] + "is not in the range from a - h")
            return None
        column_legend = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return 8 - row, column_legend[col]

    except:
        print(entry + "is not in the format '[number][letter]'")
        return None


class Game:
    if __name__ == "__main__":

        game = chess.Chess()
        game.board.print_board()

        while True:

            is_white_player_turn = game.is_white_player_turn

            if not is_white_player_turn:
                print("Black player's turn:")
            else:
                print("White player's turn:")

            print("Move a piece")
            start = input("From: ")
            to = input("To: ")

            start = translate(start)
            to = translate(to)

            if start is None or to is None:
                continue

            is_a_checkmate = checker.check_if_the_move_is_a_checkmate(is_white_player_turn, to, game.board)
            move = game.move(start, to)

            if is_a_checkmate:
                game.board.print_board()
                print("CHECKMATE!")
                print("White Player won!") if not game.is_white_player_turn else print("Black Player won!")
                break

            checker.check_for_promotion_pawns(game)

            game.board.print_board()
