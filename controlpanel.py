import numpy as np
from PyQt6.QtWidgets import QMainWindow, QWidget, QSlider, QLabel, QGridLayout, QPushButton, QCheckBox
from PyQt6.QtCore import Qt

class ControlPanel(QMainWindow):

    """
    Control panel window.


    Attributes:
    ----------- 
    pendulum:
        Instance of Physics class
    controller:
        Instance of Control class
    visualiser:
        Instance of Visual class
    animate:
        Instance of Animations class
    control_panel_visibility:
        Boolean that records whether control panel is visible
    various sliders & buttons:
        Sliders and buttons that are present in the control panel window


    Methods:
    --------
    update_slider(self, label, name_start, new_value, variable_name, object_from, title_name):
        Updates a given objects attribute as well as the label of the slider to the value on the slider
    add_slider(self, scale, min, max, slider_val, name_colon):
        Helper function used to create new sliders
    add_button(self, text, function, row, col, layout):
        Helper function used to create new buttons
    reset(self, press):
        Function used to reset the pendulum to its initial angle position, returning cart position, cart velocity,
        angular velocity, error integrals and control inputs to zero as well as reseting the frames
        
    """

    def __init__(self, pendulum, controller, visualiser, animate):

        super().__init__() # inherits parent class features (from QMainWindow)
        
        self.setWindowTitle("Control Panel")

        self.pendulum = pendulum
        self.controller = controller
        self.visualiser = visualiser
        self.animate = animate

        # central widget required in PyQt6
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # control panel initially invisible
        self.control_panel_visibility = False

        # helper functions used to create various sliders for variables
        kp_slider, kp_label, self.kp_value = self.add_slider(1, 0, 150, 100, "kp: ")
        kp_slider.valueChanged.connect(lambda value : self.update_slider(kp_label, "kp", value, "kp_value", self.controller, "kp"))
        # lambda function needed so that slider.valueChanged.connect() can pass the slider value in

        kd_slider, kd_label, self.kd_value = self.add_slider(1, 0, 50, 20, "kd: ")
        kd_slider.valueChanged.connect(lambda value : self.update_slider(kd_label, "kd", value, "kd_value", self.controller, "kd"))

        ki_slider, ki_label, self.ki_value = self.add_slider(1, 0, 50, 1, "ki: ")
        ki_slider.valueChanged.connect(lambda value : self.update_slider(ki_label, "ki", value, "ki_value", self.controller, "ki"))

        kp_cart_slider, kp_cart_label, self.kp_cart_value = self.add_slider(1, 0, 50, 2, "cart kp: ")
        kp_cart_slider.valueChanged.connect(lambda value : self.update_slider(kp_cart_label, "kp_cart", value/10, "kp_cart_value", self.controller, "cart kp"))

        kd_cart_slider, kd_cart_label, self.kd_cart_value = self.add_slider(10, 0, 20, 1, "cart kd: ")
        kd_cart_slider.valueChanged.connect(lambda value : self.update_slider(kd_cart_label, "kd_cart", value/10, "kd_cart_value", self.controller, "cart kd"))

        ki_cart_slider, ki_cart_label, self.ki_cart_value = self.add_slider(100, 0, 50, 1, "cart ki: ")
        ki_cart_slider.valueChanged.connect(lambda value : self.update_slider(ki_cart_label, "ki_cart", value/100, "ki_cart_value", self.controller, "cart ki"))

        v_slider, v_label, self.v_value = self.add_slider(1, -5, 5, 1, "add angle velocity: ")
        v_slider.valueChanged.connect(lambda value : self.update_slider(v_label, "", value, "v_value", self.controller, "add angle velocity"))

        init_angle_slider, init_angle_label, self.init_angle_value = self.add_slider(1, -180, 180, -20, "initial angle: ")
        init_angle_slider.valueChanged.connect(lambda value : self.update_slider(init_angle_label, "init_angle", value, "init_angle_value", self.pendulum, "initial angle"))

        angle_damping_slider, angle_damping_slider_label, self.angle_damping_value = self.add_slider(10, 0, 50, 1, "angular damping: ")
        angle_damping_slider.valueChanged.connect(lambda value : self.update_slider(angle_damping_slider_label, "angular_damping", value/10, "angle_damping_value", self.pendulum, "angular damping"))

        angle_slider, angle_slider_label, self.set_angle_value = self.add_slider(1, -180, 180, 0, "set angle value: ")
        angle_slider.valueChanged.connect(lambda value : self.update_slider(angle_slider_label, "angle", value, "set_angle_value", self, "set angle value"))

        cart_damping_slider, cart_damping_slider_label, self.cart_damping_value = self.add_slider(10, 0, 100, 5, "cart damping: ")
        cart_damping_slider.valueChanged.connect(lambda value : self.update_slider(cart_damping_slider_label, "cart_damping", value/10, "cart_damping_value", self.pendulum, "cart damping"))

        # creating and adding various widgets to layout
        layout = QGridLayout(central_widget)
        layout.addWidget(kp_slider, 1, 0)
        layout.addWidget(kp_label, 0, 0)
        layout.addWidget(kd_slider, 3, 0)
        layout.addWidget(kd_label, 2, 0)
        layout.addWidget(ki_slider, 5, 0)
        layout.addWidget(ki_label, 4, 0)
        layout.addWidget(kp_cart_slider, 1, 1)
        layout.addWidget(kp_cart_label, 0, 1)
        layout.addWidget(kd_cart_slider, 3, 1)
        layout.addWidget(kd_cart_label, 2, 1)
        layout.addWidget(ki_cart_slider, 5, 1)
        layout.addWidget(ki_cart_label, 4, 1)
        layout.addWidget(v_slider, 1, 2)
        layout.addWidget(v_label, 0, 2)
        layout.addWidget(init_angle_slider, 3, 2)
        layout.addWidget(init_angle_label, 2, 2)
        layout.addWidget(angle_slider, 5, 2)
        layout.addWidget(angle_slider_label, 4, 2)
        layout.addWidget(angle_damping_slider, 7, 0)
        layout.addWidget(angle_damping_slider_label, 6, 0)
        layout.addWidget(cart_damping_slider, 7, 1)
        layout.addWidget(cart_damping_slider_label, 6, 1)

        # only window title is visible, no minimise/maximise/close buttons
        self.setWindowFlags(Qt.WindowType.Window |
                    Qt.WindowType.CustomizeWindowHint |
                    Qt.WindowType.WindowTitleHint)

        # using helper function to create various buttons
        self.velocity_button = self.add_button("Add Velocity (press 'V')", lambda : self.pendulum.add_velocity(self.v_value), 8, 0, layout)
        self.angle_button = self.add_button("Set Angle (press 'A')", lambda : self.pendulum.set_angle(self.set_angle_value), 8, 1, layout)
        self.exit_button = self.add_button("Hide Control Panel (press 'C')", lambda : (self.hide(), setattr(self, "control_panel_visibility", False)), 8, 2, layout)
        self.reset_button = self.add_button("Reset (press 'R')", self.reset, 9, 0, layout)
        self.pause_button = self.add_button("Pause (press 'P')", self.visualiser.pause, 9, 1, layout)

        # checkbox for controller enable / disable
        enable_controller = QCheckBox()
        enable_label = QLabel("Enable Controller:")
        layout.addWidget(enable_label, 10, 2)
        enable_controller.toggled.connect(lambda value : setattr(self.controller, "controller_enabled", value))
        layout.addWidget(enable_controller, 11, 2)

        arrow_label = QLabel("Control Cart with Arrow Keys:")
        layout.addWidget(arrow_label, 10, 0)

        # arrow keys as buttons for manual control input
        self.right = QPushButton(">")
        self.right.pressed.connect(lambda : setattr(self.animate, "right_pressed", True))
        self.right.released.connect(lambda : setattr(self.animate, "right_pressed", False))
        layout.addWidget(self.right, 11, 1)

        self.left = QPushButton("<")
        self.left.pressed.connect(lambda : setattr(self.animate, "left_pressed", True))
        self.left.released.connect(lambda : setattr(self.animate, "left_pressed", False))
        layout.addWidget(self.left, 11, 0)

    def update_slider(self, label, name_start, new_value, variable_name, object_from, title_name):
        label.setText(title_name + ": " + str(new_value))
        setattr(self, variable_name, new_value) # updating label
        if name_start != "v_value": # no object update for angular velocity adding
            # updating original object attributes
            if name_start != "angle" and name_start != "init_angle":
                setattr(object_from, name_start, new_value)
            elif name_start == "init_angle": # radian conversions needed for angular sliders
                setattr(object_from, name_start, np.deg2rad(new_value))

    def add_slider(self, scale, min, max, slider_val, name_colon):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(slider_val)
        # scale used so that decimal values can be selected on sliders, as PyQt6 sliders don't natively
        # allow decimal values to be selected
        value = (slider.value()/scale)
        label = QLabel(name_colon + str(value))
        return slider, label, value
    
    def add_button(self, text, function, row, col, layout):
        button = QPushButton(text)
        button.clicked.connect(function)
        layout.addWidget(button, row, col)
        return button

    def reset(self, press):
    
        self.pendulum.x = 0
        self.pendulum.xdot = 0
        self.pendulum.angle = self.pendulum.init_angle
        self.pendulum.angular_velocity = 0
        self.pendulum.angle_error_integral = 0
        self.pendulum.cart_velocity_error_integral = 0
        self.controller.u_angle = 0
        self.controller.u_cart = 0
        self.controller.u = 0
        
        self.visualiser.frames = self.visualiser.frame_count() # resets frames