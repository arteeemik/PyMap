import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox
import typing as tp

from graph_class import Graph


class BoundingBox:
    def __init__(self, x: tp.List[float], y: tp.List[float]) -> None:
        self.left_down, self.right_up = None, None
        for px, py in zip(x, y):
            self.extend(px, py)

    def is_init(self) -> bool:
        """
        return: True если BoundingBox построен, False иначе
        """
        return self.left_down and self.right_up

    def center(self):
        """
        return: Центр BoundingBox
        """
        return [(self.left_down[0] + self.right_up[0]) / 2.0, (self.left_down[1] + self.right_up[1]) / 2.0]

    def scaling(self, scaling_param: float):
        """
        coef: коэфициент расширения

        return: self
        """
        center = self.center()
        diag = [self.right_up[0] - self.left_down[0], self.right_up[1] - self.left_down[1]]
        self.extend(center[0] + diag[0] * scaling_param * 0.5, center[1] + diag[1] * scaling_param * 0.5)
        self.extend(center[0] - diag[0] * scaling_param * 0.5, center[1] - diag[1] * scaling_param * 0.5)
        return self

    def extend(self, px: float, py: float) -> None:
        """
        px:     x координата точки, которую добавляем
        py:     y координата точки, которую добавляем
        """
        if self.is_init():
            self.left_down = [min(self.left_down[0], px), min(self.left_down[1], py)]
            self.right_up = [max(self.right_up[0], px), max(self.right_up[1], py)]
        else:
            self.left_down = self.right_up = [px, py]


def get_xy_from_path(graph: Graph, path: tp.List[int]) -> tp.Tuple[tp.List[float], tp.List[float]]:
    """
    graph:  граф местности
    path:   список node-ов в пути

    return:
    """
    x = [graph.graph.nodes[node_id]['x'] for node_id in path]
    y = [graph.graph.nodes[node_id]['y'] for node_id in path]
    return x, y


def visualize_route(graph: Graph, path: tp.List[int], tags: tp.Dict[str, bool]):
    """
    graph:  граф местности
    path:   список node-ов в пути
    tags:   список тэгов для фильтрации геометрии
    """
    x, y = get_xy_from_path(graph, path)
    bb = BoundingBox(x, y).scaling(1.1)
    objects = gpd.GeoSeries(ox.geometries.geometries_from_bbox(
            bb.left_down[1], bb.right_up[1], 
            bb.left_down[0], bb.right_up[0], 
            tags=tags).geometry)
    objects.plot()
    plt.plot(x, y, c='r')
    plt.show()
   

if __name__ == '__main__':
    graph = Graph('San Francisco, California, United States')
    _, path = graph.get_shortest_path_between_two_points((37.733795, -122.446747), (37.76521245036753, -122.46308098483024))
    visualize_route(graph, path, {'building': True})
