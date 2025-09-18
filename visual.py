import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class Visual:

    """
    Visualiser for pendulum on cart.


    Attributes:
    ----------- 
    fig:
        Matplotlib figure for pendulum animation
    ax:
        Matplotlib axes for pendulum animation
    pendulum:
        Instance of Physics class
    graph_fig:
        Matplotlib figure for graph of angle, angular velocity, cart position, cart velocity and control input
        of pendulum on cart
    ax_graph:
        Matplotlib axes for pendulum angle and angular velocity in graph of pendulum
    ax_graph2:
        Matplotlib axes for cart position, cart velocity and control input in graph of pendulum
    theta, theta_dot, x_cart, x_dot, u_plot:
        Matplotlib plots for angle, angular velocity, cart position, cart velocity and control input
    angle_label:
        Real time label showing angle of pendulum on pendulum animation figure
    x0, y0:
        Initial coordinates of pendulum 
    line, circle, leftwheel, rightwheel, cart, floor
        Pendulum rod, top of pendulum, wheels, cart and green floor as shapes drawn in matplotlib
    t:
        Time count incremented by dt each animation cycle externally
    t_list, angle_list, angular_velocity_list, cart_position_list, cart_velocity_list, u_list:
        Lists of time, angle, angular velocity, cart position, cart velocity, control input incremented each
        animation cycle used to plot the graph
    frames:
        Variable used for frame count generator
    paused:
        Boolean used for pausing animation
    

    Methods:
    --------
    frame_count(self):
        Generator function used for increasing frames in real time
    pause(self, press):
        Used to toggle pause boolean, tied to a button
    update_pendulum(self, pend):
        Used to update pendulum and cart positions repeatedly in Animations class
    update_graph_lists(self, pend, ctrl):
        Used to increment time and update lists for graph plot repeatedly in Animations class
    limit_list_lengths(self):
        Used to limit the lengths of growing lists not to cause performance issues in Animations class
    plot_graph(self, t_list, angle_list, angular_velocity_list, cart_position_list, cart_velocity_list, u_list):
        Used to repeatedly update the plots in the graph in the Animations class
        
    """

    def __init__(self, pendulum):

        # creating figure & axes for pendulum animation
        self.fig = plt.figure()
        self.fig.canvas.draw()
        self.ax = self.fig.add_subplot()
        self.ax.set_xlim(-50, 50)
        self.ax.set_ylim(-20, 50)
        self.ax.grid()
        self.ax.set_yticklabels([]) # sets y axis labels to nothing

        # for use in other member functions
        self.pendulum = pendulum

        # creating figure and axes for graph
        self.graph_fig = plt.figure()
        self.ax_graph = self.graph_fig.add_subplot()
        self.ax_graph.set_xlim(0, 10)
        self.ax_graph.set_ylim(-360, 360)
        self.ax_graph2 = self.ax_graph.twinx()
        self.ax_graph2.set_ylim(-150, 150)

        # plots for graph
        self.theta, = self.ax_graph.plot([0], [self.pendulum.init_angle], 'k', lw = 1, label=r'$\theta$')
        self.theta_dot, = self.ax_graph.plot([0], [0], 'r', lw = 1, label=r'$\dot \theta$')
        self.x_cart, = self.ax_graph2.plot([0], [0], 'b', lw = 1, label=r'$x$')
        self.x_dot, = self.ax_graph2.plot([0], [0], 'g', lw = 1, label=r'$\dot{x}$')
        self.u_plot, = self.ax_graph2.plot([0], [0], 'm', lw = 1, label=r'$u$')

        self.ax_graph.set_title('Pendulum Plots')
        self.ax_graph.set_xlabel('Time 1 s/div)')
        self.ax_graph.set_ylabel(r'$\theta$ (deg), $\dot \theta$ (deg/s)')
        self.ax_graph2.set_ylabel(r'$x$, $\dot{x}$, $\ddot{x}$')
        self.ax_graph.set_xticklabels([])

        self.ax_graph.grid()
        self.ax_graph2.grid()
        self.ax_graph.xaxis.set_major_locator(ticker.MultipleLocator(1)) # 1 s/div

        # legend for graph
        self.graph1_lines, self.graph1_labels = self.ax_graph.get_legend_handles_labels()
        self.graph2_lines, self.graph2_labels = self.ax_graph2.get_legend_handles_labels()
        self.ax_graph.legend(self.graph1_lines + self.graph2_lines, self.graph1_labels + self.graph2_labels, loc='upper right')

        self.angle_label = self.ax.text(0.5, 0.85, '', transform=self.ax.transAxes, fontsize=15, color='b')

        # creating objects in pendulum animation
        self.x0, self.y0 = self.pendulum.pendulum_pos(self.pendulum.init_angle)
        self.line, = self.ax.plot([0, self.x0], [0, self.y0], lw=2, c='k')
        self.circle = self.ax.add_patch(plt.Circle(self.pendulum.pendulum_pos(self.pendulum.init_angle), 1.2, fc='r', zorder=3))
        self.leftwheel = self.ax.add_patch(plt.Circle((-2.5, -1.5), 0.7, fc='k', facecolor = 'k', zorder=3))
        self.rightwheel = self.ax.add_patch(plt.Circle((2.5, -1.5), 0.7, fc='k', facecolor = 'k', zorder=3))
        self.cart = self.ax.add_patch(plt.Rectangle((-4, -1.5), 8, 2.5, linewidth=1, edgecolor='k', facecolor='none'))
        self.floor = self.ax.add_patch(plt.Rectangle((-50, -20), 100, 17.8, linewidth=3, edgecolor='g', facecolor='g', zorder=3))

        self.fig.canvas.manager.set_window_title('Pendulum')
        self.graph_fig.canvas.manager.set_window_title('Graph')

        self.t = 0

        # lists for graph plot
        self.t_list = [0]
        self.angle_list = [np.rad2deg(self.pendulum.init_angle)]
        self.angular_velocity_list = [0]
        self.cart_position_list = [0]
        self.cart_velocity_list = [0]
        self.u_list = [0]

        self.frames = self.frame_count()
        self.paused = False

    def frame_count(self):
        i = 0
        while True:
            yield i # pauses the function and returnes i without ending the function
            i += 1

    # pause toggle
    def pause(self, press):
        self.paused = not self.paused

    def update_pendulum(self, pend):
        # updating of pendulum positions in animation
        self.x, self.y = pend.pendulum_pos(pend.angle)
        self.line.set_data([pend.x, self.x], [0, self.y])
        self.circle.set_center((self.x, self.y))
        self.cart.set_xy((pend.x - 4, -1.5))
        self.leftwheel.set_center((pend.x - 2.5, -1.5))
        self.rightwheel.set_center((pend.x + 2.5, -1.5))
        self.angle_label.set_text(str(int(np.rad2deg(pend.angle))) + "°")

    def update_graph_lists(self, pend, ctrl):
        # incrementing t and appending to graph plot lists 
        self.t += pend.dt
        self.t_list.append(self.t)
        self.angle_list.append(np.rad2deg(pend.angle))
        self.angular_velocity_list.append(np.rad2deg(pend.angular_velocity))
        self.cart_position_list.append(pend.x)
        self.cart_velocity_list.append(pend.xdot)
        self.u_list.append(ctrl.u)

    def limit_list_lengths(self):
        if len(self.t_list) > 170:
            self.t_list.pop(0)
            self.angle_list.pop(0)
            self.angular_velocity_list.pop(0)
            self.cart_position_list.pop(0)
            self.cart_velocity_list.pop(0)
            self.u_list.pop(0)

    def plot_graph(self, t_list, angle_list, angular_velocity_list, cart_position_list, cart_velocity_list, u_list):
        self.theta.set_data(t_list, angle_list)
        self.theta_dot.set_data(t_list, angular_velocity_list)
        self.x_cart.set_data(t_list, cart_position_list)
        self.x_dot.set_data(t_list, cart_velocity_list)
        self.u_plot.set_data(t_list, u_list)