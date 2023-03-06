
def is_sq_in_board(board,y,x):

    try:
        temp = board[y][x]
    except IndexError:
        return
    else:
        return True

def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):

    # count if sequence has col immediately before or after (too long)
    if board[y_start+length*d_y][x_start+length*d_x] == col or board[y_start-d_y][x_start-d_x] == col:
        return False

    # count if sequence is at least complete
    for i in range(length-1):
        if board[y_start][x_start] == board[y_start+d_y][x_start+d_x] == col:
            y_start += d_y
            x_start += d_x
            continue
        else:
            return False
    return True

################

def is_empty(board):
    # no stones/ aka all " "
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    num_bounds = 0
    #
    marker = board[y_end][x_end] # either " ", "b", "w"
    if marker == "b":
        marker_opposite = "w"
    else:
        marker_opposite = "b"

    # bound on end counting side (start strand):
    try:
        if board[y_end - length*d_y][x_end - length*d_x] == marker_opposite:
            num_bounds += 1
    except IndexError:
        num_bounds += 1  # this means out of range error

    # bound on start counting side (end strand):
    try:
        if board[y_end + d_y][x_end + d_x] == marker_opposite:
            num_bounds +=1
    except IndexError:
        num_bounds += 1 # this means out of range error

    match num_bounds:
        case 0:
            return "OPEN"
        case 1:
            return "SEMIOPEN"
        case 2:
            return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    # start coordinate on edge of board
    break_condition = False
    open_seq_count = 0
    semi_open_seq_count = 0
    temp_list = [board[y_start][x_start]]
    # makes the temp_list
    for i in range(len(board)): # max row size = 8
        try:
            if x_start+d_x == -1:
                break
            else:
                temp_list.append(board[y_start+d_y][x_start+d_x])
        except IndexError:
            break
        else:
            y_start += d_y
            x_start += d_x

    for m in range(len(temp_list) - length + 1):
        # count if sequence is at least complete starting at position m
        for i in range(length - 1):
            if temp_list[m] == temp_list[m + 1] == col:
                pass
            else:
                break_condition = True
                break
            m += 1
        if break_condition == False:
            # check if any of the following tests will be out of bounds
            # since farthest program checks is index m+1
            closed_ends = 0
            try:
                temp_var = temp_list[m + 1]

            except IndexError:
                # can't be open, is it at least semi-open?
                if temp_list[m - length] == " ":
                    semi_open_seq_count += 1
            else:  # within index
                closed_ends += 1
                if m - length == -1:
                    if temp_list[m + 1] == " ":
                        semi_open_seq_count += 1
                else:
                    closed_ends += 1
            # try:
            #     temp_var = temp_list[m-length]
            #     # NOTE Error here may be m-length = -1, loops back
            # except IndexError:
            #     # can't be open, is it at least semi-open?
            #     if temp_list[m+1] == " ":
            #         semi_open_seq_count += 1
            # else:
            #     closed_ends += 1

            if closed_ends == 2:
                if temp_list[m] == temp_list[m + 1] == col or temp_list[m] == temp_list[m - length] == col:  # too long?
                    pass
                else:
                    if temp_list[m - length] == " " and temp_list[
                        m + 1] == " ":  # m-(length) checks open space at start of seq, m+1 checks open space at end of seq
                        open_seq_count += 1
                    else:
                        if temp_list[m - length] == " " or temp_list[
                            m + 1] == " ":  # either one, wont be both and or first case would have caught it
                            semi_open_seq_count += 1
        else:
            break_condition = False

    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    # brute force strategy:
    # y_start, x_start - test on EVERY index of board on outer rim
    # d_y, d_x - 4 tuples (0,1) - right, (1,0) - down, (1,1) - ↘, (1,-1) - ↙
    # detect_row(board, col, y_start, x_start, length, d_y, d_x) returns a tuple, and inputs these vars

    # HORIZONTALS:
    for y in range(len(board)):
        temp_tuple = detect_row(board, col, y, 0, length, 0, 1)
        open_seq_count += temp_tuple[0]
        semi_open_seq_count += temp_tuple[1]
    # VERTICALS:
    for x in range(len(board[0])):
        temp_tuple = detect_row(board, col, 0, x, length, 1, 0)
        open_seq_count += temp_tuple[0]
        semi_open_seq_count += temp_tuple[1]
    # Left column:
    for y in range(len(board)):
        temp_tuple = detect_row(board, col, y, 0, length, 1, 1)
        open_seq_count += temp_tuple[0]
        semi_open_seq_count += temp_tuple[1]
    # Top row:
    for x in range(len(board[0])-2):
        for delta in [(1,1),(1,-1)]:
            temp_tuple = detect_row(board, col, 0, x+1, length, delta[0], delta[1])
            open_seq_count += temp_tuple[0]
            semi_open_seq_count += temp_tuple[1]
    # # Bottom row:
    # for x in range(len(board[0])-1):
    #     for delta in [(1,1),(1,-1)]:
    #         temp_tuple = detect_row(board, col, len(board)-1, x+1, length, delta[0], delta[1])
    #         open_seq_count += temp_tuple[0]
    #         semi_open_seq_count += temp_tuple[1]
    # Right column:
    for y in range(len(board)):
        temp_tuple = detect_row(board, col, y, len(board[0])-1, length, 1, -1)
        open_seq_count += temp_tuple[0]
        semi_open_seq_count += temp_tuple[1]

    return open_seq_count, semi_open_seq_count


