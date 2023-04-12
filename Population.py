import typing 

class Population():
    
    """
    A class to represent a population of people.
    Attributes
        pop_size(int): The total population size
        infected_pop(int): The number of infected people in the population
        recovered_pop(int): The number of recovered people in the population
        dead_pop(int): The number of dead people in the population
    """
    
    def __init__(self, pop_size: int,
                    infected_pop: int,
                    recovered_pop: int,
                    dead_pop: int):
        
        assert pop_size == infected_pop + recovered_pop + dead_pop, "Population size must be equal to the sum of infected, recovered and dead populations"
        self._pop_size = pop_size
        self._infected_pop = infected_pop
        self._recovered_pop = recovered_pop
        self._dead_pop = dead_pop

    @property
    def pop_size(self) -> int:
        return self._pop_size
    
    @property
    def infected_pop(self) -> int:
        return self._infected_pop
    
    @property
    def recovered_pop(self) -> int:
        return self._recovered_pop
    
    @property
    def dead_pop(self) -> int:
        return self._dead_pop

