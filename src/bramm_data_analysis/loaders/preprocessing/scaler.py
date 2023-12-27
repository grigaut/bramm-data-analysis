"""Standardize Data."""

import pandas as pd
from sklearn.preprocessing import StandardScaler


class Scaler:

    """Normalize Data."""

    longitude_field = "longitude"
    latitude_field = "latitude"

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """Instantiate Object."""
        self._df = dataframe

    @property
    def data(self) -> pd.DataFrame:
        """DataFrame."""
        return self._df

    @property
    def _lon_lat(self) -> pd.DataFrame:
        """View of longitude and latitude columns."""
        return self.data.filter([self.longitude_field, self.latitude_field])

    def scale(self, *columns: str) -> pd.DataFrame:
        """Scale the dataframe on the given columns.

        Returns
        -------
        pd.DataFrame
            Scaled DataFrame with longitude and latitude.

        Raises
        ------
        KeyError
            If the longitude or latitude columns are set to be scaled.
        """
        normalize_longitude = self.longitude_field in columns
        normalize_latitude = self.latitude_field in columns

        if normalize_longitude or normalize_latitude:
            msg = (
                f"Normalizing of columns {self.longitude_field} "
                f"or {self.latitude_field} forbidden."
            )
            raise KeyError(msg)

        scaler = StandardScaler()
        scaled_arr = scaler.fit_transform(self.data.filter(columns))
        scaled_df = pd.DataFrame(
            data=scaled_arr,
            columns=columns,
            index=self.data.index,
        )
        return pd.concat([self._lon_lat, scaled_df], axis=1)
