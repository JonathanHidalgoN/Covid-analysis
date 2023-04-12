from numpy import array as np_array
from numpy import int32 as np_int32


class Population:

    """
    This class represents the population of the simulation.
    Attributes:
        population (int): The population of the simulation.
        infected_people (np_array(np_int32)): The number of infected people in the simulation.
        dead_people (np_array(np_int32)): The number of dead people in the simulation.
        recovered_people (np_array(np_int32)): The number of recovered people in the simulation.
        vaccinated_people (np_array(np_int32)): The number of vaccinated people in the simulation.
        data_points (int): The number of data points in the simulation.
    """

    def __init__(
        self,
        population: int,
        infected_people: np_array(np_int32),
        dead_people: np_array(np_int32),
        recovered_people: np_array(np_int32),
        vaccinated_people: np_array(np_int32),
    ):
        self._population = population
        self._infected_people = infected_people
        self._dead_people = dead_people
        self._recovered_people = recovered_people
        self._vaccinated_people = vaccinated_people
        self._check_length()
        self._data_points = len(infected_people)
        self._inmune_people = self._compute_inmune_people()
        self._active_infected_people = self._compute_active_infected_people() 

    def _compute_inmune_people(self) -> np_array(np_int32):
        """
        This method computes the number of inmune people.
        Returns:
            np_array(np_int32): The number of inmune people.
        """
        #Dont know if this is correct
        #return self._vaccinated_people + self._recovered_people + self._dead_people
        return self._recovered_people + self._dead_people

    def _compute_active_infected_people(self) -> np_array(np_int32):
        """
        This method computes the number of active infected people.
        Returns:
            np_array(np_int32): The number of active infected people.
        """
        return self._infected_people - self._inmune_people

    @property
    def data_points(self) -> int:
        return self._data_points

    @property
    def population(self) -> int:
        return self._population

    @property
    def infected_people(self) -> np_array(np_int32):
        return self._infected_people

    @property
    def dead_people(self) -> np_array(np_int32):
        return self._dead_people

    @property
    def recovered_people(self) -> np_array(np_int32):
        return self._recovered_people

    @property
    def vaccinated_people(self) -> np_array(np_int32):
        return self._vaccinated_people

    def _check_length(self) -> None:
        """
        This method checks if the length of the infected, dead, recovered and vaccinated people are equal.
        """
        # len(np_array) is not that fast, maybe change it.
        len_infected = len(self._infected_people)
        len_dead = len(self._dead_people)
        len_recovered = len(self._recovered_people)
        len_vaccinated = len(self._vaccinated_people)
        assert len_infected == len_dead == len_recovered == len_vaccinated

    @population.setter
    def population(self, population: int) -> None:
        assert population > 0
        self._population = population

    @infected_people.setter
    def infected_people(self, infected_people: np_array(np_int32)) -> None:
        self._infected_people = infected_people
        self._check_length()

    @dead_people.setter
    def dead_people(self, dead_people: np_array(np_int32)) -> None:
        self._dead_people = dead_people
        self._check_length()

    @recovered_people.setter
    def recovered_people(self, recovered_people: np_array(np_int32)) -> None:
        self._recovered_people = recovered_people
        self._check_length()


if __name__ == "__main__":
    population = Population(
        population=12,
        infected_people=np_array([1, 2, 3], dtype=np_int32),
        dead_people=np_array([1, 2, 3], dtype=np_int32),
        recovered_people=np_array([1, 2, 3], dtype=np_int32),
        vaccinated_people=np_array([1, 2, 3], dtype=np_int32),
    )
    population.infected_people = np_array([1, 2, 4], dtype=np_int32)
    try:
        population.infected_people = np_array([1, 2, 4, 5], dtype=np_int32)
    except AssertionError:
        print("AssertionError")
    try:
        population.population = -1
    except AssertionError:
        print("AssertionError")
    print("Done")
