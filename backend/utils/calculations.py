import pandas as pd
import pyproj
from shapely.geometry import Point

from .get_data import Datasets
from .coordinate_getter import get_coordinates

data = Datasets()


def distance_calculator(longitude, latitude, n_closest):
    """
    This function calculates the distance between any given location and all power plants and transmission substation and returns the n_closest locations
    """

    power_plants_2 = data.power_plants_2.set_crs('EPSG:4326')
    power_plants_2 = power_plants_2.to_crs('EPSG:3857')
    # Creating a shapely point geometry for the given location
    location = Point(longitude, latitude)

    # I converted the crs of the input
    # Create a transformer object to transform from EPSG:4326 to EPSG:32645
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32645")

    location = Point(transformer.transform(location.x, location.y))

    # The power plants locations come in two different datasets with no direct field to concat on.
    # This first half calculates the distance between the given location and the plants on the first dataset and creates a dataframe to hold the information
    distance = list(data.power_plants.geometry.distance(location))
    plant_distance = pd.DataFrame({'power_plant': list(data.power_plants['description']), 'distance': distance})

    # Repeats the process for the second dataframe then concat the two dataframes
    distance_2 = list(power_plants_2.geometry.distance(location))
    plant_distance_2 = pd.DataFrame({'power_plant': list(power_plants_2['PLANT']), 'distance': distance_2})
    plant_distance = pd.concat([plant_distance, plant_distance_2])
    plant_distance.drop_duplicates('power_plant', inplace=True)

    # sorts the distances and returns the requested amount
    plant_distance = plant_distance.sort_values('distance', ascending=True)

    # Repeating for the transmission substations
    distance = list(data.transmission_substations.geometry.distance(location))
    transmission_substations_distance = pd.DataFrame({'transmission_substation': list(data.transmission_substations['FID']),
                                                      'osm_id': list(data.transmission_substations['osm_id']),
                                                      'distance': distance})
    transmission_substations_distance = transmission_substations_distance.sort_values('distance')

    return plant_distance.head(n_closest), transmission_substations_distance.head(n_closest)


# print(distance_calculator(7.5000, 5.20000, 5))


def viability_score(location: str) -> float:
    """
        This function calculates the score for a particular region. This score is an indicator of the potential of a region
        as a good place for solar power intervention.
    """
    weight_ghi = 0.4
    weight_distance = 0.4
    weight_electricity = 0.2

    latitude, longitude = get_coordinates(location)

    location = Point(longitude, latitude)
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32645")
    location = Point(transformer.transform(location.x, location.y))

    # I've not normalized the distance
    # distance = list(transmission_substations.geometry.distance(location))
    distance = list(data.solar_viability.geometry.distance(location))
    distance = min(distance)

    for _, row in data.solar_viability.iterrows():
        if row.geometry.contains(location):
            ghi = row.ghi_normalized
            electricity = row.electricity_normalized
            score = (weight_ghi * ghi) + (weight_distance * distance) + (weight_electricity * electricity)
            return score

