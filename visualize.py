import geopandas as gpd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    nybb = gpd.read_file(gpd.datasets.get_path('nybb'))
    gpd.GeoSeries(nybb.geometry).plot()
    plt.show()
