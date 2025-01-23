import flet as ft
import random
import time
import threading
import flet.canvas as canvas

# Definición de las piezas de Tetris
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Colores de las piezas
COLORS = [
    ft.colors.CYAN,
    ft.colors.YELLOW,
    ft.colors.RED,
    ft.colors.GREEN,
    ft.colors.PURPLE,
    ft.colors.ORANGE,
    ft.colors.BLUE,
]

# Tamaño del bloque
BLOCK_SIZE = 20

# Dimensiones del tablero
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

class TetrisApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.current_x = BOARD_WIDTH // 2 - 2
        self.current_y = 0
        self.score = 0
        self.game_over = False

        # Crear el canvas para dibujar el tablero
        self.canvas = canvas.Canvas(
            width=BOARD_WIDTH * BLOCK_SIZE,
            height=BOARD_HEIGHT * BLOCK_SIZE,
        )
        self.score_text = ft.Text(value=f"Score: {self.score}", size=20)
        self.game_over_text = ft.Text(value="", size=30, color=ft.colors.RED)

        # Contenedor principal
        self.container = ft.Column(
            controls=[
                self.score_text,
                self.canvas,
                self.game_over_text,
            ]
        )

        # Configurar eventos del teclado
        self.page.on_keyboard_event = self.on_keyboard

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color}

    def valid_move(self, piece, x, y):
        for i, row in enumerate(piece["shape"]):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT or self.board[new_y][new_x]:
                        return False
        return True

    def place_piece(self):
        for i, row in enumerate(self.current_piece["shape"]):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + i][self.current_x + j] = self.current_piece["color"]
        
        # Verificar si alguna parte de la pieza está en la fila superior
        if any(self.current_y + i == 0 for i in range(len(self.current_piece["shape"]))):
            self.game_over = True
            return

        self.clear_lines_and_columns()
        self.current_piece = self.new_piece()
        self.current_x = BOARD_WIDTH // 2 - 2
        self.current_y = 0
        if not self.valid_move(self.current_piece, self.current_x, self.current_y):
            self.game_over = True

    def clear_lines_and_columns(self):
        # Eliminar filas con 5 o más bloques del mismo color
        for y in range(BOARD_HEIGHT):
            color_count = {}
            for x in range(BOARD_WIDTH):
                color = self.board[y][x]
                if color:
                    color_count[color] = color_count.get(color, 0) + 1
            for color, count in color_count.items():
                if count >= 5:
                    for x in range(BOARD_WIDTH):
                        if self.board[y][x] == color:
                            self.board[y][x] = 0
                    self.score += 100  # Aumentar el score por eliminar fila

        # Eliminar columnas con 5 o más bloques del mismo color
        for x in range(BOARD_WIDTH):
            color_count = {}
            for y in range(BOARD_HEIGHT):
                color = self.board[y][x]
                if color:
                    color_count[color] = color_count.get(color, 0) + 1
            for color, count in color_count.items():
                if count >= 5:
                    for y in range(BOARD_HEIGHT):
                        if self.board[y][x] == color:
                            self.board[y][x] = 0
                    self.score += 100  # Aumentar el score por eliminar columna

        # Hacer caer los bloques superiores
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT - 1, -1, -1):
                if self.board[y][x] == 0:
                    for y_above in range(y - 1, -1, -1):
                        if self.board[y_above][x] != 0:
                            self.board[y][x] = self.board[y_above][x]
                            self.board[y_above][x] = 0
                            break

        self.score_text.value = f"Score: {self.score}"
        self.score_text.update()

    def move(self, dx, dy):
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        if self.valid_move(self.current_piece, new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
            self.update()

    def drop_piece(self):
        """Hace caer la pieza rápidamente hasta el fondo o hasta que colisione."""
        while self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
            self.current_y += 1
        self.place_piece()  # Coloca la pieza cuando ya no puede moverse más hacia abajo
        self.update()

    def rotate(self):
        piece = self.current_piece
        new_shape = [list(row) for row in zip(*piece["shape"][::-1])]
        if self.valid_move({"shape": new_shape, "color": piece["color"]}, self.current_x, self.current_y):
            self.current_piece["shape"] = new_shape
            self.update()

    def on_keyboard(self, e: ft.KeyboardEvent):
        if self.game_over:
            return
        if e.key == "Arrow Left":
            self.move(-1, 0)
        elif e.key == "Arrow Right":
            self.move(1, 0)
        elif e.key == "Arrow Down":
            self.drop_piece()  # Hace caer la pieza rápidamente
        elif e.key == "Arrow Up":
            self.rotate()

    def draw_board(self):
        shapes = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    shapes.append(
                        canvas.Rect(
                            x * BLOCK_SIZE,
                            y * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                            paint=ft.Paint(color=cell),
                        )
                    )
        for i, row in enumerate(self.current_piece["shape"]):
            for j, cell in enumerate(row):
                if cell:
                    shapes.append(
                        canvas.Rect(
                            (self.current_x + j) * BLOCK_SIZE,
                            (self.current_y + i) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                            paint=ft.Paint(color=self.current_piece["color"]),
                        )
                    )
        return shapes

    def update(self):
        self.canvas.shapes = self.draw_board()
        self.score_text.value = f"Score: {self.score}"
        if self.game_over:
            self.game_over_text.value = "Game Over!"
        self.canvas.update()
        self.score_text.update()  # Asegurar que el score se actualice

    def tick(self):
        if not self.game_over:
            self.move(0, 1)
            if self.current_y + len(self.current_piece["shape"]) >= BOARD_HEIGHT or not self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                self.place_piece()
            self.update()

def main(page: ft.Page):
    page.title = "Tetris"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window.width = 300
    page.window.height = 600
    page.window.resizable = False

    tetris = TetrisApp(page)
    page.add(tetris.container)

    def game_loop():
        while True:
            tetris.tick()
            time.sleep(0.5)

    threading.Thread(target=game_loop, daemon=True).start()

ft.app(target=main)