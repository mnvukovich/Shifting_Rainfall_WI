#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from climate_data import *
# %%

df = load_data(r"Data\Project3 Data.csv")

# Aggregate monthly rainfall totals
monthly_totals = df.groupby(['STATION', 'NAME', 'YEAR', 'MONTH'])['PRCP'].sum().reset_index()

# Aggregate seasonal rainfall totals
seasonal_totals = df.groupby(['STATION', 'NAME', 'YEAR', 'SEASON'])['PRCP'].sum().reset_index()



# %%

df
county_seasonal_avg = seasonal_totals.groupby(['YEAR', 'SEASON'])['PRCP'].mean().reset_index()
county_seasonal_avg = county_seasonal_avg[county_seasonal_avg['YEAR'] < 2025]


# %%
