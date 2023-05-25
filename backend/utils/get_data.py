import geopandas as gpd
import pandas as pd

# get path of data folder
from pathlib import Path
parent_path = str( Path(__file__).parent.absolute() )

data_folder_path = parent_path + "/../../data"
# --------------------------------------------


class Datasets:
    def __init__(self) -> None:
        # Loading all the datasets
        self.power_plants = gpd.read_file(f"{data_folder_path}/power_plants.csv",
                                          GEOM_POSSIBLE_NAMES='geom',
                                          KEEP_GEOM_COLUMNS='NO')

        self.power_plants_2 = gpd.read_file(
            f'{data_folder_path}/NGA_PowerPlants/NGA_PowerPlants.shp')

        self.state_boundaries = gpd.read_file(f'{data_folder_path}/nigeria_state_boundaries.csv',
                                              GEOM_POSSIBLE_NAMES='geom',
                                              KEEP_GEOM_COLUMNS='NO')

        self.transmission_substations = gpd.read_file(f'{data_folder_path}/all_transmission_substations.csv',
                                                      GEOM_POSSIBLE_NAMES='geom',
                                                      KEEP_GEOM_COLUMNS='NO')

        self.grid = gpd.read_file(f'{data_folder_path}/modelled_grid_original.csv',
                                  GEOM_POSSIBLE_NAMES='geom',
                                  KEEP_GEOM_COLUMNS='NO')

        self.irradiance = self.get_ghi_data()

        self.electricity = self.get_electricity_data()

        self.solar_viability = self._get_solar_viability_data()
        # self.convert_to_crs_types()

    # def convert_to_crs_types(self) -> None:
    #     # power_plants
    #     self.power_plants.set_crs("EPSG:3857", inplace=True)
    #     self.power_plants.to_crs("EPSG:4326", inplace=True)
    #     self.power_plants = self.power_plants.dropna()
    #
    #     # power_plants_2
    #     self.power_plants_2.set_crs('EPSG:4326',inplace=True)
    #
    #     # state_boundaries
    #     self.state_boundaries.set_crs("EPSG:3857",inplace=True)
    #     self.state_boundaries.to_crs("EPSG:4326",inplace=True)
    #     self.state_boundaries['center'] = self.state_boundaries.geometry.centroid
    #
    #     # transmission_substations
    #     self.transmission_substations.set_crs("EPSG:3857",inplace=True)
    #     self.transmission_substations.to_crs("EPSG:4326",inplace=True)
    #
    #     # grid
    #     self.grid.set_crs("EPSG:3857",inplace=True)
    #     self.grid.to_crs("EPSG:4326",inplace=True)

    def get_ghi_data(self):
        solcast_index = pd.read_csv(f"{data_folder_path}/Solcast/Solcast/solcast_index.csv")

        state_boundaries = gpd.read_file(f'{data_folder_path}/nigeria_state_boundaries.csv', GEOM_POSSIBLE_NAMES='geom',
                                         KEEP_GEOM_COLUMNS='NO')

        # literally cut and join. Will be revised later.

        # Applies the function across all states dataset and appends the result to the empty list
        irradiance_list = []
        with open(f'{data_folder_path}/links.txt', 'r') as links:
            filepaths = links.read().split('\n')
        for index, link in enumerate(filepaths):
            state = solcast_index.loc[index, 'State']
            irradiance_list.append(self._get_irradiance(state,
                                                        link.replace("/content/drive/MyDrive/TID_Innovation/Data",
                                                                     f"{data_folder_path}/Solcast")))

        # Creates_DataFrame
        Ghi = [item[0] for item in irradiance_list]
        GtiFixedTilt = [item[1] for item in irradiance_list]
        GtiTracking = [item[2] for item in irradiance_list]
        state = list(solcast_index.State)
        df_dict = {'state': state, 'ghi': Ghi, 'gtifixed': GtiFixedTilt, 'gtitracking': GtiTracking}
        avg_daily_irradiance_2022 = pd.DataFrame(df_dict)

        # Merges the irradiance data to the state_map Data
        state_irradiance = state_boundaries.merge(avg_daily_irradiance_2022, left_on='adm1_en', right_on='state')

        return state_irradiance

    @staticmethod
    def _get_irradiance(state, csv_path):
        """
            This function reads in, cleans and calculates the relevant data from given files
        """
        # Reading_csv
        state = pd.read_csv(csv_path)
        # Retrieving_the_date_from_the_PeriodStart_column
        state[['date', 'start_time']] = state['PeriodStart'].str.split('T', expand=True)
        # Converting the hourly irradiance data to daily irradiance data(Wh/day/m2)                                          
        daily_irradiance = state.groupby('date').sum()[['Ghi', 'GtiFixedTilt', 'GtiTracking']]
        # calculates and returns the average daily irradiance data for the year 2022. It also converts it from W to KW                               
        return list(round(daily_irradiance.mean() / 1000, 2))

    @staticmethod
    def get_electricity_data():
        file = f"{data_folder_path}/Nigeria Electricity Data.xlsx"
        df_2021 = pd.read_excel(file, sheet_name="2021 MIS").set_index("State").drop(columns=["Country", "Survey"])
        df_2018 = pd.read_excel(file, sheet_name="2018 DHS").set_index("State").drop(columns=["Country", "Survey"])
        df_2015 = pd.read_excel(file, sheet_name="2015 MIS").set_index("State").drop(columns=["Country", "Survey"])
        df_2013 = pd.read_excel(file, sheet_name="2013 DHS").set_index("State").drop(columns=["Country", "Survey"])

        # drop 'household with electricity column for all dataframes
        pop_2021 = df_2021.drop(columns="Households with electricity")
        pop_2018 = df_2018.drop(columns="Households with electricity")
        pop_2015 = df_2015.drop(columns="Households with electricity")
        pop_2013 = df_2013.drop(columns="Households with electricity")

        # merge the dataframes into one
        pop_df = pd.merge(pop_2013, pop_2015, on='State', suffixes=(' (2013)', ' (2015)'))
        pop_df = pd.merge(pop_df, pop_2018, on='State')
        pop_df = pd.merge(pop_df, pop_2021, on='State', suffixes=(' (2018)', ' (2021)'))
        pop_df.columns = ["2013", "2015", "2018", "2021"]

        return pop_df

    def _get_solar_viability_data(self) -> pd.DataFrame:
        """
        This function reads in and prepares the solar viability dataframe.
        """
        solar_viability_data = gpd.read_file(f'{data_folder_path}/solar_viability_data.csv',
                                             GEOM_POSSIBLE_NAMES='geometry',
                                             KEEP_GEOM_COLUMNS='NO')

        solar_viability_data.ghi = solar_viability_data.ghi.astype('float')
        solar_viability_data.percent_electricity = solar_viability_data.percent_electricity.astype('float')

        solar_viability_data['ghi_normalized'] = (solar_viability_data.ghi - solar_viability_data.ghi.min()) / (
                solar_viability_data.ghi.max() - solar_viability_data.ghi.min())
        solar_viability_data['electricity_normalized'] = (
                                                                 solar_viability_data.percent_electricity - solar_viability_data.percent_electricity.min()) / \
                                                         (
                                                                     solar_viability_data.percent_electricity.max() - solar_viability_data.percent_electricity.min())

        return solar_viability_data
