from math import radians, cos, sin, asin, sqrt

import pandas as pd


class PointOfInterest:
    def __init__(self, lat, lon, name):
        self.lat = lat
        self.lat_rad = radians(lat)
        self.lon = lon
        self.lon_rad = radians(lon)
        self.name = name

    def calculate_distance(self, lat, lon):
        lat = radians(lat)
        lon = radians(lon)
        dlon = self.lon_rad - lon
        dlat = self.lat_rad - lat
        a = sin(dlat / 2) ** 2 + cos(self.lat_rad) * cos(lat) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers
        r = 6371
        # calculate the result
        return c * r


class SubwayEntrance(PointOfInterest):
    pass


stations = pd.read_csv("NYC_Transit_Subway_Entrance_And_Exit_Data.csv")
locations = stations[["Station Name","Entrance Latitude","Entrance Longitude"]]

station_Objs = []

for i in locations.iterrows():
    station_Objs.append(SubwayEntrance(i[1][1],i[1][2],i[1][0]))

time_square = PointOfInterest(lat=40.758896, lon=-73.985130, name="TimeSquare")

# import json
# from shapely.geometry import shape, Point
# from haversine import haversine
#
# def nearest_point_distance(point_lon, point_lat, geojson_shape):
#     # Create a Shapely Point object from the input longitude and latitude
#     point = Point(point_lon, point_lat)
#     # Load the GeoJSON shape and convert it to a Shapely shape object
#     shape_geom = shape(json.loads(geojson_shape))
#     # Find the point on the shape's boundary closest to the input point
#     nearest_point = shape_geom.boundary.interpolate(shape_geom.boundary.project(point))
#     # Use the haversine library to calculate the distance between the input point and the closest point on the shape
#     return haversine( (point.y, point.x), (nearest_point.y, nearest_point.x) )

# In the first line, we import the json library which will be used to parse the GeoJSON object.
# In the second line, we import two classes from the shapely library: shape and Point. we use the shape class to convert the GeoJSON object into a Shapely shape object and the Point class to create a Shapely Point object from the input longitude and latitude.
# In the third line, we import the haversine library. It will be used to calculate the distance between two coordinates in kilometers.
# In the function definition, we take three arguments, point_lon, point_lat and geojson_shape. point_lon and point_lat are the longitude and latitude of the point respectively and geojson_shape is the GeoJSON shape in string format.
# In the first line of the function, we create a Shapely Point object from the input longitude and latitude.
# In the second line, we parse the GeoJSON shape and convert it to a Shapely shape object.
# In the third line, we find the point on the shape's boundary closest to the input point using the boundary.interpolate and boundary.project methods.
# In the fourth line, we use the haversine library to calculate the distance between the input point and the closest point on the shape and return the result.
# Please note that this function is assuming that the GeoJson is in WGS84 (EPSG:4326) projection. If your GeoJson is in different projection you need to first project it to WGS84 then use this function.