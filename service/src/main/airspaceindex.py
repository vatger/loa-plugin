import numpy as np
from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree

from models.vatglasses import Airspace
from utils.coordinate import coord_to_decimal


class AirspaceSectorGeometry:
    __slots__ = ("polygon", "sector_max", "sector_min", "uid")

    def __init__(
        self, uid: str, latlons: list[list[str]], min_alt: int | None, max_alt: int | None
    ):
        poly_points = [
            (coord_to_decimal(lat_s), coord_to_decimal(lon_s)) for lat_s, lon_s in latlons
        ]
        self.polygon = Polygon(poly_points)
        self.uid = uid
        self.sector_min = min_alt
        self.sector_max = max_alt


class AirspaceIndex:
    """Spatial index for fast airspace UID lookups."""

    def __init__(self, airspaces: list[Airspace]):
        self._entries: list[AirspaceSectorGeometry] = []

        for airspace in airspaces:
            for sector in airspace.sectors:
                self._entries.append(
                    AirspaceSectorGeometry(
                        uid=airspace.uid,
                        latlons=sector.points,
                        min_alt=sector.min,
                        max_alt=sector.max,
                    )
                )

        self._polygons = [entry.polygon for entry in self._entries]
        self._tree = STRtree(self._polygons)

    def query(self, lat: float, lon: float, alt: float) -> str | None:
        """
        Return the UID of the airspace that contains (lat, lon, alt),
        or None if not inside any airspace.
        """
        p = Point(lat, lon)
        candidates = self._tree.query(p)

        for candidate in candidates:
            if isinstance(candidate, (int, np.integer)):
                entry = self._entries[candidate]
            else:
                entry = self._entries[self._polygons.index(candidate)]

            if entry.sector_min is not None and alt < entry.sector_min:
                continue
            if entry.sector_max is not None and alt > entry.sector_max:
                continue
            if entry.polygon.contains(p):
                return entry.uid

        return None
