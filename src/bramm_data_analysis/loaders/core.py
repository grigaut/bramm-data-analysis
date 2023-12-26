"""Database Loader."""

from pathlib import Path

from pandas.core.api import DataFrame

from bramm_data_analysis.loaders.moss import MossLoader
from bramm_data_analysis.loaders.pandas import PandasDFLoader
from bramm_data_analysis.loaders.rmqs import RMQSLoader


def from_moss_csv(data_path: Path) -> MossLoader:
    """Load DataBase from Moss CSV file."""
    return MossLoader(source=data_path)


def from_rmqs_csv(data_path: Path) -> RMQSLoader:
    """Load DataBase from RMQS CSV file."""
    return RMQSLoader(source=data_path)


def from_pandas(dataframe: DataFrame) -> PandasDFLoader:
    """Load DataBase from pandas DataFrame."""
    return PandasDFLoader(source=dataframe)