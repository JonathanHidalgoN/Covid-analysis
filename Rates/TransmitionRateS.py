from Rate import Rate
import numpy as np
import typing

class TransmitionRateS(Rate):

    """
    This class represents the transmition rate.
    Attributes:
        infected_people (np.array): The number of infected people.
        days_to_consider (int): The number of days to consider.
        xaxis (np.array): The x axis of the transmition rate.
        yaxis (np.array): The y axis of the transmition rate.
        gamma (float): The gamma parameter.
    """
    def __init__(self,active_infected_people: np.array(np.int32), 
                 gamma,
                 days_to_consider: int = 30,
                ):
        self._active_infected_people = active_infected_people
        self._data_points = len(active_infected_people)
        self._days_to_consider = days_to_consider
        self._xaxis, self._yaxis = self._compute_axis()
        self._gamma = gamma


    @property
    def xaxis(self):
        return self._xaxis
    
    @property
    def yaxis(self):    
        return self._yaxis
    
    @property
    def infected_people(self):
        return self._infected_people
    
    @property
    def days_to_consider(self):
        return self._days_to_consider
    
    def _compute_axis(self) -> typing.Tuple[np.array, np.array]:
        """
        This method computes the x and y axis of the transmition rate.
        Returns:
            x_axis (np.array): The x axis of the transmition rate.
            y_axis (np.array): The y axis of the transmition rate.
        """
        x_axis = np.arange(range(self._data_points - self._days_to_consider - 1, self._data_points))
        y_axis = np.diff(
            self._active_infected_people[self._data_points - self._days_to_consider - 2 :],
        )
        y_axis = np.divide(
            y_axis,
            self._active_infected_people[self._data_points - self._days_to_consider - 1 :] + self._gamma,
        )
        y_axis = np.log(y_axis)
        return self._filter_low_values(x_axis,y_axis)

    @staticmethod
    def _filter_low_values(x,y,tolerance : float = 1e-8):
        """
        This method filters the low values of the transmition rate.
        Args:
            tolerance (float): The tolerance to filter the low values.
        """
        index = np.where(y < tolerance)
        x = np.delete(x,index)
        y = np.delete(y,index)
        return x,y
        
    def compute_rate_with_error(self) -> typing.Tuple[float, float]:
        """
        Computes the transmition rate with the error.
        Returns:
            beta (float): The transmition rate.
            beta_error (float): The error of the transmition rate.
        """
        beta , beta_var = np.polyfit(self._xaxis,self._yaxis,1,cov=True)
        beta_error = np.sqrt(np.diag(beta_var))
        return beta, beta_error
    
    def plot_rate(self):
        pass