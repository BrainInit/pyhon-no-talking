import flet as ft
import flet.canvas as canvas
import random
import asyncio

class MatrixEffect(ft.Container):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        self.characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.columns = []
        self.initialize_columns()

        # Configuramos el canvas
        self.canvas = canvas.Canvas(
            expand=True,
            shapes=self.draw(),
        )
        self.content = self.canvas

    def initialize_columns(self):
        for x in range(0, 1600, 15):
            column = {
                "x": x,
                "y": random.randint(-600, 0),
                "speed": random.randint(5, 20),   
                "length": random.randint(5, 20),
                "chars": [random.choice(self.characters) for _ in range(20)]
            }
            self.columns.append(column)

    def draw(self):
        shapes = []
        for column in self.columns:
            for i in range(column["length"]):
                shapes.append(
                    canvas.Text(
                        x=column["x"],
                        y=column["y"] + i * 20,
                        text=column["chars"][i],
                        style=ft.TextStyle(
                            size=20,
                            font_family="Courier New",
                            color=ft.colors.GREEN if i == 0 else ft.colors.GREEN_900,
                        ),
                    )
                )
        return shapes

    def update(self):
        for column in self.columns:
            column["y"] += column["speed"]
            if column["y"] > 600:
                column["y"] = -600
                column["chars"] = [random.choice(self.characters) for _ in range(20)]
                column["length"] = random.randint(5, 20)
                column["speed"] = random.randint(5, 20) 
        self.canvas.shapes = self.draw()
        self.canvas.update()

async def matrix_loop(matrix_effect):
    try:
        while True:
            matrix_effect.update()
            await asyncio.sleep(0.01)  # Tiempo de espera constante
    except asyncio.CancelledError:
        print("Matrix loop cancelled")

async def main(page: ft.Page):
    page.title = "Matrix Effect"
 
    page.bgcolor = ft.colors.BLACK

    matrix_effect = MatrixEffect(page)
    page.add(matrix_effect)

    # Iniciar el bucle de Matrix
    matrix_task = asyncio.create_task(matrix_loop(matrix_effect))

    # Manejar el cierre de la aplicación
    async def on_close(event):
        matrix_task.cancel()  # Cancelar la tarea asíncrona
        await asyncio.sleep(0.01)  # Esperar un momento para que la tarea se cancele
        page.window_destroy()

    page.on_close = on_close

# Ejecutar la aplicación
ft.app(target=main)