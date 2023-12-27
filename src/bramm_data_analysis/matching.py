"""Matching Tools to Match Moss Points with RMQS Points.."""

from typing import Literal, overload

import numpy as np
from pandas.core.api import DataFrame
from sklearn.neighbors import NearestNeighbors


class Matcher:

    """Tool to Match Moss Data With RMQS Data."""

    metric = "haversine"
    moss_suffix = "_moss"
    rmqs_suffix = "_rmqs"
    distance_column = "distance"
    rmqs_date_column = "date_complete"
    _earth_radius_km = 6371

    def __init__(
        self,
        *,
        year_threshold: int = 2000,
        km_threshold: float = 1,
    ) -> None:
        """Instanciate Matcher object.

        Parameters
        ----------
        year_threshold : int, optional
            Date Threshold to verify for RMQS data.,
            by default datetime(2000, 1, 1, tzinfo=UTC)
        km_threshold : float, optional
            Maximum accepted distance for closest point in km., by default 1
        """
        self.year_threshold = year_threshold
        self.km_threshold = km_threshold

    @property
    def rad_threshold(self) -> float:
        """Distance Threshold in Radians."""
        return self.km_threshold / self._earth_radius_km

    @staticmethod
    def convert_to_radians(degree_dataframe: DataFrame) -> DataFrame:
        """Convert a DataFrame in Degree into a DataFrame in Radian.

        Parameters
        ----------
        degree_dataframe : DataFrame
            DataFrame whose values are all in degree.

        Returns
        -------
        DataFrame
            DataFrame whose values are all in radians.
        """
        return np.deg2rad(degree_dataframe)

    def _apply_year_threshold(
        self,
        rmqs_data: DataFrame,
        date_column: str,
    ) -> DataFrame:
        """Apply the year threshold to the RMQS Data.

        Parameters
        ----------
        rmqs_data : DataFrame
            RMQS Data.
        date_column : str
            Name of the column with the year informations.

        Returns
        -------
        DataFrame
            RMQS Data whose dates are more recent than the threshold.
        """
        dates = rmqs_data[date_column]

        is_greater_than_threshold = dates.dt.year >= self.year_threshold

        return rmqs_data[is_greater_than_threshold]

    @overload
    def right_to_left(
        self,
        left_data: DataFrame,
        right_data: DataFrame,
        radians: bool,
        *,
        left_longitude: str = ...,
        left_latitude: str = ...,
        right_longitude: str = ...,
        right_latitude: str = ...,
        suffixes: tuple[str, str] = ...,
        leftovers: Literal[False] = ...,
    ) -> DataFrame:
        ...

    @overload
    def right_to_left(
        self,
        left_data: DataFrame,
        right_data: DataFrame,
        radians: bool,
        *,
        left_longitude: str = ...,
        left_latitude: str = ...,
        right_longitude: str = ...,
        right_latitude: str = ...,
        suffixes: tuple[str, str] = ...,
        leftovers: Literal[True] = ...,
    ) -> tuple[DataFrame, DataFrame]:
        ...

    def right_to_left(
        self,
        left_data: DataFrame,
        right_data: DataFrame,
        radians: bool,
        *,
        left_longitude: str = "longitude",
        left_latitude: str = "latitude",
        right_longitude: str = "longitude",
        right_latitude: str = "latitude",
        suffixes: tuple[str, str] = ("_left", "_right"),
        leftovers: bool = False,
    ) -> DataFrame | tuple[DataFrame, DataFrame]:
        """Match a Dataframe (right) onto another one (left).

        Parameters
        ----------
        left_data : DataFrame
            Left DataFrame.
        right_data : DataFrame
            Right DataFrame.
        radians: bool
            Whether the provided Data is in radians or not.
        left_longitude : str, optional
            Longitude column for the left DataFrame., by default "longitude"
        left_latitude : str, optional
            Latitude column for the left DataFrame., by default "latitude"
        right_longitude : str, optional
            Longitude column for the right DataFrame., by default "longitude"
        right_latitude : str, optional
            Latitude column for the right DataFrame., by default "latitude"
        suffixes : tuple[str, str], optional
            Suffixes to use for merging., by default ("_left", "_right")
        leftovers: bool, optional
            Whether to return unused data from right dataframe or not.
            , by default False

        Returns
        -------
        DataFrame | tuple[DataFrame, DataFrame]
            Matched DataFrame of right onto left and
             leftovers dataframe if `leftovers` is True.
        """
        # Slice to conserve only coordinates.
        left_xy = left_data.filter([left_longitude, left_latitude])
        right_xy = right_data.filter([right_longitude, right_latitude])
        if not radians:
            left_xy = Matcher.convert_to_radians(left_xy)
            right_xy = Matcher.convert_to_radians(right_xy)

        # Estimator fitting
        estimator = NearestNeighbors(n_neighbors=1, metric=self.metric)
        estimator.fit(right_xy)
        distances, indexes = estimator.kneighbors(left_xy)

        is_lower_than_threshold = (distances <= self.rad_threshold).flatten()

        left_data_cropped = left_data[is_lower_than_threshold]
        indexes_cropped = indexes.flatten()[is_lower_than_threshold]

        merged = left_data_cropped.merge(
            right=right_data,
            left_on=right_data.index[indexes_cropped],
            right_index=True,
            suffixes=suffixes,
        )
        if leftovers:
            is_conserved = right_data.index.isin(indexes_cropped)
            leftovers = right_data[~is_conserved]
            return merged, leftovers
        return merged

    @overload
    def match_rmqs_to_moss(
        self,
        moss_data: DataFrame,
        rmqs_data: DataFrame,
        radians: bool = ...,
        *,
        moss_longitude: str = ...,
        moss_latitude: str = ...,
        rmqs_longitude: str = ...,
        rmqs_latitude: str = ...,
        leftovers: Literal[True],
    ) -> tuple[DataFrame, DataFrame]:
        ...

    @overload
    def match_rmqs_to_moss(
        self,
        moss_data: DataFrame,
        rmqs_data: DataFrame,
        radians: bool = ...,
        *,
        moss_longitude: str = ...,
        moss_latitude: str = ...,
        rmqs_longitude: str = ...,
        rmqs_latitude: str = ...,
        leftovers: Literal[False],
    ) -> DataFrame:
        ...

    def match_rmqs_to_moss(
        self,
        moss_data: DataFrame,
        rmqs_data: DataFrame,
        radians: bool = False,
        *,
        moss_longitude: str = "longitude",
        moss_latitude: str = "latitude",
        rmqs_longitude: str = "longitude",
        rmqs_latitude: str = "latitude",
        leftovers: bool = False,
    ) -> tuple[DataFrame, DataFrame] | DataFrame:
        """Match RMQS to Moss Data.

        Final Output will have as many rows as Moss DataFrame.

        Parameters
        ----------
        moss_data : DataFrame
            DataFrame containing Moss Data.
        rmqs_data : DataFrame
            DataFrame containing RMQS Data.
        radians: bool
            Whether the provided Data is in radians or not.by default False
        moss_longitude : str, optional
            Label for longitude in moss DataFrame., by default "longitude"
        moss_latitude : str, optional
            Label for latitude in moss DataFrame., by default "latitude"
        rmqs_longitude : str, optional
            Label for longitude in RMQS DataFrame., by default "longitude"
        rmqs_latitude : str, optional
            Label for latitude in RMQS DataFrame., by default "latitude"
        leftovers: bool, optional
            Whether to return unused data from right dataframe or not.
            , by default False

        Returns
        -------
        DataFrame | tuple[DataFrame, DataFrame]
            Matched DataFrame of right onto left and
             leftovers dataframe if `leftovers` is True.
        """
        rmqs_sliced = self._apply_year_threshold(
            rmqs_data=rmqs_data,
            date_column=self.rmqs_date_column,
        )

        return self.right_to_left(
            left_data=moss_data,
            right_data=rmqs_sliced,
            radians=radians,
            left_longitude=moss_longitude,
            left_latitude=moss_latitude,
            right_longitude=rmqs_longitude,
            right_latitude=rmqs_latitude,
            suffixes=(self.moss_suffix, self.rmqs_suffix),
            leftovers=leftovers,
        )

    @overload
    def match_moss_to_rmqs(
        self,
        moss_data: DataFrame,
        rmqs_data: DataFrame,
        radians: bool = ...,
        *,
        moss_longitude: str = ...,
        moss_latitude: str = ...,
        rmqs_longitude: str = ...,
        rmqs_latitude: str = ...,
        leftovers: Literal[True],
    ) -> tuple[DataFrame, DataFrame]:
        ...

    @overload
    def match_moss_to_rmqs(
        self,
        moss_data: DataFrame,
        rmqs_data: DataFrame,
        radians: bool = ...,
        *,
        moss_longitude: str = ...,
        moss_latitude: str = ...,
        rmqs_longitude: str = ...,
        rmqs_latitude: str = ...,
        leftovers: Literal[False],
    ) -> DataFrame:
        ...

    def match_moss_to_rmqs(
        self,
        moss_data: DataFrame,
        rmqs_data: DataFrame,
        radians: bool = True,
        *,
        moss_longitude: str = "longitude",
        moss_latitude: str = "latitude",
        rmqs_longitude: str = "longitude",
        rmqs_latitude: str = "latitude",
        leftovers: bool = False,
    ) -> tuple[DataFrame, DataFrame] | DataFrame:
        """Match Moss to RMQS Data.

        Final Output will have as many rows as RMQS DataFrame.

        Parameters
        ----------
        moss_data : DataFrame
            DataFrame containing Moss Data.
        rmqs_data : DataFrame
            DataFrame containing RMQS Data.
        radians: bool
            Whether the provided Data is in radians or not.by default False
        moss_longitude : str, optional
            Label for longitude in moss DataFrame., by default "longitude"
        moss_latitude : str, optional
            Label for latitude in moss DataFrame., by default "latitude"
        rmqs_longitude : str, optional
            Label for longitude in RMQS DataFrame., by default "longitude"
        rmqs_latitude : str, optional
            Label for latitude in RMQS DataFrame., by default "latitude"
        leftovers: bool, optional
            Whether to return unused data from right dataframe or not.
            , by default False

        Returns
        -------
        DataFrame | tuple[DataFrame, DataFrame]
            Matched DataFrame of right onto left and
             leftovers dataframe if `leftovers` is True.
        """
        rmqs_sliced = self._apply_year_threshold(
            rmqs_data=rmqs_data,
            date_column=self.rmqs_date_column,
        )

        return self.right_to_left(
            right_data=moss_data,
            left_data=rmqs_sliced,
            radians=radians,
            right_longitude=moss_longitude,
            right_latitude=moss_latitude,
            left_longitude=rmqs_longitude,
            left_latitude=rmqs_latitude,
            suffixes=(self.moss_suffix, self.rmqs_suffix),
            leftovers=leftovers,
        )