def search_max(board):
    max_move_score = -696969696969696969
    move_y, move_x = 0,0
    # loop thru all empties
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                board[y][x] = "b"
                if score(board) > max_move_score:
                    max_move_score = score(board)
                    move_y = y
                    move_x = x
                board[y][x] = " "
    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    def detect_row_all(board, col, y_start, x_start, length, d_y, d_x):
        # start coordinate on edge of board
        break_condition = False
        seq = 0
        temp_list = [board[y_start][x_start]]
        # makes the temp_list
        for i in range(len(board)):  # max row size = 8
            try:
                if x_start + d_x == -1:
                    break
                else:
                    temp_list.append(board[y_start + d_y][x_start + d_x])
            except IndexError:
                break
            else:
                y_start += d_y
                x_start += d_x

        for m in range(len(temp_list) - length + 1):
            # count if sequence is at least complete starting at position m
            for i in range(length - 1):
                if temp_list[m] == temp_list[m + 1] == col:
                    pass
                else:
                    break_condition = True
                    break
                m += 1

            if break_condition == False:
                try:
                    temp_var = temp_list[m+1]
                except IndexError:
                    if temp_list[m] == temp_list[m-length] == col and m-length != -1:
                        pass
                    else:
                        seq += 1
                else:
                    if temp_list[m] == temp_list[m + 1] == col or temp_list[m] == temp_list[
                        m - length] == col and m-length != -1:  # too long?
                        pass
                    else:
                        seq += 1
            else:
                break_condition = False
        return seq

    def detect_rows_all(board, col, length):
        seq = 0
        # brute force strategy:
        # y_start, x_start - test on EVERY index of board on outer rim
        # d_y, d_x - 4 tuples (0,1) - right, (1,0) - down, (1,1) - ↘, (1,-1) - ↙
        # detect_row(board, col, y_start, x_start, length, d_y, d_x) returns a tuple, and inputs these vars

        # HORIZONTALS:
        for y in range(len(board)):
            temp_tuple = detect_row_all(board, col, y, 0, length, 0, 1)
            seq += temp_tuple
        # VERTICALS:
        for x in range(len(board[0])):
            temp_tuple = detect_row_all(board, col, 0, x, length, 1, 0)
            seq += temp_tuple
        # Left column:
        for y in range(len(board)):
            temp_tuple = detect_row_all(board, col, y, 0, length, 1, 1)
            seq += temp_tuple
        # Top row:
        for x in range(len(board[0]) - 2):
            for delta in [(1, 1), (1, -1)]:
                temp_tuple = detect_row_all(board, col, 0, x + 1, length, delta[0], delta[1])
                seq += temp_tuple
        # Right column:
        for y in range(len(board)):
            temp_tuple = detect_row_all(board, col, y, len(board[0]) - 1, length, 1, -1)
            seq += temp_tuple

        return seq


    seqs2 = detect_rows_all(board, "b", 5)
    if seqs2 >= 1: # at least one complete 5-sequence of blacks
        return "Black won"

    seqs4 = detect_rows_all(board, "w", 5)
    if seqs4 >= 1: # at least one complete 5-sequence of blacks
        return "White won"
    # full board or no winner yet
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ": # if not full board yet
                return "Continue playing"
    return "Draw" # only runs this code when all options are exhausted -- full board

def print_board(board):
    s = "*"
    for i in range(len(board[0]) - 1):
        s += str(i % 10) + "|"
    s += str((len(board[0]) - 1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0]) - 1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0]) - 1])

        s += "*\n"
    s += (len(board[0]) * 2 + 1) * "*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5;
    y = 1;
    d_x = 0;
    d_y = 1;
    length = 3;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6;
    y = 0;
    d_x = 0;
    d_y = 1;
    length = 4;
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4, 6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5;
    x = 2;
    d_x = 0;
    d_y = 1;
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3;
    x = 5;
    d_x = -1;
    d_y = 1;
    length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5;
    x = 3;
    d_x = -1;
    d_y = 1;
    length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    play_gomoku(8)


    # print(is_sq_in_board(board, 8,9))
    # print(is_sq_in_board(board, 6,7))
    # put_seq_on_board(board, 1, 1, 1, 0, 3, "b")
    # print_board(board)
    # print(is_sequence_complete(board, "b", 1, 1, 3, 1, 0))
    # print(is_sequence_complete(board, "b", 1, 1, 5, 1, 0))
    # put_seq_on_board(board, 0, 1, 1, 0, 4, "b")
    # print_board(board)
    # print(is_sequence_complete(board, "b", 1, 1, 3, 1, 0))





