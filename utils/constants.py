import pandas as pd
from scipy.stats import gamma

from core.data_handling import get_service_time_df
from utils.types import Scalar



# Standard plot dimensions.
width: Scalar = 400
height: Scalar = 180

# Colors for the plots.
color = '#000000'
scolor = "#003366"
tcolor = "#CF3C3C"
qcolor = "#3fdc93"
noise_color = "rgba(238, 191, 81, 0.4)" 


# Special rho character.
rho_char = chr(961)
