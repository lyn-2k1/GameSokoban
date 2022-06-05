import numpy as np
import os
from colorama import Fore
from colorama import Style
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import bfs
import astar

''' Time out cho các thuật toán: 30 phut '''
TIME_OUT = 1800
''' Lấy đường dẫn của checkpoint(vị trí đúng) và testcase(bản đồ) '''
path_board = os.getcwd() + '\\Sources\\..\\Testcases'
path_checkpoint = os.getcwd() + '\\Sources\\..\\Checkpoints'

# print(path_board)

''' Duyệt file TESTCASE Và Trả về danh sánh các bản đồ '''
def get_boards():
    os.chdir(path_board)
    list_boards = [] 
    for file in os.listdir(): 
        if file.endswith(".txt"):
            file_path = f"{path_board}\{file}"
            board = get_board(file_path)
            list_boards.append(board)
    return list_boards

''' Duyệt file CHECKPOINT và danh sách các checkpoint '''
def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir(path_checkpoint):
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}\{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point

''' Định dang lại input file txt TESTCASE '''
def format_row(row):
    for i in range(len(row)):
        if row[i] == '1':
            row[i] = '#'
        elif row[i] == 'p':
            row[i] = '@'
        elif row[i] == 'b':
            row[i] = '$'
        elif row[i] == 'c':
            row[i] = '%'

''' Định dạng lại input file txt CHECKPOINT '''
def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result

''' Đọc 1 testcase từ dường dẫn path '''
def get_board(path):
    result = np.loadtxt(f"{path}", dtype=str, delimiter=',')
    for row in result:
        format_row(row)
    return result

''' Đọc 1 checkpoin từ đường dẫn path'''
def get_pair(path):
    result = np.loadtxt(f"{path}", dtype=int, delimiter=',')
    return result

maps = get_boards()
check_points = get_check_points()

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
'''
Load các đối tượng
'''
assets_path = os.getcwd() + "\\..\\Assets"
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '\\player.png')
wall = pygame.image.load(os.getcwd() + '\\wall.png')
box = pygame.image.load(os.getcwd() + '\\box.png')
point = pygame.image.load(os.getcwd() + '\\point.png')
space = pygame.image.load(os.getcwd() + '\\space.png')
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '\\init_background.png')
loading_background = pygame.image.load(os.getcwd() + '\\loading_background.png')
notfound_background = pygame.image.load(os.getcwd() + '\\notfound_background.png')
found_background = pygame.image.load(os.getcwd() + '\\found_background.png')

'''
Hiển thị map
'''
def renderMap(board):
	width = len(board[0])
	height = len(board)
	indent = (640 - width * 32) / 2.0
	for i in range(height):
		for j in range(width):
			screen.blit(space, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '#':
				screen.blit(wall, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '$':
				screen.blit(box, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '%':
				screen.blit(point, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '@':
				screen.blit(player, (j * 32 + indent, i * 32 + 250))
'''
Khởi tạo biến
'''
mapNumber = 0
algorithm = "Breadth First Search"
sceneState = "init"
loading = False

''' hàm SOKOBAN '''
def sokoban():
	running = True
	global sceneState
	global loading
	global algorithm
	global list_board
	global mapNumber
	stateLenght = 0
	currentState = 0
	found = True

	while running:
    	# Tạo background
		screen.blit(init_background, (0, 0))

		# Nếu cảnh là init thì hiện map đầu tiên
		if sceneState == "init":
			#Chọn map và hiển thị
			initGame(maps[mapNumber])
		# Màn chạy thuật toán
		if sceneState == "executing":
			#chọn map
			list_check_point = check_points[mapNumber]

			#BFS
			list_board = bfs.BFS_search(maps[mapNumber], list_check_point) 

			# Kiểm tra chiều dài mảng kết quả
			if len(list_board) > 0:
				sceneState = "playing"
				stateLenght = len(list_board[0])
				currentState = 0
			else:
    			# Trường hợp không tìm được kết quả
				sceneState = "end"
				found = False
		
		if sceneState == "loading":
			loadingGame()
			sceneState = "executing"

		# Màn hình kết thúc
		if sceneState == "end":
			if found:
				foundGame(list_board[0][stateLenght - 1])
			else:
				notfoundGame()

		if sceneState == "playing":
			clock.tick(5)
			renderMap(list_board[0][currentState])
			print(currentState)
			currentState = currentState + 1
			if currentState == stateLenght:
				sceneState = "end"
				found = True
				
		#Kiểm tra sự kiện người dùng ấn phím
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:				
				# Nhấn phím mũi tên để thay đổi map
				if event.key == pygame.K_RIGHT and sceneState == "init":
					if mapNumber < len(maps) - 1:
						mapNumber = mapNumber + 1
				if event.key == pygame.K_LEFT and sceneState == "init":
					if mapNumber > 0:
						mapNumber = mapNumber - 1
				#Nhấn enter để chạy 
				if event.key == pygame.K_RETURN:
					if sceneState == "init":
						sceneState = "loading"
					if sceneState == "end":
						sceneState = "init"
		pygame.display.flip()
	pygame.quit()

''' Màn hình chính hiển thị '''
#Màn hình hiển thị ban đầu
def initGame(map):
	titleSize = pygame.font.Font('gameFont.ttf', 60)
	titleText = titleSize.render('Boom-koban', True, WHITE)
	titleRect = titleText.get_rect(center=(320, 80))
	screen.blit(titleText, titleRect)

	desSize = pygame.font.Font('gameFont.ttf', 20)
	desText = desSize.render('Now, select your map!!!', True, WHITE)
	desRect = desText.get_rect(center=(320, 140))
	screen.blit(desText, desRect)

	mapSize = pygame.font.Font('gameFont.ttf', 30)
	mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
	mapRect = mapText.get_rect(center=(320, 200))
	screen.blit(mapText, mapRect)

	screen.blit(arrow_left, (246, 188))
	screen.blit(arrow_right, (370, 188))

	algorithmSize = pygame.font.Font('gameFont.ttf', 30)
	algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
	algorithmRect = algorithmText.get_rect(center=(320, 600))
	screen.blit(algorithmText, algorithmRect)
	renderMap(map)

''' Màn hình tải'''
#Màn hình tải hiển thị
def loadingGame():
	screen.blit(loading_background, (0, 0))

	fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = fontLoading_1.render('Loading...', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 60))
	screen.blit(text_1, text_rect_1)

	fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = fontLoading_2.render('The problem is being solved, stay right there!', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 100))
	screen.blit(text_2, text_rect_2)

# Hiện màn hình từng bước giải
def foundGame(map):
	screen.blit(found_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 30)
	text_1 = font_1.render('Yeah! The problem is solved!!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)

	renderMap(map)

# Màn hình nếu ko tìm được kết quả
def notfoundGame():
	screen.blit(notfound_background, (0, 0))

	font_1 = pygame.font.Font('gameFont.ttf', 40)
	text_1 = font_1.render('Oh no, I tried my best :(', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20)
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)

	

def main():
	sokoban()

if __name__ == "__main__":
	main()

