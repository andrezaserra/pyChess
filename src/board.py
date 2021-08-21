import piece


class Board:
    """
    A class to represent a chess board.

    ...

    Attributes:
    -----------
    board : list[list[Piece]]
        represents a chess board
        
    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
        
    """

    def __init__(self):

        self.board = []

        # Board set-up clean
        for i in range(8):
            self.board.append([None] * 8)

        # White
        self.board[7][0] = piece.Rook(True)
        self.board[7][1] = piece.Knight(True)
        self.board[7][2] = piece.Bishop(True)
        self.board[7][3] = piece.Queen(True)
        self.board[7][4] = piece.King(True)
        self.board[7][5] = piece.Bishop(True)
        self.board[7][6] = piece.Knight(True)
        self.board[7][7] = piece.Rook(True)
        for i in range(8):
            self.board[6][i] = piece.Pawn(True)

        # Black
        self.board[0][0] = piece.Rook(False)
        self.board[0][1] = piece.Knight(False)
        self.board[0][2] = piece.Bishop(False)
        self.board[0][3] = piece.Queen(False)
        self.board[0][4] = piece.King(False)
        self.board[0][5] = piece.Bishop(False)
        self.board[0][6] = piece.Knight(False)
        self.board[0][7] = piece.Rook(False)
        for i in range(8):
            self.board[1][i] = piece.Pawn(False)

    def print_board(self):

        column_legend = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        legend_line = ['8', '7', '6', '5', '4', '3', '2', '1']

        columns_string = "**"
        for i in range(8):
            columns_string += " " + column_legend[i] + "  "
        columns_string += "**"

        print(columns_string)

        for i in range(len(self.board)):
            lines_string = legend_line[i] + "|"
            for j in self.board[i]:
                if j is None or j.name == 'GP':
                    lines_string += "   |"
                elif len(j.name) == 2:
                    lines_string += (" " + str(j) + "|")
                else:
                    lines_string += (" " + str(j) + " |")
            print(lines_string + legend_line[i])

        print(columns_string)

