"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx


COLORS = {
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "calculator_bg": "rgba(255, 255, 255, 0.1)",
    "primary": "rgba(255, 255, 255, 0.08)",
    "secondary": "rgba(255, 255, 255, 0.16)",
    "accent": "rgba(255, 99, 71, 0.7)",
    "text": "#ffffff",
    "display": "rgba(0, 0, 0, 0.3)",
    "button_text": "#ffffff",
    "border": "rgba(255, 255, 255, 0.2)"
}


class CalculatorState(rx.State):
    display: str = "0"
    waiting_for_operand: bool = False
    current_operation: str = ""
    stored_value: str = "0"
    should_reset_display: bool = False


    def clear(self):
        self.display = "0"
        self.waiting_for_operand: bool = False
        self.current_operation: str = ""
        self.stored_value: str = "0"
        self.should_reset_display: bool = False        

    def toggle_sign(self):
        if self.display.startswith("-"):
            self.display = self.display[1:]
        else:
            self.display = "-" + self.display


    def percentage(self):
        try:
            value = float(self.display)/100
            self.display = str(int(value) if value.is_integer() else value)
            self.should_reset_display = True
        except:
            self.display = "Error"
            self.should_reset_display = True


    def set_operation(self, operation: str):
        if self.current_operation and not self.waiting_for_operand:
            self.calculate()
        
        self.stored_value = self.display
        self.current_operation = operation
        self.waiting_for_operand = True
        self.should_reset_display = False


    def input_digit(self, digit: str):
        if self.display =="0" or self.waiting_for_operand or self.should_reset_display:
            self.display = digit
            self.waiting_for_operand= False
            self.should_reset_display = False
        else:
            self.display +=digit

    def input_decimal(self):
        if self.waiting_for_operand or self.should_reset_display:
            self.display = "0."
            self.waiting_for_operand = False
            self.should_reset_display = False
        elif "." not in self.display:
            self.display +="."


    def calculate(self):
        try:
            if self.current_operation == "+":
                result = float(self.stored_value) + float(self.display)
            elif self.current_operation == "-":
                result = float(self.stored_value) - float(self.display)
            elif self.current_operation == "×":
                result = float(self.stored_value) * float(self.display)
            elif self.current_operation == "÷":
                result = float(self.stored_value) / float(self.display)
            else:
                return
            
            # Formatear el resultado para evitar decimales innecesarios
            self.display = str(int(result) if result.is_integer() else result)
            self.stored_value = self.display
            self.current_operation = ""
            self.should_reset_display = True
        except ZeroDivisionError:
            self.display = "Error"
            self.current_operation = ""
            self.should_reset_display = True
        except:
            self.display = "Error"
            self.current_operation = ""
            self.should_reset_display = True






def calculator_button(label: str, color: str= COLORS["primary"], **props) ->  rx.Component:
    return rx.button(
        label,
        bg = color,
        color = COLORS["button_text"],
        border_radius = "12px",
        padding = "1em",
        font_size = "1.2em",
        font_weight = "bold",
        border = f"1px solid {COLORS["border"]}",
        backdrop_filter = "blur(10px)",
        _hover = {
            "bg": COLORS["accent"],
            "transform": "scale(1.1)",
            "transition": "all 0.4s ease",
            "box_shadow": "0 0 15px rgba(255, 99, 71, 0.5)",
        },
        _active = {
            "transform": "scale(0.95)"
        },
         **props

    )

def index()-> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box(
                rx.text(
                    CalculatorState.display,
                    font_size = "2.5em",
                    text_align= "right",
                    padding = "0.5em",
                    width ="100%"

                ),
                bg = COLORS["display"],
                border_radius = "12px",
                width = "100%",
                padding = "0.5em",
                margin_bottom = "1em",
                border = f"1px solid {COLORS["border"]}",
                backdrop_filter = "blur(10px)",
                box_shadow = "0 4px 30px rgb(0,0,0, 0.1)",
            ),

        # teclado de la calculadora

        rx.grid(
            calculator_button("C", COLORS["accent"],on_click = CalculatorState.clear ),
            calculator_button("±", COLORS["secondary"], on_click=CalculatorState.toggle_sign),
            calculator_button("%", COLORS["secondary"], on_click=CalculatorState.percentage),
            calculator_button("÷", COLORS["secondary"], on_click=lambda: CalculatorState.set_operation("÷")),
          
            # Fila 2
            calculator_button("7", on_click=lambda: CalculatorState.input_digit("7")),
            calculator_button("8", on_click=lambda: CalculatorState.input_digit("8")),
            calculator_button("9", on_click=lambda: CalculatorState.input_digit("9")),
            calculator_button("×", COLORS["secondary"], on_click=lambda: CalculatorState.set_operation("×")),
            
            # Fila 3
            calculator_button("4", on_click=lambda: CalculatorState.input_digit("4")),
            calculator_button("5", on_click=lambda: CalculatorState.input_digit("5")),
            calculator_button("6", on_click=lambda: CalculatorState.input_digit("6")),
            calculator_button("-", COLORS["secondary"], on_click=lambda: CalculatorState.set_operation("-")),
            
            # Fila 4
            calculator_button("1", on_click=lambda: CalculatorState.input_digit("1")),
            calculator_button("2", on_click=lambda: CalculatorState.input_digit("2")),
            calculator_button("3", on_click=lambda: CalculatorState.input_digit("3")),
            calculator_button("+", COLORS["secondary"], on_click=lambda: CalculatorState.set_operation("+")),
            
            # Fila 5
            calculator_button("0", grid_column_span=2, on_click=lambda: CalculatorState.input_digit("0")),
            calculator_button(".", on_click=CalculatorState.input_decimal),
            calculator_button("=", COLORS["accent"], on_click=CalculatorState.calculate),

        # estilos del grid 

        grid_template_columns = "repeat(4, 1fr)",
        gap = "0.75em",
        width = "100%",
        ),

        # estilos del contenedor principal
        width = ["90%", "80%", "60%", "400px"],
        bg = COLORS["calculator_bg"],
        padding = "2em",
        border_radius = "20px",
        border = f"1px solid {COLORS["border"]}",
        backdrop_filter = "blue(16px)",
        box_shadow = "0 4px 30px rgb(0,0,0,0.1)",

        ),

        # estilo de la pagina 
        width = "100%",
        height = "100vh",
        background = COLORS["background"],
        background_attachment = "fixed",
    )


app = rx.App()
app.add_page(index, title= "Calculator")