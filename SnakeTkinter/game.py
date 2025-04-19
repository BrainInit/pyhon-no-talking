import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)
        
        # Configuración del juego
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.speed = 150
        
        # Crear el canvas
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        # Inicializar serpiente
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        
        # Comida
        self.food = self.create_food()
        self.score = 0
        
        # Etiqueta de puntuación
        self.score_label = tk.Label(master, text=f"Puntuación: {self.score}", font=('Arial', 14))
        self.score_label.pack()
        
        # Controles
        self.master.bind("<KeyPress>", self.change_direction)
        
        # Iniciar juego
        self.game_loop()
    
    def create_food(self):
        """Crea comida en una posición aleatoria"""
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            food = (x, y)
            if food not in self.snake:
                return food
    
    def draw_snake(self):
        """Dibuja la serpiente en el canvas"""
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size,
                fill="green", tag="snake"
            )
    
    def draw_food(self):
        """Dibuja la comida en el canvas"""
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(
            x, y, x + self.cell_size, y + self.cell_size,
            fill="red", tag="food"
        )
    
    def move_snake(self):
        """Mueve la serpiente en la dirección actual"""
        head_x, head_y = self.snake[0]
        
        if self.direction == "Right":
            new_head = (head_x + self.cell_size, head_y)
        elif self.direction == "Left":
            new_head = (head_x - self.cell_size, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.cell_size)
        
        # Comprobar colisiones
        if (new_head in self.snake or 
            new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over()
            return
        
        self.snake.insert(0, new_head)
        
        # Comprobar si come la comida
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"Puntuación: {self.score}")
            self.food = self.create_food()
        else:
            self.snake.pop()
    
    def change_direction(self, event):
        """Cambia la dirección de la serpiente"""
        key = event.keysym
        if (key == "Right" and self.direction != "Left" or
            key == "Left" and self.direction != "Right" or
            key == "Up" and self.direction != "Down" or
            key == "Down" and self.direction != "Up"):
            self.direction = key
    
    def game_loop(self):
        """Bucle principal del juego"""
        self.move_snake()
        self.draw_snake()
        self.draw_food()
        self.master.after(self.speed, self.game_loop)
    
    def game_over(self):
        """Muestra mensaje de fin de juego"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width/2, self.height/2,
            text=f"¡Juego terminado! Puntuación: {self.score}",
            fill="white", font=('Arial', 16)
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()