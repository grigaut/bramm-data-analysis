"""Reading Objects."""

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseReader(ABC):

    """Base Class for Readers."""

    def __init__(self, data_path: Path | None) -> None:
        """Instantiate the Reader.

        Parameters
        ----------
        data_path : Path | None
            Path to the file containing data.
        """
        self._path = data_path

    @property
    def data_path(self) -> Path | None:
        """Data Path."""
        return self._path

    @abstractmethod
    def retrieve(self) -> pd.DataFrame:
        """Retrieve data from the source file."""
