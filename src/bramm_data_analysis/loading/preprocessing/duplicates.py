"""Handle Duplicates in Data."""

from collections.abc import Callable
from typing import ClassVar

import pandas as pd


class DuplicatesRemoval:

    """Handle Duplicates."""

    _remove_method = "remove"

    _aggregating_methods: ClassVar[dict[str, Callable]] = {
        "mean": lambda x: x.mean(),
        "sum": lambda x: x.sum(),
        "median": lambda x: x.median(),
        _remove_method: None,
    }

    def __init__(
        self, grouping_field: list[str], aggregating_method: str = "mean"
    ) -> None:
        """Instantiate the object."""
        self._fields = grouping_field
        self._method = aggregating_method

    @property
    def grouping_field(self) -> list[str]:
        """Fields by which to group the data."""
        return self._fields

    @grouping_field.setter
    def grouping_field(self, value: list[str]) -> None:
        self._fields = value

    @property
    def aggregating_method(self) -> str:
        """Aggregating Method."""
        return self._method

    @aggregating_method.setter
    def aggregating_method(self, value: str) -> None:
        if value not in self._aggregating_methods:
            msg = (
                "Unrecognized Aggregating Method. "
                f"Accepted methods are {self._aggregating_methods.keys()}"
            )
            raise KeyError(msg)

    def correct_data(
        self,
        duplicated_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Correct Data according to parameters.

        Parameters
        ----------
        duplicated_data : pd.DataFrame
            DataFrame with potentially duplicated data.

        Returns
        -------
        pd.DataFrame
            Correct DataFrame.
        """
        to_modify = duplicated_data.copy()

        if self.aggregating_method == self._remove_method:
            return to_modify.drop_duplicates(subset=self.grouping_field)

        grouped_data = to_modify.groupby(by=self.grouping_field)

        aggregate = self._aggregating_methods[self.aggregating_method]

        return aggregate(grouped_data).reset_index()
