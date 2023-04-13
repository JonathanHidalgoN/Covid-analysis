import abc
import matplotlib.pyplot as plt
from typing import Callable
import numpy as np

class Rate(abc.ABC):

    """
    This class represents a rate, it is an abstract class.
    Attributes:
        xaxis (np.array): The x axis of the rate.
        yaxis (np.array): The y axis of the rate.
    """

    def __init__(self):
        self._xaxis, self._yaxis = self._compute_axis()
        self._check_length()
        self.data_points = len(self._xaxis)

    def _check_length(self):
        """
        This method checks if the x and y axis have the same length.
        """
        if len(self._xaxis) != len(self._yaxis):
            raise ValueError("The x and y axis must have the same length.")

    @abc.abstractmethod
    def compute_rate_with_error(self):
        """
        This method computes the rate with error.
        Returns:
            rate (float): The rate.
            error (float): The error of the rate.
        """
        pass

    @abc.abstractmethod
    def _compute_axis(self):
        """
        This method computes the axis of the rate.
        Returns:
            x_axis (np.array): The x axis of the rate.
            y_axis (np.array): The y axis of the rate.
        """
        pass

    def plot_rate(self, function : Callable[[float]], tags : list[str] = None) -> None:
        """
        This method plots the rate.
        Args:
            function (Callable[[float]]): The function to plot.
            tags (list[str]): The tags for the plot [title,x_axis_name, y_axis_name].
        """
        x_cont = np.linspace(self._xaxis.min(), self._xaxis.max(), endpoint=True)
        y_function = function(x_cont)

        fig , ax = plt.subplots()

        plt.scatter(self._xaxis, self._yaxis, label="Data", c = "red", marker = ".")
        plt.plot(x_cont, y_function, label="Fit", c = "black")

        if tags is not None:
            plt.title(tags[0])
            plt.xlabel(tags[1])
            plt.ylabel(tags[2])
            plt.legend()

        plt.show()
    
    def _compute_confidence_interval(self, ):
        pass