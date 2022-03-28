"""The file describes the graph class."""
import typing
import enum

import osmnx as ox
from osmnx import distance as osmnx_distance
from osmnx import utils_graph
import networkx as nx


class MovementType(enum.Enum):
    """Тип способа передвижения для задания графа области."""

    BIKE: str = "bike"
    DRIVE: str = "drive"
    WALK: str = "walk"
    DRIVE_SERVICE: str = "drive_service"
    ALL: str = "all"
    ALL_PRIVATE: str = "all_private"


class MetricaType(enum.Enum):
    """Тип метрики, по которой будет считаться оптимальный маршрут."""

    LENGTH: str = "length"
    TIME: str = "time"


class Graph:
    """
    Класс графа некоторой области и функции, необходимые для работы с ним.

    Attributes
    --------
    graph : networkx.MultiDiGraph
    """

    def __init__(
        self,
        place_full_name: str,
        movement_type: MovementType = MovementType.WALK,
    ):
        """
        Определяет объект graph в классе.

        Parameters
        ---------
        place_full_name : str
            Полное имя области, для которой хотим создать граф.
            example: "San Francisco, California, United States"
        movement_type : MovementType
            Тип передвижения.
        """
        ox.config(log_console=True, use_cache=True)
        self.graph = ox.graph_from_place(
            place_full_name, network_type=movement_type.value
        )

    def get_nearest_nodes(
        self, points: typing.List[typing.Tuple[float, float]]
    ) -> typing.List[int]:
        """
        Возвращает ids ближайших вершин к координатам в points в графе.

        Parameters
        ---------
        points : typing.List[typing.Tuple[float, float]]
            Список координат точек.
        Returns
        ---------
        ids : typing.List[int]
           IDs ближайших вершины к координатам из points в графе.
        """
        latitude_coordinates = [point[0] for point in points]
        longitude_coordinates = [point[1] for point in points]
        return list(
            osmnx_distance.nearest_nodes(
                self.graph, longitude_coordinates, latitude_coordinates
            )
        )

    def get_shortest_path_between_two_points(
        self,
        first_point: typing.Tuple[float, float],
        second_point: typing.Tuple[float, float],
        metrica_type: MetricaType = MetricaType.LENGTH,
    ) -> (float, typing.List[int]):
        # pylint: disable=unbalanced-tuple-unpacking
        """
        Возвращает кратчайший путь между двумя координатами в области графа.

        Для точек first_point и second_point возьмется ближайший
            объект из графа.

        Parameters
        ---------
        first_point : typing.Tuple[float, float]
            Координаты точки.
        second_point : typing.Tuple[float, float]
            Координаты точки.
        metrica_type : MetricaType
            Метрика, по которой ищем минимальный путь между двумя координатами.

        Returns
        ---------
        (distance, shortest_route) : (float, typing.List[int])
            distance:
                Если optimizer_type == MetricaType.LENGTH: длина в метрах.
                Если optimizer_type == MetricaType.TIME: время в часах.
            shortest_route - путь от first_point до second_point в виде списка
                айдишников объектов из графа.
        """
        first_node, second_node = self.get_nearest_nodes(
            [first_point, second_point]
        )

        shortest_route = nx.shortest_path(
            self.graph, first_node, second_node, weight=metrica_type.value
        )
        edge_lengths = utils_graph.get_route_edge_attributes(
            self.graph, shortest_route, metrica_type.value
        )

        return sum(edge_lengths), shortest_route
