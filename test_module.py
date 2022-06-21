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

from mymodule.utils import extract_field
from mymodule.processor import compute_g_slope

if __name__ == "__main__":
    """ Execute the test """

    # Load data
    datapath = 'data/elasticc_test0.parquet'
    pdf = pd.read_parquet(datapath)

    # Extract history
    sub = pdf[['diaSource', 'prvDiaSources']]

    pdf['midpointtais'] = sub.apply(
        lambda x: extract_field(x, 'midPointTai'), axis=1
    )

    pdf['psfluxes'] = sub.apply(
        lambda x: extract_field(x, 'psFlux'), axis=1
    )

    pdf['filternames'] = sub.apply(
        lambda x: extract_field(x, 'filterName'), axis=1
    )

    # Apply the science module
    slope = compute_g_slope(
        pdf['midpointtais'], pdf['filternames'], pdf['psfluxes'], min_hist_length=2
    )

    # Check valid values
    nonzeros = slope[~np.isnan(slope)]
    msg = """
    --> {}
    Number of incoming alerts: {:,}
    Number of alerts enriched: {:,}
    Statistics (slope for g-band in units of flux per day):
    """.format(datapath, len(pdf), len(nonzeros))
    print(msg)
    print(nonzeros.describe())
