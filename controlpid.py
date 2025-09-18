class Control:

    """
    PID controllers for inverted pendulum on cart.
    Includes controller for keeping pendulum upright and controller for minimising cart movement.


    Attributes:
    ----------- 
    kp:
        Proportional gain for angle error
    kd:
        Derivative gain for angular velocity
    ki:
        Integral gain for angle error integral
    kp_cart:
        Proportional gain for cart velocity error
    kd_cart:
        Derivate gain for cart acceleration / control input
    ki_cart:
        Integral gain for cart velocity error integral / cart displacement
    u:
        Control input
    u_angle:
        Control input from angle controller
    u_cart:
        Control input from cart controller
    controller_enabled:
        Boolean controlled externally used to enable / disable controller


    Methods:
    --------
    compute(self, angle_error, angular_velocity, angle_error_integral, cart_velocity_error, cart_velocity_error_integral):
        Determines control inputs from angle & cart velocity controllers

    """

    def __init__(self):

        # gains
        self.kp = 100
        self.kd = 20
        self.ki = 1
        self.kp_cart = 0.2
        self.kd_cart = 0.1
        self.ki_cart = 0.01

        self.u = 0 # initial cart control input (acceleration)

        # individual control inputs for angle & cart PID 
        self.u_angle = 0
        self.u_cart = 0

        self.controller_enabled = False

    def compute(self, angle_error, angular_velocity, angle_error_integral, cart_velocity_error, cart_velocity_error_integral):

        # calculating control input
        if self.controller_enabled == True:
            self.u_angle = - self.kp*angle_error + self.kd*(angular_velocity) - self.ki*angle_error_integral
            self.u_cart = self.kp_cart*cart_velocity_error - self.kd_cart*(self.u) + self.ki_cart*cart_velocity_error_integral

        # controller off
        else:
            self.u_angle = 0
            self.u_cart = 0  
            
        self.u = self.u_angle + self.u_cart