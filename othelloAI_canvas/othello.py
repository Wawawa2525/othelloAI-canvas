from .canvas import Canvas
import math
import random

# 定数定義
BLACK = 1
WHITE = 2

# 初期盤面
board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# 石を置けるか確認する関数
def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

# 石を置ける場所があるか確認
def can_place(board, stone):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

# ランダムに石を置く関数
def random_place(board, stone):
    while True:
        x = random.randint(0, len(board[0]) - 1)
        y = random.randint(0, len(board) - 1)
        if can_place_x_y(board, stone, x, y):
            return x, y

# 盤面をコピーする関数
def copy(board):
    return [row[:] for row in board]

# 石を置き、ひっくり返す関数
def move_stone(board, stone, x, y):
    moves = [copy(board)]
    if not can_place_x_y(board, stone, x, y):
        return moves

    board[y][x] = stone
    moves.append(copy(board))
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            stones_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        if stones_to_flip and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for flip_x, flip_y in stones_to_flip:
                board[flip_y][flip_x] = stone
                moves.append(copy(board))

    return moves

# PandaAIクラス
class PandaAI(object):
    def face(self):
        return "🐼"

    def place(self, board, stone):
        x, y = random_place(board, stone)
        return x, y

# ボードを描画する関数
def draw_board(canvas, board):
    ctx = canvas.getContext("2d")
    grid = canvas.width // len(board)
    for y, row in enumerate(board):
        for x, stone in enumerate(row):
            cx = x * grid + grid // 2
            cy = y * grid + grid // 2
            #ctx.fillStyle = "green"
            #ctx.fillRect(x * grid, y * grid, grid, grid)
            if stone != 0:
                ctx.beginPath()
                ctx.arc(cx, cy, grid // 2, 0, 2 * math.pi)
                ctx.fillStyle = "black" if stone == BLACK else "white"
                ctx.fill()
width=300

# AI同士の対戦を行う関数
def ai_vs_ai(ai_black, ai_white, board=None):
    if board is None:
        board = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 0],
            [0, 0, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]

    canvas = Canvas(background="green", grid=300 // 6, width=300, height=300)
    draw_board(canvas, board)

    current_player = BLACK
    ai = {BLACK: ai_black, WHITE: ai_white}

    while True:
        if can_place(board, current_player):
            x, y = ai[current_player].place(board, current_player)
            if not can_place_x_y(board, current_player, x, y):
                print(f"AI {ai[current_player].face()} が無効な場所に置こうとしました: ({x}, {y})")
                print(f"AI {ai[current_player].face()} の反則負けです！")
                break
            move_stone(board, current_player, x, y)
            print(f"{ai[current_player].face()} が ({x}, {y}) に石を置きました")
        else:
            print(f"AI {ai[current_player].face()} は置ける場所がありません: スキップ")

        if not can_place(board, BLACK) and not can_place(board, WHITE):
            black_score = sum(row.count(BLACK) for row in board)
            white_score = sum(row.count(WHITE) for row in board)
            print(f"ゲーム終了！黒: {black_score}, 白: {white_score}")
            if black_score > white_score:
                print("黒の勝利！")
            elif black_score < white_score:
                print("白の勝利！")
            else:
                print("引き分け！")
            break

        current_player = 3 - current_player
        draw_board(canvas, board)

    display(canvas)

# メイン関数
if __name__ == "__main__":
    ai_black = PandaAI()
    ai_white = PandaAI()
    ai_vs_ai(ai_black, ai_white)
