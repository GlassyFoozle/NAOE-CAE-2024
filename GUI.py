import os
import sys
import io
import folium
from folium.plugins import MousePosition
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtTest import *
from PyQt5 import uic, QtGui
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
        self.setWindowTitle('MAPS')
        self.setWindowIcon(QtGui.QIcon(resource_path('icon.ico')))
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

        acc_types = ['기관이상', '부유물감김', '운항저해', '작업 중 인명사상', '전복', '좌초', '충돌', '침몰', '침수', '표류', '해양오염']
        self.plot_graph(acc_types, [0 for i in range(len(acc_types))])

        self.update_button.clicked.connect(self.update_map)
        self.example_button.clicked.connect(self.example_route)
        self.viewdata_button.clicked.connect(self.view_data)

    # Update map and accident cases
    def update_map(self, route_coordinates=None):
        # 현재 위치 마커 아이콘
        icon_url = 'https://cdn4.iconfinder.com/data/icons/web-ui-color/128/Marker_red-512.png'
        ship_icon = folium.features.CustomIcon(icon_url, icon_size=(30, 30))

        lat = float(self.lat_input.value())
        lon = float(self.lon_input.value())

        self.coordinate = (lat, lon)
        self.map = folium.Map(
            title="Start Point",
            zoom_start=13,
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

        print(route_coordinates)
        if route_coordinates is not False:
            for coord in route_coordinates:
                folium.CircleMarker(location=coord, radius=1, fill_color='black', color='black').add_to(self.map)
            folium.PolyLine(locations=route_coordinates, color='black', weight=1).add_to(self.map)

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

        colors = ['#B3B3B3'] * (len(ylab) -3) + ['#FF0000'] * 3
        bargraph = pg.BarGraphItem(x0=0, y=yval, height=0.6, width=prob, brushes=colors)
        self.graphWidget.addItem(bargraph)
        ax = self.graphWidget.getAxis('left')
        ax.setTicks(ticks)

    def example_route(self):
        route_coordinates = [
            (35.62057, 126.46879),
            (35.62194, 126.46332),
            (35.62015, 126.45814),
            (35.62933, 126.45611),
            (35.64131, 126.45255),
            (35.6509, 126.45294),
            (35.6748, 126.45229),
            (35.70157, 126.45041),
            (35.72903, 126.44019),
            (35.76323, 126.41324),
            (35.7853, 126.40165),
            (35.81113, 126.38672),
            (35.82366, 126.38161),
            (35.83792, 126.38904),
            (35.85434, 126.39101),
            (35.86669, 126.39625),
            (35.89058, 126.41556),
            (35.91728, 126.43032),
            (35.94702, 126.46637),
            (35.96877, 126.48826),
            (35.98058, 126.51323),
            (35.98, 126.53503),
            (35.97974, 126.54847),
            (35.97974, 126.56593),
            (35.98012, 126.57928),
            (35.98077, 126.59402),
            (35.98137, 126.60649),
            (35.98169, 126.6185),
            (35.97946, 126.62795)
        ]
        for curcoord in route_coordinates:
            self.lat_input.setValue(curcoord[0])
            self.lon_input.setValue(curcoord[1])
            self.update_map(route_coordinates)
            QTest.qWait(1000)

    def view_data(self):
        acc = self.acc_comboBox.currentText()
        filename = "html_files/" + acc + "_heatmap.html"
        url = QUrl.fromLocalFile(resource_path(filename))
        self.webEngineView.load(url)

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