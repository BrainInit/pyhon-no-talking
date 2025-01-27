#  ASMR de Programación: Codifica PAC-MAN en Python  usando Flet 
#  https://youtu.be/iNMp7BXaBWc
#  https://www.youtube.com/@braininit 

import flet as ft 
import flet.canvas as canvas 
import random
import math 
import asyncio

# Definimos el mapa de Pac-Man
MAP = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X            XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X                          X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X XXXX XX XXXXXXXX XX XXXX X",
    "X      XX    XX    XX      X",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XXXXX XX XXXXX XXXXXX",
    "XXXXXX XX          XX XXXXXX",
    "XXXXXX XX XXXXXXXX XX XXXXXX",
    "XXXXXX XX X      X XX XXXXXX",
    "X            XX            X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X XXXX XXXXX XX XXXXX XXXX X",
    "X   XX                XX   X",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "XXX XX XX XXXXXXXX XX XX XXX",
    "X      XX    XX    XX      X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X XXXXXXXXXX XX XXXXXXXXXX X",
    "X                          X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

TILE_SIZE = 20

class PacManGame(ft.Container):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        self.pacman_pos = [1*TILE_SIZE, 1*TILE_SIZE]
        self.direction = "right"
        self.game_over = False 
        self.win = False
        self.alignment = ft.alignment.center
        self.food = self.generate_food()
        self.ghosts = [self.generate_ghost() for _ in range(4) ]
        self.pacman_frame = 0 


        self.canvas = canvas.Canvas(
            width=len(MAP[0])*TILE_SIZE,
            height= len(MAP)*TILE_SIZE,
            shapes= self.draw_map()
        )

        self.pacman_images = [
            ft.Image(src="assets/pacman_open.png", width=TILE_SIZE, height=TILE_SIZE),
            ft.Image(src="assets/pacman_closed.png", width=TILE_SIZE, height=TILE_SIZE),
        ]

        self.ghost_images =  [
            ft.Image(src=f"assets/ghost{i+1}.png", width=TILE_SIZE, height=TILE_SIZE)
            for i in range(4)
        ]

        self.content = ft.Stack([
            self.canvas,
            *self.pacman_images,
            *self.ghost_images,
        ],
        width=len(MAP[0])*TILE_SIZE,
        height=len(MAP)*TILE_SIZE,
        )
    
 
    def generate_food(self):
        food = []
        for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                if cell ==" ":
                    food.append((x*TILE_SIZE, y*TILE_SIZE))
        return food

    def move(self):
        if self.game_over or self.win:
            return
        new_x, new_y = self.pacman_pos[0], self.pacman_pos[1]
        if self.direction == "right":
            new_x += TILE_SIZE
        elif self.direction =="left":
            new_x -= TILE_SIZE
        elif self.direction =="up":
            new_y -= TILE_SIZE
        elif self.direction =="down":
            new_y += TILE_SIZE

        map_x = new_x//TILE_SIZE
        map_y =  new_y//TILE_SIZE
        if 0<=map_x< len(MAP[0]) and 0 <=map_y < len(MAP) and MAP[map_y][map_x] !="X":
            self.pacman_pos[0], self.pacman_pos[1] = new_x, new_y

        pacman_tile = (self.pacman_pos[0], self.pacman_pos[1] )
        if pacman_tile in self.food:
            self.food.remove(pacman_tile)
            #score 
        
        if not self.food:
            self.win = True
            self.update()
            return
        # verificar colisiones
        for ghost in self.ghosts:
            if (self.pacman_pos[0], self.pacman_pos[1]) ==ghost:
                self.game_over = True
                self.update()
                return
            
        
        self.update()


    def move_ghosts(self):
        for i, ghost in enumerate(self.ghosts):
            direction = random.choice(["right", "left", "up", "down"])
            new_x, new_y = ghost[0], ghost[1]
            if direction == "right":
                new_x += TILE_SIZE
            elif direction =="left":
                new_x -= TILE_SIZE
            elif direction =="up":
                new_y -= TILE_SIZE
            elif direction =="down":
                new_y += TILE_SIZE
        
            map_x = new_x//TILE_SIZE
            map_y =  new_y//TILE_SIZE
            if 0<=map_x< len(MAP[0]) and 0 <=map_y < len(MAP) and MAP[map_y][map_x] !="X":
                self.ghosts[i] = (new_x, new_y)


    def on_keyboard(self, e:ft.KeyboardEvent):
        if e.key =="Arrow Up":
            self.direction ="up"
        elif e.key =="Arrow Down":
            self.direction ="down"
        elif e.key =="Arrow Left":
            self.direction ="left"
        elif e.key =="Arrow Right":
            self.direction ="right"
        self.page.update()

    def draw_map(self):
        shapes = []
        for y, row in enumerate(MAP):
            for x, cell in enumerate(row):
                if cell =="X":
                    shapes.append(
                        canvas.Rect(
                            x =x*TILE_SIZE,
                            y = y*TILE_SIZE,
                            width=TILE_SIZE,
                            height= TILE_SIZE,
                            paint= ft.Paint(color= ft.colors.BLUE)
                        )
                    )
                elif cell ==" " and (x*TILE_SIZE, y*TILE_SIZE) in self.food:
                    shapes.append(
                        canvas.Circle(
                            x = x*TILE_SIZE + TILE_SIZE//2,
                            y = y*TILE_SIZE + TILE_SIZE//2,
                            radius= TILE_SIZE//8,
                            paint= ft.Paint(color = ft.colors.YELLOW),
                        )
                    )
        return shapes    

    def update(self):
        for i, img in enumerate(self.pacman_images):
            img.visible = (i==self.pacman_frame)
            img.left = self.pacman_pos[0]
            img.top = self.pacman_pos[1]

            if self.direction =="right":
                img.rotate = 0
            elif self.direction =="left":
                img.rotate = math.radians(180)
            elif self.direction =="up":
                img.rotate = math.radians(270)
            elif self.direction =="down":
                img.rotate = math.radians(90)
                
        for i, img in enumerate(self.ghost_images):
            img.left = self.ghosts[i][0]
            img.top = self.ghosts[i][1]         
        self.canvas.shapes = self.draw_map()
        self.canvas.update()   

    def reset(self):
        self.pacman_pos = [1*TILE_SIZE, 1*TILE_SIZE]
        self.direction = "right"
        self.game_over = False 
        self.win = False
        self.alignment = ft.alignment.center
        self.food = self.generate_food()
        self.ghosts = [self.generate_ghost() for _ in range(4) ]
        self.pacman_frame = 0 
        self.update()


    def generate_ghost(self):
        while True:
            x = random.randint(0, len(MAP[0])-1)
            y = random.randint(0, len(MAP)-1)
            if MAP[y][x]==" ":
                return (x*TILE_SIZE, y*TILE_SIZE)

