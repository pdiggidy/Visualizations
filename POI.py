from math import radians, cos, sin, asin, sqrt


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


time_square = PointOfInterest(lat=40.758896, lon=-73.985130, name="TimeSquare")
