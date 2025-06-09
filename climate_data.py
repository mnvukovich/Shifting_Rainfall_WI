import pandas as pd


def load_data(file_path):

    df = pd.read_csv(file_path) 
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.dropna(subset=['PRCP'])

    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month

    df['SEASON'] = df["DATE"].dt.month.apply(get_season)

    return df
    
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'