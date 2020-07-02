### Load Packages
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import import_ipynb

#cd Projects/ian_scarff/Covid19Project

### Generate data.
import Data_Preprocessing


### Load Datasets
countyData = pd.read_csv("data/countyData.csv", dtype = "str")
stateData = pd.read_csv("data/stateData.csv", dtype = "str")
usaData = pd.read_csv("data/usaData.csv", dtype = "str")

import json
counties = open("data/geojson-counties-fips.json",)
counties = json.load(counties)


### Convert data types

countyData = countyData.astype({"Date" : "datetime64",
                                "Total Cases" : "int64",
                                "Total Deaths" : "int64",
                                "Population" : "int64",
                                "New Cases" : "int64",
                                "New Deaths" : "int64",
                                "%Cases" : "float64",
                                "%Deaths" : "float64", 
                                "log(Total Cases)" : "float64",
                                "log(Total Deaths)" : "float64",
                                "log(New Cases)" : "float64", 
                                "log(New Deaths)" : "float64",
                                "%Retail/Rec Change" : "float64",
                                "%Grocery/Pharm Change" : "float64",
                                "%Parks Change" : "float64",
                                "%Transit Change" : "float64",
                                "%Workplace Change" : "float64",
                                "%Residential Change" : "float64"})

stateData = stateData.astype({"Date" : "datetime64",
                              "Total Cases" : "int64",
                              "Total Deaths" : "int64",
                              "Population" : "int64",
                              "New Cases" : "int64",
                              "New Deaths" : "int64",
                              "%Cases" : "float64",
                              "%Deaths" : "float64", 
                              "log(Total Cases)" : "float64",
                              "log(Total Deaths)" : "float64",
                              "log(New Cases)" : "float64", 
                              "log(New Deaths)" : "float64",
                              "%Retail/Rec Change" : "float64",
                              "%Grocery/Pharm Change" : "float64",
                              "%Parks Change" : "float64",
                              "%Transit Change" : "float64",
                              "%Workplace Change" : "float64",
                              "%Residential Change" : "float64"})

usaData = usaData.astype({"Date" : "datetime64",
                          "Total Cases" : "int64",
                          "Total Deaths" : "int64",
                          "Population" : "int64",
                          "New Cases" : "int64",
                          "New Deaths" : "int64",
                          "%Cases" : "float64",
                          "%Deaths" : "float64", 
                          "log(Total Cases)" : "float64",
                          "log(Total Deaths)" : "float64",
                          "log(New Cases)" : "float64", 
                          "log(New Deaths)" : "float64",
                          "%Retail/Rec Change" : "float64",
                          "%Grocery/Pharm Change" : "float64",
                          "%Parks Change" : "float64",
                          "%Transit Change" : "float64",
                          "%Workplace Change" : "float64",
                          "%Residential Change" : "float64"})






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    html.H1("Covid-19 & Mobility Dashboard", style = {'text-align' : 'center'})
    
      
])

if __name__ == '__main__':
    app.run_server(debug=True, port=2346, host='10.26.105.230')
