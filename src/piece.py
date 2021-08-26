import checker
import alert


# ok
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


# ok
class Rook(Piece):
    def __init__(self, color, is_first_move=True):
        super().__init__(color)
        self.name = "\u265c"
        self.is_first_move = is_first_move

    def is_valid_move(self, board, start, to):
        keep_same_line = start[0] == to[0]
        keep_same_column = start[1] == to[1]

        if keep_same_line or keep_same_column:
            return checker.check_straight_paths(board, start, to)

        print(alert.incorrect_path)
        return False


# ok
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


# ok
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


# ok
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
            return checker.check_straight_paths(board, start, to)

        print(alert.incorrect_path)
        return False


class King(Piece):
    def __init__(self, color, first_move=True):
        super().__init__(color)
        self.name = "\u265A"
        self.first_move = first_move

    def can_castle(self, board, start, to, right):
        """
        Returns True if king at `start` can move to `to` on `board`.

        board : Board
            Represents the current board
        start : tup
            Position of the king
        to : tup
            Position of the resulting move
        right: bool
            True if castling to the right False otherwise

        Precondition: moving from `start` to `to` is a castling move
        """

        # White castling to the right
        if self.color and right:
            knight_attack = checker.check_knight(self.color, board, (6, 3)) and \
                            checker.check_knight(self.color, board, (6, 4)) and \
                            checker.check_knight(self.color, board, (5, 4)) and \
                            checker.check_knight(self.color, board, (5, 5)) and \
                            checker.check_knight(self.color, board, (5, 6)) and \
                            checker.check_knight(self.color, board, (5, 7)) and \
                            checker.check_knight(self.color, board, (6, 7))
            if not knight_attack:
                return False

            diags = checker.check_diag_castle(self.color, board, (7, 5), (2, 0)) and \
                    checker.check_diag_castle(self.color, board, (7, 6), (1, 0)) and \
                    checker.check_diag_castle(self.color, board, (7, 5), (5, 7)) and \
                    checker.check_diag_castle(self.color, board, (7, 6), (6, 7))
            if not diags:
                return False

            updowns = checker.check_updown_castle(self.color, board, (7, 5), (0, 5)) and \
                      checker.check_updown_castle(self.color, board, (7, 6), (0, 6))
            if not updowns:
                return False

            board.board[to[0]][to[1]] = King(True, False)
            board.board[to[0]][to[1] - 1] = Rook(True, False)
            board.board[start[0]][start[1]] = None
            board.board[7][7] = None
            return True

        # White castling to the left
        if self.color and not right:
            knight_attack = checker.check_knight(self.color, board, (6, 0)) and \
                            checker.check_knight(self.color, board, (6, 1)) and \
                            checker.check_knight(self.color, board, (5, 1)) and \
                            checker.check_knight(self.color, board, (5, 2)) and \
                            checker.check_knight(self.color, board, (5, 3)) and \
                            checker.check_knight(self.color, board, (5, 4)) and \
                            checker.check_knight(self.color, board, (6, 4)) and \
                            checker.check_knight(self.color, board, (6, 5))
            if not knight_attack:
                return False

            diags = checker.check_diag_castle(self.color, board, (7, 2), (5, 0)) and \
                    checker.check_diag_castle(self.color, board, (7, 3), (4, 0)) and \
                    checker.check_diag_castle(self.color, board, (7, 2), (2, 7)) and \
                    checker.check_diag_castle(self.color, board, (7, 3), (3, 7))
            if not diags:
                return False

            updowns = checker.check_updown_castle(self.color, board, (7, 2), (0, 2)) and \
                      checker.check_updown_castle(self.color, board, (7, 3), (0, 3))
            if not updowns:
                return False
            board.board[to[0]][to[1]] = King(True, False)
            board.board[to[0]][to[1] + 1] = Rook(True, False)
            board.board[start[0]][start[1]] = None
            board.board[7][0] = None

            return True

        # Black castling to the right
        if not self.color and right:
            knight_attack = checker.check_knight(self.color, board, (1, 3)) and \
                            checker.check_knight(self.color, board, (1, 4)) and \
                            checker.check_knight(self.color, board, (1, 7)) and \
                            checker.check_knight(self.color, board, (2, 4)) and \
                            checker.check_knight(self.color, board, (2, 5)) and \
                            checker.check_knight(self.color, board, (2, 6)) and \
                            checker.check_knight(self.color, board, (2, 7))
            if not knight_attack:
                return False

            diags = checker.check_diag_castle(self.color, board, (0, 5), (5, 0)) and \
                    checker.check_diag_castle(self.color, board, (0, 6), (6, 0)) and \
                    checker.check_diag_castle(self.color, board, (0, 5), (2, 7)) and \
                    checker.check_diag_castle(self.color, board, (0, 6), (1, 7))
            if not diags:
                return False

            updowns = checker.check_updown_castle(self.color, board, (0, 2), (7, 2)) and \
                      checker.check_updown_castle(self.color, board, (0, 3), (7, 3))
            if not updowns:
                return False

            board.board[to[0]][to[1]] = King(False, False)
            board.board[to[0]][to[1] - 1] = Rook(False, False)
            board.board[start[0]][start[1]] = None
            board.board[0][7] = None

            return True

        # Black castling to the left
        if not self.color and not right:
            knight_attack = checker.check_knight(self.color, board, (1, 0)) and \
                            checker.check_knight(self.color, board, (1, 1)) and \
                            checker.check_knight(self.color, board, (1, 4)) and \
                            checker.check_knight(self.color, board, (1, 5)) and \
                            checker.check_knight(self.color, board, (2, 1)) and \
                            checker.check_knight(self.color, board, (2, 2)) and \
                            checker.check_knight(self.color, board, (2, 3)) and \
                            checker.check_knight(self.color, board, (2, 4))
            if not knight_attack:
                return False

            diags = checker.check_diag_castle(self.color, board, (0, 2), (5, 7)) and \
                    checker.check_diag_castle(self.color, board, (0, 3), (4, 7)) and \
                    checker.check_diag_castle(self.color, board, (0, 2), (2, 0)) and \
                    checker.check_diag_castle(self.color, board, (0, 3), (3, 0))
            if not diags:
                return False

            updowns = checker.check_updown_castle(self.color, board, (0, 2), (7, 2)) and \
                      checker.check_updown_castle(self.color, board, (0, 3), (7, 3))
            if not updowns:
                return False

            board.board[to[0]][to[1]] = King(False, False)
            board.board[to[0]][to[1] + 1] = Rook(False, False)
            board.board[start[0]][start[1]] = None
            board.board[0][0] = None

            return True

    def is_valid_move(self, board, start, to):
        if self.first_move and abs(start[1] - to[1]) == 2 and start[0] - to[0] == 0:
            return self.can_castle(board, start, to, to[1] - start[1] > 0)

        if abs(start[0] - to[0]) == 1 or start[0] - to[0] == 0:
            if start[1] - to[1] == 0 or abs(start[1] - to[1]) == 1:
                self.first_move = False
                return True

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
                    traveled_lines = range(start[0] - 1, to[0] - 1, -1)

                    for i in traveled_lines:
                        there_is_a_piece_in_the_path = board.board[i][start[1]] is not None
                        if there_is_a_piece_in_the_path:
                            print(alert.blocked_path)
                            return False

                    if is_a_double_move:
                        board.board[start[0]-1][start[1]] = GhostPawn(self.color)
                        # board.white_ghost_piece = (start[0] - 1, start[1])

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

                    traveled_lines = range(start[0]+1, to[0]+1)

                    for i in traveled_lines:

                        there_is_a_piece_in_the_path = board.board[i][start[1]] is not None

                        if there_is_a_piece_in_the_path:
                            print(alert.blocked_path)
                            return False

                    if is_a_double_move:
                        board.board[start[0]+1][start[1]] = GhostPawn(self.color)
                        # board.black_ghost_piece = (start[0] + 1, start[1])

                    self.first_move = False
                    return True

                print(alert.invalid_move + " or " + alert.pawn_twice_move)
                return False

            print(alert.incorrect_path)
            return False
