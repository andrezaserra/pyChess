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

    while i < to[0] if line_iterator == 1 else i > to[0]:
        if board.board[i][j] is not None:
            print(alert.blocked_path)
            # print("At: " + str((i, j)))
            return False

        i += line_iterator
        j += column_iterator
    return True


# ok
def check_for_promotion_pawns(game):
    is_white_player_turn = game.is_white_player_turn
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


# returns true if it find a threat in 'position_to_check'
def check_for_opponent_knight(my_color, board, start, check_right, check_up):

    check_to_black_side = check_up
    check_to_right_side = check_right

    i = start[0] + 2 if check_up else start[0] - 2
    j = start[1] + 1 if check_right else start[1] + 1

    if 0 < i < 7 and 0 < j < 7:
        square_to_check = board.board[i][j]
        exists_piece = square_to_check is not None

        if exists_piece:

            piece = square_to_check
            piece_is_a_opponent_knight = piece.color != my_color and piece.name == "\u265E"

            if piece_is_a_opponent_knight:
                return True

    i = start[0] + 1 if check_up else start[0] - 1
    j = start[1] + 2 if check_right else start[1] + 2

    if 0 < i < 7 and 0 < j < 7:
        square_to_check = board.board[i][j]
        exists_piece = square_to_check is not None

        if exists_piece:

            piece = square_to_check
            piece_is_a_opponent_knight = piece.color != my_color and piece.name == "\u265E"

            if piece_is_a_opponent_knight:
                return True

    return False


# returns true if it find a threat on the piece's straight path to the end of the board
def check_for_opponent_in_straight(my_color, board, start, check_right, check_up):
    check_to_black_side = check_up
    check_to_right_side = check_right

    line_iterator = 1 if check_to_black_side else -1
    column_iterator = 1 if check_to_right_side else -1

    i = start[0] + line_iterator
    j = start[1] + column_iterator

    if 0 < i < 7 and 0 < j < 7:

        front_square = board.board[i][start[1]]
        exists_front_piece = front_square is not None

        side_square = board.board[start[1]][j]
        exists_side_piece = side_square is not None

        if exists_front_piece:
            front_piece = front_square

            the_piece_is_opponent_king = front_piece.name == "\u265A" and front_piece.color != my_color
            the_piece_is_opponent_rook_or_queen = front_piece.color != my_color and front_piece.name in ["\u265c", "\u265B"]

            if front_piece.color != my_color and (the_piece_is_opponent_king or the_piece_is_opponent_rook_or_queen):
                print("there is a " + str(front_piece.name) + "in the path")
                return True

        while 0 < i < 7 and 0 < j < 7:
            if exists_front_piece:

                front_piece = front_square
                the_piece_is_opponent_rook_or_queen = front_piece.color != my_color and front_piece.name in ["\u265c", "\u265B"]

                if the_piece_is_opponent_rook_or_queen:
                    return True

            i += line_iterator

            front_square = board.board[i][start[1]]
            exists_front_piece = front_square is not None

        if exists_side_piece:
            side_piece = side_square

            the_piece_is_opponent_king = side_piece.name == "\u265A" and side_piece.color != my_color
            the_piece_is_opponent_rook_or_queen = side_piece.color != my_color and side_piece.name in ["\u265c", "\u265B"]

            if side_piece.color != my_color and (the_piece_is_opponent_king or the_piece_is_opponent_rook_or_queen):
                print("there is a " + str(side_piece.name) + "in the path")
                return True

        while 0 < i < 7 and 0 < j < 7:
            if exists_side_piece:

                side_piece = side_square
                the_piece_is_opponent_rook_or_queen = side_piece.color != my_color and side_piece.name in ["\u265c", "\u265B"]

                if the_piece_is_opponent_rook_or_queen:
                    return True

            j += column_iterator

            side_square = board.board[start[1]][j]
            exists_side_piece = side_square is not None

    return False


# returns true if it find a threat on the piece's diagonal path to the end of the board
def check_for_opponent_in_diagonal(my_color, board, start, check_right, check_up):

    check_to_black_side = check_up
    check_to_right_side = check_right

    line_iterator = 1 if check_to_black_side else -1
    column_iterator = 1 if check_to_right_side else -1

    i = start[0] + line_iterator
    j = start[1] + column_iterator

    if 0 < i < 7 and 0 < j < 7:
        square_to_check = board.board[i][j]

        if square_to_check is not None:
            piece = square_to_check
            the_piece_is_pawn = piece.name == "\u265F"
            the_piece_is_king = piece.name == "\u265A"
            the_piece_is_queen = piece.name == "\u265B"

            if (the_piece_is_pawn or the_piece_is_king or the_piece_is_queen) and piece.color != my_color:
                print("threat in diagonal: " + str(piece.name))
                return True

        while 0 < i < 7 and 0 < j < 7:

            if square_to_check is not None:
                piece = square_to_check
                the_piece_is_bishop = piece.name == "\u265D"
                the_piece_is_queen = piece.name == "\u265B"

                if (the_piece_is_bishop or the_piece_is_queen) and piece.color != my_color:
                    print("threat in diagonal: " + str(piece.name))
                    return True
                elif piece.color == my_color:
                    return False

            i += line_iterator
            j += column_iterator

            square_to_check = board.board[i][j]
            exists_piece = square_to_check is not None

    return False


def check_if_king_is_in_check(king_position, king_color, board):
    checking_diagonals = check_for_opponent_in_diagonal(king_color, board, king_position, True, True) or \
                         check_for_opponent_in_diagonal(king_color, board, king_position, True, False) or \
                         check_for_opponent_in_diagonal(king_color, board, king_position, False, True) or \
                         check_for_opponent_in_diagonal(king_color, board, king_position, False, False)

    checking_straights = check_for_opponent_in_straight(king_color, board, king_position, True, True) or \
                         check_for_opponent_in_straight(king_color, board, king_position, True, False) or \
                         check_for_opponent_in_straight(king_color, board, king_position, False, True) or \
                         check_for_opponent_in_straight(king_color, board, king_position, False, False)

    checking_knights = check_for_opponent_knight(king_color, board, king_position, True, True) or \
                       check_for_opponent_knight(king_color, board, king_position, True, False) or \
                       check_for_opponent_knight(king_color, board, king_position, False, True) or \
                       check_for_opponent_knight(king_color, board, king_position, False, False)

    the_king_is_in_check = checking_diagonals or checking_straights or checking_knights

    if the_king_is_in_check:
        return True

    return False

