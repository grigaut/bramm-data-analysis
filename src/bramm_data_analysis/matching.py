"""Matching Tools to Match Moss Points with RMQS Points.."""

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


class Matcher:

    """Tool to Match Moss Data With RMQS Data."""

    metric = "haversine"
    moss_suffix = "_moss"
    rmqs_suffix = "_rmqs"
    distance_column = "distance"
    rmqs_date_column = "date_complete"

    def __init__(
        self,
        *,
        year_threshold: int = 2000,
        distance_threshold: float = 1,
    ) -> None:
        """Instanciate Matcher object.

        Parameters
        ----------
        year_threshold : int, optional
            Date Threshold to verify for RMQS data.,
            by default datetime(2000, 1, 1, tzinfo=UTC)
        distance_threshold : float, optional
            Maximum accepted distance for closest point., by default 1
        """
        self.year_threshold = year_threshold
        self.distance_threshold = distance_threshold

    @staticmethod
    def convert_to_radians(degree_dataframe: pd.DataFrame) -> pd.DataFrame:
        """Convert a DataFrame in Degree into a DataFrame in Radian.

        Parameters
        ----------
        degree_dataframe : pd.DataFrame
            DataFrame whose values are all in degree.

        Returns
        -------
        pd.DataFrame
            DataFrame whose values are all in radians.
        """
        return np.deg2rad(degree_dataframe)

    def _apply_year_threshold(
        self,
        rmqs_data: pd.DataFrame,
        date_column: str,
    ) -> pd.DataFrame:
        """Apply the year threshold to the RMQS Data.

        Parameters
        ----------
        rmqs_data : pd.DataFrame
            RMQS Data.
        date_column : str
            Name of the column with the year informations.

        Returns
        -------
        pd.DataFrame
            RMQS Data whose dates are more recent than the threshold.
        """
        dates = rmqs_data[date_column]

        is_greater_than_threshold = dates.dt.year >= self.year_threshold

        return rmqs_data[is_greater_than_threshold]

    def right_to_left(
        self,
        left_data: pd.DataFrame,
        right_data: pd.DataFrame,
        radians: bool,
        *,
        left_longitude: str = "longitude",
        left_latitude: str = "latitude",
        right_longitude: str = "longitude",
        right_latitude: str = "latitude",
        suffixes: tuple[str, str] = ("_left", "_right"),
    ) -> pd.DataFrame:
        """Match a Dataframe (right) onto another one (left).

        Parameters
        ----------
        left_data : pd.DataFrame
            Left DataFrame.
        right_data : pd.DataFrame
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

        Returns
        -------
        pd.DataFrame
            Matched DataFrame of right onto left.
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

        merged = left_data.merge(
            right=right_data,
            left_on=right_data.index[indexes.flatten()],
            right_index=True,
            suffixes=suffixes,
        )
        merged[self.distance_column] = distances
        print(distances)
        return merged

    def _apply_distance_threshold(
        self,
        matched_data: pd.DataFrame,
        distance_column: str,
    ) -> pd.DataFrame:
        """Apply distance threshold after matching.

        Parameters
        ----------
        matched_data : pd.DataFrame
            Matched data.
        distance_column : str
            Maximum distance threshold.

        Returns
        -------
        pd.DataFrame
            Data whose distance is smaller than the threshold.
            (Distance column is removed afterward).
        """
        distances = matched_data.pop(distance_column)

        is_lower_than_threshold = distances <= self.distance_threshold

        return matched_data[is_lower_than_threshold]

    def match_rmqs_to_moss(
        self,
        moss_data: pd.DataFrame,
        rmqs_data: pd.DataFrame,
        radians: bool = False,
        *,
        moss_longitude: str = "longitude",
        moss_latitude: str = "latitude",
        rmqs_longitude: str = "longitude",
        rmqs_latitude: str = "latitude",
    ) -> pd.DataFrame:
        """Match RMQS to Moss Data.

        Final Output will have as many rows as Moss DataFrame.

        Parameters
        ----------
        moss_data : pd.DataFrame
            DataFrame containing Moss Data.
        rmqs_data : pd.DataFrame
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

        Returns
        -------
        pd.DataFrame
            Concatenation of Matched RMQS Data with Moss Data.
        """
        rmqs_sliced = self._apply_year_threshold(
            rmqs_data=rmqs_data,
            date_column=self.rmqs_date_column,
        )

        matched = self.right_to_left(
            left_data=moss_data,
            right_data=rmqs_sliced,
            radians=radians,
            left_longitude=moss_longitude,
            left_latitude=moss_latitude,
            right_longitude=rmqs_longitude,
            right_latitude=rmqs_latitude,
            suffixes=(self.moss_suffix, self.rmqs_suffix),
        )

        return self._apply_distance_threshold(
            matched_data=matched,
            distance_column=self.distance_column,
        )

    def match_moss_to_rmqs(
        self,
        moss_data: pd.DataFrame,
        rmqs_data: pd.DataFrame,
        radians: bool = True,
        *,
        moss_longitude: str = "longitude",
        moss_latitude: str = "latitude",
        rmqs_longitude: str = "longitude",
        rmqs_latitude: str = "latitude",
    ) -> pd.DataFrame:
        """Match Moss to RMQS Data.

        Final Output will have as many rows as RMQS DataFrame.

        Parameters
        ----------
        moss_data : pd.DataFrame
            DataFrame containing Moss Data.
        rmqs_data : pd.DataFrame
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

        Returns
        -------
        pd.DataFrame
            Concatenation of Matched Moss Data with RMQS Data.
        """
        rmqs_sliced = self._apply_year_threshold(
            rmqs_data=rmqs_data,
            date_column=self.rmqs_date_column,
        )

        matched = self.right_to_left(
            right_data=moss_data,
            left_data=rmqs_sliced,
            radians=radians,
            right_longitude=moss_longitude,
            right_latitude=moss_latitude,
            left_longitude=rmqs_longitude,
            left_latitude=rmqs_latitude,
            suffixes=(self.moss_suffix, self.rmqs_suffix),
        )

        return self._apply_distance_threshold(
            matched_data=matched,
            distance_column=self.distance_column,
        )
