"""Moss-files reading toools."""


import pandas as pd
from pandas.core.api import DataFrame

from bramm_data_analysis.loaders.reading._base import BaseReader


class RMQSReader(BaseReader):

    """RMQS File Readers."""

    def retrieve(self) -> DataFrame:
        """Retrieve Data from file.

        Returns
        -------
        DataFrame
            RMQS DataFrame.
        """
        return pd.read_csv(self.data_path)
