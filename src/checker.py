import alert


# ok
def check_straight_paths(board, start, to):

    keep_same_line = start[0] == to[0]

    if keep_same_line:
        smaller_column = start[1] if start[1] < to[1] else to[1]
        bigger_column = start[1] if start[1] > to[1] else to[1]

        for i in range(smaller_column + 1, bigger_column):
            if board.board[start[0]][i] is not None:
                print(alert.blocked_path)
                return False

        return True

    else:
        smaller_line = start[0] if start[0] < to[0] else to[0]
        bigger_line = start[0] if start[0] > to[0] else to[0]

        for i in range(smaller_line + 1, bigger_line):
            if board.board[i][start[1]] is not None:
                print(alert.blocked_path)
                return False

        return True


# ok
def check_diagonal_path(board, start, to):

    move_to_up = to[0] - start[0] > 0
    move_to_right = to[1] - start[1] > 0

    line_iterator = 1 if move_to_up else -1
    column_iterator = 1 if move_to_right else -1

    i = start[0] + line_iterator
    j = start[1] + column_iterator

    while i < to[0] if line_iterator is 1 else i > to[0]:
        if board.board[i][j] is not None:
            print(alert.blocked_path)
            # print("At: " + str((i, j)))
            return False

        i += line_iterator
        j += column_iterator
    return True


def check_for_promotion_pawns(game):
    is_white_player_turn = game.white_player_turn
    i = 0
    while i < 8:
        black_pawn_is_on_eighth_rank = game.board.board[0][i] is not None and game.board.board[0][i].name == "\u265F"
        white_pawn_is_on_eighth_rank = game.board.board[7][i] is not None and game.board.board[7][i].name == "\u265F"

        if not is_white_player_turn and black_pawn_is_on_eighth_rank:
            game.promotion((0, i))
            break
        elif is_white_player_turn and white_pawn_is_on_eighth_rank:
            game.promotion((7, i))
            break
        i += 1


def check_knight(color, board, pos):
    """
    Check if there is a knight of the opposite `color` at
    position `pos` on board `board`.

    color : bool
        True if white

    board : Board
        Representation of the current chess board

    pos : tup
        Indices to check if there's is a knight

    Precondition `pos` is a valid position on the board.
    """
    piece = board.board[pos[0]][pos[1]]
    if piece != None and piece.color != color and piece.name == 'N':
        return False
    return True


def check_diag_castle(color, board, start, to):
    """
    Checks the diagonal path from `start` (non-inclusive) to `to` (inclusive)
    on board `board` for any threats from the opposite `color`

    color : bool
        True if white

    board : Board
        Representation of the current chess board

    start : tup
        Starting point of the diagonal path

    to : tup
        Ending point of the diagonal path

    Precondition: `start` and `to` are valid positions on the board
    """

    if abs(start[0] - to[0]) != abs(start[1] - to[1]):
        print(alert.incorrect_path)
        return False

    x_pos = 1 if to[0] - start[0] > 0 else -1
    y_pos = 1 if to[1] - start[1] > 0 else -1

    i = start[0] + x_pos
    j = start[1] + y_pos

    exists_piece = board.board[i][j] != None
    if exists_piece and (board.board[i][j].name == 'P' or board.board[i][j].name == 'K') and \
            board.board[i][j].color != color:
        return False

    while (i <= to[0] if x_pos == 1 else i >= to[0]):
        if exists_piece and board.board[i][j].color != color:
            if board.board[i][j].name in ['B', 'Q']:
                return False
            else:
                return True
        if exists_piece and board.board[i][j].color == color:
            return True
        i += x_pos
        j += y_pos
        exists_piece = board.board[i][j] != None

    return True


def check_updown_castle(color, board, start, to):
    """
    Checks if there are any threats from the opposite `color` from `start` (non-inclusive)
    to `to` (inclusive) on board `board`.

    color : bool
        True if white's turn

    board : Board
        Representation of the current board

    start : tup
        Start location of vertical path

    to : tup
        End location of vertical path
    """

    x_pos = 1 if to[0] - start[0] > 0 else -1
    i = start[0] + x_pos

    front_piece = board[i][start[1]]
    if front_piece != None and front_piece.name == 'K' and front_piece.color != color:
        return False

    while (i <= to[0] if x_pos == 1 else i >= to[0]):
        if board.board[i][start[1]] != None and board.board[i][start[1]].color != color:
            if board.board[i][start[1]].name in ['R', 'Q']:
                return False
            else:
                return True
        if board.board[i][start[1]] != None and board.board[i][start[1]].color == color:
            return True

    return True
