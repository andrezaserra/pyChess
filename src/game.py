import chess


def check_for_promotion_pawns(game):
    i = 0
    while i < 8:
        if not game.white_player_turn and game.board.board[0][i] is not None and \
                game.board.board[0][i].name == "\u265F":
            game.promotion((0, i))
            break
        elif game.white_player_turn and game.board.board[7][i] is not None and \
                game.board.board[7][i].name == "\u265F":
            game.promotion((7, i))
            break
        i += 1


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
            if not game.white_player_turn:
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

            game.move(start, to)

            # check for promotion pawns
            check_for_promotion_pawns(game)

            game.board.print_board()
