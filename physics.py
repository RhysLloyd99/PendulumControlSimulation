import numpy as np

class Physics:

    """
    Physics calculations for pendulum on a cart.


    Attributes:
    ----------- 
    angle:
        Angle of the pendulum relative to verically upwards
    angular_velocity:
        Angular velocity of the pendulum
    angular_acceleration:
        Angular acceleration of the pendulum
    u:
        Control input of the pendulum on the cart
    xdot:
        Velocity of the cart
    x:
        position of the cart
    dt:
        Time interval used for Euler integration
    g:
        Acceleration due to gravity
    length:
        Length of the pendulum
    angular_damping:
        Damping constant for angular acceleration
    cart_damping:
        Damping constant for cart acceleration
    angle_error_integral:
        Euler integral of angle error
    angle_error:
        Error of current angle from angle_ref
    cart_velocity_error:
        Error of current cart velocity from cart_ref
    cart_velocity_error_integral:
        Euler integral of cart velocity error
    cart_ref:
        Reference velocity used to calculate cart_velocity_error
    angle_ref:
        Reference angle used to calculate angle_error
    graph_visibility:
        Boolean used externally to determine visibility of graph window
    init_angle:
        Initial angle of pendulum relative to vertically upwards when simulation begins or is reset


    Methods:
    --------
    compute(self, u):
        Updates angular acceleration, angular velocity, angle, cart velocity (xdot), cart position (x)
        and errors, aswell as limiting the angle of the pendulum to [-180, 180]
    pendulum_pos(self, theta):
        Returns x, y coordinates of pendulum from angle, cart position (x), and length of the pendulum
    add_velocity(self, add_v):
        Adds parameter "add_v" to angular angular velocity, connected to a button
    set_angle(self, angle_in):
        Sets angle to an input slider value determined by the user, connected to a button

    """

    def __init__(self, u):
        
        self.angle = np.deg2rad(-20)
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.u = u # control input
        self.xdot = 0
        self.x = 0
        self.dt = 0.03

        self.g = 9.81
        self.length = 15
        self.angular_damping = 0.1
        self.cart_damping = 0.5

        self.angle_error_integral = 0
        self.angle_error = 0
        self.cart_velocity_error = 0
        self.cart_velocity_error_integral = 0

        self.cart_ref = 0
        self.angle_ref = 0

        self.graph_visibility = False
        self.init_angle = np.deg2rad(-20)

        
    def compute(self, u):

        self.angular_acceleration = ( 
            (self.g*np.sin(self.angle)/self.length) 
            - u*np.cos(self.angle)/self.length 
            - (self.angular_damping * self.angular_velocity) )

        self.angle_error = np.deg2rad(self.angle_ref) - self.angle
        self.cart_velocity_error = self.cart_ref - self.xdot

        # Euler integration
        self.angle_error_integral += self.angle_error * self.dt
        self.cart_velocity_error_integral += self.cart_velocity_error * self.dt
        self.angular_velocity += self.angular_acceleration * self.dt
        self.angle += self.angular_velocity * self.dt
        self.xdot += (u - self.cart_damping*self.xdot) * self.dt
        self.x += self.xdot*self.dt

        # limiting angle
        if self.angle < - np.pi:
            self.angle += 2 * np.pi

        elif self.angle > np.pi:
            self.angle -= 2* np.pi
            
    
    def pendulum_pos(self, theta): # returns x & y coordinates as function of theta (polar)
        return (self.x + self.length*np.sin(theta), self.length*np.cos(theta)) 
    
    def add_velocity(self, add_v):
        self.angular_velocity += add_v

    def set_angle(self, angle_in):
        self.angle = np.deg2rad(angle_in)
