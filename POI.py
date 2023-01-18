from shapely.geometry import shape, Point, Polygon
from haversine import haversine
import pandas as pd


class PointOfInterest:
    def __init__(self,name, type, lat=None, lon=None, geojson=None, cat=None):
        self.lat = lat
        self.lon = lon
        self.name = name
        if type == "Point":
            self.point = Point(lon, lat)
        elif type == "Shape":
            self.shape = Polygon(geojson[0][0])
        self.cat=cat

    def point_distance(self, lon_house, lat_house):
        point_house = Point(lon_house, lat_house)
        return self.point.distance(point_house)

    def shape_distance(self, house_lat,house_lon):
        # Create a Shapely Point object from the input longitude and latitude
        point = Point(house_lon, house_lat)
        # Find the point on the shape's boundary closest to the input point
        nearest_point = self.shape.boundary.interpolate(self.shape.boundary.project(point))
        # Use the haversine library to calculate the distance between the input point and the closest point on the shape
        return haversine((point.y, point.x), (nearest_point.y, nearest_point.x))


class SubwayEntrance(PointOfInterest):
    pass


# stations = pd.read_csv("NYC_Transit_Subway_Entrance_And_Exit_Data.csv")
# locations = stations[["Station Name","Entrance Latitude","Entrance Longitude"]]
#
# station_Objs = []
#
# for i in locations.iterrows():
#     station_Objs.append(SubwayEntrance(i[1][1],i[1][2],i[1][0]))
#
# time_square = PointOfInterest(lat=40.758896, lon=-73.985130, name="TimeSquare")
