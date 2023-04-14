from Rates import EffectiveInfectionRate, TransmitionRateS
from Data import DataFormater, Population

DATA_PATH = "Data/GtoDatOK150322 - GtoDatOK291020.csv"

# Steps -----------------------------------------------------------------------
# 1. Load the data using the DataFormater class 
# 2. Instantiate the population class with the data
# 3. Instantiate the rates classes with the data
# 4. Compute the rates (Work in progress)
# 5. Make predictions(?)
# I dont know if plotting functions should be in the rates classes or in a
# different class
# 6. Plot the rates and the predictions (Maybe this should be in a different class, so the rates classes are independent of the plotting library)
# 7. Save info to a file
# -----------------------------------------------------------------------------