"""RMQS Preprocessing Tools."""


from typing import Literal, overload

import pandas as pd

from bramm_data_analysis.loaders.preprocessing._base import Preprocessor


class RMQSPreprocessor(Preprocessor):

    """Preprocessor for RMQS Data."""

    date_column_to_convert = "date_complete"

    def __init__(self) -> None:
        """Instantiate the Preprocessor."""

    @overload
    def preprocess(
        self,
        unprocessed_data: pd.DataFrame = ...,
        *,
        inplace: Literal[True] = ...,
    ) -> None:
        ...

    @overload
    def preprocess(
        self,
        unprocessed_data: pd.DataFrame = ...,
        *,
        inplace: Literal[False] = ...,
    ) -> pd.DataFrame:
        ...

    def preprocess(
        self, unprocessed_data: pd.DataFrame, *, inplace: bool = False
    ) -> pd.DataFrame | None:
        """Run the preprocessing routines.

        Parameters
        ----------
        unprocessed_data : pd.DataFrame
            DataFrame to process.
        inplace : bool
            Will modify the DataFrame in place if True.

        Returns
        -------
        pd.DataFrame or None
            Processed DataFrame if inplace is False.
        """
        to_modify = unprocessed_data if inplace else unprocessed_data.copy()

        # Correct data

        date_column = to_modify[self.date_column_to_convert]

        to_modify[self.date_column_to_convert] = pd.to_datetime(date_column)

        return None if inplace else to_modify
