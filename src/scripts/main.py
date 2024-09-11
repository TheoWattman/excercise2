import csv
import datetime
import os

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import numpy as np
import tikzplotlib


# Expression used in the excerise
def h(t):
    return 3 * np.pi * np.exp(-5 * np.sin( 2 * np.pi* t ))

class Plot:
    def __init__(self, x_label, y_label, expression, res):

        self.experiment_name = "Experiment"
        self.expression = expression
        self.res = res
        self.x = []
        self.y = []

        # flags
        self.is_open = True
        self.is_paused = False

        # init the plot and figure
        self.fig = plt.figure()
        self.ax = plt.subplot()
        self.line, = self.ax.plot([],[])

        self.ax.set_xlabel(xlabel=x_label)
        self.ax.set_ylabel(ylabel=y_label)
        self.x_label = x_label
        self.y_label = y_label

        plt.grid()

        # ---- Events ----
        self.cid = self.fig.canvas.mpl_connect('close_event', self.on_close)

    # plots a point on the graph
    def plot_point(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.line.set_data(self.x, self.y)

    #updates the view and makes sure that limits are autoscaled
    def update(self):
        self.ax.relim()
        self.ax.autoscale_view()
        plt.draw()
        plt.pause(0.001)

    # Handles user closing the program
    def on_close(self, event):
        plt.close(self.fig)
        self.is_open = False

    # Turns auto limits on
    def reset_limits(self):
        self.ax.set_xlim(auto=True)
        self.ax.set_ylim(auto=True)


# A static plot that gets generated from a range, xmin to xmax. Cant be expanded later

class staticPlot(Plot):
    def __init__(self, x_min, x_max, x_label, y_label, expression, res):
        super().__init__(x_label, y_label, expression, res)
        self.x_min = x_min
        self.x_max = x_max

    def plot(self):
        for x in np.arange(self.x_min, self.x_max, self.res):
            self.plot_point(x, self.expression(x))
        self.update()
    
    def run(self):
        self.plot()
        while self.is_open:
            plt.pause(0.01)

# A dynamic plot that updates live as new data gets collected

class dynamicPlot(Plot):
    def __init__(self, x_label, y_label, expression, res):
        super().__init__(x_label, y_label, expression, res)
        self.init_gui()

    def init_gui(self):
        # Pause button
        self.ax_button_pause = plt.axes([0.01, 0.01, 0.1, 0.05])  # Custom position for the button
        self.button_pause = Button(self.ax_button_pause, 'Pause')
        self.button_pause.on_clicked(self.toggle_pause)
        # Reset Button
        self.ax_button_reset = plt.axes([0.12, 0.01, 0.1, 0.05])  # Custom position for the button
        self.button_reset = Button(self.ax_button_reset, 'Reset')
        self.button_reset.on_clicked(self.reset)
        # Experiment name text Box
        self.ax_text_box = plt.axes([0.68, 0.01, 0.2, 0.05])
        self.text_box = TextBox(self.ax_text_box, 'Exp Name:', initial="Experiment")
        self.text_box.on_submit(self.update_experiment_name)
        # Save Button
        self.ax_button_save = plt.axes([0.89, 0.01, 0.1, 0.05])  # Custom position for the button
        self.button_save = Button(self.ax_button_save, 'Save')
        self.button_save.on_clicked(self.save_data_csv)
        # Tikz Button
        self.ax_button_tikz = plt.axes([0.23, 0.01, 0.1, 0.05])  # Custom position for the button
        self.button_tikz = Button(self.ax_button_tikz, 'Tikz')
        self.button_tikz.on_clicked(self.save_data_tikz)


    def save_data_tikz(self, event):

        # Due to issues with how tikzplotlib handles buttons we are forced to copy over the plot onto a
        # new plot and save that

        # Create a new figure and axes
        fig, ax = plt.subplots()

        # Copy plot data
        ax.plot(self.x, self.y)

        # Set labels and grid
        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        ax.grid(True)

        # Get file name
        current_date = datetime.datetime.now()
        file_name = f"plot_{current_date.strftime('%Y-%m-%d_%H-%M-%S')}"

        directory = "../output"

        file_path = os.path.join(directory, file_name)

        print(f"Saving TikZ file as: {file_name}")  # Debug line
        
        # Save to TikZ
        tikzplotlib.save(file_path)

        # Close the new plot
        plt.close(fig)

    # Update experiment name before saving to CSV
    def update_experiment_name(self, event):
        self.experiment_name = self.text_box.text

    def save_data_csv(self, event):
        current_date = datetime.datetime.now()
        file_name = f"{self.experiment_name}_{current_date.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

        directory = "../output"

        file_path = os.path.join(directory, file_name)

        with open(file_path, mode="w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["x", "y"])
            for i in range(0,len(self.x)):
                csv_writer.writerow([self.x[i], self.y[i]])

        print(f"Data saved to file -> {file_name}")

    # Pauses the program and resumes it
    def toggle_pause(self, event):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.button_pause.label.set_text('Resume')
        else:
            self.button_pause.label.set_text('Pause')
            self.reset_limits()
        
    # resets the data collected and starts over

    def reset(self, event):
        # Clear plot
        self.x = []
        self.y = []
        self.line.set_data([], [])

        self.reset_limits()

        # Redraw the plot to show the cleared state
        plt.draw()

    # the main loop for updating the plot
    def run(self):
        t = 0.0
        while self.is_open:
            if not self.is_paused:    
                self.plot_point(t, self.expression(t))
                self.update()
                t += self.res
            else:
                plt.pause(0.001)
    


myPlot = dynamicPlot(x_label="t", y_label="h(t)", expression=h, res=0.01)
myPlot.run()