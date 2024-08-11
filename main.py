from typing import Union

from fastapi import FastAPI
import json
import pandas as pd
app = FastAPI()


def prepareData(col):
    
    key = col
    
    carbonDF = pd.read_csv('data/GCB2022v27_MtCO2_flat.csv')

    # Get the years 1940 - 2022
    years =  [x for x in range(1940, 2023)]

    # Filter out the dataset
    vals = carbonDF[carbonDF['Year'].isin(years)]

    # Init the dict
    year_dict = {}

    # Group by 'Year' and iterate over the groups
    for year, group in vals.groupby('Year'):
        top_100 = group.reset_index(drop=True).set_index('Country')   
        year_dict[year] = top_100[key].to_json()

    return year_dict

def returnData():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')

@app.get("/")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    res = df[df['Country'] == 'Philippines']['Cost of Living Index'].reset_index(drop=True)
    # print(df.head())
    return res.to_json()

@app.get("/carbon")
def read_carbon():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    res = df[df['Country'] == 'Philippines']['Cost of Living Index'].reset_index(drop=True)
    # print(df.head())
    return res.to_json()

@app.get("/coal")
def read_coal():
    return prepareData('Coal')


@app.get("/rent/{country}")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    # print(df.head())
    return df[df['Country' == 'Philippines']]['Cost of Living Index'].to_json()

@app.get("/grocery/{country}")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    # print(df.head())
    return df.to_json()

@app.get("/restaurant/{country}")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    # print(df.head())
    return df.to_json()

@app.get("/purchase/{country}")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    # print(df.head())
    return df.to_json()

@app.get("/living/{country}")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    res = df[df['Country'] == 'Philippines']['Cost of Living Index']
    # print(df.head())
    return res.to_json()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}