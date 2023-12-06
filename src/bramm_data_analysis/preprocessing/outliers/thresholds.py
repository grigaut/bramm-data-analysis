"""Thresholds."""

from abc import ABC, abstractmethod

import pandas as pd


class Threshold(ABC):

    """Threshold."""

    def __init__(self, *, field: str, lower: float, upper: float) -> None:
        """Instantiate a Threshold.

        Parameters
        ----------
        field : str
            Field on which to apply the threshold.
        lower : float
            Condition on lower value.
        upper : float
            Condition on upper value.
        """
        self._field = field
        self._lower = lower
        self._upper = upper

    @property
    def field(self) -> str:
        """Field Name."""
        return self._field

    @property
    def lower(self) -> float:
        """Lower Bound of the Threshold."""
        return self._lower

    @property
    def upper(self) -> float:
        """Upper Bound of the Threshold."""
        return self._upper

    @abstractmethod
    def check_threshold(self, dataframe: pd.DataFrame) -> pd.Series:
        """Verify the Threshold for a given DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame to check.

        Returns
        -------
        pd.Series
            Boolean Series : True if the value matches both Thresholds.
        """


class ValueThreshold(Threshold):

    """Value Threshold."""

    def check_threshold(self, dataframe: pd.DataFrame) -> pd.Series:
        """Verify the Threshold for a given DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame to check.

        Returns
        -------
        pd.Series
            Boolean Series : True if the value matches both Thresholds.
        """
        field_values = dataframe[self.field].astype(float)
        match_lower_bound = field_values >= self.lower
        match_upper_bound = field_values <= self.upper

        return match_lower_bound & match_upper_bound


class QuantileThreshold(Threshold):

    """Quantile Threshold."""

    def check_threshold(self, dataframe: pd.DataFrame) -> pd.Series:
        """Verify the Threshold for a given DataFrame.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame to check.

        Returns
        -------
        pd.Series
            Boolean Series : True if the value matches both Thresholds.
        """
        field_values = dataframe[self.field].astype(float)

        lower_bound = field_values.quantile(self.lower)
        upper_bound = field_values.quantile(self.upper)

        match_lower_bound = field_values >= lower_bound
        match_upper_bound = field_values <= upper_bound

        return match_lower_bound & match_upper_bound
