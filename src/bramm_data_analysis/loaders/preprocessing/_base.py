"""BAse Tools for preprocessing."""

from abc import ABC, abstractmethod
from typing import Literal, overload

import pandas as pd


class Preprocessor(ABC):

    """Preprocessing base class."""

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

    @abstractmethod
    def preprocess(
        self,
        unprocessed_data: pd.DataFrame,
        *,
        inplace: bool = False,
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
