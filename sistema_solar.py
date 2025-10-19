import flet as ft
import math 
import asyncio

def main(page: ft.Page):
    page.title = "Sistema Solar"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0A0E27"
    page.padding = 20

    canvas_size =600
    center_x = canvas_size/2
    center_y = canvas_size/2

    is_playing = [True]
    time_speed = [1.0]
    show_orbits = [True]
    show_names = [True]
    angle = [0]

    planets = [
        {"name": "Mercurio", "distance": 60, "size": 6, "color": "#8C7853", "speed": 4.15, "angle": 0},
        {"name": "Venus", "distance": 85, "size": 10, "color": "#FFC649", "speed": 1.62, "angle": 0},
        {"name": "Tierra", "distance": 115, "size": 11, "color": "#4A90E2", "speed": 1.0, "angle": 0},
        {"name": "Marte", "distance": 145, "size": 8, "color": "#E27B58", "speed": 0.53, "angle": 0},
        {"name": "Júpiter", "distance": 200, "size": 30, "color": "#C88B3A", "speed": 0.08, "angle": 0},
        {"name": "Saturno", "distance": 260, "size": 25, "color": "#FAD5A5", "speed": 0.03, "angle": 0},
        {"name": "Urano", "distance": 305, "size": 16, "color": "#4FD0E7", "speed": 0.01, "angle": 0},
        {"name": "Neptuno", "distance": 340, "size": 15, "color": "#4166F5", "speed": 0.006, "angle": 0},
    ]

    planet_containers = []
    orbit_containers = []
    name_containers = []
    trail_points = [[] for _ in range(len(planets))]


    def create_planet(planet_data):
        return ft.Container(
            width= planet_data["size"],
            height= planet_data["size"],
            bgcolor= planet_data["color"],
            border_radius= planet_data["size"]//2,
            left= center_x,
            top= center_y,
            shadow= ft.BoxShadow(
                spread_radius=2,
                blur_radius=10,
                color= ft.Colors.with_opacity(0.5, planet_data["color"]),

            ),

        )
    
    def create_orbit(distance):
        size = distance*2
        return ft.Container(
            width=size,
            height=size,
            left= center_x-distance,
            top= center_y- distance,
            border= ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
            border_radius=distance,
        )
    
    def create_name_label(name):
        return ft.Container(
            content= ft.Text(name, size=10, color=ft.Colors.WHITE70, weight=ft.FontWeight.BOLD),
            bgcolor= ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            padding=3,
            border_radius=5,
            left=center_x,
            top=center_y,
        )
    
    for planet in planets:
        orbit_containers.append(create_orbit(planet["distance"]))
        planet_containers.append(create_planet(planet))
        name_containers.append(create_name_label(planet["name"]))

    
    sun = ft.Container(
        width=40,
        height=40,
        bgcolor= ft.Colors.YELLOW,
        border_radius=20,
        left=center_x-20,
        top= center_y-20,
        shadow= ft.BoxShadow(
            spread_radius=5,
            blur_radius=30,
            color= ft.Colors.with_opacity(0.5, ft.Colors.ORANGE)
        )
    )

    trails_container = ft.Stack([], width=canvas_size, height=canvas_size)


    space = ft.Stack(
        [
            trails_container,
            *orbit_containers,
            sun,
            *planet_containers,
            *name_containers,
        ],
        width=canvas_size,
        height=canvas_size,
    )


    async def animate_planets():
        try: 
            while True:
                await asyncio.sleep(0.03)
                
                if is_playing[0]:
                    angle[0] += 0.01 * time_speed[0]
                    
                    for i, planet in enumerate(planets):
                        planet["angle"] += planet["speed"] * 0.01 * time_speed[0]
                        
                        x = center_x + planet["distance"] * math.cos(planet["angle"])
                        y = center_y + planet["distance"] * math.sin(planet["angle"])
                        
                        planet_containers[i].left = x - planet["size"] / 2
                        planet_containers[i].top = y - planet["size"] / 2
                        
                        if show_names[0]:
                            name_containers[i].left = x + planet["size"]
                            name_containers[i].top = y - planet["size"]
                            name_containers[i].visible = True
                        else:
                            name_containers[i].visible = False
                        
                        trail_points[i].append((x, y))
                        if len(trail_points[i]) > 50:
                            trail_points[i].pop(0)
                    
                    space.update()
        except BaseException as e:
            print(f"Animación detenida {e}")

    def toggle_play(e):
        is_playing[0] = not is_playing[0]
        play_btn.icon = ft.Icons.PAUSE if is_playing[0]  else ft.Icons.PLAY_ARROW
        play_btn.icon_color = ft.Colors.RED_400 if is_playing[0] else ft.Colors.GREEN_400
        play_btn.update()

    def change_speed(e):
        time_speed[0] = float(e.control.value)
        speed_text.value = f"Velocidad: {time_speed[0]:.1f}x"
        speed_text.update()
    
    def toggle_orbits(e):
        show_orbits[0] = not show_orbits[0]
        for orbit in orbit_containers:
            orbit.visible = show_orbits[0]
        space.update()
    
    def toggle_names(e):
        show_names[0] = not show_names[0]
    
    def reset_system(e):
        for i, planet in enumerate(planets):
            planet["angle"] = i * (2 * math.pi / len(planets))
            trail_points[i].clear()
        angle[0] = 0

    def zoom_in(e):
        for planet in planets:
            planet["distance"] *= 1.1
        for i, orbit in enumerate(orbit_containers):
            new_dist = planets[i]["distance"]
            orbit.width = new_dist * 2
            orbit.height = new_dist * 2
            orbit.left = center_x - new_dist
            orbit.top = center_y - new_dist
            orbit.border_radius = new_dist
        space.update()
    
    def zoom_out(e):
        for planet in planets:
            planet["distance"] /= 1.1
        for i, orbit in enumerate(orbit_containers):
            new_dist = planets[i]["distance"]
            orbit.width = new_dist * 2
            orbit.height = new_dist * 2
            orbit.left = center_x - new_dist
            orbit.top = center_y - new_dist
            orbit.border_radius = new_dist
        space.update()
    

    
    play_btn = ft.IconButton(
        icon= ft.Icons.PAUSE,
        icon_color="red",
        icon_size=35,
        on_click= toggle_play,
        tooltip="Play/Pause"
    )

    speed_text = ft.Text(f"Velocidad: {time_speed[0]:.1f}x", size=14, color=ft.Colors.WHITE)
    

    page.add(
        ft.Row(
            [

                ft.Column([

                    ft.Text("Sistema Solar Interativo", size=28, color="white"),
                    ft.Container(
                        content=space,
                        bgcolor="#000814",
                        border_radius=15,
                        border=ft.border.all(2, "purple"),
                        animate= ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
                    )
                ],
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                spacing=20,
                scroll= ft.ScrollMode.AUTO,
                ),


                ############# controles

                  ft.Column(
            [
                            ft.Container(
                content=ft.Column([
                    ft.Row([
                        play_btn,
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            icon_color=ft.Colors.BLUE_400,
                            icon_size=30,
                            on_click=reset_system,
                            tooltip="Reset",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ZOOM_IN,
                            icon_color=ft.Colors.GREEN_400,
                            icon_size=30,
                            on_click=zoom_in,
                            tooltip="Zoom In",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ZOOM_OUT,
                            icon_color=ft.Colors.ORANGE_400,
                            icon_size=30,
                            on_click=zoom_out,
                            tooltip="Zoom Out",
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            "Mostrar/Ocultar Órbitas",
                            icon=ft.Icons.CIRCLE_OUTLINED,
                            on_click=toggle_orbits,
                            bgcolor=ft.Colors.INDIGO_700,
                            color=ft.Colors.WHITE,
                        ),
                        ft.ElevatedButton(
                            "Mostrar/Ocultar Nombres",
                            icon=ft.Icons.LABEL,
                            on_click=toggle_names,
                            bgcolor=ft.Colors.PURPLE_700,
                            color=ft.Colors.WHITE,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    
                    ft.Container(
                        content=ft.Column([
                            speed_text,
                            ft.Slider(
                                min=0.1,
                                max=5.0,
                                value=1.0,
                                divisions=49,
                                on_change=change_speed,
                                active_color=ft.Colors.PURPLE_400,
                            ),
                        ]),
                        padding=15,
                        bgcolor="#16213e",
                        border_radius=10,
                        width=400,
                        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                    ),
                    
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.CYAN_400, size=20),
                            ft.Text("Los planetas orbitan a escala relativa de velocidad", 
                                   size=12, 
                                   color=ft.Colors.WHITE70),
                        ]),
                        padding=10,
                        bgcolor="#1a1a3e",
                        border_radius=8,
                    ),
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
                padding=20,
            ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,            
            )
 

            ]
        )
    )



    page.run_task(animate_planets)



ft.app(target=main)