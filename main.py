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



#os.makedirs("images", exist_ok=True) # But your directory is Images...

pivot_table_avg = county_seasonal_avg.pivot(index='YEAR', columns='SEASON', values='PRCP').fillna(0)
pivot_table_avg = pivot_table_avg[['Winter', 'Spring', 'Summer', 'Fall']]  # Order seasons

pivot_table_avg.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='Set2')
plt.title("Average Seasonal Rainfall in Waukesha County (All Stations, Excluding 2025)")
plt.xlabel("Year")
plt.ylabel("Avg. Precipitation per Station (inches)")
plt.legend(title="Season") # Should be able to relocate the legend here too
plt.tight_layout()

plt.savefig("Images/AHHHHHHHHH.png", dpi=300)  # Save the figure with high resolution

# %%
