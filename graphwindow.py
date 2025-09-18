from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # widget for matplotlib

class GraphWindow(QMainWindow):

    """
    Graph Plot Window.


    Attributes:
    ----------- 
    visualiser:
        Instance of Visual class
    canvas:
        Matplotlib graph figure embedded in widget
    exit_button:
        Button for closing / toggling visibility of graph window
        
    """

    def __init__(self, visualiser):
        super().__init__() # inherits parent class (from QMainWindow)
        
        self.setWindowTitle("Inverted Pendulum Graph")

        # central widget required in PyQt6
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.graph_visibility = False

        self.visualiser = visualiser

        layout = QGridLayout(central_widget)
        # embedding graph figure
        self.canvas = FigureCanvas(self.visualiser.graph_fig)
        layout.addWidget(self.canvas, 0, 0)

        # only window title is visible, no minimise/maximise/close buttons
        self.setWindowFlags(Qt.WindowType.Window |
                    Qt.WindowType.CustomizeWindowHint |
                    Qt.WindowType.WindowTitleHint)
        
        self.exit_button = QPushButton("Hide Graph (press 'G')")
        self.exit_button.clicked.connect(lambda : (self.hide(), setattr(self, "graph_visibility", False)))
        layout.addWidget(self.exit_button, 7, 0)
