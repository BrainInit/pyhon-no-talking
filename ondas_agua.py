"""
Simulador de Ondas de Agua - Propagación y Física
Simulación zen de ondas que se propagan al hacer clic
"""
import flet as ft
import math
import asyncio


class WavePoint:
    """Representa un punto de origen de onda"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.max_age = 100
        self.amplitude = 30
    
    def update(self):
        """Actualiza la edad de la onda"""
        self.age += 1
        return self.age < self.max_age
    
    def get_influence(self, x, y):
        """Calcula la influencia de esta onda en un punto dado"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        wave_speed = 3
        wave_position = self.age * wave_speed
        
        # Calcular si el punto está en la onda
        diff = abs(distance - wave_position)
        if diff < 10:
            # Atenuación con la edad
            attenuation = 1 - (self.age / self.max_age)
            # Amplitud de la onda
            wave_value = math.sin((distance - wave_position) * 0.5) * self.amplitude * attenuation
            return wave_value
        return 0


class WaterGrid:
    """Representa una cuadrícula de puntos de agua"""
    
    def __init__(self, width, height, resolution=15):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.cols = width // resolution
        self.rows = height // resolution
        
        # Matriz de altura de agua
        self.heights = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.velocities = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Ondas activas
        self.waves = []
        
        # Parámetros físicos
        self.damping = 0.98
        self.spread = 0.5
    
    def add_wave(self, x, y):
        """Agrega una nueva onda en las coordenadas dadas"""
        grid_x = int(x / self.resolution)
        grid_y = int(y / self.resolution)
        
        if 0 <= grid_x < self.cols and 0 <= grid_y < self.rows:
            self.waves.append(WavePoint(grid_x, grid_y))
    
    def update(self):
        """Actualiza la simulación de agua"""
        # Actualizar ondas y remover las que terminaron
        self.waves = [wave for wave in self.waves if wave.update()]
        
        # Aplicar influencia de las ondas
        for row in range(self.rows):
            for col in range(self.cols):
                total_influence = 0
                for wave in self.waves:
                    total_influence += wave.get_influence(col, row)
                
                self.heights[row][col] = total_influence
    
    def get_color(self, height):
        """Obtiene el color basado en la altura del agua"""
        # Agua más oscura en reposo, más clara en crestas
        base_blue = 100
        intensity = int(abs(height) * 5)
        blue = min(255, base_blue + intensity)
        green = min(180, 50 + intensity)
        
        return f"#{0:02x}{green:02x}{blue:02x}"
    
    def get_grid_data(self):
        """Obtiene los datos de la cuadrícula para visualización"""
        data = []
        for row in range(self.rows):
            for col in range(self.cols):
                height = self.heights[row][col]
                x = col * self.resolution
                y = row * self.resolution
                color = self.get_color(height)
                data.append((x, y, color, height))
        return data


