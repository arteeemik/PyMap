"""
Full search path.

Functions for finding a shortest path
to traverse all nodes using a full search.
"""
from typing import Dict
from typing import Tuple
from typing import List
from typing import Optional

from pymap.open_street_map.route_search_algorithms.models import Node


def __make_edges_dict(nodes: List[Node]) -> Dict[Tuple[int, int], float]:
    edges_dict = {}
    for node in nodes:
        for target_node_name, dist in node.edges:
            edges_dict[(node.name, target_node_name)] = dist
    return edges_dict


def __permutations(nodes: List[Node]) -> List[Node]:
    if len(nodes) == 1:
        yield [nodes[0]]
    else:
        for perm in __permutations(nodes[1:]):
            for i in range(len(nodes)):
                yield perm[:i] + [nodes[0]] + perm[i:]


def __get_path(nodes: List[Node], start: Optional[int] = None) -> List[Node]:
    if start:
        for permutation in __permutations(nodes[:start] + nodes[start + 1 :]):
            yield [nodes[start]] + permutation
    else:
        for permutation in __permutations(nodes):
            yield permutation


def __get_dist_for_path(
    path: List[Node], edges_dict: Dict[Tuple[int, int], float]
) -> float:
    result = 0
    for i in range(len(path) - 1):
        result += edges_dict[(path[i].name, path[i + 1].name)]
    return result


def find_shortest_path_all_nodes(
    nodes: List[Node], start: Optional[int] = None
) -> Tuple[float, List[Node]]:
    """
    Возвращает кратчайший путь для обхода всех вершин.

    Алгоритм - полный перебор всевозможных путей.

    Parameters
    ---------
    nodes : List[Node]
        Точки в графе
    start: Optional[int]
        Стартовая точка для обхода всех вершин.

    Returns
    ---------
    Tuple[distance, path] : Tuple[float, List[Node]]
        distance: длина кратчайшего пути.
        path: путь для обхода всех вершин.
    """
    edges_dict = __make_edges_dict(nodes)
    min_dist = None
    min_path = None
    for maybe_path in __get_path(nodes, start=start):
        path_dist = __get_dist_for_path(maybe_path, edges_dict)
        if min_dist is None or min_dist > path_dist:
            min_dist = path_dist
            min_path = maybe_path

    return min_dist, min_path
