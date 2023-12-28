"""Moss Data Loader."""

from pathlib import Path

from bramm_data_analysis.loaders._base import BaseLoader
from bramm_data_analysis.loaders.preprocessing.moss import MossPreprocessor
from bramm_data_analysis.loaders.reading.moss import MossReader


class MossLoader(BaseLoader[Path]):

    """Loader for Moss' data."""

    def __init__(self, source: Path) -> None:
        """Instantiate the Loader.

        Parameters
        ----------
        source : T
            Source object.
        """
        super().__init__(source=source)
        # Instantiate Reader with MossReader
        self._reader = MossReader(data_path=self.source)
        # Instantiate Preprocessor wit MossPreprocessor
        self._preprocessor = MossPreprocessor()
