"""The file describes models for geo objects."""
from typing import NamedTuple


class Point(NamedTuple):
    """
    Класс гео-координаты.

    Attributes
    --------
    latitude_coordinate : float
        latitude координата.
    longitude_coordinate : float
        longitude координата.
    """

    latitude_coordinate: float
    longitude_coordinate: float
