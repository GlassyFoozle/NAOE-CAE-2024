import sys
import io
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Test Map')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Input fields and button
        input_layout = QHBoxLayout()
        self.lat_input = QLineEdit(self)
        self.lon_input = QLineEdit(self)
        self.add_marker_button = QPushButton('Add Marker', self)

        input_layout.addWidget(QLabel('Latitude:'))
        input_layout.addWidget(self.lat_input)
        input_layout.addWidget(QLabel('Longitude:'))
        input_layout.addWidget(self.lon_input)
        input_layout.addWidget(self.add_marker_button)

        self.layout.addLayout(input_layout)

        self.coordinate = (35.532600, 127.524612)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=8,
            location=self.coordinate
        )

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(self.data.getvalue().decode())
        self.layout.addWidget(self.webView)

        self.add_marker_button.clicked.connect(self.update_map)

    def update_map(self):
        lat = float(self.lat_input.text())
        lon = float(self.lon_input.text())

        self.coordinate = (lat, lon)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=8,
            location=self.coordinate
        )

        # Add new marker
        folium.Marker(location=self.coordinate).add_to(self.map)

        # Save updated map to data object
        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)

        # Update web view with new map
        self.webView.setHtml(self.data.getvalue().decode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 20px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
