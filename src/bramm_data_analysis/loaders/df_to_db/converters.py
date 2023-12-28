"""Converter from DataFrame to Db."""

import gstlearn as gl
from gstlearn import Db
from pandas.core.api import DataFrame


class DF2Db:

    """Convert Pandas' DataFrame to Gstlearn's Db."""

    def __init__(self, source: DataFrame) -> None:
        """INstantiate the Converter.

        Parameters
        ----------
        source : DataFrame
            Source DataFrame.
        """
        self._df = source

    @property
    def source(self) -> DataFrame:
        """Source DataFrame."""
        return self._df

    def raise_if_unsuitable(self, column_name: str) -> None:
        """Verify that a column is suitable for the DataBase.

        Parameters
        ----------
        column_name : str
            Column to verify the type of.

        Raises
        ------
        ValueError
            If the Column is not composed of floats or contains nans.
        """
        column = self.source[column_name]
        # Assert Column is composed of floats
        if column.dtype != "float64":
            msg = f"The column {column_name} must contain only floats."
            raise ValueError(msg)
        # Assert Column has no nans
        if column.isna().any():
            msg = f"The column {column_name} contains NaNs."
            raise ValueError(msg)

    def slice_df(self, xs: list[str] | str, zs: list[str] | str) -> DataFrame:
        """Slice the source dataframe given a list of x and z locators.

        Parameters
        ----------
        xs : list[str] | str
            X locators.
        zs : list[str] | str
            Z locators

        Returns
        -------
        DataFrame
            Sliced copy of source.
        """
        slice_components = []
        # Check all fields
        if isinstance(xs, str):
            self.raise_if_unsuitable(xs)
            slice_components.append(xs)
        else:
            for x in xs:
                self.raise_if_unsuitable(x)
            slice_components += xs
        if isinstance(zs, str):
            self.raise_if_unsuitable(zs)
            slice_components.append(zs)
        else:
            for z in zs:
                self.raise_if_unsuitable(z)
            slice_components += zs
        # Return filtered DataFrame
        return self.source.filter(slice_components).copy()

    def retrieve_db(self, xs: list[str] | str, zs: list[str] | str) -> Db:
        """Retrieve DataBase.

        Parameters
        ----------
        xs : list[str] | str
            X locator(s).
        zs : list[str] | str
            Z locator(s).

        Returns
        -------
        Db
            DataBase.
        """
        # Slice DataFrame
        sliced_source = self.slice_df(xs=xs, zs=zs)
        # Convert to DataFrame
        database = gl.Db_fromPanda(sliced_source)
        # Set locator(s)
        if isinstance(xs, str):
            database.setLocator(xs, gl.ELoc.X)
        else:
            database.setLocators(xs, gl.ELoc.X)
        if isinstance(zs, str):
            database.setLocator(zs, gl.ELoc.Z)
        else:
            database.setLocators(zs, gl.ELoc.Z)
        return database
