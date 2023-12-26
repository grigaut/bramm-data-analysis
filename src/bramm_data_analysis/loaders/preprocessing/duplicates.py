"""Handle Duplicates in Data."""

from collections.abc import Callable
from typing import ClassVar

import pandas as pd
from pandas.core.api import DataFrame

aggregating_dict_type = dict[str, Callable[[DataFrame], DataFrame]]


class DuplicatesRemoval:

    """Handle Duplicates."""

    date_field = "date"
    longitude_field = "longitude"
    latitude_field = "latitude"

    _remove_method = "remove"

    _aggregating_methods: ClassVar[aggregating_dict_type] = {
        "mean": lambda x: x.mean(),
        "sum": lambda x: x.sum(),
        "median": lambda x: x.median(),
        _remove_method: None,
    }

    def __init__(self, aggregating_method: str = "mean") -> None:
        """Instantiate the object."""
        self._method = aggregating_method

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

    def remove_spatial_overlap(self, dataframe: DataFrame) -> DataFrame:
        """Remove Spatial Overlapping in a DataFrame.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame to modify.

        Returns
        -------
        DataFrame
            DataFrame without Spatial overlapping.
        """
        # copy dataframe
        to_modify = dataframe.copy()
        # Sort by Date
        sorted_df = to_modify.sort_values(self.date_field, ascending=False)
        # Remove
        return sorted_df.drop_duplicates(
            subset=[self.longitude_field, self.latitude_field],
        )

    def aggregate_samples(self, dataframe: DataFrame) -> DataFrame:
        """Aggregate Samples taken in same space-time location.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame to modify.

        Returns
        -------
        DataFrame
            DataFrame same-location points have been aggregated.
        """
        # copy dataframe
        to_modify = dataframe.copy()
        # Group by Date, Longitude and Latitude
        grouped_data = to_modify.groupby(
            by=[self.date_field, self.longitude_field, self.latitude_field]
        )
        aggregate = self._aggregating_methods[self.aggregating_method]
        return aggregate(grouped_data).reset_index()

    def process_duplicates(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """Correct Data according to parameters.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame with potentially duplicated data.

        Returns
        -------
        pd.DataFrame
            Correct DataFrame.
        """
        aggregated = self.aggregate_samples(dataframe=dataframe)
        return self.remove_spatial_overlap(dataframe=aggregated)
