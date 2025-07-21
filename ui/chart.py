from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush, QPainter
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChartView(QChartView):
    """Custom QChartView to handle zooming, panning and value display"""
    def __init__(self, chart, parent):
        super().__init__(chart)
        self.setRubberBand(QChartView.RectangleRubberBand)
        self.setInteractive(True)
        self.setDragMode(QChartView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMouseTracking(True)
        
        # Reference to parent chart widget
        self.chart_widget = parent
        
        # Store original range for zoom limits
        self.original_range_set = False
        self.original_x_range = None
        self.original_y_range = None
        self.max_zoom_factor = 10.0
        self.min_zoom_factor = 0.1

    def wheelEvent(self, event):
        """Handle zooming with mouse wheel with limits"""
        zoom_factor = 1.2
        
        # Get current axis ranges
        x_axis = self.chart().axes(Qt.Horizontal)[0] if self.chart().axes(Qt.Horizontal) else None
        y_axis = self.chart().axes(Qt.Vertical)[0] if self.chart().axes(Qt.Vertical) else None
        
        if not x_axis or not y_axis:
            return
            
        # Store original ranges if not done yet
        if not self.original_range_set:
            self.original_x_range = (x_axis.min(), x_axis.max())
            self.original_y_range = (y_axis.min(), y_axis.max())
            self.original_range_set = True
        
        current_x_range = x_axis.max() - x_axis.min()
        current_y_range = y_axis.max() - y_axis.min()
        original_x_range = self.original_x_range[1] - self.original_x_range[0]
        original_y_range = self.original_y_range[1] - self.original_y_range[0]
        
        # Calculate current zoom levels
        current_x_zoom = original_x_range / current_x_range
        current_y_zoom = original_y_range / current_y_range
        
        # Check zoom limits
        if event.angleDelta().y() > 0:  # Zoom in
            new_x_zoom = current_x_zoom * zoom_factor
            new_y_zoom = current_y_zoom * zoom_factor
            if new_x_zoom > self.max_zoom_factor or new_y_zoom > self.max_zoom_factor:
                return
        else:  # Zoom out
            new_x_zoom = current_x_zoom / zoom_factor
            new_y_zoom = current_y_zoom / zoom_factor
            if new_x_zoom < self.min_zoom_factor or new_y_zoom < self.min_zoom_factor:
                return
        
        # Apply zoom
        if event.angleDelta().y() > 0:
            self.chart().zoom(zoom_factor)
        else:
            self.chart().zoom(1/zoom_factor)

    def mouseDoubleClickEvent(self, event):
        """Reset zoom on double click"""
        self.chart().zoomReset()

    def mouseMoveEvent(self, event):
        """Handle mouse move for value display"""
        super().mouseMoveEvent(event)
        
        # Convert mouse position to chart coordinates
        chart_pos = self.chart().mapToValue(event.position())
        
        # Find closest points on both series
        growth_series = None
        invested_series = None
        
        for series in self.chart().series():
            if series.name() == "Investment Value":
                growth_series = series
            elif series.name() == "Invested Amount":
                invested_series = series
        
        if not growth_series or not invested_series:
            return
            
        # Find closest data points
        growth_point = self.find_closest_point(growth_series, chart_pos.x())
        invested_point = self.find_closest_point(invested_series, chart_pos.x())
        
        if growth_point and invested_point:
            # Update label with values
            year = int(growth_point.x())
            growth_value = growth_point.y()
            invested_value = invested_point.y()
            
            self.chart_widget.update_values_label(year, growth_value, invested_value)

    def find_closest_point(self, series, x_value):
        """Find the closest point in a series to the given x value"""
        if not series.points():
            return None
            
        closest_point = None
        min_distance = float('inf')
        
        for point in series.points():
            distance = abs(point.x() - x_value)
            if distance < min_distance:
                min_distance = distance
                closest_point = point
                
        return closest_point

    def leaveEvent(self, event):
        """Clear values when mouse leaves the chart"""
        self.chart_widget.clear_values_label()
        super().leaveEvent(event)

class Chart(QWidget):
    """Widget to display investment growth chart"""

    def __init__(self, years, values, invested_values, theme="dark"):
        """Initialize the Chart widget with investment data"""
        super().__init__()
        self.setFixedSize(600, 400)
        self.setObjectName("graphWidget")
        self.theme = theme
        
        # Create values label
        self.values_label = QLabel("Move mouse over chart to see values")
        self.values_label.setAlignment(Qt.AlignLeft)
        self.values_label.setMinimumHeight(30)
        
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
        
        # Improve X axis (Years)
        self.axis_x.setLabelFormat("%d")  # Integer format for years
        self.axis_x.setTickCount(min(10, len(years)))  # Reasonable number of ticks
        self.axis_x.setMinorTickCount(0)  # No minor ticks for cleaner look
        
        # Improve Y axis (Amount)
        self.axis_y.setLabelFormat("$%.0f")  # Currency format without decimals
        max_value = max(max(values), max(invested_values))
        min_value = min(min(values), min(invested_values))
        
        # Set nice round numbers for Y axis range
        y_range = max_value - min_value
        y_padding = y_range * 0.1  # 10% padding
        self.axis_y.setMin(max(0, min_value - y_padding))
        self.axis_y.setMax(max_value + y_padding)
        
        # Calculate appropriate tick count based on value range
        if max_value < 10000:
            tick_count = 8
        elif max_value < 100000:
            tick_count = 6
        else:
            tick_count = 5
        self.axis_y.setTickCount(tick_count)
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        
        self.growth_series.attachAxis(self.axis_x)
        self.growth_series.attachAxis(self.axis_y)
        self.invested_series.attachAxis(self.axis_x)
        self.invested_series.attachAxis(self.axis_y)
        
        self.apply_theme()
        self.chart_view = ChartView(self.chart, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.values_label)
        layout.addWidget(self.chart_view)
        self.setLayout(layout)

    def apply_theme(self):
        """Apply the selected theme to the chart"""
        if self.theme == "dark":
            bg_color = QColor("#2d2d2d")
            text_color = QColor("#E0E0E0")
            grid_color = QColor("#444444")
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
            # Make axis lines more visible
            axis.setLineVisible(True)
            axis.setGridLineVisible(True)
            # Improve font size for better readability
            axis.setLabelsFont(axis.labelsFont())
            font = axis.labelsFont()
            font.setPointSize(9)
            axis.setLabelsFont(font)
            # Make title font slightly larger
            title_font = axis.titleFont()
            title_font.setPointSize(10)
            title_font.setBold(True)
            axis.setTitleFont(title_font)
        
        legend = self.chart.legend()
        legend.setLabelColor(text_color)
        legend.setBackgroundVisible(True)
        legend.setBrush(QBrush(bg_color))
        legend.setPen(QPen(grid_color))
        
        # Apply theme to values label
        if hasattr(self, 'values_label'):
            self.values_label.setStyleSheet(f"color: {text_color.name()}; font-size: 12px; font-weight: bold;")

    def update_values_label(self, year, growth_value, invested_value):
        """Update the values label with current data"""
        text = f"Year: {year} | Investment Value: ${growth_value:,.2f} | Invested Amount: ${invested_value:,.2f}"
        self.values_label.setText(text)
        
    def clear_values_label(self):
        """Clear the values label"""
        self.values_label.setText("Move mouse over chart to see values")

    def change_theme(self, theme):
        """Change the theme of the chart"""
        self.theme = theme
        self.apply_theme()