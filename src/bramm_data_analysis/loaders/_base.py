"""DataBase Converting Tools."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import numpy as np
from gstlearn import Db
from pandas.core.api import DataFrame

from bramm_data_analysis.loaders.df_to_db.converters import DF2Db
from bramm_data_analysis.loaders.preprocessing._base import BasePreprocessor
from bramm_data_analysis.loaders.preprocessing.duplicates import (
    DuplicatesRemover,
)
from bramm_data_analysis.loaders.preprocessing.outliers.thresholds import (
    Threshold,
)
from bramm_data_analysis.loaders.reading._base import BaseReader

T = TypeVar("T")


class BaseLoader(ABC, Generic[T]):

    """Base class for Loaders."""

    date_field = "date"
    longitude_field = "longitude"
    latitude_field = "latitude"
    _reader: BaseReader
    _preprocessor: BasePreprocessor

    @abstractmethod
    def __init__(self, source: T) -> None:
        """Instantiate the Loader.

        Parameters
        ----------
        source : T
            Source object.
        """
        self._source = source

    @property
    def source(self) -> T:
        """Data Path."""
        return self._source

    def _handle_duplicates(
        self, dataframe: DataFrame, *, duplicates_handling_strategy: str | None
    ) -> DataFrame:
        """Remove Duplicated rows.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame containing duplicates.
        duplicates_handling_strategy : str | None
            Strategy to follow to aggregate duplicates.

        Returns
        -------
        DataFrame
            DataFrame without duplicates if strategy is not None
            , else same DataFrame.
        """
        if duplicates_handling_strategy is None:
            return dataframe
        # Create Duplicate Remover
        duplicate_remover = DuplicatesRemover(
            aggregating_method=duplicates_handling_strategy,
        )
        # Modify fields to match dataframe's
        duplicate_remover.date_field = self.date_field
        duplicate_remover.longitude_field = self.longitude_field
        duplicate_remover.latitude_field = self.latitude_field
        # Process duplicates
        return duplicate_remover.process_duplicates(dataframe)

    def raise_if_essential_columns_missing(self, dataframe: DataFrame) -> None:
        """Raise an error if one essential column is missing.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame to check.

        Raises
        ------
        KeyError
            If there is no date, longitude or latitude column.
        """
        date_in = self.date_field in dataframe.columns
        longitude_in = self.longitude_field in dataframe.columns
        latitude_in = self.latitude_field in dataframe.columns
        if not (date_in and longitude_in and latitude_in):
            msg = "One of the essential columns are missing in the dataframe."
            raise KeyError(msg)

    def retrieve_filtered_df(
        self,
        fields: list[str],
        *,
        duplicates_handling_strategy: str | None = None,
        thresholds: list[Threshold] | None = None,
    ) -> DataFrame:
        """Retrieve Filtered DataFrame.

        Parameters
        ----------
        fields : list[str]
            List of fields to conserve. If empty, return the same DataFrame.
        duplicates_handling_strategy : str | None, optional
            Aggregation method to handle duplicates.
            If None, the duplicates will not be removed., by default None
        thresholds : list[Threshold] | None, optional
            Thresholds to satisfy for the data.
              If None, no threshold selection is made., by default None

        Returns
        -------
        DataFrame
            Filtered DataFrame
        """
        # Retrieve filtered df
        dataframe = self._reader.retrieve_and_filter(fields)
        self.raise_if_essential_columns_missing(dataframe)
        # Preprocess Data
        preprocessed = self._preprocessor.preprocess(
            unprocessed_data=dataframe,
            inplace=False,
        )
        if thresholds is None:
            # Handle Dulicates
            return self._handle_duplicates(
                preprocessed,
                duplicates_handling_strategy=duplicates_handling_strategy,
            )
        # Check Thresholds
        verify_threshold = np.full(
            fill_value=True,
            shape=(preprocessed.shape[0],),
        )
        for threshold in thresholds:
            verify_threshold &= threshold.check_threshold(preprocessed)
        # Handle Dulicates
        return self._handle_duplicates(
            preprocessed[verify_threshold],
            duplicates_handling_strategy=duplicates_handling_strategy,
        )

    def retrieve_df(
        self, *, duplicates_handling_strategy: str | None = None
    ) -> DataFrame:
        """Retrieve Filtered DataFrame.

        Parameters
        ----------
        duplicates_handling_strategy: str | None
            Aggregation method to handle duplicates.
            If None, the duplicates will not be removed., by default None

        Returns
        -------
        DataFrame
            DataFrame
        """
        # Retrieve unfiltered DF
        dataframe = self._reader.retrieve()
        self.raise_if_essential_columns_missing(dataframe)
        # Preprocess Data
        preprocessed = self._preprocessor.preprocess(
            unprocessed_data=dataframe,
            inplace=False,
        )
        # remove Duplicates
        return self._handle_duplicates(
            preprocessed,
            duplicates_handling_strategy=duplicates_handling_strategy,
        )

    def retrieve_db(
        self,
        *,
        xs: list[str],
        zs: list[str],
        duplicates_handling_strategy: str | None = None,
        thresholds: list[Threshold] | None = None,
    ) -> Db:
        """Retrieve the DataBase.

        Parameters
        ----------
        xs : list[str]
            X Loacator(s).
        zs : list[str]
            Z Locator(s).
        duplicates_handling_strategy: str | None
            Aggregation method to handle duplicates.
            If None, the duplicates will not be removed., by default None
        thresholds : list[Threshold] | None, optional
            Thresholds to satisfy for the data.
              If None, no threshold selection is made., by default None

        Returns
        -------
        Db
            DataBase.
        """
        # Parse fields to filter
        fields = []
        if isinstance(xs, str):
            fields.append(xs)
        else:
            fields += xs
        if isinstance(zs, str):
            fields.append(zs)
        else:
            fields += zs

        fields += [self.date_field, self.longitude_field, self.latitude_field]

        fields = list(set(fields))

        # Retrieve filtered df containing only useful fields
        source_df = self.retrieve_filtered_df(
            fields=fields,
            duplicates_handling_strategy=duplicates_handling_strategy,
            thresholds=thresholds,
        )

        # Convert DataFrame to Db
        converter = DF2Db(source=source_df)
        return converter.retrieve_db(xs=xs, zs=zs)
