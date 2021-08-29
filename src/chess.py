import board
import piece
import alert


class Chess:

    def __init__(self):
        self.board = board.Board()
        self.is_white_player_turn = True

    def change_turn(self):
        self.is_white_player_turn = not self.is_white_player_turn

    def promotion(self, position):

        pawn = None

        while pawn is None:
            promote_to = input("Promote pawn to [Q, R, N, B, P (or nothing)]: ")

            if promote_to not in ['Q', 'R', 'N', 'B', 'P', '']:
                print(alert.invalid_promotion)

            else:
                if promote_to == 'Q':
                    pawn = piece.Queen(True)

                elif promote_to == 'R':
                    pawn = piece.Rook(True)

                elif promote_to == 'N':
                    pawn = piece.Knight(True)

                elif promote_to == 'B':
                    pawn = piece.Bishop(True)

                elif promote_to == 'P' or promote_to == '':
                    pawn = piece.Pawn(True)

        self.board.board[position[0]][position[1]] = pawn

    def move(self, start, to):

        if self.board.board[start[0]][start[1]] is None:
            print(alert.empty_start)
            return False

        piece_that_will_be_moved = self.board.board[start[0]][start[1]]
        is_white_player_turn = self.is_white_player_turn

        if is_white_player_turn and piece_that_will_be_moved.color is not True:
            print(alert.incorrect_piece)
            return False

        end_square = self.board.board[to[0]][to[1]]
        piece_in_end_square = end_square if end_square is not None else None

        if piece_in_end_square is not None and piece_in_end_square.color == piece_that_will_be_moved.color:
            print(alert.blocked_path)
            return False

        if piece_that_will_be_moved.is_valid_move(self.board, start, to):

            is_a_castling_move = piece_that_will_be_moved.name == "\u265A" and abs(start[1] - to[1]) == 2

            if is_a_castling_move:
                print("Castled")

                if is_white_player_turn and self.board.black_ghost_piece is not None:
                    i = self.board.black_ghost_piece[0]
                    j = self.board.black_ghost_piece[1]
                    self.board.board[i][j] = None

                elif not is_white_player_turn and self.board.white_ghost_piece is not None:
                    i = self.board.white_ghost_piece[0]
                    j = self.board.white_ghost_piece[1]
                    self.board.board[i][j] = None

                self.change_turn()
                return True

            if piece_in_end_square is not None:
                print(str(end_square) + " taken.") if piece_in_end_square.name != "GP" else \
                    print(str(end_square) + " taken by 'en passant' move.")

                if piece_in_end_square.name == "GP":
                    i = to[0]
                    j = to[1]
                    if is_white_player_turn:
                        self.board.board[i + 1][j] = None
                        self.board.black_ghost_piece = None
                    else:
                        self.board.board[i - 1][j] = None
                        self.board.white_ghost_piece = None

            self.board.board[to[0]][to[1]] = piece_that_will_be_moved
            print(str(piece_that_will_be_moved) + " moved.")
            self.board.board[start[0]][start[1]] = None

            if is_white_player_turn and self.board.black_ghost_piece is not None:
                i = self.board.black_ghost_piece[0]
                j = self.board.black_ghost_piece[1]
                self.board.board[i][j] = None

            elif not is_white_player_turn and self.board.white_ghost_piece is not None:
                i = self.board.white_ghost_piece[0]
                j = self.board.white_ghost_piece[1]
                self.board.board[i][j] = None

            self.change_turn()
