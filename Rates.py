import Population 
from itertools import product
import typing
import numpy as np
from scipy.optimize import curve_fit

class Rates:

    """
    This class computes the rates of the SIR model.
    Attributes:
        population (Population): The population of the simulation.
    """

    def __init__(self, population: Population):
        self._population = population
        self._data_points = population.data_points

    def compute_effective_infection_rate(self, days_to_consider: int = 151) -> typing.Tuple[float, float]:
        """
        This method computes the effective infection rate.
        Args:
            days_to_consider (int): The number of days to consider.
        Returns:
            : The effective infection rate and error.
        """
        gamma_x = self._population.active_infected_people[self._population.data_points - days_to_consider:]
        gamma_y = np.diff(
            self._population.inmune_people[self._population.data_points - days_to_consider - 1:]
        )
        gamma, gamma_var = curve_fit(self.proportionality
                                     , gamma_x, gamma_y)
        gamma = gamma[0]
        gamma_error = np.sqrt(gamma_var[0][0])
        return gamma, gamma_error

    @staticmethod
    def proportionality(x,a):
        return a*x
