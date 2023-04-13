from Rates import Rate
import typing
import numpy as np
from scipy.optimize import curve_fit

class EffectiveInfectionRate(Rate):

    """
    This class represents the effective infection rate.
    Attributes:
        active_infected_people (np.array): The number of active infected people.
        inmune_people (np.array): The number of inmune people.
        days_to_consider (int): The number of days to consider.
        xaxis (np.array): The x axis of the effective infection rate.
        yaxis (np.array): The y axis of the effective infection rate.
    """

    def __init__(
        self,
        active_infected_people: np.array,
        inmune_people: np.array,
        days_to_consider: int = 150,
    ):
        self._inmune_people = inmune_people
        self._active_infected_people = active_infected_people
        self._days_to_consider = days_to_consider
        # Call the parent constructor
        super().__init__()

    @property
    def days_to_consider(self):
        return self._days_to_consider

    def _compute_axis(self) -> typing.Tuple[np.array, np.array]:
        """
        This method computes the axis of the effective infection rate.
        Args:
            days_to_consider (int): The number of days to consider.
        Returns:
            typing.Tuple[np.array, np.array]: The axis of the effective infection rate.
        """
        x_axis = self._active_infected_people[
            self._data_points - self._days_to_consider - 1 :
        ]
        y_axis = np.diff(
            self._inmune_people[self._data_points - self._days_to_consider - 2 :]
        )
        return x_axis, y_axis

    @staticmethod
    def _proportionality(x, a):
        return a * x

    def _compute_rate_with_error(self) -> typing.Tuple[float, float]:
        """
        This method computes the effective infection rate with its error.
        Returns:
            typing.Tuple[float, float]: The effective infection rate with its error.
        """
        gamma, gamma_var = curve_fit(
            self._proportionality,
            self._xaxis,
            self._yaxis,
        )
        gamma = gamma[0]
        gamma_error = np.sqrt(gamma_var[0][0])
        return gamma, gamma_error

