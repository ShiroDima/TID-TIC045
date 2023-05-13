import geopandas as gpd


class Datasets:
    def __init__(self) -> None:

        # Loading all the datasets
        self.power_plants = gpd.read_file("../../data/power_plants.csv",
                                    GEOM_POSSIBLE_NAMES='geom',
                                    KEEP_GEOM_COLUMNS='NO')

        self.power_plants_2 = gpd.read_file(
            '../../data/NGA_PowerPlants/NGA_PowerPlants.shp')

        self.state_boundaries = gpd.read_file('../../data/nigeria_state_boundaries.csv',
                                        GEOM_POSSIBLE_NAMES='geom',
                                        KEEP_GEOM_COLUMNS='NO')

        self.transmission_substations = gpd.read_file('../../data/all_transmission_substations.csv',
                                                GEOM_POSSIBLE_NAMES='geom',
                                                KEEP_GEOM_COLUMNS='NO')

        self.grid = gpd.read_file('../../data/modelled_grid_original.csv',
                            GEOM_POSSIBLE_NAMES='geom',
                            KEEP_GEOM_COLUMNS='NO')
        
        # self.convert_to_crs_types()
    
    def convert_to_crs_types(self) -> None:
        # power_plants
        self.power_plants.set_crs("EPSG:3857", inplace=True)
        self.power_plants.to_crs("EPSG:4326", inplace=True)
        self.power_plants = self.power_plants.dropna()

        # power_plants_2
        self.power_plants_2.set_crs('EPSG:4326',inplace=True)

        # state_boundaries
        self.state_boundaries.set_crs("EPSG:3857",inplace=True)
        self.state_boundaries.to_crs("EPSG:4326",inplace=True)
        self.state_boundaries['center'] = self.state_boundaries.geometry.centroid

        # transmission_substations
        self.transmission_substations.set_crs("EPSG:3857",inplace=True)
        self.transmission_substations.to_crs("EPSG:4326",inplace=True)

        # grid
        self.grid.set_crs("EPSG:3857",inplace=True)
        self.grid.to_crs("EPSG:4326",inplace=True)
