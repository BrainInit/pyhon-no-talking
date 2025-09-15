import sys 
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QFrame, QHBoxLayout, QVBoxLayout
)

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App")
        self.setGeometry(100, 100, 1200,  700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.menu_frame = QFrame()
        self.menu_frame.setFixedWidth(160)
        self.menu_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(90, 0, 140, 0.45); /* base púrpura translúcida */
                border-right: 1px solid rgba(255, 255, 255, 0.25);
            }
            """
        )

        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(15,15,15,15)
        menu_layout.setSpacing(15)

        self.menu_container = QFrame()
        self.menu_container.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 18px;
            }
            """
        )

        self.menu_container.setLayout(QVBoxLayout())
        menu_layout.addWidget(self.menu_container)

        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(90, 0, 140, 0.45);
                border-left: 1px solid rgba(255, 255, 255, 0.25);
                }
            """)
        
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(15,15,15,15)
        content_layout.setSpacing(15)

        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(60)
        self.header_frame.setStyleSheet(
            """
                QFrame {
                    background-color: rgba(255, 255, 255, 0.15);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 15px;
                }
            """
        )

        content_layout.addWidget(self.header_frame)

        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet("background: transparent; ")

        grid_layout = QHBoxLayout(self.grid_frame)
        grid_layout.setSpacing(15)

        card_style = """
            QFrame {
                background-color: rgba(255, 255, 255, 0.18);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 18px;
            }
        """

        self.card_col1 = QFrame()
        self.card_col1.setStyleSheet(card_style)
        self.card_col1.setLayout(QVBoxLayout())

        self.card_col2 = QFrame()
        self.card_col2.setStyleSheet(card_style)
        self.card_col2.setLayout(QVBoxLayout())

        self.card_col3 = QFrame()
        self.card_col3.setStyleSheet(card_style)
        self.card_col3.setLayout(QVBoxLayout())


        grid_layout.addWidget(self.card_col1)
        grid_layout.addWidget(self.card_col2)
        grid_layout.addWidget(self.card_col3)


        content_layout.addWidget(self.grid_frame)

        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(self.content_frame)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())