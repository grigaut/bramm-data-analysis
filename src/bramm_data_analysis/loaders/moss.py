"""Moss Data Loader."""

from pathlib import Path

from pandas.core.api import DataFrame

from bramm_data_analysis.loaders._base import BaseLoader
from bramm_data_analysis.loaders.preprocessing.moss import MossPreprocessor
from bramm_data_analysis.loaders.reading.moss import MossReader


class MossLoader(BaseLoader[Path]):

    """Loader for Moss' data."""

    def retrieve_df(self) -> DataFrame:
        """Retrieve Moss' DataFrame."""
        moss_df = MossReader(data_path=self.source).retrieve()
        self.raise_if_essential_columns_missing(moss_df)
        return MossPreprocessor().preprocess(
            unprocessed_data=moss_df,
            inplace=False,
        )

    def retrieve_filtered_df(self, fields: list[str]) -> DataFrame:
        """Retrieve Filtered DataFrame.

        Parameters
        ----------
        fields : list[str]
            List of fields to conserve. If empty, return the same DataFrame.

        Returns
        -------
        DataFrame
            Filtered DataFrame
        """
        moss_df = MossReader(data_path=self.source).retrieve_and_filter(fields)
        self.raise_if_essential_columns_missing(moss_df)
        return MossPreprocessor().preprocess(
            unprocessed_data=moss_df,
            inplace=False,
        )