class WaterSimulatorVisualizer:
    """Controla la visualización y UI del simulador de agua"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.canvas_size = 500
        
        self.water_grid = WaterGrid(self.canvas_size, self.canvas_size)
        self.is_playing = True
        self.auto_waves = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Contenedores para los puntos de agua
        self.water_points = []
        for row in range(self.water_grid.rows):
            for col in range(self.water_grid.cols):
                point = ft.Container(
                    width=self.water_grid.resolution,
                    height=self.water_grid.resolution,
                    bgcolor="#003366",
                    left=col * self.water_grid.resolution,
                    top=row * self.water_grid.resolution,
                )
                self.water_points.append(point)
        
        # Canvas principal con gesture detector
        self.canvas = ft.Stack(
            self.water_points,
            width=self.canvas_size,
            height=self.canvas_size,
        )
        
        self.gesture_detector = ft.GestureDetector(
            content=self.canvas,
            on_tap_down=self.on_canvas_tap,
        )
        
        # Controles
        self.play_btn = ft.IconButton(
            icon=ft.Icons.PAUSE,
            icon_color=ft.Colors.RED_400,
            icon_size=35,
            on_click=self.toggle_play,
            tooltip="Play/Pause"
        )
        
        self.page.add(
            ft.Column([
                ft.Text("🌊 Simulador de Ondas de Agua", 
                       size=32, 
                       weight=ft.FontWeight.BOLD, 
                       color=ft.Colors.WHITE),
                ft.Container(
                    content=self.gesture_detector,
                    bgcolor="#001a33",
                    border_radius=15,
                    border=ft.border.all(2, ft.Colors.BLUE_400),
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
                ),
                ft.Row([
                    self.play_btn,
                    ft.IconButton(
                        icon=ft.Icons.WATER_DROP,
                        icon_color=ft.Colors.CYAN_400,
                        icon_size=30,
                        on_click=self.create_random_wave,
                        tooltip="Onda Aleatoria"
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLEAR_ALL,
                        icon_color=ft.Colors.ORANGE_400,
                        icon_size=30,
                        on_click=self.clear_waves,
                        tooltip="Limpiar"
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.ElevatedButton(
                    "Ondas Automáticas",
                    icon=ft.Icons.AUTO_MODE,
                    on_click=self.toggle_auto_waves,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.TOUCH_APP, color=ft.Colors.CYAN_400, size=20),
                        ft.Text("Haz clic en el agua para crear ondas", 
                               size=12, 
                               color=ft.Colors.WHITE70),
                    ]),
                    padding=10,
                    bgcolor="#1a1a3e",
                    border_radius=8,
                ),
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20)
        )
    
    def on_canvas_tap(self, e: ft.TapEvent):
        """Maneja el clic en el canvas"""
        self.water_grid.add_wave(e.local_x, e.local_y)
    
    def update_visualization(self):
        """Actualiza la visualización del agua"""
        grid_data = self.water_grid.get_grid_data()
        
        for i, (x, y, color, height) in enumerate(grid_data):
            if i < len(self.water_points):
                self.water_points[i].bgcolor = color
                # Efecto 3D: elevar puntos con mayor altura
                offset = max(-5, min(5, height * 0.2))
                self.water_points[i].scale = 1.0 + abs(offset * 0.02)
        
        self.canvas.update()
    
    def toggle_play(self, e):
        """Alterna entre play y pause"""
        self.is_playing = not self.is_playing
        self.play_btn.icon = ft.Icons.PAUSE if self.is_playing else ft.Icons.PLAY_ARROW
        self.play_btn.icon_color = ft.Colors.RED_400 if self.is_playing else ft.Colors.GREEN_400
        self.play_btn.update()
    
    def create_random_wave(self, e):
        """Crea una onda en posición aleatoria"""
        import random
        x = random.uniform(50, self.canvas_size - 50)
        y = random.uniform(50, self.canvas_size - 50)
        self.water_grid.add_wave(x, y)
    
    def clear_waves(self, e):
        """Limpia todas las ondas"""
        self.water_grid.waves.clear()
    
    def toggle_auto_waves(self, e):
        """Activa/desactiva ondas automáticas"""
        self.auto_waves = not self.auto_waves
    
    async def animate(self):
        """Loop principal de animación"""
        import random
        frame_count = 0
        
        while True:
            await asyncio.sleep(0.05)
            if self.is_playing:
                self.water_grid.update()
                self.update_visualization()
                
                # Generar ondas automáticas
                if self.auto_waves and frame_count % 30 == 0:
                    x = random.uniform(100, self.canvas_size - 100)
                    y = random.uniform(100, self.canvas_size - 100)
                    self.water_grid.add_wave(x, y)
                
                frame_count += 1


def main(page: ft.Page):
    """Función principal"""
    page.title = "Ondas de Agua"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0e27"
    page.padding = 20
    
    visualizer = WaterSimulatorVisualizer(page)
    page.run_task(visualizer.animate)


ft.app(target=main)