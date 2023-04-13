import abc
import matplotlib.pyplot as plt
from typing import Callable
import numpy as np

class Rate(abc.ABC):

    """
    This class represents a rate.
    Attributes:
        xaxis (np.array): The x axis of the rate.
        yaxis (np.array): The y axis of the rate.
        rate (float): The rate.
        error (float): The error of the rate.
        fit (Callable[[float]]): The fit of the rate.
        confidence_interval (np.array): The confidence interval of the rate.
    """

    def __init__(self):
        self._ready = False

    def _check_setup(self):
        """
        This method checks if the rate is set up.
        """
        if not self._ready:
            #I  dont like to return a string, but raise an exception is not a good idea
            return "The rate is not set up. Please call the method set_up() before using the rate."

    @property
    def xaxis(self) -> np.array:
        """
        This method returns the x axis of the rate.
        Returns:
            np.array: The x axis of the rate.
        """
        self._check_setup()
        return self._xaxis


    @property
    def yaxis(self) -> np.array:
        """
        This method returns the y axis of the rate.
        Returns:
            np.array: The y axis of the rate.
        """
        self._check_setup()
        return self._yaxis

    @property
    def rate(self) -> float:
        """
        This method returns the rate.
        Returns:
            float: The rate.
        """
        self._check_setup()
        return self._rate

    @property
    def error(self) -> float:
        """
        This method returns the error of the rate.
        Returns:
            float: The error of the rate.
        """
        self._check_setup()
        return self._error

    @property
    def fit(self) -> Callable[[float]]:
        """
        This method returns the fit of the rate.
        Returns:
            Callable[[float]]: The fit of the rate.
        """
        self._check_setup()
        return self._fit
    
    @property
    def confidence_interval(self) -> np.array:
        """
        This method returns the confidence interval of the rate.
        Returns:
            float: The confidence interval of the rate.
        """
        self._check_setup()
        return self._confidence_interval

    def set_up(self):
        """
        This method sets up the rate.
        """
        self._xaxis, self._yaxis = self._compute_axis()
        self._check_length()
        self._data_points = len(self._xaxis)
        self._rate, self._error = self._compute_rate_with_error()
        self._fit = self._compute_fit()
        self._confidence_interval = self._compute_confidence_interval()
        self._ready = True

    def _check_length(self):
        """
        This method checks if the x and y axis have the same length.
        """
        if len(self._xaxis) != len(self._yaxis):
            raise ValueError("The x and y axis must have the same length.")

    @abc.abstractmethod
    def _compute_fit(self)-> Callable[[float]]:
        """
        This method returns the fit of the rate.
        Returns:
            Callable[[float]]: The fit of the rate.
        """
        pass
    
    @abc.abstractmethod
    def _compute_rate_with_error(self):
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
    
    def _compute_confidence_interval(self) -> tuple[float, float]:
        """
        This method computes the confidence interval.
        Returns:
            tuple[float, float]: The confidence interval.
        """
        x_cons = np.linspace(self._xaxis.min(), self._xaxis.max(), endpoint=True)
        y_function = function(x_cons)
        pass