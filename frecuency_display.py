import flet as ft
import math
import random
import asyncio

def main(page: ft.Page):
    page.title = "Visualizador de Frecuencias"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0e27"
    page.padding = 20
    
    num_bars = 64
    max_height = 300
    is_playing = [False]
    animation_speed = [0.05]
    color_mode = [0]
    bar_style = [0]
    
    bars_data = [random.uniform(0.1, 0.3) for _ in range(num_bars)]
    velocities = [random.uniform(-0.02, 0.02) for _ in range(num_bars)]
    
    def get_color(index, height_ratio):
        modes = [
            lambda i, h: ft.Colors.PURPLE_400 if h < 0.5 else ft.Colors.PINK_400,
            lambda i, h: f"#{int(h*255):02x}{int((1-h)*100):02x}{255}",
            lambda i, h: ft.Colors.CYAN_400 if i % 2 == 0 else ft.Colors.BLUE_400,
            lambda i, h: f"#{int(255*h):02x}{int(255*(1-h)):02x}{int(128+127*math.sin(i*0.1)):02x}",
        ]
        return modes[color_mode[0]](index, height_ratio)
    
    def create_bar(index):
        return ft.Container(
            width=8 if num_bars > 32 else 12,
            height=50,
            bgcolor=ft.Colors.PURPLE_400,
            border_radius=ft.border_radius.only(top_left=5, top_right=5),
            alignment=ft.alignment.bottom_center,
            animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
        )
    
    bars = [create_bar(i) for i in range(num_bars)]
    
    particles = []
    
    def create_particle(x):
        return ft.Container(
            width=4,
            height=4,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
            border_radius=2,
            left=x,
            top=max_height,
            animate=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        )
    
    bars_row = ft.Row(
        bars,
        spacing=2,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    
    particles_stack = ft.Stack(
        particles,
        width=900,
        height=max_height + 50,
    )
    
    async def animate_bars():
        while True:
            await asyncio.sleep(animation_speed[0])
            
            if is_playing[0]:
                for i in range(num_bars):
                    bars_data[i] += velocities[i]
                    
                    if bars_data[i] >= 1.0:
                        bars_data[i] = 1.0
                        velocities[i] = random.uniform(-0.05, -0.02)
                        
                        if random.random() > 0.7 and len(particles) < 20:
                            particle = create_particle(i * (900 / num_bars))
                            particles.append(particle)
                            particles_stack.controls = particles
                    
                    elif bars_data[i] <= 0.1:
                        bars_data[i] = 0.1
                        velocities[i] = random.uniform(0.02, 0.08)
                    
                    velocities[i] += random.uniform(-0.01, 0.01)
                    velocities[i] = max(-0.1, min(0.1, velocities[i]))
                    
                    height = int(bars_data[i] * max_height)
                    bars[i].height = max(10, height)
                    bars[i].bgcolor = get_color(i, bars_data[i])
                
                for particle in particles[:]:
                    if hasattr(particle, 'top'):
                        particle.top -= 5
                        particle.width += 0.2
                        particle.height += 0.2
                        
                        if particle.top < -20:
                            particles.remove(particle)
                            particles_stack.controls = particles
                
                bars_row.update()
                if len(particles) > 0:
                    particles_stack.update()
    
    def toggle_play(e):
        is_playing[0] = not is_playing[0]
        play_btn.icon = ft.Icons.PAUSE if is_playing[0] else ft.Icons.PLAY_ARROW
        play_btn.icon_color = ft.Colors.RED_400 if is_playing[0] else ft.Colors.GREEN_400
        play_btn.update()
    
    def change_speed(e):
        speed_map = {0: 0.05, 1: 0.03, 2: 0.01}
        animation_speed[0] = speed_map[int(e.control.value)]
        speed_text.value = ["Normal", "Rápido", "Muy Rápido"][int(e.control.value)]
        speed_text.update()
    
    def change_colors(e):
        color_mode[0] = (color_mode[0] + 1) % 4
    
    def randomize_bars(e):
        for i in range(num_bars):
            bars_data[i] = random.uniform(0.2, 0.8)
            velocities[i] = random.uniform(-0.05, 0.05)
    
    def reset_bars(e):
        for i in range(num_bars):
            bars_data[i] = 0.1
            velocities[i] = 0.02
            bars[i].height = 10
            bars[i].update()
    
    play_btn = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW,
        icon_color=ft.Colors.GREEN_400,
        icon_size=40,
        on_click=toggle_play,
    )
    
    speed_text = ft.Text("Normal", size=14, color=ft.Colors.WHITE)
    
    page.add(
        ft.Column([
            ft.Text("🎵 Visualizador de Frecuencias", 
                   size=32, 
                   weight=ft.FontWeight.BOLD, 
                   color=ft.Colors.WHITE),
            
            ft.Container(
                content=ft.Stack([
                    particles_stack,
                    ft.Container(
                        content=bars_row,
                        alignment=ft.alignment.bottom_center,
                    ),
                ]),
                width=900,
                height=max_height + 50,
                bgcolor="#16213e",
                border_radius=15,
                padding=20,
                border=ft.border.all(2, ft.Colors.PURPLE_400),
                animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        play_btn,
                        ft.IconButton(
                            icon=ft.Icons.SHUFFLE,
                            icon_color=ft.Colors.ORANGE_400,
                            icon_size=30,
                            on_click=randomize_bars,
                            tooltip="Aleatorizar",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            icon_color=ft.Colors.BLUE_400,
                            icon_size=30,
                            on_click=reset_bars,
                            tooltip="Reset",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.PALETTE,
                            icon_color=ft.Colors.PINK_400,
                            icon_size=30,
                            on_click=change_colors,
                            tooltip="Cambiar Colores",
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Velocidad:", color=ft.Colors.WHITE70, size=14),
                            speed_text,
                            ft.Slider(
                                min=0,
                                max=2,
                                divisions=2,
                                value=0,
                                on_change=change_speed,
                                active_color=ft.Colors.PURPLE_400,
                            ),
                        ]),
                        padding=15,
                        bgcolor="#16213e",
                        border_radius=10,
                        width=300,
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    ),
                    
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.CYAN_400, size=20),
                            ft.Text("Las barras simulan frecuencias de audio en tiempo real", 
                                   size=12, 
                                   color=ft.Colors.WHITE70),
                        ]),
                        padding=10,
                        bgcolor="#1a1a3e",
                        border_radius=8,
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
                padding=20,
            ),
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    )
    
    page.run_task(animate_bars)

ft.app(target=main)