"""Generate a regular grid in a (multi)polygon."""

from pathlib import Path
from typing import Self

import geopandas as gpd
import gstlearn as gl
from gstlearn import DbGrid

from bramm_data_analysis.spatial.boundary import Boundary


class RegularGrid:

    """Create a Regular grid based on given Boundaries."""

    x_field = "longitude"
    y_field = "latitude"
    insider_field = "inland"

    def __init__(self, boundary: Boundary) -> None:
        """Instantiate the Regulargrid.

        Parameters
        ----------
        boundary : Boundary
            Boundaries for the grid.
        """
        self._boundary = boundary

    @property
    def boundary(self) -> Boundary:
        """Boundary Object."""
        return self._boundary

    def _mesh(self, step: float) -> DbGrid:
        """Generate points all around the boundary, separated by given step.

        Parameters
        ----------
        step : float
            Spacing between consecutive points.

        Returns
        -------
        DbGrid
            DbGrid containing all points within the boundary.
        """
        rmin_lon = self.boundary.lon_rmin
        rmax_lon = self.boundary.lon_rmax
        rmin_lat = self.boundary.lat_rmin
        rmax_lat = self.boundary.lat_rmax
        # Create DbGrid over entire area
        grid: DbGrid = gl.DbGrid.create(
            x0=[rmin_lon, rmin_lat],
            dx=[step, step],
            nx=[
                int((rmax_lon - rmin_lon) / step),
                int((rmax_lat - rmin_lat) / step),
            ],
        )
        grid.setName("x1", self.x_field)
        grid.setName("x2", self.y_field)
        return grid

    def _filter(self, full_grid: DbGrid) -> DbGrid:
        """Filter a dataframe of points.

        Parameters
        ----------
        full_grid : pd.DataFrame
            DbGrid containing all points.

        Returns
        -------
        DbGrid
            DbGrid with selection zone.
        """
        # Make GeoPandas geometry from grid points.
        geometry = gpd.points_from_xy(
            x=full_grid[self.x_field],
            y=full_grid[self.y_field],
        )
        # Check whether points are inside the boundary or not
        full_grid[self.insider_field] = geometry.within(self._boundary.polygon)
        # Define as selection
        full_grid.setLocator(self.insider_field, gl.ELoc.SEL)
        return full_grid

    def retrieve_grid(self, step: float) -> DbGrid:
        """Retrieve points within the boundary separated by a given spacing.

        Parameters
        ----------
        step : float
            Spacing between consecutive points.

        Returns
        -------
        DbGrid
            DataFrame of points within the boundary.
        """
        full_grid = self._mesh(step=step)
        return self._filter(full_grid=full_grid)

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
        # Create regularGrid from geojson path instead of Boundary object
        return cls(
            boundary=Boundary(boundary_geojson_path=boundary_geojson_path),
        )
