import support_function as spf
import time


def BFS_search(board, list_check_point):
    start_time = time.time()
    ''' BFS SEARCH'''
    ''' Kiểm tra có thắng hay không '''
    if spf.check_win(board,list_check_point):
        print("Found win")
        return [board]
    ''' Trạng thái bắt đầu '''
    ''' Khai báo 1 state '''
    start_state = spf.state(board, None, list_check_point)
    ''' Khởi tạo 2 mảng cho BFS '''
    list_state = [start_state]
    list_visit = [start_state]
    ''' Lặp qua những danh sách đã thăm '''
    while len(list_visit) != 0:
        ''' Lấy trạng thái hiện tại để tìm kiếm'''
        now_state = list_visit.pop(0)
        ''' Lấy vị trí hiện tại của người dùng '''
        cur_pos = spf.find_position_player(now_state.board)      

        ''' Lấy danh sách các vị trị của ngưới dùng có thể di chuyển '''
        list_can_move = spf.get_next_pos(now_state.board, cur_pos)

        ''' Tạo trạng thái mới từ vị trí có thể di chuyển '''
        for next_pos in list_can_move:
            ''' Tạo bảng mới '''
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            ''' Nếu đã tồn tại state thì bỏ qua'''
            if spf.is_board_exist(new_board, list_state):
                continue
            ''' Nếu hộp bị kẹt thì bỏ qua '''
            if spf.is_board_can_not_win(new_board, list_check_point):
                continue
            ''' Nếu tất cả hộp bị kẹt thì bỏ qua '''
            if spf.is_all_boxes_stuck(new_board, list_check_point):
                continue

            ''' Tạo state mới'''
            new_state = spf.state(new_board, now_state, list_check_point)
            ''' Kiểm tra trạng thái mới xem có thể  '''
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            
            ''' Thêm trang thái hiện tại vào danh sách và danh sách đã duyệt qua'''
            list_state.append(new_state)
            list_visit.append(new_state)

            ''' Tính timeout '''
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:
            return []
    print("Not Found")
    return []