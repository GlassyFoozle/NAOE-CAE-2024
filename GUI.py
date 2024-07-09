import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Map Coordinate Marker')
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()

        # Latitude input
        self.lat_label = QLabel('Latitude:', self)
        layout.addWidget(self.lat_label)
        self.lat_input = QLineEdit(self)
        layout.addWidget(self.lat_input)

        # Longitude input
        self.lng_label = QLabel('Longitude:', self)
        layout.addWidget(self.lng_label)
        self.lng_input = QLineEdit(self)
        layout.addWidget(self.lng_input)

        # Button to mark the point
        self.mark_button = QPushButton('Mark Point', self)
        self.mark_button.clicked.connect(self.mark_point)
        layout.addWidget(self.mark_button)

        # Web view to display the map
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("file:///map.html"))
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def mark_point(self):
        try:
            lat = float(self.lat_input.text())
            lng = float(self.lng_input.text())
            self.browser.page().runJavaScript(f'placeMarker({lat}, {lng})')
        except ValueError:
            self.show_error("Invalid input", "Please enter valid coordinates.")

    def show_error(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle(title)
        error_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapApp()
    ex.show()
    sys.exit(app.exec_())
