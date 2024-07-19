import sys
import folium
import io
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from tf_model import acc_type_predict

# UI 파일 불러오기
form_class = uic.loadUiType("GUI.ui")[0]


class WindowClass(QDialog, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('CAE Project')
        self.window_width, self.window_height = 1200, 800
        self.setGeometry(300, 100, self.window_width, self.window_height)
        self.setMinimumSize(400, 300)

        # 지도 불러오기
        self.coordinate = (35.532600, 127.524612)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=8,
            location=self.coordinate
        )

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)
        self.webEngineView.setHtml(self.data.getvalue().decode())

        self.update_button.clicked.connect(self.update_map)


    # Update map and accident cases
    def update_map(self):
        # 현재 위치 마커 아이콘
        icon_url = 'https://cdn4.iconfinder.com/data/icons/web-ui-color/128/Marker_red-512.png'
        ship_icon = folium.features.CustomIcon(icon_url, icon_size=(30, 30))

        lat = float(self.lat_input.value())
        lon = float(self.lon_input.value())

        self.coordinate = (lat, lon)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=10,
            location=self.coordinate
        )

        # 현재 위치 마커 생성
        folium.Marker(location=self.coordinate, icon=ship_icon).add_to(self.map)

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)

        # 새로운 지도 표시
        self.webEngineView.setHtml(self.data.getvalue().decode())

        weather = self.weather_comboBox.currentText()
        vessel = self.vessel_comboBox.currentText()

        # 사고 유형 업데이트
        types, probabilities = acc_type_predict(lat, lon, weather, vessel)

        self.t1_accident.setText(f"1. {types[0]}, 확률: {round(100 * probabilities[0], 1)}%")
        self.t2_accident.setText(f"2. {types[1]}, 확률: {round(100 * probabilities[1], 1)}%")
        self.t3_accident.setText(f"3. {types[2]}, 확률: {round(100 * probabilities[2], 1)}%")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_W:
            cur_lat = float(self.lat_input.value())
            self.lat_input.setValue(cur_lat + 0.1)
        elif e.key() == Qt.Key_A:
            cur_lon = float(self.lon_input.value())
            self.lon_input.setValue(cur_lon - 0.1)
        elif e.key() == Qt.Key_S:
            cur_lat = float(self.lat_input.value())
            self.lat_input.setValue(cur_lat - 0.1)
        elif e.key() == Qt.Key_D:
            cur_lon = float(self.lon_input.value())
            self.lon_input.setValue(cur_lon + 0.1)


if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()