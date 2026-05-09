import pandas as pd



def get_arrivals_df(group_arrivals: bool = False) -> pd.DataFrame:
    # Reading arrival data.
    df_arrivals = pd.read_csv('data/register_of_arrivals.csv')

    # Creating a column for the number of arrivals and reordering the DataFrame.
    df_arrivals['n'] = range(len(df_arrivals))
    df_arrivals = df_arrivals[['n', 'Arrival_Time']]

    # Converting the times to a stanadard a type (datetime).
    df_arrivals['Arrival_Time'] = pd.to_datetime(df_arrivals['Arrival_Time'], format='%H:%M:%S')

    # Creating a column for inter-arrival times.
    df_arrivals['Interval'] = df_arrivals['Arrival_Time'].diff()
    df_arrivals['Interval'] = df_arrivals['Interval'].dt.total_seconds()
    df_arrivals['Interval'] = df_arrivals['Interval'].fillna(0)

    # Converting the arrival time to date.time after using diff() on the interval.
    df_arrivals['Arrival_Time'] = df_arrivals['Arrival_Time'].dt.time

    # Removing the periods of bad internet connection.
    no_internet_flaws = df_arrivals['Interval'] < 50
    df_arrivals = df_arrivals[no_internet_flaws]

    # Isolating group arrivals.
    if group_arrivals:
        return df_arrivals[df_arrivals['Interval'] != 0]
    
    return df_arrivals


def get_service_time_df() -> pd.DataFrame:
    df = pd.read_csv('data/service_times.csv')
    return df


def get_heatmap_coordinates_df() -> pd.DataFrame:
    df = pd.read_csv('data/heatmap_positions.csv')
    return df


def get_occupancy_df() -> pd.DataFrame:
    df = pd.read_csv('data/occupancy.csv')
    return df