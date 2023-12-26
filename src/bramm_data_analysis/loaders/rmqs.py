"""RMQS Data Loader."""

from pathlib import Path

from pandas.core.api import DataFrame

from bramm_data_analysis.loaders._base import BaseLoader
from bramm_data_analysis.loaders.preprocessing.rmqs import RMQSPreprocessor
from bramm_data_analysis.loaders.reading.rmqs import RMQSReader


class RMQSLoader(BaseLoader[Path]):

    """Loader for RMQS' data."""

    def __init__(self, source: Path) -> None:
        """Instantiate the Loader.

        Parameters
        ----------
        source : Path
            Path to the source data file.
        """
        self.date_field = "date_complete"
        super().__init__(source=source)

    def retrieve_df(self) -> DataFrame:
        """Retrieve RMQS' Dataframe."""
        rmqs_df = RMQSReader(data_path=self.source).retrieve()
        self.raise_if_essential_columns_missing(rmqs_df)
        return RMQSPreprocessor().preprocess(
            unprocessed_data=rmqs_df,
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
        rmqs_df = RMQSReader(data_path=self.source).retrieve_and_filter(fields)
        self.raise_if_essential_columns_missing(rmqs_df)
        return RMQSPreprocessor().preprocess(
            unprocessed_data=rmqs_df,
            inplace=False,
        )
