import sys
from PyQt6.QtWidgets import QApplication, QGridLayout,\
    QLabel, QWidget, QPushButton, QLineEdit, QComboBox

class SpeedCalc(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setWindowTitle('Speed Calculator')

        # init widgets (blocks)
        distance_label = QLabel('Distance in km:')
        self.distance = QLineEdit()

        time_label = QLabel('Time (hours):')
        self.time = QLineEdit()
        self.system = QComboBox()
        self.system.addItems(['Metric', 'Imperial'])

        button = QPushButton('Calculate Speed')
        button.clicked.connect(self.calculate_speed)

        self.output = QLabel("")

        # Fill grid with widgets
        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance, 0, 1)
        grid.addWidget(self.system, 0, 2)

        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time, 1, 1)

        grid.addWidget(button, 2, 1)
        grid.addWidget(self.output, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_speed(self):
        distance = int(self.distance.text())
        distance = distance if 'Metric' == self.system.currentText() else distance * 1.609344
        speed = distance / int(self.time.text())
        speed_units = 'km/h' if 'Metric' == self.system.currentText() else 'mph'

        self.output.setText(f"Average speed is {speed:.2f} {speed_units}")


app = QApplication(sys.argv)
calculator = SpeedCalc()
calculator.show()

sys.exit(app.exec())


