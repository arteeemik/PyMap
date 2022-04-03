"""The file describes functions for prepare algorithmic graph."""
import typing

from pymap.open_street_map.graph_class import Graph
from pymap.open_street_map.graph_class import MetricaType
from pymap.open_street_map.route_search_algorithms.models import Node
from pymap.open_street_map.models import Point


def get_algorithmic_graph(
    points: typing.List[Point],
    graph: Graph,
    metrica_type: MetricaType = MetricaType.LENGTH,
) -> typing.List[Node]:
    """
    Возвращает кратчайший путь между двумя координатами в области графа.

    Для точек first_point и second_point возьмется ближайший
        объект из графа.

    Parameters
    ---------
    points : typing.List[Point]
        Координаты точек.
    graph : Graph
        Граф города.
    metrica_type : MetricaType
        Метрика, которая будет указана в качестве веса рёбер.

    Returns
    ---------
    [Node] : typing.List[Node]
        Node:
            Вершина из алгоритмического графа.
    """
    result: typing.List[Node] = []
    for number_point, point in enumerate(points):
        name = number_point
        edges = []
        for number_target_point, target_point in enumerate(points):
            if number_point == number_target_point:
                continue
            distance, _ = graph.get_shortest_path_between_two_points(
                point, target_point, metrica_type
            )
            edges.append((number_target_point, distance))

        result.append(Node(name=name, edges=edges))
    return result
