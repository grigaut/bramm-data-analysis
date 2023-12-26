"""Excel Reading Tools."""

from pathlib import Path

import pandas as pd
from pandas import DataFrame


class ExcelReader:

    """Loads Data from an Excel File."""

    def __init__(
        self,
        column_name_mapping: dict[str, str] | None = None,
        sheet_name: str | int = 0,
        skiprows: int | list[int] | None = None,
    ) -> None:
        """Reader Initialisation.

        Parameters
        ----------
        column_name_mapping : dict[str, str], optional
            Dictionnary to use to rename columns., by default {}
        sheet_name : str | int, optional
            Name or position of the sheet to load., by default 0
        skiprows: int | list[int] | None, optional
            Rows to skip whend loading., by default None
        """
        if column_name_mapping is None:
            column_name_mapping = {}
        self._column_mapping = column_name_mapping
        self._sheet_name = sheet_name
        self._skiprows = skiprows

    @property
    def columns_mapping(self) -> dict[str, str]:
        """Columns names mapping."""
        return self._column_mapping

    @columns_mapping.setter
    def columns_mapping(self, column_name_mapping: dict[str, str]) -> None:
        self._column_mapping = column_name_mapping

    @property
    def sheet_name(self) -> str | int:
        """Name (or number) of the sheet to load."""
        return self._sheet_name

    @sheet_name.setter
    def sheet_name(self, sheet_name: str | int) -> None:
        self._sheet_name = sheet_name

    @property
    def skiprows(self) -> int | list[int]:
        """Rows to skip."""
        return self._skiprows

    @skiprows.setter
    def skiprows(self, skiprows: int | list[int]) -> None:
        self._skiprows = skiprows

    def load(self, data_path: Path | str) -> DataFrame:
        """Load the dataframe from the excel file.

        Parameters
        ----------
        data_path : Path | str
            Path to the excel file.

        Returns
        -------
        DataFrame
            Dataframe with correct names.
        """
        raw_dataframe = pd.read_excel(
            io=data_path,
            sheet_name=self.sheet_name,
            skiprows=self.skiprows,
        )
        return raw_dataframe.rename(columns=self.columns_mapping)
