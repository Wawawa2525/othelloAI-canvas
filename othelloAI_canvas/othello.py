from .canvas import Canvas
import math
import random

BLACK = 1
WHITE = 2

board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
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

def can_place(board, stone):
    """
    石を置ける場所を調べる関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def random_place(board, stone):
    """
    石をランダムに置く関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    while True:
        x = random.randint(0, len(board[0]) - 1)
        y = random.randint(0, len(board) - 1)
        if can_place_x_y(board, stone, x, y):
            return x, y

def copy(board):
    """
    盤面をコピーする関数。
    board: 2次元配列のオセロボード
    """
    return [row[:] for row in board]

def move_stone(board, stone, x, y):
    """
    石を置き、ひっくり返す関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return:
    """
    moves = [copy(board)] * 3
    if not can_place_x_y(board, stone, x, y):
        return moves

    board[y][x] = stone
    moves.append(copy(board))
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    flipped_count = 0

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
                flipped_count += 1

    return moves

class PandaAI(object):

    def face(self):
        return "🐼"

    def place(self, board, stone):
        x, y = random_place(board, stone)
        return x, y

def draw_board(canvas, board):
    ctx = canvas.getContext("2d")
    grid = width // len(board)
    for y, line in enumerate(board):
        for x, stone in enumerate(line):
            cx = x * grid + grid // 2
            cy = y * grid + grid // 2
            if stone != 0:
                ctx.beginPath()
                ctx.arc(cx, cy, grid // 2, 0, 2 * math.pi)
                ctx.fillStyle = "black" if stone == 1 else "white"
                ctx.fill()

width = 300

def draw_board_moves(canvas, moves):
    for board in moves:
        draw_board(canvas, board)

def play_othello(ai_black=None, ai_white=None, board=None):
    """
    AI同士のオセロ対戦を実現する。
    ai_black: 黒石プレイヤー (AI)
    ai_white: 白石プレイヤー (AI)
    board: 初期盤面
    """
    if board is None:
        board = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0, 0],
            [0, 0, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]

    if ai_black is None or ai_white is None:
        print("両方のAIを指定してください。")
        return

    moves = []

    while True:
        # 黒石（AI Black）のターン
        if can_place(board, BLACK):
            x, y = ai_black.place(board, BLACK)
            if not can_place_x_y(board, BLACK, x, y):
                print(f"{ai_black.face()}が無効な位置({x}, {y})を選びました。反則負けです。")
                break
            print(f"{ai_black.face()} (黒) は ({x}, {y}) に置きました。")
            moves.extend(move_stone(board, BLACK, x, y))
        else:
            print(f"{ai_black.face()} (黒) は置ける場所がありません。スキップします。")

        # 白石（AI White）のターン
        if can_place(board, WHITE):
            x, y = ai_white.place(board, WHITE)
            if not can_place_x_y(board, WHITE, x, y):
                print(f"{ai_white.face()}が無効な位置({x}, {y})を選びました。反則負けです。")
                break
            print(f"{ai_white.face()} (白) は ({x}, {y}) に置きました。")
            moves.extend(move_stone(board, WHITE, x, y))
        else:
            print(f"{ai_white.face()} (白) は置ける場所がありません。スキップします。")

        # 勝敗判定
        if not can_place(board, BLACK) and not can_place(board, WHITE):
            black_count = sum(row.count(BLACK) for row in board)
            white_count = sum(row.count(WHITE) for row in board)
            print(f"最終結果: 黒: {black_count}, 白: {white_count}")
            if black_count > white_count:
                print(f"{ai_black.face()} (黒) の勝利！")
            elif black_count < white_count:
                print(f"{ai_white.face()} (白) の勝利！")
            else:
                print("引き分けです！")
            break

    draw_board_moves(Canvas(background='green', grid=width // 6, width=width, height=width), moves)
