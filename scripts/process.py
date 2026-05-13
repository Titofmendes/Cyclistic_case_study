#!/usr/bin/env python
# coding: utf-8

import pandas as pd

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

# function to load a specific dataset
def load_csv(month):
    return pd.read_csv(f"../cleaned_data/20260510-no_nulls/{month}_no_nulls.csv")

# function to convert the 'started_at' and 'ended_at' columns into datetime
def convert_to_datetime(df):
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    return df

# function to calculate the weekday
def calculate_weekday(df):
    df['weekday'] = df['started_at'].dt.day_name()
    return df

# function to calculate the ride duration
def calculate_ride_duration(month):
    df = load_csv(month)
    df = convert_to_datetime(df)
    df['ride_duration'] = df['ended_at'] - df['started_at']
    df = calculate_weekday(df)
    return df

# function to check if ride duration has negative values
def check_ride_duration(month):
    df = calculate_ride_duration(month)
    mask = df['ride_duration'] <= pd.Timedelta(0)
    if len(df[mask]) > 0:
        return f"There are {len(df[mask])} rows with zero or negative values."
    return "There are no zero or negative values."

# function to remove the rows with zero or negative values for the 'ride_duration' column
def remove_negative_ride_durations(month):
    df = calculate_ride_duration(month)
    mask = df['ride_duration'] > pd.Timedelta(0)
    return df[mask]    

# function to load cleaned datasets
def load_clean_csv(month):
    return pd.read_csv(f"../cleaned_data/20260510-no_negative_ride_durations/{month}_no_negative_ride_durations.csv")

# function to check if there are incorrectly registered datetimes
def check_datetime(month, start=True):
    df = load_clean_csv(month)
    df = convert_to_datetime(df)
    year = int(str(month)[:4])
    mon = int(str(month)[-2:])
    if start:
        mask_start = (df['started_at'].dt.year == year) & (df['started_at'].dt.month == mon)
        df = df[~mask_start]
        mask_end = (df['ended_at'].dt.year == year) & (df['ended_at'].dt.month == mon)
        return df[~mask_end]
    else:
        mask = (df['ended_at'].dt.year == year) & (df['ended_at'].dt.month == mon)
        return df[~mask]

# Check if there are zero or negative values for the 'ride_duration' column for all datasets
for month in months:
    print(f"Month: {month}")
    print(check_ride_duration(month))
    print("----------------------------------------")

# Create new data files with converted datetimes and added 'ride_duration' and 'weekday' columns
for month in months:
    df = calculate_ride_duration(month)
    df.to_csv(f"../cleaned_data/20260510-ride_durations/{month}_ride_durations.csv", index=False)
    print(f"{month} csv file created!")

# Create new data files with converted datetimes, 'ride_duration' and 'weekday' columns, and removed rows with zero or negative ride durations
for month in months:
    df = remove_negative_ride_durations(month)
    df.to_csv(f"../cleaned_data/20260510-no_negative_ride_durations/{month}_no_negative_ride_durations.csv", index=False)
    print(f"{month} csv file created!")

# Check for incorrectly defined datetime values for the 'started_at' column
for month in months:
    print(f"Month: {month}")
    print(len(check_datetime(month, start=True)))
    print("----------------------------------------")

# Check for incorrectly defined datetime values for the 'ended_at' column
for month in months:
    print(f"Month: {month}")
    print(len(check_datetime(month, start=False)))
    print("----------------------------------------")

# Check the last dataset which presented 20 rows outside the defined time window
df = check_datetime(months[11], start=False)
df

# Perform the final cleaning
for month in months:
    df = load_clean_csv(month)
    if len(check_datetime(month, start=False)) > 0:
        mask = check_datetime(month, start=False)
        df.drop(mask.index).to_csv(f"../cleaned_data/20260510-final/{month}_final.csv", index=False)
    else:
        df.to_csv(f"../cleaned_data/20260510-final/{month}_final.csv", index=False)
    print(f"{month} .csv file created!")