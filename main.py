from PyQt6.QtWidgets import QApplication
import matplotlib.animation as animation
import sys

from physics import Physics
from controlpid import Control
from visual import Visual
from animations import Animations
from controlpanel import ControlPanel
from graphwindow import GraphWindow
from pendulumwindow import PendulumWindow

"""
Main file for inverted pendulum on cart simulation
"""

# initialising classes
controller = Control()
pendulum = Physics(controller.u)
visualiser = Visual(pendulum)
animate = Animations(pendulum, controller, visualiser)

ctrl_panel = ControlPanel(pendulum, controller, visualiser, animate)
graph = GraphWindow(visualiser)
    
# animations with 50 fps
ani = animation.FuncAnimation(visualiser.fig, animate.animate_pendulum, frames=visualiser.frames, interval = 20, blit = True)
ani_graph = animation.FuncAnimation(visualiser.graph_fig, animate.animate_graph, frames=visualiser.frames, interval = 20, blit = True)
# start applicaiton
app = QApplication(sys.argv)
main_window = PendulumWindow(visualiser, graph, ctrl_panel)
main_window.show()
sys.exit(app.exec())