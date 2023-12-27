"""Database Loader."""

from pathlib import Path

from bramm_data_analysis.loaders.moss import MossLoader
from bramm_data_analysis.loaders.rmqs import RMQSLoader


def from_moss_csv(data_path: Path) -> MossLoader:
    """Retrieve Loader for Moss Data.

    Parameters
    ----------
    data_path : Path
        Path to the source file containing the data.

    Returns
    -------
    MossLoader
        Loader for Moss Data.
    """
    return MossLoader(source=data_path)


def from_rmqs_csv(data_path: Path) -> RMQSLoader:
    """Retrieve Loader for RMQS Data.

    Parameters
    ----------
    data_path : Path
        Path to the source file containing the data.

    Returns
    -------
    RMQSLoader
        Loader for RMQS Data.
    """
    return RMQSLoader(source=data_path)
