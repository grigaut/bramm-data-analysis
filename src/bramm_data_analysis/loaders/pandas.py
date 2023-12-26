"""Pandas DataFrame Loader."""

from pandas.core.api import DataFrame

from bramm_data_analysis.loaders._base import BaseLoader


class PandasDFLoader(BaseLoader[DataFrame]):

    """Loader for pandas' dataframes data sources."""

    def retrieve_df(self) -> DataFrame:
        """Retrieve the Original DataFrame."""
        return self.source
