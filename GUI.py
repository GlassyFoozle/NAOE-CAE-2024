import sys
import folium
import io
from PyQt5.QtWidgets import *
from PyQt5 import uic

# Load UI file
form_class = uic.loadUiType("GUI.ui")[0]


class WindowClass(QDialog, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('CAE Project')
        self.window_width, self.window_height = 1400, 800
        self.setMinimumSize(400, 300)

        # Load folium map
        self.coordinate = (35.532600, 127.524612)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=8,
            location=self.coordinate
        )

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)
        self.webEngineView.setHtml(self.data.getvalue().decode())

    # Update map and accident cases
    def update_map(self):
        # 현재 위치 아이콘
        icon_url = 'https://cdn4.iconfinder.com/data/icons/web-ui-color/128/Marker_red-512.png'
        ship_icon = folium.features.CustomIcon(icon_url, icon_size=(30, 30))

        lat = float(self.lat_input.text())
        lon = float(self.lon_input.text())

        self.coordinate = (lat, lon)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=11,
            location=self.coordinate
        )

        # Add new marker
        folium.Marker(location=self.coordinate, icon=ship_icon).add_to(self.map)

        # Save updated map to data object
        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)

        # Update web view with new map
        self.webView.setHtml(self.data.getvalue().decode())


if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()