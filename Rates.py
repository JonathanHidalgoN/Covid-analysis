import Population 
from itertools import product
import typing

class Rates:

    """
    This class computes the rates of the SIR model.
    Attributes:
        population (Population): The population of the simulation.
    """

    def __init__(self, population: Population):
        self._population = population

    def compute_effective_infection_rate(self, days_to_consider: int = 151) -> typing.List[float]:
        pass
