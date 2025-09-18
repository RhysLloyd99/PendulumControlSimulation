from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QApplication
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PendulumWindow(QMainWindow):

    """
    Pendulum animation window.


    Attributes:
    ----------- 
    ctrl_panel:
        Instance of class Control
    visualiser:
        Instance of class Visual
    graph:
        Instance of class GraphWindow
    canvas:
        Matplotlib pendulum animation figure embedded in widget
    graph_button, control_button:
        Buttons used for showing/hiding graph/control panel windows

    Methods:
    --------
    open_graph(self):
        Toggles graph window visibility
    open_control_panel(self):
        Toggles control panel window visibility
    closeEvent(self, press):
        Quits the application when the pendulum window is closed. Prevents unclosable control panel and 
        graph window from remaining after closing
        
    """

    def __init__(self, visualiser, graph, ctrl_panel):
        super().__init__()

        self.setWindowTitle("Inverted Pendulum")

        # central widget required in PyQt6
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.ctrl_panel = ctrl_panel
        self.visualiser = visualiser
        self.graph = graph

        layout = QGridLayout(central_widget)
        # embedding pendulum animation
        self.canvas = FigureCanvas(self.visualiser.fig)
        layout.addWidget(self.canvas, 0, 0, 1, 2)

        # Adding buttons
        graph_button = QPushButton("Show/Hide Graph (press 'G')")
        graph_button.clicked.connect(self.open_graph)
        graph_button.setShortcut("g")
        layout.addWidget(graph_button, 1, 1)

        control_button = QPushButton("Control Panel (press 'C')")
        control_button.clicked.connect(self.open_control_panel)
        control_button.setShortcut("c")
        layout.addWidget(control_button, 1, 0)

        # button shortcut key binds
        self.ctrl_panel.velocity_button.setShortcut("v")
        self.ctrl_panel.angle_button.setShortcut("a")
        self.ctrl_panel.reset_button.setShortcut("r")
        self.ctrl_panel.exit_button.setShortcut("c")
        self.ctrl_panel.pause_button.setShortcut("p")
        self.ctrl_panel.right.setShortcut(Qt.Key.Key_Right)
        self.ctrl_panel.left.setShortcut(Qt.Key.Key_Left)

        self.graph.exit_button.setShortcut("g")

    def open_graph(self):

        self.graph.graph_visibility = not self.graph.graph_visibility
        if self.graph.graph_visibility == True:
            self.graph.show()
        else:
            self.graph.hide()

    def open_control_panel(self):

        self.ctrl_panel.control_panel_visibility = not self.ctrl_panel.control_panel_visibility
        if self.ctrl_panel.control_panel_visibility == True:
            self.ctrl_panel.show()
        else:
            self.ctrl_panel.hide()

    def closeEvent(self, press): # method which is called when window is closed
        QApplication.quit()
        press.accept()
