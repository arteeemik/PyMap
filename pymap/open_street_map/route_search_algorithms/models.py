"""The file describes models for algorithms graph."""
from typing import List
from typing import Tuple
from typing import NamedTuple


class Node(NamedTuple):
    """
    Класс вершины в алгоритмическом графе.

    Attributes
    --------
    name : int
        Номер вершины в графе
    edges : List[Tuple[int, float]]
        Список ребер, исходящих из вершины.
        edges : List[Tuple[<номер вершины-соседа>, <вес ребра>]]
    """

    name: int
    edges: List[Tuple[int, float]]
