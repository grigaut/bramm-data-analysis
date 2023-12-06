"""Moss Preprocessing Tools."""

from pathlib import Path
from typing import ClassVar, Literal, overload

import pandas as pd

from bramm_data_analysis import loading
from bramm_data_analysis.preprocessing._base import Preprocessor


class MossPreprocessor(Preprocessor):

    """Preprocessor for Moss Data."""

    merge_sites_with_samples_on = "site_code"
    merge_sites_samples_with_values_on = "sample_code"
    cols_to_set_as_float: ClassVar[list[str]] = [
        "sodium",
        "platinium",
        "rhodium",
        "antimony",
        "strontium",
        "vanadium",
        "zinc",
    ]

    def __init__(self, data_path: Path) -> None:
        """Instanciates the preprocessor."""
        super().__init__(data_path)

    def load(self) -> pd.DataFrame:
        """Load the DataFrame.

        Returns
        -------
        pd.DataFrame
            Loaded Data.
        """
        sites_data = loading.load_sites(self._data)
        samples_data = loading.load_samples(self._data)
        values_data = loading.load_values(self._data)

        sites_with_samples = sites_data.merge(
            right=samples_data,
            on=self.merge_sites_with_samples_on,
        )
        return sites_with_samples.merge(
            right=values_data,
            on=self.merge_sites_samples_with_values_on,
        )

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
            to_modify[col] = to_modify[col].astype(str)
            to_modify[col] = to_modify[col].apply(replace_commas)
            to_modify[col] = to_modify[col].apply(remove_lt)
            to_modify[col].astype("float64")

        return None if inplace else to_modify
