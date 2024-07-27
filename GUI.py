import os
import sys
import io
import folium
from folium.plugins import MousePosition
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from model import acc_type_predict


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# UI 파일 불러오기
form_class = uic.loadUiType(resource_path("GUI.ui"))[0]


class WindowClass(QDialog, form_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Marine Accident Prediction System')
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

        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        mouse_position = MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Lat: ',
            lat_formatter=formatter,
            lng_formatter=formatter,
        )
        self.map.add_child(mouse_position)

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)
        self.webEngineView.setHtml(self.data.getvalue().decode())

        self.plot_graph(['기관이상', '부유물감김', '운항저해', '작업 중 인명사상', '전복', '좌초', '충돌', '침몰', '침수', '표류', '해양오염'], [1 for i in range(11)])

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
            zoom_start=11,
            location=self.coordinate
        )

        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        mouse_position = MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Lat: ',
            lat_formatter=formatter,
            lng_formatter=formatter,
        )
        self.map.add_child(mouse_position)

        # 현재 위치 마커 생성
        folium.Marker(location=self.coordinate, icon=ship_icon).add_to(self.map)

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)

        # 새로운 지도 표시
        self.webEngineView.setHtml(self.data.getvalue().decode())

        hour = int(self.hour_lineEdit.text())
        weather = self.weather_comboBox.currentText()
        vessel = self.vessel_comboBox.currentText()
        tons = float(self.tons_lineEdit.text())

        types, prob = acc_type_predict(lat, lon, hour, weather, vessel, tons)

        # 사고 유형 업데이트
        self.plot_graph(types, prob)

    def plot_graph(self, ylab, prob):
        self.graphWidget.setBackground('w')
        self.graphWidget.clear()
        yval = list(range(len(ylab)))

        ticks = []
        for i, item in enumerate(ylab):
            ticks.append((yval[i], item))
        ticks = [ticks]

        accident_colors = {'기관이상': '#B3B3B3', '부유물감김': '#FF0000', '운항저해': '#FF0000', '작업 중 인명사상': '#B3B3B3'
            , '전복': '#FF0000', '좌초': '#FF0000', '충돌': '#FF0000', '침몰': '#B3B3B3', '침수': '#B3B3B3'
            , '표류': '#B3B3B3', '해양오염': '#FF0000'}
        bargraph = pg.BarGraphItem(x0=0, y=yval, height=0.6, width=prob, brushes=[accident_colors[y] for y in ylab])
        self.graphWidget.addItem(bargraph)
        ax = self.graphWidget.getAxis('left')
        ax.setTicks(ticks)

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