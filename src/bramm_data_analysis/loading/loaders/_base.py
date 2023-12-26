"""DataBase Converting Tools."""

from abc import ABC, abstractmethod

from gstlearn import Db


class BaseLoader(ABC):
    @abstractmethod
    def retrieve_database(self, xs: list[str], zs: list[str]) -> Db:
        """Retrieve the DataBase."""
