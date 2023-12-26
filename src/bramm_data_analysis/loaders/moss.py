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
        return MossPreprocessor().preprocess(
            unprocessed_data=moss_df,
            inplace=False,
        )
