"""Generate a regular grid in a (multi)polygon."""

from pathlib import Path
from typing import Self

import geopandas as gpd
import numpy as np
import pandas as pd

from bramm_data_analysis.spatial.boundary import Boundary


class RegularGrid:

    """Create a Regular grid based on given Boundaries."""

    x_field = "longitude"
    y_field = "latitude"

    def __init__(self, boundary: Boundary) -> None:
        """Instantiate the Regulargrid.

        Parameters
        ----------
        boundary : Boundary
            Boundaries for the grid.
        """
        self._boundary = boundary

    def divise_area(self, step: float) -> pd.DataFrame:
        """Divise the area within the boundary on points separated by step.

        Parameters
        ----------
        step : float
            Division length between points.

        Returns
        -------
        pd.DataFrame
            DataFrame containing all points within the boundaries.
        """
        x_points = np.arange(
            start=self._boundary.lon_rmin,
            stop=self._boundary.lon_rmax,
            step=step,
        )
        y_points = np.arange(
            start=self._boundary.lat_rmin,
            stop=self._boundary.lat_rmax,
            step=step,
        )[::-1]
        x_2d, y_2d = np.meshgrid(x_points, y_points)
        locations = pd.DataFrame(
            data={
                self.x_field: x_2d.ravel(),
                self.y_field: y_2d.ravel(),
            }
        )
        geometry = gpd.points_from_xy(
            x=locations[self.x_field],
            y=locations[self.y_field],
        )
        is_inside = geometry.within(self._boundary.polygon)
        return locations[is_inside]

    @classmethod
    def from_boundary_path(
        cls: type["RegularGrid"], boundary_geojson_path: Path
    ) -> Self:
        """Instantiate the RegularGrid from the boundaries geojson.

        Parameters
        ----------
        boundary_geojson_path : Path
            Path to the geojson boundary file.

        Returns
        -------
        Self
            RegularGrid
        """
        return cls(
            boundary=Boundary(boundary_geojson_path=boundary_geojson_path),
        )
