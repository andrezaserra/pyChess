import checker
import alert


class Piece:
    def __init__(self, color):
        self.name = ""
        self.color = color

    def is_valid_move(self, board, start, to):
        return False

    def is_white(self):
        return self.color

    def __str__(self):
        if self.color:
            return self.name
        else:
            return '\033[94m' + self.name + '\033[0m'


class Rook(Piece):
    def __init__(self, color, is_first_move=True):
        super().__init__(color)
        self.name = "\u265c"
        self.is_first_move = is_first_move

    def is_valid_move(self, board, start, to):
        keep_same_line = start[0] == to[0]
        keep_same_column = start[1] == to[1]

        if keep_same_line or keep_same_column:
            return checker.check_straight_path(board, start, to)

        print(alert.incorrect_path)
        return False


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "\u265E"

    def is_valid_move(self, board, start, to):
        vertical_move = abs(start[0] - to[0]) == 2 and abs(start[1] - to[1]) == 1
        horizontal_move = abs(start[0] - to[0]) == 1 and abs(start[1] - to[1]) == 2

        if vertical_move or horizontal_move:
            return True

        print(alert.incorrect_path)
        return False


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "\u265D"

    def is_valid_move(self, board, start, to):
        is_a_diagonal_move = abs(start[0] - to[0]) == abs(start[1] - to[1])

        if not is_a_diagonal_move:
            print(alert.incorrect_path)
            return False

        return checker.check_diagonal_path(board, start, to)


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "\u265B"

    def is_valid_move(self, board, start, to):

        is_a_diagonal_move = abs(start[0] - to[0]) == abs(start[1] - to[1])
        is_a_straight_move = start[0] == to[0] or start[1] == to[1]

        if is_a_diagonal_move:
            return checker.check_diagonal_path(board, start, to)

        elif is_a_straight_move:
            return checker.check_straight_path(board, start, to)

        print(alert.incorrect_path)
        return False


class King(Piece):
    def __init__(self, color, first_move=True):
        super().__init__(color)
        self.name = "\u265A"
        self.first_move = first_move

    # return true if the king do a castling - Function Precondition: path start->to is a castling move
    def do_castling(self, board, start, to, is_to_the_right):

        is_a_white_castling = self.color

        # White castling to the right
        if is_a_white_castling and is_to_the_right:

            king_is_in_check = checker.check_if_king_is_in_check(start, True, board)

            if king_is_in_check:
                print(alert.king_is_in_check)
                return False

            king_will_be_in_check = checker.check_if_king_is_in_check(to, True, board)

            if king_will_be_in_check:
                print(alert.king_will_be_in_check)

            if not king_is_in_check and not king_will_be_in_check:
                board.board[to[0]][to[1]] = King(True, False)
                board.board[to[0]][to[1] - 1] = Rook(True, False)
                board.board[start[0]][start[1]] = None
                board.board[7][7] = None
                return True

        # White castling to the left
        elif is_a_white_castling and not is_to_the_right:
            king_is_in_check = checker.check_if_king_is_in_check(start, True, board)
            king_will_be_in_check = checker.check_if_king_is_in_check(to, True, board)

            if not king_is_in_check and not king_will_be_in_check:
                board.board[to[0]][to[1]] = King(True, False)
                board.board[to[0]][to[1] + 1] = Rook(True, False)
                board.board[start[0]][start[1]] = None
                board.board[7][0] = None
                return True

            elif king_is_in_check:
                print(alert.king_is_in_check)
                return False

            elif king_will_be_in_check:
                print(alert.king_will_be_in_check)
                return False

        # Black castling to the right
        elif not is_a_white_castling and is_to_the_right:
            king_is_in_check = checker.check_if_king_is_in_check(start, False, board)
            king_will_be_in_check = checker.check_if_king_is_in_check(to, False, board)

            if not king_will_be_in_check and not king_will_be_in_check:
                board.board[to[0]][to[1]] = King(False, False)
                board.board[to[0]][to[1] - 1] = Rook(False, False)
                board.board[start[0]][start[1]] = None
                board.board[0][7] = None
                return True

            elif king_is_in_check:
                print(alert.king_is_in_check)
                return False

            elif king_will_be_in_check:
                print(alert.king_will_be_in_check)
                return False

        # Black castling to the left
        elif not is_a_white_castling and not is_to_the_right:
            king_is_in_check = checker.check_if_king_is_in_check(start, False, board)

            king_will_be_in_check = checker.check_if_king_is_in_check(to, False, board)

            if not king_will_be_in_check and not king_will_be_in_check:
                board.board[to[0]][to[1]] = King(False, False)
                board.board[to[0]][to[1] + 1] = Rook(False, False)
                board.board[start[0]][start[1]] = None
                board.board[0][0] = None
                return True

            elif king_is_in_check:
                print(alert.king_is_in_check)
                return False

            elif king_will_be_in_check:
                print(alert.king_will_be_in_check)
                return False
        else:
            print(alert.incorrect_path)
            return False

    def is_valid_move(self, board, start, to):

        is_the_king_first_move = self.first_move
        is_a_castling_move = abs(start[1] - to[1]) == 2 and start[0] - to[0] == 0

        if is_the_king_first_move and is_a_castling_move:
            is_a_castling_to_the_right = to[1] - start[1] > 0
            return self.do_castling(board, start, to, is_a_castling_to_the_right)

        elif abs(start[0] - to[0]) == 1 or start[0] - to[0] == 0:
            if start[1] - to[1] == 0 or abs(start[1] - to[1]) == 1:
                self.first_move = False
                return True

        else:
            print(alert.incorrect_path)
            return False


class GhostPawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "GP"

    def is_valid_move(self, board, start, to):
        return False


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = "\u265F"
        self.first_move = True

    def is_valid_move(self, board, start, to):
        the_pawn_is_white = self.color
        is_a_straight_move = start[1] == to[1]
        there_is_a_piece_to_taken = board.board[to[0]][to[1]] is not None
        piece_that_will_be_taken = board.board[to[0]][to[1]] if there_is_a_piece_to_taken else None

        if the_pawn_is_white:

            white_diagonal_move = start[0] == to[0] + 1 and (start[1] == to[1] + 1 or start[1] == to[1] - 1)

            if white_diagonal_move:

                if there_is_a_piece_to_taken:
                    self.first_move = False
                    return True
                print(alert.pawn_diagonal_move)
                return False

            if is_a_straight_move:

                is_a_double_move = start[0] - to[0] == 2 and self.first_move
                is_a_basic_move = start[0] - to[0] == 1

                if is_a_double_move or is_a_basic_move:
                    traveled_lines = range(start[0]-1, to[0]-1, -1)

                    for i in traveled_lines:
                        there_is_a_piece_in_the_path = board.board[i][start[1]] is not None
                        if there_is_a_piece_in_the_path:
                            print(alert.blocked_path)
                            return False

                    if is_a_double_move:
                        ghost_pawn_line = start[0]-1
                        board.board[ghost_pawn_line][start[1]] = GhostPawn(self.color)
                        board.white_ghost_piece = (start[0] - 1, start[1])

                    self.first_move = False
                    return True

                print(alert.invalid_move + " or " + alert.pawn_twice_move)
                return False

            print(alert.incorrect_path)
            return False

        else:

            black_diagonal_move = start[0] == to[0] - 1 and (start[1] == to[1] - 1 or start[1] == to[1] + 1)

            if black_diagonal_move:

                if there_is_a_piece_to_taken:
                    self.first_move = False
                    return True

                print(alert.pawn_diagonal_move)
                return False

            if is_a_straight_move:

                is_a_double_move = to[0] - start[0] == 2 and self.first_move
                is_a_basic_move = to[0] - start[0] == 1

                if is_a_double_move or is_a_basic_move:

                    traveled_lines = range(start[0] + 1, to[0] + 1)

                    for i in traveled_lines:

                        there_is_a_piece_in_the_path = board.board[i][start[1]] is not None

                        if there_is_a_piece_in_the_path:
                            print(alert.blocked_path)
                            return False

                    if is_a_double_move:
                        board.board[start[0] + 1][start[1]] = GhostPawn(self.color)
                        board.black_ghost_piece = (start[0] + 1, start[1])

                    self.first_move = False
                    return True

                print(alert.invalid_move + " or " + alert.pawn_twice_move)
                return False

            print(alert.incorrect_path)
            return False
