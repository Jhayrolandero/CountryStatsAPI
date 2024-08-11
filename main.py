from typing import Union
from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import math

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

def prepareData(col):
    key = col
    carbonDF = pd.read_csv('data/clean_co2.csv')
    
    # Get the years 1940 - 2022
    years =  [x for x in range(1940, 2023)]

    # Filter out the dataset
    vals = carbonDF[carbonDF['Year'].isin(years)]

    # Init the dict
    year_dict = {}
    
    # Group by 'Year' and iterate over the groups
    for year, group in vals.loc[(vals['Country'] != 'Global') & (vals['Country'] != 'International Transport')].groupby('Year'):
        top_100 = group.reset_index(drop=True).set_index('Country')   
        year_dict[year] = {'Countries':[{'Country': x,key:y.item() if not math.isnan(y.item()) else 0} for x,y in zip(group['Country'].values,group[key].values)]}
        year_dict[year]['Max'] = top_100[key].max().item()
        year_dict[year]['Min'] = top_100[key].min().item()


    return year_dict

def returnData():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')

@app.get("/")
def read_root():
    df = pd.read_csv('data/Cost_of_Living_Index_by_Country_2024.csv')
    res = df[df['Country'] == 'Philippines']['Cost of Living Index'].reset_index(drop=True)
    # print(df.head())
    return res.to_json()

@app.get("/coal")
def read_coal():
    return prepareData('Coal')

@app.get("/oil")
def read_oil():
    return prepareData('Oil')

@app.get("/gas")
def read_gas():
    return prepareData('Gas')

@app.get("/cement")
def read_cement():
    return prepareData('Cement')

@app.get("/flaring")
def read_flaring():
    return prepareData('Flaring')

@app.get("/other")
def read_other():
    return prepareData('Other')




@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}