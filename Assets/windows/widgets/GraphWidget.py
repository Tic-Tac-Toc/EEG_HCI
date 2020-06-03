from PySide2.QtWidgets import (QHBoxLayout, QHeaderView, QSizePolicy, QTableView, QWidget)
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QFont
from PySide2.QtCharts import QtCharts

from Assets.windows.table_model import CustomTableModel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class GraphWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Creating a QTableView
        self.table_view = QTableView()

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        self.size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)   
        
        # generate the plot
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout = True
        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        self.ax.margins(0,0)
        self.canvas = FigureCanvas(self.fig)  

        ## Left layout
        self.size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(self.size)
        self.main_layout.addWidget(self.table_view)        

        ## Right Layout
        self.size.setHorizontalStretch(4)
        self.canvas.setSizePolicy(self.size)
        self.main_layout.addWidget(self.canvas)

        # Creating QChartView
        self.chart_view = QtCharts.QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)  

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    def Load(self, data):
        # Getting the Model
        self.model = CustomTableModel(data)

        self.table_view.setModel(self.model)

        # QTableView Headers
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)

        #Update plot
        self.ax.clear()
        for i in range(10):
            x, y = [], []
            for j in range(i * 200, i * 200 + 200):
                x.append(data[0].values[j])
                y.append(data[1].values[j])

            self.ax.plot(x,y, linewidth=0.5, label="Epoch : " + str(i + 1))

        self.ax.legend(loc='best', fontsize='small')   
        # generate the canvas to display the plot  
        self.canvas.draw()
        self.canvas.flush_events()

        def use_qchart():
            # Creating QChart
            self.chart = QtCharts.QChart()
            self.chart.setAnimationOptions(QtCharts.QChart.AllAnimations)

            font = QFont()
            font.setPixelSize(20)
            self.chart.setTitleFont(font)

            self.add_series("Amplitude (mV)")
            self.chart_view.setChart(self.chart)

    def add_series(self, name):
        for i in range(10):
            self.add_epoch_series(name, i*200)           

        self.chart.addSeries(self.series)

        # Setting X-axis
        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setTickCount(10)
        #self.axis_x.setTitleText("Time (s)")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        # Setting Y-axis
        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setTickCount(10)
        #self.axis_y.setLabelFormat("%.5f")
        self.axis_y.setTitleText("Amplitude (mV)")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        # Getting the color from the QChart to use it on the QTableView
        self.model.color = "{}".format(self.series.pen().color().name())

    def add_epoch_series(self, name, startIndex):
        # Create QLineSeries
        if startIndex == 0:
            self.series = QtCharts.QLineSeries()
            self.series.setName(name)

        # Filling QLineSeries
        for i in range(startIndex, startIndex + 200):
            # Getting the data
            t = float(self.model.index(i, 0).data())
            y = float(self.model.index(i, 1).data())

            self.series.append(t, y)
        

    def SetChartTitle(self, title):        
        self.chart.setTitle(title)