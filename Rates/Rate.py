import abc


class Rate(abc.ABC):

    """
    This class represents a rate, it is an abstract class.
    Attributes:
        xaxis (np.array): The x axis of the rate.
        yaxis (np.array): The y axis of the rate.
    """

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

    @abc.abstractmethod
    def plot_rate(self):
        """
        This method plots the rate.
        """
        pass
