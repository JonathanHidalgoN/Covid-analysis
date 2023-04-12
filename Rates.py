from Population import Population
from itertools import product
import typing
import numpy as np
#scipy just for curve_fit
from scipy.optimize import curve_fit
import abc

class Rate(abc.ABC):

    @abc.abstractmethod
    def compute_rate_with_error(self):
        pass

    @abc.abstractmethod
    def plot_rate(self):
        pass

class EffectiveInfectionRate(Rate):

    """
    This class represents the effective infection rate.
    Attributes:
    """

    def __init__(self, active_infected_people: np.array, inmune_people: np.array, days_to_consider: int = 150):
        self._inmune_people = inmune_people
        self._active_infected_people = active_infected_people
        self._data_points = len(active_infected_people)
        self._days_to_consider = days_to_consider
        self._xaxis , self._yaxis = self._compute_axis()
    
    def _compute_axis(self) -> typing.Tuple[np.array, np.array]:
        """
        This method computes the axis of the effective infection rate.
        Args:
            days_to_consider (int): The number of days to consider.
        Returns:
            typing.Tuple[np.array, np.array]: The axis of the effective infection rate.
        """
        x_axis = self._active_infected_people[self._data_points - self._days_to_consider - 1 :]
        y_axis = np.diff(
            self._inmune_people[self._data_points - self._days_to_consider - 2 :]
        )
        return x_axis, y_axis

    @staticmethod
    def _proportionality(x, a):
        return a * x 

    def compute_rate_with_error(self) -> typing.Tuple[float, float]:
        """
        This method computes the effective infection rate with its error.
        Returns:
            typing.Tuple[float, float]: The effective infection rate with its error.
        """
        gamma, gamma_var = curve_fit(self._proportionality,
                            self._xaxis,
                            self._yaxis,
        )
        gamma = gamma[0]
        gamma_error = np.sqrt(gamma_var[0][0])
        return gamma, gamma_error
        
    def plot_rate(self, plotter = None):
        print("here is an object to plot")    
                          


if __name__ == "__main__":
    from DataFormater import DataFormater
    path = "GtoDatOK150322 - GtoDatOK291020.csv"
    data_reader = DataFormater(path)
    GTO_POPULATION = 6.167e6
    params = {
        "population": GTO_POPULATION,
        "infected_people": data_reader.read_col(3,True,2),
        "dead_people": data_reader.read_col(4,True,2),
        "recovered_people": data_reader.read_col(5,True,2),
        "vaccinated_people": data_reader.read_col(6,True,2),
    }
    population = Population(**params)
    infecion_rate = EffectiveInfectionRate(population.active_infected_people, population.inmune_people).compute_rate_with_error()
