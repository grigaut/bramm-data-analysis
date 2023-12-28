"""Reading Objects."""

from abc import ABC, abstractmethod
from pathlib import Path

from pandas.core.api import DataFrame, Index


class BaseReader(ABC):

    """Base Class for Readers."""

    def __init__(self, data_path: Path | None) -> None:
        """Instantiate the Reader.

        Parameters
        ----------
        data_path : Path | None
            Path to the file containing data.
        """
        self._path = data_path

    @property
    def data_path(self) -> Path | None:
        """Data Path."""
        return self._path

    def raise_if_inexistent_column(
        self, df_columns: Index, fields: list[str]
    ) -> None:
        """Raise Error if some columns do not exist in the DataFrame.

        Parameters
        ----------
        df_columns : Index
            Index of the DataFrame's columns.
        fields : list[str]
            Fields to check in the columns

        Raises
        ------
        KeyError
            If a field is not in the columns.
        """
        if not all(col in df_columns for col in fields):
            msg = (
                f"{fields} are not all columns of the DataFrame."
                f" Existing columns are: {df_columns}."
            )
            raise KeyError(msg)

    def filter_dataframe(
        self,
        dataframe: DataFrame,
        fields: list[str],
    ) -> DataFrame:
        """Filter DataFrame's Columns.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame to filter.
        fields : list[str]
            List of fields to conserve. If empty, return the same DataFrame.

        Returns
        -------
        DataFrame
            Filtered DataFrame.
        """
        if not fields:
            return dataframe
        self.raise_if_inexistent_column(
            df_columns=dataframe.columns,
            fields=fields,
        )
        # Filter Columns
        return dataframe.filter(fields)

    def retrieve_and_filter(self, fields: list[str]) -> DataFrame:
        """Retrieve the DataFrame and Filter its columns.

        Parameters
        ----------
        fields : list[str]
            List of fields to conserve. If empty, return the same DataFrame.

        Returns
        -------
        DataFrame
            Final DataFrame.
        """
        return self.filter_dataframe(self.retrieve(), fields=fields)

    @abstractmethod
    def retrieve(self) -> DataFrame:
        """Retrieve data from the source file."""
