## AAE 718 
## Project 3
## Madeline Vukovich

# Cleaning Data
import pandas as pd
df = pd.read_csv(r"C:\AAE 718\Data Files\Project3 Data.csv")
df['DATE'] = pd.to_datetime(df['DATE'])
df_clean = df.dropna(subset=['PRCP'])


df_clean['YEAR'] = df_clean['DATE'].dt.year
df_clean['MONTH'] = df_clean['DATE'].dt.month

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'

df_clean['SEASON'] = df_clean['MONTH'].apply(get_season)

# Aggregate monthly rainfall totals
monthly_totals = df_clean.groupby(['STATION', 'NAME', 'YEAR', 'MONTH'])['PRCP'].sum().reset_index()

# Aggregate seasonal rainfall totals
seasonal_totals = df_clean.groupby(['STATION', 'NAME', 'YEAR', 'SEASON'])['PRCP'].sum().reset_index()


df_clean = df.dropna(subset=['PRCP']).copy()

df_clean['DATE'] = pd.to_datetime(df_clean['DATE'])
df_clean['YEAR'] = df_clean['DATE'].dt.year
df_clean['MONTH'] = df_clean['DATE'].dt.month
df_clean['SEASON'] = df_clean['MONTH'].apply(get_season)


# Graph 1
county_seasonal_avg = seasonal_totals.groupby(['YEAR', 'SEASON'])['PRCP'].mean().reset_index()
county_seasonal_avg = county_seasonal_avg[county_seasonal_avg['YEAR'] < 2025]

os.makedirs("images", exist_ok=True)

pivot_table_avg = county_seasonal_avg.pivot(index='YEAR', columns='SEASON', values='PRCP').fillna(0)
pivot_table_avg = pivot_table_avg[['Winter', 'Spring', 'Summer', 'Fall']]  # Order seasons

pivot_table_avg.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='Set2')
plt.title("Average Seasonal Rainfall in Waukesha County (All Stations, Excluding 2025)")
plt.xlabel("Year")
plt.ylabel("Avg. Precipitation per Station (inches)")
plt.legend(title="Season")
plt.tight_layout()


# Graph 2
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")
sns.lineplot(data=county_seasonal_avg, x='YEAR', y='PRCP', hue='SEASON')
plt.title("Average Seasonal Precipitation Trends – Waukesha County (Excluding 2025)")
plt.xlabel("Year")
plt.ylabel("Avg. Precipitation per Station (inches)")
plt.legend(title='Season')
plt.tight_layout()


# Aggregating monthly averages
monthly_avg = monthly_totals.groupby(['YEAR', 'MONTH'])['PRCP'].mean().reset_index()
monthly_avg = monthly_avg[monthly_avg['YEAR'] < 2025]

peak_months = monthly_avg.loc[monthly_avg.groupby('YEAR')['PRCP'].idxmax()].reset_index(drop=True)


# Graph 3
plt.figure(figsize=(12, 6))
sns.boxplot(data=monthly_avg, x='MONTH', y='PRCP')
plt.title("Monthly Rainfall Distribution (1980–2024) – Waukesha County")
plt.xlabel("Month")
plt.ylabel("Precipitation (inches)")
plt.tight_layout()


# Graph 4
plt.figure(figsize=(10, 5))
sns.set(style="whitegrid")

sns.regplot(data=peak_months, x='YEAR', y='MONTH', scatter_kws={'s': 60}, line_kws={'color': 'red'})

plt.title("Trend in Peak Rainfall Month by Year – Waukesha County")
plt.xlabel("Year")
plt.ylabel("Peak Rainfall Month (1 = Jan, ..., 12 = Dec)")
plt.yticks(range(1, 13))
plt.grid(True)
plt.tight_layout()


# Graph 5
peak_months['YEAR_BIN'] = pd.cut(
    peak_months['YEAR'],
    bins=range(peak_months['YEAR'].min(), peak_months['YEAR'].max() + 3, 3),
    right=False,
    labels=[f"{y}-{y+2}" for y in range(peak_months['YEAR'].min(), peak_months['YEAR'].max(), 3)]
)

plt.figure(figsize=(10, 6))
sns.histplot(data=peak_months, x='MONTH', hue='YEAR_BIN', multiple='dodge', binwidth=1, palette='rocket_r')
plt.title("Distribution of Peak Rainfall Months by 3-Year Periods")
plt.xlabel("Peak Rainfall Month (1 = Jan, ..., 12 = Dec)")
plt.ylabel("Count of Years")
plt.xticks(range(1, 13))
plt.yticks(range(0,3))
plt.tight_layout()
