"""Moss Preprocessing Tools."""

from typing import ClassVar, Literal, overload

import pandas as pd

from bramm_data_analysis.loaders.preprocessing._base import BasePreprocessor


class MossPreprocessor(BasePreprocessor):

    """Preprocessor for Moss Data."""

    cols_to_set_as_float: ClassVar[list[str]] = [
        "sodium",
        "platinium",
        "rhodium",
        "antimony",
        "strontium",
        "vanadium",
        "zinc",
    ]

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

        replace_commas = lambda x: x.replace(",", ".")
        remove_lt = lambda x: x.replace("< ", "")

        for col in self.cols_to_set_as_float:
            if col not in to_modify.columns:
                continue
            to_modify[col] = to_modify[col].astype(str)
            to_modify[col] = to_modify[col].apply(replace_commas)
            to_modify[col] = to_modify[col].apply(remove_lt)
            to_modify[col].astype("float64")

        return None if inplace else to_modify
