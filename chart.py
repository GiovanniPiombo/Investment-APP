from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush, QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtWidgets import QWidget, QVBoxLayout

class ChartView(QChartView):
    def __init__(self, chart):
        super().__init__(chart)
        self.setRubberBand(QChartView.RectangleRubberBand)
        self.setInteractive(True)
        self.setDragMode(QChartView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)

    def wheelEvent(self, event):
        zoom_factor = 1.2
        if event.angleDelta().y() > 0:
            self.chart().zoom(zoom_factor)
        else:
            self.chart().zoom(1/zoom_factor)

    def mouseDoubleClickEvent(self, event):
        self.chart().zoomReset()

class Chart(QWidget):
    def __init__(self, years, values, invested_values, theme="dark"):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setObjectName("graphWidget")
        self.theme = theme
        
        self.growth_series = QLineSeries()
        self.growth_series.setName("Investment Value")
        
        self.invested_series = QLineSeries()
        self.invested_series.setName("Invested Amount")
        
        for year, value, invested in zip(years, values, invested_values):
            self.growth_series.append(year, value)
            self.invested_series.append(year, invested)

        self.chart = QChart()
        self.chart.addSeries(self.growth_series)
        self.chart.addSeries(self.invested_series)
        self.chart.setTitle("Investment Growth vs. Invested Amount")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.axis_x.setTitleText("Years")
        self.axis_y.setTitleText("Amount ($)")
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        
        self.growth_series.attachAxis(self.axis_x)
        self.growth_series.attachAxis(self.axis_y)
        self.invested_series.attachAxis(self.axis_x)
        self.invested_series.attachAxis(self.axis_y)
        
        self.apply_theme()
        self.chart_view = ChartView(self.chart)
        
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def apply_theme(self):
        if self.theme == "dark":
            bg_color = QColor("#2d2d2d")
            text_color = QColor("#E0E0E0")
            grid_color = QColor("#444")
            growth_color = QColor("#BB86FC")  
            invested_color = QColor("#03DAC6")  
        else:
            bg_color = QColor("#f8f8f8")
            text_color = QColor("#2C2C2C")
            grid_color = QColor("#c0c0c0")
            growth_color = QColor("#35b15a")  
            invested_color = QColor("#FF6D00")  
            
        self.chart.setBackgroundBrush(QBrush(bg_color))
        self.chart.setTitleBrush(QBrush(text_color))
        
        growth_pen = QPen(growth_color, 3)
        self.growth_series.setPen(growth_pen)
        
        invested_pen = QPen(invested_color, 2, Qt.DashLine)
        self.invested_series.setPen(invested_pen)
        
        for axis in [self.axis_x, self.axis_y]:
            axis.setLabelsBrush(QBrush(text_color))
            axis.setTitleBrush(QBrush(text_color))
            axis.setGridLineColor(grid_color)
            axis.setLinePenColor(text_color)
        
        legend = self.chart.legend()
        legend.setLabelColor(text_color)
        legend.setBackgroundVisible(True)
        legend.setBrush(QBrush(bg_color))
        legend.setPen(QPen(grid_color))

    def change_theme(self, theme):
        self.theme = theme
        self.apply_theme()