async def game_loop(game, reset_button):
    while True:
        if not game.game_over and not game.win:
            game.move()
            game.move_ghosts()
            game.pacman_frame = (game.pacman_frame +1)%2 # alternar entre 0 y 1 
        else:
            reset_button.visible = True
        game.page.update()
        await asyncio.sleep(0.2)


async def main(page:ft.Page):
    page.title = "Pac-Man"
    page.window.width = len(MAP[0])*TILE_SIZE + 40
    page.window.height = len(MAP)*TILE_SIZE + 40
    page.window.resizable = False
    page.bgcolor = "black"

    game = PacManGame(page)

    reset_button = ft.TextButton(
        on_click=lambda e: restart_game(game, reset_button),
        visible= False,
        content= ft.Text("REINICIAR JUEGO",
                         style= ft.TextStyle(
                             size=20,
                             weight= "bold",
                             font_family= "ROG Fonts",
                             color="white"
                         )
                         )
    )

    centered_button = ft.Column([
        reset_button,
    ],
    alignment= ft.MainAxisAlignment.CENTER,
    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
    expand=True
    )

    page.on_keyboard_event = game.on_keyboard

    page.add(ft.Stack(
        alignment= ft.alignment.center,
        controls=[
            game,
            centered_button,
        ]
    ))


    def restart_game(game, reset_button):
        game.reset()
        reset_button.visible = False
        page.update()
    
    asyncio.create_task(game_loop(game, reset_button))


ft.app(target=main)