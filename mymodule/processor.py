# Copyright 2022 AstroLab Software
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pandas as pd
import numpy as np

from mymodule.utils import apply_selection_cuts
from mymodule.utils import return_fitted_slope
from mymodule.utils import linear_model

def compute_g_slope(
        midpointtais: pd.Series,
        filternames: pd.Series,
        psfluxes: pd.Series,
        min_hist_length=2):
    """ Compute the slope for the g-band data

    Parameters
    ----------
    midpointtais: pd.Series
        Pandas series. Each row (array of floats) contains
        all the times (lightcurve = current measurement + history) for an alert
    filternames: pd.Series
        Pandas series. Each row (array of strings) contains
        all the filter names (lightcurve = current measurement + history) for
        an alert.
    psfluxes: pd.Series
        Pandas series. Each row (array of floats) contains
        all the fluxes (lightcurve = current measurement + history) for an alert
    min_hist_length: int, optional
        Minimum number of measurements in g band in the lightcurve to
        compute the slope. Default (and minimum) is 2.
    """
    # Set defaut values
    slopes = pd.Series([np.nan] * len(midpointtais), dtype=float)

    # Define which alerts will be processed
    mask = apply_selection_cuts(
        filternames, min_hist_length=min_hist_length
    )

    # return default if no alerts survive the cuts
    if len(midpointtais[mask]) == 0:
        return slopes

    # Compute slopes in the g-band
    slopes[mask] = pd.DataFrame([midpointtais[mask], psfluxes[mask]])\
        .apply(lambda x: return_fitted_slope(linear_model, *x))

    return slopes
