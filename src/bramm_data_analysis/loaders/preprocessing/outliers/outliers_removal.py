"""Tools to Remove Outliers."""

import numpy as np
import pandas as pd

from bramm_data_analysis.loaders.preprocessing.outliers.thresholds import (
    Threshold,
)


class OutlierRemoval:

    """Tool to Remove Outlier from Data."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """Instatiate Object."""
        self._df = dataframe

    @property
    def data(self) -> pd.DataFrame:
        """DataFrame."""
        return self._df

    def apply_thresholds(
        self,
        *thresholds: Threshold,
    ) -> pd.DataFrame:
        """Apply a given list of threshold to the DataFrame.

        Returns
        -------
        pd.DataFrame
            Cropped DataFrame Matching all Thresholds.
        """
        all_checks = np.all(
            [x.check_threshold(self.data) for x in thresholds], axis=0
        )

        return self.data[all_checks]
