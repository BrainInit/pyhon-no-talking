import flet as ft
import math
import asyncio

def main(page: ft.Page):
    page.title = "Generador de Mandalas"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0015"
    page.padding = 20
    
    canvas_size = 600
    center_x = canvas_size / 2
    center_y = canvas_size / 2
    
    is_playing = [True]
    rotation_angle = [0]
    speed = [1.0]
    num_petals = [12]
    color_mode = [0]
    
    color_palettes = [
        ["#ff006e", "#8338ec", "#3a86ff", "#06ffa5", "#ffbe0b"],
        ["#ff0080", "#ff8c00", "#ffd700", "#00ff80", "#00ffff"],
        ["#e63946", "#f1faee", "#a8dadc", "#457b9d", "#1d3557"],
        ["#d62828", "#f77f00", "#fcbf49", "#eae2b7", "#003049"],
    ]
    
    petal_containers = []
    circle_containers = []
    
    def create_petal(radius, angle, size, color, layer):
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        return ft.Container(
            width=size,
            height=size,
            bgcolor=color,
            border_radius=size / 2,
            left=x - size / 2,
            top=y - size / 2,
            opacity=0.7,
            blur=ft.Blur(5, 5, ft.BlurTileMode.CLAMP),
        )
    
    def create_circle(radius, color):
        return ft.Container(
            width=radius * 2,
            height=radius * 2,
            left=center_x - radius,
            top=center_y - radius,
            border=ft.border.all(2, color),
            border_radius=radius,
            opacity=0.3,
        )
    
    def generate_mandala():
        petal_containers.clear()
        circle_containers.clear()
        
        colors = color_palettes[color_mode[0]]
        petals = num_petals[0]
        
        for circle_layer in range(6):
            radius = 40 + circle_layer * 35
            circle_containers.append(
                create_circle(radius, colors[circle_layer % len(colors)])
            )
        
        for layer in range(5):
            radius = 60 + layer * 40
            petal_size = 30 - layer * 3
            
            for i in range(petals):
                angle = (2 * math.pi / petals) * i + rotation_angle[0] + (layer * 0.1)
                color = colors[(i + layer) % len(colors)]
                
                petal = create_petal(radius, angle, petal_size, color, layer)
                petal_containers.append(petal)
                
                sub_angle = angle + (math.pi / petals)
                sub_radius = radius + 15
                sub_petal = create_petal(
                    sub_radius, sub_angle, petal_size * 0.6, color, layer
                )
                petal_containers.append(sub_petal)
        
        center_circle = ft.Container(
            width=50,
            height=50,
            bgcolor=colors[0],
            border_radius=25,
            left=center_x - 25,
            top=center_y - 25,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=20,
                color=ft.Colors.with_opacity(0.6, colors[0]),
            ),
        )
        petal_containers.append(center_circle)
        
        update_canvas()
    
    space = ft.Stack([], width=canvas_size, height=canvas_size)
    
    def update_canvas():
        space.controls = circle_containers + petal_containers
        space.update()
    
    async def animate_mandala():
        try:
            while True:
                await asyncio.sleep(0.05)
                
                if is_playing[0]:
                    rotation_angle[0] += 0.02 * speed[0]
                    generate_mandala()
                    
        except Exception as e:
            print(f"Animación detenida: {e}")
    
    def toggle_play(e):
        is_playing[0] = not is_playing[0]
        play_btn.icon = ft.Icons.PAUSE if is_playing[0] else ft.Icons.PLAY_ARROW
        play_btn.icon_color = ft.Colors.PURPLE_400 if is_playing[0] else ft.Colors.GREEN_400
        play_btn.update()
    
    def change_speed(e):
        speed[0] = float(e.control.value)
        speed_text.value = f"Velocidad: {speed[0]:.1f}x"
        speed_text.update()
    
    def change_petals(e):
        num_petals[0] = int(e.control.value)
        petals_text.value = f"Pétalos: {num_petals[0]}"
        petals_text.update()
        generate_mandala()
    
    def change_colors(e):
        color_mode[0] = (color_mode[0] + 1) % len(color_palettes)
        generate_mandala()
    
    def reset_mandala(e):
        rotation_angle[0] = 0
        num_petals[0] = 12
        speed[0] = 1.0
        color_mode[0] = 0
        speed_slider.value = 1.0
        petals_slider.value = 12
        speed_text.value = "Velocidad: 1.0x"
        petals_text.value = "Pétalos: 12"
        speed_slider.update()
        petals_slider.update()
        speed_text.update()
        petals_text.update()
        generate_mandala()
    
    play_btn = ft.IconButton(
        icon=ft.Icons.PAUSE,
        icon_color=ft.Colors.PURPLE_400,
        icon_size=35,
        on_click=toggle_play,
        tooltip="Play/Pause"
    )
    
    speed_text = ft.Text(
        f"Velocidad: {speed[0]:.1f}x",
        size=14,
        color=ft.Colors.PURPLE_300,
        weight=ft.FontWeight.BOLD
    )
    
    speed_slider = ft.Slider(
        min=0.1,
        max=3.0,
        value=1.0,
        divisions=29,
        on_change=change_speed,
        active_color=ft.Colors.PURPLE_400,
        thumb_color=ft.Colors.PURPLE_600,
    )
    
    petals_text = ft.Text(
        f"Pétalos: {num_petals[0]}",
        size=14,
        color=ft.Colors.PINK_300,
        weight=ft.FontWeight.BOLD
    )
    
    petals_slider = ft.Slider(
        min=6,
        max=24,
        value=12,
        divisions=18,
        on_change=change_petals,
        active_color=ft.Colors.PINK_400,
        thumb_color=ft.Colors.PINK_600,
    )
    
    page.add(
        ft.Row(
            [
                ft.Text(
                    "✨ GENERADOR DE MANDALAS ✨",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.PURPLE_300,
                    text_align=ft.TextAlign.CENTER,
                ),
                
                ft.Container(
                    content=space,
                    bgcolor="#000000",
                    border_radius=15,
                    border=ft.border.all(3, ft.Colors.PURPLE_700),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=30,
                        color=ft.Colors.with_opacity(0.5, ft.Colors.PURPLE_400),
                    ),
                ),
                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    play_btn,
                                    ft.IconButton(
                                        icon=ft.Icons.REFRESH,
                                        icon_color=ft.Colors.CYAN_400,
                                        icon_size=30,
                                        on_click=reset_mandala,
                                        tooltip="Reset"
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.PALETTE,
                                        icon_color=ft.Colors.PINK_400,
                                        icon_size=30,
                                        on_click=change_colors,
                                        tooltip="Cambiar Colores"
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            
                            ft.Container(
                                content=ft.Column([speed_text, speed_slider]),
                                padding=15,
                                bgcolor="#1a0a2e",
                                border_radius=10,
                                border=ft.border.all(2, ft.Colors.PURPLE_700),
                            ),
                            
                            ft.Container(
                                content=ft.Column([petals_text, petals_slider]),
                                padding=15,
                                bgcolor="#1a0a2e",
                                border_radius=10,
                                border=ft.border.all(2, ft.Colors.PINK_700),
                            ),
                            
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.AUTO_AWESOME, color=ft.Colors.PURPLE_300, size=20),
                                        ft.Text(
                                            "Mandala hipnótico en rotación continua",
                                            size=12,
                                            color=ft.Colors.PURPLE_200,
                                        ),
                                    ],
                                ),
                                padding=10,
                                bgcolor="#1a0a2e",
                                border_radius=8,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    padding=20,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
    
    generate_mandala()
    page.run_task(animate_mandala)

ft.app(target=main)