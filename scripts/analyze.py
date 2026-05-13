#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker

# List of months used in the analysis
months = [
    202505,
    202506,
    202507,
    202508,
    202509,
    202510,
    202511,
    202512,
    202601,
    202602,
    202603,
    202604
]

month_list = [
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
    "April"
]

# function to load the cleaned data files
def load_csv(month):
    return pd.read_csv(f"../cleaned_data/20260510-final/{month}_final.csv")

# function to compare both types of members
def compare_member_casual(df):
    return df.groupby('member_casual').size()

# function to compare the usage of both types of bikes
def compare_bike_usage(df):
    return df.groupby('rideable_type').size()

# function to compare both types of bikes grouped by membsership
def compare_bike_usage_by_membership(df):
    return df.groupby(['member_casual', 'rideable_type']).size()

# function to compare ride durations
def compare_ride_duration(df):
    df['ride_duration'] = pd.to_timedelta(df['ride_duration'])
    return df['ride_duration'].agg(['min', 'median', 'mean', 'max'])

# function to compare ride durations between membership
def compare_ride_duration_by_membership(df):
    df['ride_duration'] = pd.to_timedelta(df['ride_duration'])
    return df.groupby('member_casual')['ride_duration'].agg(['median', 'mean'])

# function to compare bike usage by weekday
def compare_bike_usage_by_weekday(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['weekday'] = pd.Categorical(df['weekday'], categories=order, ordered=True)
    return df.groupby('weekday').size()

# function to compare bike usage by weekday and membership
def compare_bike_usage_by_weekday_and_membership(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df['weekday'] = pd.Categorical(df['weekday'], categories=order, ordered=True)
    return df.groupby(['member_casual', 'weekday']).size()

# Check seasonal differences in rides
for month in months:
    print(f"Month: {month}")
    df = load_csv(month)
    print(f"Total no rides: {len(df)}")
    print("------------------------------------------------------------")    

results = {}
index = 0

for month in months:
    df = load_csv(month)
    results[month_list[index]] = len(df)
    index += 1

plot_df = pd.DataFrame(results, index=['Total Rides']).T

fig, ax = plt.subplots(figsize=(10, 6))

plot_df.plot(kind='bar', ax=ax, width=0.8, legend=False)

ax.set_title('Seasonal ride variation', fontsize=14)
ax.set_ylabel('Number of Rides', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation.png")
plt.show()

# Check differences between bike types and membership
for month in months:
    print(f"Month: {month}")
    df = load_csv(month)
    print(f"Member vs. Casual: {compare_member_casual(df)}")
    print(f"Classic vs. Electric: {compare_bike_usage(df)}")
    print(f"Membership & Bike Type: {compare_bike_usage_by_membership(df)}")
    print("-------------------------------------------------------------")

results = {}
index = 0

for month in months:
    df = load_csv(month)
    results[month_list[index]] = compare_member_casual(df)
    index += 1

plot_df = pd.DataFrame(results).T

fig, ax = plt.subplots(figsize=(10, 6))

plot_df.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Member vs. Casual rides seasonal variation', fontsize=14)
ax.set_ylabel('Number of Rides', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Membership')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation_member_vs_casual.png")
plt.show()

results = {}
index = 0

for month in months:
    df = load_csv(month)
    results[month_list[index]] = compare_bike_usage(df)
    index += 1

plot_df = pd.DataFrame(results).T

fig, ax = plt.subplots(figsize=(10, 6))

plot_df.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Classic vs. Electric rides seasonal variation', fontsize=14)
ax.set_ylabel('Number of Rides', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Bike Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation_classic_vs_electric.png")
plt.show()

results = {}
index = 0

for month in months:
    df = load_csv(month)
    results[month_list[index]] = compare_bike_usage_by_membership(df)
    index += 1

plot_df = pd.DataFrame(results).T
plot_df_casual = plot_df['casual']
plot_df_member = plot_df['member']

fig, ax = plt.subplots(figsize=(10, 6))

plot_df_casual.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Casual rides seasonal variation', fontsize=14)
ax.set_ylabel('Number of Rides', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Casual')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation_casual.png")
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))

plot_df_member.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Member rides seasonal variation', fontsize=14)
ax.set_ylabel('Number of Rides', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Member')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation_member.png")
plt.show()

# Check seasonal differences in ride duration
for month in months:
    print(f"Month: {month}")
    df = load_csv(month)
    print(f"Ride duration:\n{compare_ride_duration(df)}")
    print("------------------------------------------------------------")

# Check seasonal differences in ride duration by membership
for month in months:
    print(f"Month: {month}")
    df = load_csv(month)
    print(f"Ride duration:\n{compare_ride_duration_by_membership(df)}")
    print("------------------------------------------------------------")

results = {}
index = 0
for month in months:
    df = load_csv(month)
    df['ride_duration'] = pd.to_timedelta(df['ride_duration'])/pd.Timedelta(minutes=1)
    results[month_list[index]] = df.groupby('member_casual')['ride_duration'].agg('median')
    index += 1

plot_df = pd.DataFrame(results).T
plot_df
fig, ax = plt.subplots(figsize=(10, 6))

plot_df.plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Casual vs. Member median rides duration', fontsize=14)
ax.set_ylabel('Ride Duration', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Membership')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_duration_variation_casual_vs_member_median.png")
plt.show()

# Check seasonal differences among weekdays
for month in months:
    print(f"Month: {month}")
    df = load_csv(month)
    print(f"{compare_bike_usage_by_weekday(df)}")
    print("------------------------------------------------------------")

# Check seasonal differences among weekdays and between membership
for month in months:
    print(f"Month: {month}")
    df = load_csv(month)
    print(f"{compare_bike_usage_by_weekday_and_membership(df)}")
    print("------------------------------------------------------------")

results = {}
index = 0

for month in months:
    df = load_csv(month)
    results[month_list[index]] = compare_bike_usage_by_weekday_and_membership(df)
    index += 1

plot_df = pd.DataFrame(results).T
plot_df_casual = plot_df['casual']
plot_df_member = plot_df['member']
plot_df_casual['workdays'] = plot_df_casual[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].sum(axis=1)/5
plot_df_casual['weekend'] = plot_df_casual[['Saturday', 'Sunday']].sum(axis=1)/2
plot_df_member['workdays'] = plot_df_member[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].sum(axis=1)/5
plot_df_member['weekend'] = plot_df_member[['Saturday', 'Sunday']].sum(axis=1)/2

fig, ax = plt.subplots(figsize=(10, 6))

plot_df_casual[['workdays', 'weekend']].plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Workdays vs. Weekend Casual rides', fontsize=14)
ax.set_ylabel('Average Rides by Day', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Casual')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation_workdays_vs_weekend_casual.png")
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))

plot_df_member[['workdays', 'weekend']].plot(kind='bar', ax=ax, width=0.8)

ax.set_title('Workdays vs. Weekend Member rides', fontsize=14)
ax.set_ylabel('Average Rides by Day', fontsize=12)
ax.set_xlabel('Month', fontsize=12)
ax.legend(title='Member')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../plots/seasonal_ride_variation_workdays_vs_weekend_member.png")
plt.show()

# Comparison between Membership and Casual riders starting points in August (summer reference)
df = load_csv(months[3])
mask = df['member_casual'] == 'member'
results = df[mask].groupby(['start_lng', 'start_lat']).size().reset_index(name='count')
plot_df = pd.DataFrame(results)
plt.figure(figsize=(6, 6))
plt.scatter(plot_df['start_lng'], plot_df['start_lat'], alpha=0.3, s=plot_df['count'] * 0.05, color='blue')
plt.title('Start station frequency: Membership - August')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("../plots/start_station_freq_member_august.png")
plt.show()

df = load_csv(months[3])
mask = df['member_casual'] == 'casual'
results = df[mask].groupby(['start_lng', 'start_lat']).size().reset_index(name='count')
plot_df = pd.DataFrame(results)
plt.figure(figsize=(6, 6))
plt.scatter(plot_df['start_lng'], plot_df['start_lat'], alpha=0.3, s=plot_df['count'] * 0.05, color='red')
plt.title('Start station frequency: Casual - August')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("../plots/start_station_freq_casual_august.png")
plt.show()

# Comparison between Membership and Casual riders starting points in January (winter reference)
df = load_csv(months[8])
mask = df['member_casual'] == 'member'
results = df[mask].groupby(['start_lng', 'start_lat']).size().reset_index(name='count')
plot_df = pd.DataFrame(results)
plt.figure(figsize=(6, 6))
plt.scatter(plot_df['start_lng'], plot_df['start_lat'], alpha=0.3, s=plot_df['count'] * 0.05, color='blue')
plt.title('Start station frequency: Membership - January')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("../plots/start_station_freq_member_january.png")
plt.show()

df = load_csv(months[8])
mask = df['member_casual'] == 'casual'
results = df[mask].groupby(['start_lng', 'start_lat']).size().reset_index(name='count')
plot_df = pd.DataFrame(results)
plt.figure(figsize=(6, 6))
plt.scatter(plot_df['start_lng'], plot_df['start_lat'], alpha=0.3, s=plot_df['count'] * 0.05, color='red')
plt.title('Start station frequency: Casual - January')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.1))
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("../plots/start_station_freq_casual_january.png")
plt.show()