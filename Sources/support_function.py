from copy import deepcopy

TIME_OUT = 1800


class state:
    def __init__(self, board, state_parent, list_check_point):
        '''Lưu trữ bảng hiện tại và trạng thái cha'''
        self.board = board
        self.state_parent = state_parent
        self.check_points = deepcopy(list_check_point)
    ''' Đệ quy để lấy ra danh sách kết quả '''
    def get_line(self):
        if self.state_parent is None:
            return [self.board]
        # [[init],[bước 2],...,[đích]]
        return (self.state_parent).get_line() + [self.board]

''' Kiểm tra thắng hay không '''
def check_win(board, list_check_point):
    for p in list_check_point:
        if board[p[0]][p[1]] != '$':
            return False
    return True

# ''' coppy ma trận board hiện tại '''
def assign_matrix(board):
    return [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

''' Tìm vị trí của ng chơi trên board '''
def find_position_player(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '@':
                return (x,y)
    return (-1,-1)  # error board

''' So sánh 2 broad'''
def compare_matrix(board_A, board_B):
    '''Trả về true nếu hai board giống nhau'''
    if len(board_A) != len(board_B) or len(board_A[0]) != len(board_B[0]):
        return False
    for i in range(len(board_A)):
        for j in range(len(board_A[0])):
            if board_A[i][j] != board_B[i][j]:
                return False
    return True

''' Kiểm tra board có tồn tại trong list_state'''
def is_board_exist(board, list_state):
    for state in list_state:
        if compare_matrix(state.board, board):
            return True
    return False

''' Kiểm tra xem 1 hộp có là trạng thái đích không '''
def is_box_on_check_point(box, list_check_point):
    for check_point in list_check_point:
        if box[0] == check_point[0] and box[1] == check_point[1]:
            return True
    return False

''' Kiểm tra xung quanh hộp có phải tường hay ko'''
def check_in_corner(board, x, y, list_check_point):
    if board[x-1][y-1] == '#':
        if board[x-1][y] == '#' and board[x][y-1] == '#':
            if not is_box_on_check_point((x,y), list_check_point):
                return True
    if board[x+1][y-1] == '#':
        if board[x+1][y] == '#' and board[x][y-1] == '#':
            if not is_box_on_check_point((x,y), list_check_point):
                return True
    if board[x-1][y+1] == '#':
        if board[x-1][y] == '#' and board[x][y+1] == '#':
            if not is_box_on_check_point((x,y), list_check_point):
                return True
    if board[x+1][y+1] == '#':
        if board[x+1][y] == '#' and board[x][y+1] == '#':
            if not is_box_on_check_point((x,y), list_check_point):
                return True
    return False

''' Tìm vị trí của các hộp trên broad '''
def find_boxes_position(board):
    result = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                result.append((i,j))
    return result


''' Kiểm tra 1 hộp có thể di chuyển được không'''
def is_box_can_be_moved(board, box_position):
    left_move = (box_position[0], box_position[1] - 1) 
    right_move = (box_position[0], box_position[1] + 1)
    up_move = (box_position[0] - 1, box_position[1])
    down_move = (box_position[0] + 1, box_position[1])
    if (board[left_move[0]][left_move[1]] == ' ' or board[left_move[0]][left_move[1]] == '%' or board[left_move[0]][left_move[1]] == '@') and board[right_move[0]][right_move[1]] != '#' and board[right_move[0]][right_move[1]] != '$':
        return True
    if (board[right_move[0]][right_move[1]] == ' ' or board[right_move[0]][right_move[1]] == '%' or board[right_move[0]][right_move[1]] == '@') and board[left_move[0]][left_move[1]] != '#' and board[left_move[0]][left_move[1]] != '$':
        return True
    if (board[up_move[0]][up_move[1]] == ' ' or board[up_move[0]][up_move[1]] == '%' or board[up_move[0]][up_move[1]] == '@') and board[down_move[0]][down_move[1]] != '#' and board[down_move[0]][down_move[1]] != '$':
        return True
    if (board[down_move[0]][down_move[1]] == ' ' or board[down_move[0]][down_move[1]] == '%' or board[down_move[0]][down_move[1]] == '@') and board[up_move[0]][up_move[1]] != '#' and board[up_move[0]][up_move[1]] != '$':
        return True
    return False

''' Kiểm tra tất cả các hộp có bị kẹt ko '''
def is_all_boxes_stuck(board, list_check_point):
    box_positions = find_boxes_position(board)
    result = True
    for box_position in box_positions:
        if is_box_on_check_point(box_position, list_check_point):
            return False
        if is_box_can_be_moved(board, box_position):
            result = False
    return result

''' Kiểm tra đường đi board có khả năng chiến thắng không'''
def is_board_can_not_win(board, list_check_point):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == '$':
                if check_in_corner(board, x, y, list_check_point):
                    return True
    return False

''' Lấy các vị trí có thể di chuyển của người dùng '''
def get_next_pos(board, cur_pos):
    x,y = cur_pos[0], cur_pos[1]
    list_can_move = []
    # MOVE UP (x - 1, y)
    if 0 <= x - 1 < len(board):
        value = board[x - 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x - 1, y))
        elif value == '$' and 0 <= x - 2 < len(board):
            next_pos_box = board[x - 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x - 1, y))
    # MOVE DOWN (x + 1, y)
    if 0 <= x + 1 < len(board):
        value = board[x + 1][y]
        if value == ' ' or value == '%':
            list_can_move.append((x + 1, y))
        elif value == '$' and 0 <= x + 2 < len(board):
            next_pos_box = board[x + 2][y]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x + 1, y))
    # MOVE LEFT (x, y - 1)
    if 0 <= y - 1 < len(board[0]):
        value = board[x][y - 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y - 1))
        elif value == '$' and 0 <= y - 2 < len(board[0]):
            next_pos_box = board[x][y - 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y - 1))
    # MOVE RIGHT (x, y + 1)
    if 0 <= y + 1 < len(board[0]):
        value = board[x][y + 1]
        if value == ' ' or value == '%':
            list_can_move.append((x, y + 1))
        elif value == '$' and 0 <= y + 2 < len(board[0]):
            next_pos_box = board[x][y + 2]
            if next_pos_box != '#' and next_pos_box != '$':
                list_can_move.append((x, y + 1))
    return list_can_move

''' Di chuyển từ vị trí hiện tại tới vị trí tiếp theo '''
def move(board, next_pos, cur_pos, list_check_point):
    '''trả về 1 board mới'''
    # tạo board mới trùng với board hiện tại
    new_board = assign_matrix(board) 
    # tìm vị trí tiếp theo có thể di chuyển hộp
    if new_board[next_pos[0]][next_pos[1]] == '$':
        x = 2*next_pos[0] - cur_pos[0] 
        y = 2*next_pos[1] - cur_pos[1]
        new_board[x][y] = '$'
    # Di chuyển người chơi
    new_board[next_pos[0]][next_pos[1]] = '@'
    new_board[cur_pos[0]][cur_pos[1]] = ' '

    # Giữ các vị trí checkpoint
    for p in list_check_point:
        if new_board[p[0]][p[1]] == ' ':
            new_board[p[0]][p[1]] = '%'
    return new_board 

