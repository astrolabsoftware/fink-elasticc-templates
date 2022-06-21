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

from scipy.optimize import curve_fit

def apply_selection_cuts(filternames: pd.Series, min_hist_length: int) -> pd.Series:
    """ Apply selection cuts defined by the user. In this case, flag out
    alerts with not enough points in the g band.

    Alerts that do not satisfy the criteria are not processed.

    Parameters
    ----------
    filternames: pd.Series
        Series containing filter values (array of str). Each row contains
        all filter values for one alert (with its history).
    min_hist_length: int
        Minimum number of measurements in g

    Returns
    ---------
    mask: pd.Series
        Series containing `True` if the alert is valid, `False` otherwise.
        Each row contains one boolean.
    """
    # Keep only g-band
    hist_g_duration = filternames.apply(lambda x: np.sum(x == 'g'))

    mask = (hist_g_duration >= min_hist_length)

    return mask


def linear_model(x: float, a: float, b: float) -> float:
    """ Linear model of the form f(x) = ax + b
    """
    return a * x + b

def return_fitted_slope(func, midpointtais: list, psfluxes: list) -> float:
    """ Wrapper for `curve_fit`

    Parameters
    ----------
    func: function
        Function to fit
    midpointtais: list of floats
        List containing time steps for one alert
    psfluxes: list of floats
        List containing fluxes for one alert
    """
    try:
        fit, cov = curve_fit(func, midpointtais, psfluxes, p0=[0.0, 0.0])
    except RuntimeError:
        return np.nan

    return fit[0]

def extract_history(history_list: list, field: str) -> list:
    """Extract the historical measurements contained in the alerts
    for the parameter `field`.

    Parameters
    ----------
    history_list: list of dict
        List of dictionary from alert['prvDiaSources'].
    field: str
        The field name for which you want to extract the data. It must be
        a key of elements of history_list (alert['prvDiaSources'])

    Returns
    ----------
    measurement: list
        List of all the `field` measurements contained in the alerts.
    """
    try:
        measurement = [obs[field] for obs in history_list]
    except KeyError:
        print('{} not in history data'.format(field))
        measurement = [None] * len(history_list)

    return measurement

def extract_field(alert: dict, field: str) -> np.array:
    """ Concatenate current and historical observation data for a given field.

    Parameters
    ----------
    alert: dict
        Dictionnary containing alert data
    field: str
        Name of the field to extract.

    Returns
    ----------
    data: np.array
        List containing previous measurements and current measurement at the
        end. If `field` is not in `prvDiaSources` fields, data will be
        [None, None, ..., alert['diaSource'][field]].
    """
    data = np.concatenate(
        [
            extract_history(alert['prvDiaSources'], field),
            [alert["diaSource"][field]]
        ]
    )
    return data
