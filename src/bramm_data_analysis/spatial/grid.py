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

    def _mesh(self, step: float) -> gpd.GeoDataFrame:
        """Generate points all around the boundary, separated by given step.

        Parameters
        ----------
        step : float
            Spacing between consecutive points.

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame containing all points within the boundary.
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
        return pd.DataFrame(
            data={
                self.x_field: x_2d.ravel(),
                self.y_field: y_2d.ravel(),
            }
        )

    def _filter(self, locations: pd.DataFrame) -> pd.DataFrame:
        """Filter a dataframe of points.

        Parameters
        ----------
        locations : pd.DataFrame
            Points to filter.

        Returns
        -------
        pd.DataFrame
            Points within the boundaries.
        """
        geometry = gpd.points_from_xy(
            x=locations[self.x_field],
            y=locations[self.y_field],
        )
        is_inside = geometry.within(self._boundary.polygon)
        return gpd.GeoDataFrame(data=locations, geometry=geometry)[is_inside]

    def _divise_area(self, step: float) -> gpd.GeoDataFrame:
        """Compute points within the boundary separated by a given spacing.

        Parameters
        ----------
        step : float
            Spacing between consecutive points.

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame containing all points within the boundary.
        """
        locations = self._mesh(step=step)
        return self._filter(locations=locations)

    def save_insiders(self, step: float, output_path: Path) -> None:
        """Save inside points in a json file.

        Parameters
        ----------
        step : float
            Spacing between consecutive points.
        output_path : Path
            Path to the json file in which to save the points.
        """
        insiders = self._divise_area(step=step)
        insiders.geometry.to_file(output_path, driver="GeoJSON")

    def retrieve_insiders(self, step: float) -> pd.DataFrame:
        """Retrieve points within the boundary separated by a given spacing.

        Parameters
        ----------
        step : float
            Spacing between consecutive points.

        Returns
        -------
        pd.DataFrame
            DataFrame of points within the boundary.
        """
        insiders = self._divise_area(step=step)
        return pd.DataFrame(
            data={
                self.x_field: insiders[self.x_field],
                self.y_field: insiders[self.y_field],
            }
        )

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

    @classmethod
    def read_json(
        cls: type["RegularGrid"], geojson_path: Path
    ) -> pd.DataFrame:
        """Read a geojson file to return the grid."""
        geometry = gpd.read_file(geojson_path).geometry
        return pd.DataFrame(
            data={
                cls.x_field: geometry.x,
                cls.y_field: geometry.y,
            }
        )
