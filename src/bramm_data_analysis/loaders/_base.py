"""DataBase Converting Tools."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from gstlearn import Db
from pandas.core.api import DataFrame

from bramm_data_analysis.loaders.df_to_db.converters import DF2Db

T = TypeVar("T")


class BaseLoader(ABC, Generic[T]):

    """Base class for Loaders."""

    def __init__(self, source: T) -> None:
        """Instantiate the Loader."""
        self._source = source

    @property
    def source(self) -> T:
        """Data Path."""
        return self._source

    @abstractmethod
    def retrieve_df(self) -> DataFrame:
        """Retrieve the original DataFrame."""

    def retrieve_db(self, *, xs: list[str], zs: list[str]) -> Db:
        """Retrieve the DataBase.

        Parameters
        ----------
        xs : list[str]
            X Loacator(s).
        zs : list[str]
            Z Locator(s).

        Returns
        -------
        Db
            DataBase.
        """
        source_df = self.retrieve_df()

        converter = DF2Db(source=source_df)

        return converter.retrieve_db(xs=xs, zs=zs)
