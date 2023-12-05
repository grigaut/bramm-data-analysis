"""Evaluate Correlation."""

from typing import TYPE_CHECKING

import gstlearn as gl
import gstlearn.plot as gp
import matplotlib.pyplot as plt
import pandas as pd

if TYPE_CHECKING:
    from matplotlib.axes import Axes


class CorrelationEvaluation:

    """Evaluation for Correlation between two variables."""

    def __init__(
        self,
        dataframe: pd.DataFrame,
        *,
        x1: str = "longitude",
        x2: str = "latitude",
    ) -> None:
        """Instantiate the Object.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame to use as Base.
        x1 : str
            X1 field.,
        x2 : str
            X2 field.
        """
        self._x1 = x1
        self._x2 = x2
        self._df = dataframe

    @property
    def x1(self) -> str:
        """X1."""
        return self._x1

    @property
    def x2(self) -> str:
        """X2."""
        return self._x2

    @property
    def data(self) -> pd.DataFrame:
        """DataFrame."""
        return self._df

    def compute_correlation(self, *, z1: str, z2: str) -> "Axes":
        """Compute Correlation Plot between variables z1 and z2.

        Parameters
        ----------
        z1 : str
            First variable (x-axis).
        z2 : str
            Second Variable (y-axis).
        """
        df_view = self.data.filter([self.x1, self.x2, z1, z2]).astype("float")
        db = gl.Db_fromPanda(df_view)
        db.setLocators([self.x1, self.x2], gl.ELoc.X)
        db.setLocator(z1, gl.ELoc.Z)
        ax: Axes = gp.correlation(
            db,
            namex=z1,
            namey=z2,
            asPoint=True,
            regrLine=True,
        )
        ax.decoration(title=f"Correlation between {z1} and {z2}")
        return ax

    def show_correlation(self, *, z1: str, z2: str) -> None:
        """Show Correlation Plot between variables z1 and z2.

        Parameters
        ----------
        z1 : str
            First variable (x-axis).
        z2 : str
            Second Variable (y-axis).
        """
        ax = self.compute_correlation(
            z1=z1,
            z2=z2,
        )
        plt.show(ax)
