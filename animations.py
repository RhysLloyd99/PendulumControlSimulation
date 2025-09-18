import numpy as np

class Animations:

    """
    Animation of pendulum on cart and graphs.


    Attributes:
    ----------- 
    pendulum:
        Instance of Physics class
    controller:
        Instance of Control class
    visualiser:
        Instance of Visual class
    right_pressed:
        Boolean recording whether right arrow is pressed
    left_pressed:
        Boolean recording whether left arrow is pressed
    

    Methods:
    --------
    animate_pendulum(self, i):
        Function used when animating to repeatedly compute attributes of Physics and Control class
        as well as aspects of animation such as positions of various objects. Parameter 'i' is required
        by FuncAnimation, but isn't used directly in function.
    animate_graph(self, i):
        Function used to repeatedly append to lists and update plots for graph animation. Also features
        limiting of list sizes as well as rolling of the time axis, similar to the visual of an oscilloscope.
        Again parameter 'i' is required by FuncAnimation, but isn't used directly in function.
        
    """

    def __init__(self, pendulum, controller, visualiser):

        self.pendulum = pendulum
        self.controller = controller
        self.visualiser = visualiser

        self.right_pressed = False
        self.left_pressed = False

    def animate_pendulum(self, i):

        # no animation if paused is true
        if self.visualiser.paused == False:

            self.pendulum.compute(self.controller.u)
            self.controller.compute(self.pendulum.angle_error, self.pendulum.angular_velocity, 
                    self.pendulum.angle_error_integral, self.pendulum.cart_velocity_error, 
                    self.pendulum.cart_velocity_error_integral)
            
            # arrow buttons can be used to manually accelerate cart
            if self.right_pressed == True:
                self.controller.u += 50

            if self.left_pressed == True:
                self.controller.u -= 50
            
            # updating pendulum positions
            self.visualiser.update_pendulum(self.pendulum)

            # objects altered must be returned for real time simulation
        return self.visualiser.line, self.visualiser.circle, self.visualiser.cart, self.visualiser.leftwheel, self.visualiser.rightwheel, self.visualiser.angle_label

    def animate_graph(self, i):

        if self.visualiser.paused == False:
            
            # updating lists for graph
            self.visualiser.update_graph_lists(self.pendulum, self.controller)

            # limiting lengths of lists
            self.visualiser.limit_list_lengths
        
            # graph plotting
            self.visualiser.plot_graph(self.visualiser.t_list, self.visualiser.angle_list, self.visualiser.angular_velocity_list, self.visualiser.cart_position_list, self.visualiser.cart_velocity_list, self.visualiser.u_list) 

            # rolling of graph time axis
            if self.visualiser.t > 5:
                self.visualiser.ax_graph.set_xlim(self.visualiser.t - 5, self.visualiser.t + 5)                

        return self.visualiser.theta, self.visualiser.theta_dot, self.visualiser.x_cart, self.visualiser.x_dot, self.visualiser.u_plot
    