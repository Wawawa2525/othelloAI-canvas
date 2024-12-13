from .canvas import Canvas
import math
import random

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

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

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
    valid_moves = [
        (x, y)
        for y in range(len(board))
        for x in range(len(board[0]))
        if can_place_x_y(board, stone, x, y)
    ]
    if valid_moves:
        return random.choice(valid_moves)
    return None  # 置ける場所がない場合

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
    """
    if not can_place_x_y(board, stone, x, y):
        return board  # 置けない場合は何もしない

    board[y][x] = stone  # 石を置く
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

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

    return board

class BaseAI:
    """
    AIクラスの基底クラス。すべてのAIはこのクラスを継承する必要があります。
    """
    def face(self):
        return "🤖"

    def place(self, board, stone):
        """
        石を置く場所を選ぶ関数。子クラスで実装する必要があります。
        """
        raise NotImplementedError("AIクラスはplaceメソッドを実装してください")

class PandaAI(BaseAI):
    def face(self):
        return "🐼"

    def place(self, board, stone):
        move = random_place(board, stone)
        if move is not None:
            return move
        return None

def draw_board(canvas, board):
    ctx = canvas.getContext("2d")
    grid = canvas.width // len(board)
    stone_radius = grid // 2.5

    for y, row in enumerate(board):
        for x, stone in enumerate(row):
            cx = x * grid + grid // 2
            cy = y * grid + grid // 2
            ctx.fillStyle = "green"
            ctx.fillRect(x * grid, y * grid, grid, grid)
            if stone != 0:
                ctx.beginPath()
                ctx.arc(cx, cy, stone_radius, 0, 2 * math.pi)
                ctx.fillStyle = "black" if stone == BLACK else "white"
                ctx.fill()

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
            move = ai[current_player].place(board, current_player)
            if move is None:
                print(f"AI {ai[current_player].face()} は置ける場所がありません")
            else:
                x, y = move
                if not can_place_x_y(board, current_player, x, y):
                    print(f"AI {ai[current_player].face()} が無効な場所に置こうとしました: ({x}, {y})")
                    print(f"AI {ai[current_player].face()} の反則負けです！")
                    break
                move_stone(board, current_player, x, y)
                print(f"{ai[current_player].face()} が ({x}, {y}) に石を置きました")
                draw_board(canvas, board)
        else:
            print(f"AI {ai[current_player].face()} は置ける場所がないためスキップします")

        if not can_place(board, BLACK) and not can_place(board, WHITE):
            draw_board(canvas, board)
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

    display(canvas)
