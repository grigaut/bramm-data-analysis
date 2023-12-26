"""RMQS Data Loader."""

from pathlib import Path

from pandas.core.api import DataFrame

from bramm_data_analysis.loaders._base import BaseLoader
from bramm_data_analysis.loaders.preprocessing.rmqs import RMQSPreprocessor
from bramm_data_analysis.loaders.reading.rmqs import RMQSReader


class RMQSLoader(BaseLoader[Path]):

    """Loader for RMQS' data."""

    def retrieve_df(self) -> DataFrame:
        """Retrieve RMQS' Dataframe."""
        rmqs_df = RMQSReader(data_path=self.source).retrieve()
        return RMQSPreprocessor().preprocess(
            unprocessed_data=rmqs_df,
            inplace=False,
        )
