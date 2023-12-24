"""Generate the Boundary Object."""

import json
import math
from pathlib import Path

from shapely.geometry import MultiPolygon, shape


class Boundary:

    """Spatial Boundary Object."""

    def __init__(self, boundary_geojson_path: Path) -> None:
        """Instantiate the boundary.

        Parameters
        ----------
        boundary_geojson_path : Path
            Path to the geojson boundary file.
        """
        self.polygon = boundary_geojson_path

    @property
    def polygon(self) -> MultiPolygon:
        """Boundary Polygon."""
        return self._polygon

    @polygon.setter
    def polygon(self, boundary_geojson_path: Path) -> None:
        geojson_geometry_bins = json.load(boundary_geojson_path.open("rb"))
        self._polygon = shape(geojson_geometry_bins["geometry"])
        self.bounds = self._polygon.bounds

    @property
    def bounds(self) -> tuple[float]:
        """Spatial bounds of the polygon."""
        return self._bounds

    @bounds.setter
    def bounds(self, bounds: tuple[float]) -> None:
        self._bounds = bounds
        self._x_min, self._y_min, self._x_max, self._y_max = bounds
        self._x_rmin = math.floor(self._x_min)
        self._y_rmin = math.floor(self._y_min)
        self._x_rmax = math.ceil(self._x_max)
        self._y_rmax = math.ceil(self._y_max)

    @property
    def lon_min(self) -> float:
        """Minimum longitude of the boundary."""
        return self._x_min

    @property
    def lon_rmin(self) -> int:
        """Rounded down minimum longitude of the boundary."""
        return self._x_rmin

    @property
    def lat_min(self) -> float:
        """Minimum latitude of the boundary."""
        return self._y_min

    @property
    def lat_rmin(self) -> int:
        """Rounded down minimum latitude of the boundary."""
        return self._y_rmin

    @property
    def lon_max(self) -> float:
        """Maximum longitude of the boundary."""
        return self._x_max

    @property
    def lon_rmax(self) -> int:
        """Rounded up maximum longitude of the boundary."""
        return self._x_rmax

    @property
    def lat_max(self) -> float:
        """Maximum latitude of the boundary."""
        return self._y_max

    @property
    def lat_rmax(self) -> int:
        """Rounded up maximum latitude of the boundary."""
        return self._y_rmax
