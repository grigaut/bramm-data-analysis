"""RMQS Data Loader."""

from pathlib import Path

from bramm_data_analysis.loaders._base import BaseLoader
from bramm_data_analysis.loaders.preprocessing.rmqs import RMQSPreprocessor
from bramm_data_analysis.loaders.reading.rmqs import RMQSReader


class RMQSLoader(BaseLoader[Path]):

    """Loader for RMQS' data."""

    date_field = "date_complete"

    def __init__(self, source: Path) -> None:
        """Instantiate the Loader.

        Parameters
        ----------
        source : Path
            Source object.
        """
        super().__init__(source=source)
        self._reader = RMQSReader(data_path=self.source)
        self._preprocessor = RMQSPreprocessor()
