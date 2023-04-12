import csv
from numpy import array as np_array
from numpy import int32 as np_int32
from numpy import delete as np_delete

class DataFormater:

    """
    This class formats the data.
    Attributes:
        data_path (str): The path to the data.
    """
    
    def __init__(self, data_path : str, info : dict = None) -> None:
        self._data_path = data_path

    def read_col(self, col : int, num : bool, items_to_delete : int = 0) -> np_array:
        """
        This method reads a column from a csv file.
        Args:
            col (int): The column to read.
            num (bool): If the column is numeric.
            items_to_delete (int): The number of items to delete at the beginig of array.
        Returns:
            array: The column.
        """
        assert col >= 0, "The column must be positive."
        with open(self._data_path, 'r') as f:
            reader = csv.reader(f)
            col = np_array([
                    row[col] for row in reader
                    ])
        if num:
            col = self._delete_str(col)
        return col[items_to_delete:]
        
    @staticmethod
    def _delete_str(array : np_array) -> np_array:
        """
        This method deletes the string in the array.
        Args:
            array (array): The array to delete the string.
        Returns:
            array: The array without the string.
        """
        copy = array.copy()
        idx = 0
        while  idx < len(copy):  
            try:
                copy[idx] = np_int32(copy[idx])
            except ValueError:
                copy = np_delete(copy, idx)
            idx += 1
        return copy

if __name__ == "__main__":
    path = "GtoDatOK150322 - GtoDatOK291020.csv"
    dataformat = DataFormater(path)
    no = dataformat.read_col(0, False, 2)
    date = dataformat.read_col(1, False, 2)
    active_infected = dataformat.read_col(3, True, 1)
    dead = dataformat.read_col(4, True, 1)
    recovered = dataformat.read_col(5, True, 1)
    vaccinated = dataformat.read_col(6, True, 1)
    #Missing data on vaccinated people (1)
    assert len(no) == len(date) == len(active_infected) == len(dead) == len(recovered) == len(vaccinated)