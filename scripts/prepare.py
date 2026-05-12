#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[4]:


# function to load a specific dataset
def load_csv(month):
    return pd.read_csv(f"../raw_data/{month}-divvy-tripdata/{month}-divvy-tripdata.csv")


# In[5]:


# function to return the number of rows of a dataset
def calculate_no_rows(df):
    return len(df)


# In[6]:


# function to return the columns of a dataset
def get_columns(df):
    return df.columns


# In[7]:


# function to assess if all datasets have the same columns
def check_columns(months):
    # Define the reference for the columns based on the first dataset
    columns = get_columns(load_csv(months[0]))
    # Iterate over the remaining datasets and get the columns
    for month in months[1:]:
        df_columns_list = get_columns(load_csv(month))
        # Compare the columns of the dataset with the reference
        for x in range(len(df_columns_list)):
            if df_columns_list[x] != columns[x]:
                break
                return f"Columns in {month} are different from the reference"
    return f"All datasets have the same columns"



# In[8]:


# function to check if the 'ride_id' column has null values
def check_ride_id(df):
    if len(df) == df['ride_id'].count():
        return "No null values for 'ride_id'."
    return "'ride_id' presents null values!"


# In[9]:


# function to check if there are duplicates in 'ride_id'
def check_unique_ride_id(df):
    if len(df) == len(df['ride_id'].unique()):
        return "No duplicates."
    return "There are duplicates!"


# In[10]:


# function to check if the 'member_casual' column has null values
def check_member_casual(df):
    if len(df) == df['member_casual'].count():
        return "No null values for 'member_casual'."
    return "'member_casual' presents null values!"


# In[11]:


# function to check if the 'started_at' column has null values
def check_started_at(df):
    if len(df) == df['started_at'].count():
        return "No null values for 'started_at'."
    return "'started_at' presents null values!"


# In[12]:


# function to check if the 'ended_at' column has null values
def check_ended_at(df):
    if len(df) == df['ended_at'].count():
        return "No null values for 'ended_at'."
    return "'ended_at' presents null values!"


# In[13]:


# function to calculate the number of rows with null values
def calculate_null_values(month):
    df = load_csv(month)
    return f"Total rows: {len(df)} | Rows without null: {len(df.dropna())} | Rows with null: {len(df) - len(df.dropna())} | % null: {((len(df) - len(df.dropna()))/len(df))*100:.2f}"


# In[14]:


# function to remove rows with null values from the dataset
def remove_nulls(month):
    df = load_csv(month)
    return df.dropna()


# In[15]:


# Print the column names
print(load_csv(months[0]).info())


# In[17]:


# Print the number of rows for each data file
for month in months:
    print(f"Data file '{month}' -> {calculate_no_rows(load_csv(month))} rows.")


# In[18]:


# Check if all datasets have the same columns
print(check_columns(months))


# In[19]:


# Check if there are null values in the 'ride_id' column for all datasets
for month in months:
    print(f"Month: {month}")
    print(check_ride_id(load_csv(month)))
    print("----------------")


# In[20]:


# Check if there are null values in the 'member_casual' column for all datasets
for month in months:
    print(f"Month: {month}")
    print(check_member_casual(load_csv(month)))
    print("----------------")


# In[21]:


# Check if there are duplicate values in the 'ride_id' column for all datasets
for month in months:
    print(f"Month: {month}")
    print(check_unique_ride_id(load_csv(month)))
    print("----------------")


# In[22]:


# Check unique values for the 'member_casual' column
for month in months:
    print(f"Month: {month}")
    print(load_csv(month)['member_casual'].unique())
    print("------------------")


# In[23]:


# Check if there are null values in the 'started_at' column
for month in months:
    print(f"Month: {month}")
    print(check_started_at(load_csv(month)))
    print("----------------")


# In[24]:


# Check if there are null values in the 'ended_at' column
for month in months:
    print(f"Month: {month}")
    print(check_ended_at(load_csv(month)))
    print("----------------")


# In[25]:


# Check number of rows with null values for all datasets
for month in months:
    print(f"Month: {month}")
    print(calculate_null_values(month))
    print("-------------------------")


# In[27]:


# Removal of rows with null values for all datasets
for month in months:
    df = remove_nulls(month)
    df.to_csv(f"../cleaned_data/20260510-no_nulls/{month}_no_nulls.csv", index=False)
    print(f"{month} .csv file created!")

