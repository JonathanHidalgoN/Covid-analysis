import matplotlib.pyplot as plt

class DataPlotter:

    """
    This class is used to plot the data.
    Attributes:
        x_axis : The x axis of the plot.
        y_axis : The y axis of the plot.
    """

    def __init__(self, x_axis, y_axis):
        self._x_axis = x_axis
        self._y_axis = y_axis

    def plot_with_intervals():
        pass

    def plot_results(self):
        pass

    def plot(self):
        """
        This method plots the data.
        """
        plt.plot(self._x_axis, self._y_axis)
        plt.show()