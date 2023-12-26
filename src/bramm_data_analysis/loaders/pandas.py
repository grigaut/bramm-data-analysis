"""Pandas DataFrame Loader."""

from pandas.core.api import DataFrame

from bramm_data_analysis.loaders._base import BaseLoader


class PandasDFLoader(BaseLoader[DataFrame]):

    """Loader for pandas' dataframes data sources."""

    def retrieve_df(self) -> DataFrame:
        """Retrieve the Original DataFrame."""
        self.raise_if_essential_columns_missing(self.source)
        return self.source

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
        filtered_df = self.source.filter(fields)
        self.raise_if_essential_columns_missing(filtered_df)
        return filtered_df
