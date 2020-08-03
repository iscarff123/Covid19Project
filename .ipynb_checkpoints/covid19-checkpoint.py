### Load Packages
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
from dash.dependencies import Input, Output
import math


#cd Projects/ian_scarff/Covid19Project

### Generate data.
# import Data_Preprocessing


### Load Datasets
countyData = pd.read_csv("data/countyData.csv", dtype = "str") ### county level
stateData = pd.read_csv("data/stateData.csv", dtype = "str") ### state level
usaData = pd.read_csv("data/usaData.csv", dtype = "str") ### country level
demoDeaths = pd.read_csv("data/demoDeaths.csv") ### demographic deaths data
raceDeaths = pd.read_csv("data/raceDeaths.csv") ### racial deaths data
hospital = pd.read_csv("data/hospitalData.csv") ### hospitalization estimates
GoogleUsaMobility = pd.read_csv('data/GoogleUsaMobility.csv')
GoogleStateMobility = pd.read_csv('data/GoogleStateMobility.csv')
GoogleCountyMobility = pd.read_csv('data/GoogleCountyMobility.csv', dtype = "str")
NYTusa = pd.read_csv('data/NYTusa.csv')
NYTstate = pd.read_csv('data/NYTstate.csv')
NYTcounty = pd.read_csv('data/NYTcounty.csv', dtype = "str")



import json
counties = open("data/geojson-counties-fips.json",) ### Data for creating maps
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
                                "log(New Deaths)" : "float64"})

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
                              "log(New Deaths)" : "float64"})

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
                          "log(New Deaths)" : "float64"})

GoogleCountyMobility = GoogleCountyMobility.astype({"Date" : "datetime64",
                                                    "%Retail/Rec Change" : "float64",
                                                    "%Grocery/Pharm Change" : "float64",
                                                    "%Parks Change" : "float64",
                                                    "%Transit Change" : "float64",
                                                    "%Workplace Change" : "float64",
                                                    "%Residential Change" : "float64"})



NYTcounty = NYTcounty.astype({"Date" : "datetime64",
                              "Total Cases" : "float64",
                              "Total Deaths" : "float64",
                              "Population" : "float64",
                              "New Cases" : "float64",
                              "New Deaths" : "float64",
                              "%Cases" : "float64",
                              "%Deaths" : "float64", 
                              "log(Total Cases)" : "float64",
                              "log(Total Deaths)" : "float64",
                              "log(New Cases)" : "float64", 
                              'log(New Deaths)' : "float64"})
                                


    
    
    
    
    
    
####### Plot for when Metrics = 0 or -inf
noneFig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = "No Data / Deaths = 0", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=55,
                    color="black")))
    
    
    
    
    
PAGE_SIZE = 250    

################################################# Create Dashboard #######################################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


### Create Dashboard layout.
def create_layout():
    return html.Div([

        ### Header
        html.H1("United States Covid-19 Dashboard", style = {'text-align' : 'center'}),
        html.H6('***Data from various sources were used in the creating of this dashboard. Numbers may vary between sources.***',
               style = {'text-align' : 'center'}),
        html.H6("***Dashboard creator(s) is/are not responsible for the validity of the data.***",
               style = {'text-align' : 'center'}),
               
        ### Refresh data button
        html.Div([
            html.Button('Refresh Dashboard Data', id = 'DataRefresh', n_clicks = 0),
            html.A(html.Button('Refresh Page'), href = '/'),
            dcc.Loading(id = 'loadingData', children = [
                html.Div(id = "updateData")
            ])
        ]),



        ### Main Tabs
        dcc.Tabs(id="tabs", value = "countryTab", children = [

            ### Country Level 
            dcc.Tab(label = "National Level", value = "countryTab", children = [          


    ################################################ Part 1 #####################################################


####################### USA Choropleth Map, Statistics, and Data Table Controls #######################
                ######## Controls ############
                html.Div([
                    html.Div(children = [
                        html.Div([
                            html.H6("Choose Date"),
                            dcc.DatePickerSingle(id = "USmapDate",
                                                 min_date_allowed = usaData["Date"].unique().astype(str)[0][:10],
                                                 max_date_allowed = usaData["Date"].unique().astype(str)[-1][:10],
                                                 initial_visible_month = usaData["Date"].unique().astype(str)[-1][:10],
                                                 date = usaData["Date"].unique().astype(str)[-1][:10])],
                        style = {"float" : 'left'}),

                        html.Div([
                            html.H6("Choose Scale:"),
                            dcc.RadioItems(id = "USmapScale",
                                           options = [{'label' : "Regular Scale", 'value' : "regular"}, 
                                                      {'label' : "Logarithmic Scale", 'value' : "log"}],
                                           value = "regular")],
                        style = {"float" : 'left', 'marginLeft' : 20}),

                        html.Div([
                            html.H6("Choose Metric:"),
                            dcc.RadioItems(id = 'USmapMetric',
                                           options = [{'label' : "Total Cases", 'value' : 'Total Cases'},
                                                      {'label' : 'Total Deaths', 'value' : 'Total Deaths'}],
                                           value = "Total Cases")],
                        style = {"float" : 'left', 'marginLeft' : 20}),

                        html.Div([
                            html.H6("Choose View:"),
                            dcc.RadioItems(id = "USmapView",
                                          options = [{'label' : 'County', 'value' : 'County'},
                                                     {'label' : 'State', 'value' : 'State'}],
                                          value = "County")],
                            style = {"float" : 'left', 'marginLeft' : 20}),
                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "USdataSource1",
                                           options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                      {'label' : 'New York Times', 'value' : 'NYT'}],
                                           value = 'USAFacts')],
                            style = {"float" : 'left', 'marginLeft' : 20, 'marginRight' : 0}),


                        html.Div(html.H4(id = "usaStats"), style = {"float" : 'right', 'marginRight' : 5, 'marginBottom' : 0, 'marginTop' : 15})


                    ], className = "row"),

                ]),

                ########### Maps & Table ##############
                html.Div([

                    ### Map ###
                    html.Div([
                        dcc.Loading(id = "loadingMap1", children = [
                            dcc.Graph(id = "usaMap", className = "six columns")])
                    ]),

                    #### Table ####
                    html.Div([
                        dcc.Loading(id = "loadingMap2", children = [
                            dash_table.DataTable(
                            id = "StateSummaryTable",
                            columns = [{"name" : i, "id" : i} for i in stateData.columns[[0,1,4,5,6,7,8,9,10]]],
                            page_action = 'none',
                            editable = False,
                            sort_action = "native",
                            style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                            style_cell = {'width' : '{}%'.format(len(stateData.columns[[0,1,4,5,6,7,8,9,10]]))},)
                        ])
                    ], className = "six columns") 
                ], className = "row"),





    ############################################ Part 2 ##############################################


                html.Div([html.H3("For the plots below, click on items in the legends to hide them.", style = {'text-align' : 'center'})]),



                ### Controls for part 2
                 html.Div([

                    html.Div(children = [

                        ### Controls for Cases
                        html.Div([
                            html.H6("Choose Left Y-Axis"),
                            dcc.RadioItems(id = "USAcasesYaxis",
                                options = [{'label' : 'Total Cases', 'value' : "Total Cases"},
                                           {'label' : 'New Cases', 'value' : 'New Cases'}],
                                value = "Total Cases")  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),

                        ### Controls for Deaths
                        html.Div([
                            html.H6("Choose Right Y-Axis"),
                            dcc.RadioItems(id = "USAdeathsYaxis",
                                options = [{'label' : 'Total Deaths', 'value' : "Total Deaths"},
                                           {'label' : 'New Deaths', 'value' : 'New Deaths'}],
                                value = "Total Deaths")  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),


                        #### Controls for Scale
                        html.Div([
                            html.H6("Choose Scale:"),
                            dcc.RadioItems(id = "UScasesdeathsScale",
                                           options = [{'label' : "Regular Scale", 'value' : "regular"}, 
                                                      {'label' : "Logarithmic Scale", 'value' : "log"}],
                                           value = "regular")],
                        style = {"float" : 'left', 'marginLeft' : 20}),
                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "USdataSource2",
                                           options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                      {'label' : 'New York Times', 'value' : 'NYT'}],
                                           value = 'USAFacts')],
                            style = {"float" : 'left', 'marginLeft' : 20, 'marginRight' : 0}),


                        ### Controls for Mobility
                        html.Div([
                            html.H6("Choose Comparison Metric:"),
                            dcc.RadioItems(id = "USAmobilityMetric",
                                options = [{'label' : 'Total Cases', 'value' : "Total Cases"},
                                           {'label' : 'New Cases', 'value' : 'New Cases'},
                                           {'label' : 'Total Deaths', 'value' : "Total Deaths"},
                                           {'label' : 'New Deaths', 'value' : 'New Deaths'}],
                                value = "Total Cases",
                                labelStyle = {'display' : 'inline-block'})  
                        ], style = {"float" : 'right', 'marginRight' : 100}),
                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "USdataSource3",
                                           options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                      {'label' : 'New York Times', 'value' : 'NYT'}],
                                           value = 'USAFacts')],
                            style = {"float" : 'right', 'marginRight' : 20, 'marginRight' : 0}),


                    ], className = "row")

                ]),


                ##### Comparing Cases, Deaths, and Mobility
                html.Div([

                    ### Cases & Deaths
                    html.Div([
                        dcc.Loading(id = "USAloading1", children = [
                            dcc.Graph(id = "USACasesDeaths", className = "six columns")])
                    ]),

                    ### Mobility
                    html.Div([
                        dcc.Loading(id = "USAloading2", children = [
                            dcc.Graph(id = "USAMobility", className = "six columns")])
                    ])

                ]),


    ###################################### Part 3 ##################################################################   
                 ### Controls for part 2
                 html.Div([

                    html.Div(children = [

                        ### Controls for sex
                        html.Div([
                            html.H6("Choose Sex:"),
                            dcc.Dropdown(id = "USAchooseSex",
                                options = [{'label' : 'All', 'value' : "All"},
                                           {'label' : 'By Sex', 'value' : 'sex'}],
                                value = "All",
                                clearable = False)  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),

                        ### Controls for race metrics
                        html.Div([
                            html.H6("Choose Metric"),
                            dcc.Dropdown(id = "USAraceMetric",
                                options = [{'label' : 'Count of COVID-19 deaths', 'value' : "Count of COVID-19 deaths"},
                                           {'label' : 'Distribution of COVID-19 deaths (%)', 'value' : 'Distribution of COVID-19 deaths (%)'},
                                           {'label' : 'Unweighted distribution of population (%)', 'value' : 'Unweighted distribution of population (%)'},
                                           {'label' : 'Weighted distribution of population (%)', 'value' : 'Weighted distribution of population (%)'}],
                                value = "Count of COVID-19 deaths",
                                clearable = False,
                                style = {'width' : '500px'})  
                        ], style = {"float" : 'Right', 'marginLeft' : 0, 'marginRight' : 30}),                 

                    ], className = "row")

                 ]),

                 html.Div([

                    ### Sex bar graph
                    html.Div([
                        dcc.Loading(id = "USAloading3", children = [
                            dcc.Graph(id = "USAsex", className = "six columns")])
                    ]),

                    ### Race bar graph
                    html.Div([
                        dcc.Loading(id = "USAloading4", children = [
                            dcc.Graph(id = "USArace", className = "six columns")])
                    ])

                ]),


                ########################################## Part 4 ##############################

                html.Div([
                    html.Div(children = [

                        ### Measurement Type
                        html.Div([
                            html.H6("Choose Measurment Type"),
                            dcc.RadioItems(id = "UShospitalMeasureType",
                                options = [{'label' : 'Regular', "value" : 'regular'},
                                           {'label' : 'Percent', 'value' : 'percent'}],
                                value = "regular",
                                labelStyle = {'display' : 'inline-block'}
                            )
                        ], style = {"float" : 'left', 'marginLeft' : 20}),

                        html.Div([
                            html.H6("Choose Metric"),
                            dcc.Dropdown(id = "UShospitalMetric",
                                options = [{'label' : 'Hospital Inpatient Bed Occupancy', 'value' : 'InpatBeds_Occ_AnyPat'},
                                           {'label' : 'Number of Patients in an Inpatient Care Location who have Suspected or Confirmed Covid-19', 'value' : 'InpatBeds_Occ_COVID'},
                                           {'label' : 'ICU Bed Occupancy' , 'value' : 'ICUBeds_Occ_AnyPat'}],
                                value = 'InpatBeds_Occ_AnyPat',
                                clearable = False
                            ) 
                        ], style = {"float" : 'center', 'marginLeft' : 375, 'marginRight' : 450})

                    ], className = "row")
                ]),


                html.Div([

                    ### Hospital line graph
                    html.Div([
                        dcc.Loading(id = "USAloading5", children = [
                            dcc.Graph(id = "USAhospital")])
                    ])

                ]),

                html.Div(html.H6("*One or more data points have counts between 1–9 and have been suppressed in accordance with NCHS confidentiality standards.")),
                html.Div(html.H6("**As of July 15, 2020, hospital data is no longer reported to the CDC. This data will not be updated after July 14, 2020."))




                ]), ### Tab 1 Ends







    ######################################################################################################################################################        
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################      






            ### State Level
            dcc.Tab(label = "State Level", value = "stateTab", children = [

#################################################### Part 1 #############################################################################
                
    ####################### State Choropleth Map, Statistics, and Data Table Controls #######################
               html.Div([
                   html.Div([
                       html.Div(html.H4('Choose State: '), style = {'float' : 'left', 'marginRight' : 0}),
                       
                       html.Div(dcc.Dropdown(id = 'StateSelect1',
                                             options = [{'label' : state, 'value' : value} for state, value in zip(stateData["State"].unique(), stateData["State"].unique())],
                                             value = "Alabama",
                                             searchable = False,
                                             clearable = False, style = {'width' : '150px'}), 
                                 style = {"float" : 'left', 'marginLeft' : 10, 'marginTop' : 10})
                   ], className = 'row')
               
               ]),
                
               html.Div(html.H2(id = "SelectedState1"), style = {'text-align' : 'center'}),
                
                
                
                html.Div([
                    html.Div(children = [
                        html.Div([
                            html.H6("Choose Date"),
                            dcc.DatePickerSingle(id = 'StateMapDate')],
                        style = {"float" : 'left'}),

                        html.Div([
                            html.H6("Choose Scale:"),
                            dcc.RadioItems(id = "StatemapScale",
                                           options = [{'label' : "Regular Scale", 'value' : "regular"}, 
                                                      {'label' : "Logarithmic Scale", 'value' : "log"}],
                                           value = "regular")],
                        style = {"float" : 'left', 'marginLeft' : 20}),
                        
                        

                        html.Div([
                            html.H6("Choose Metric:"),
                            dcc.RadioItems(id = 'StatemapMetric',
                                           options = [{'label' : "Total Cases", 'value' : 'Total Cases'},
                                                      {'label' : 'Total Deaths', 'value' : 'Total Deaths'}],
                                           value = "Total Cases")],
                        style = {"float" : 'left', 'marginLeft' : 20}),

                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "StatedataSource1",
                                           options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                      {'label' : 'New York Times', 'value' : 'NYT'}],
                                           value = 'USAFacts')],
                            style = {"float" : 'left', 'marginLeft' : 20, 'marginRight' : 0}),


                        html.Div(html.H4(id = "StateStats"), style = {"float" : 'right', 'marginRight' : 5, 'marginBottom' : 0, 'marginTop' : 15})


                    ], className = "row"),

                ]),
                
                html.Div([

                    ### Map ###
                    html.Div([
                        dcc.Loading(id = "loadingMap3", children = [
                            dcc.Graph(id = "stateMap", className = "six columns")])
                    ]),

                    #### Table ####
                    html.Div([
                        dcc.Loading(id = "loadingMap4", children = [
                            dash_table.DataTable(
                            id = "CountySummaryTable",
                            columns = [{"name" : i, "id" : i} for i in countyData.columns[[5,0,6,7,8,9,10,11,12]]],
                            page_action = 'none',
                            editable = False,
                            sort_action = "native",
                            style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                            style_cell = {'width' : '{}%'.format(len(countyData.columns[[5,0,6,7,8,9,10,11,12]]))},)
                        ])
                    ], className = "six columns") 
                ], className = "row"),
                
                
                
                
############################### Part 2 #########################################################################################################                
                
                
                html.Div([html.H3("For the plots below, click on items in the legends to hide them.", style = {'text-align' : 'center'})]),



                ### Controls for part 2
                 html.Div([

                    html.Div(children = [

                        ### Controls for Cases
                        html.Div([
                            html.H6("Choose Left Y-Axis"),
                            dcc.RadioItems(id = "StatecasesYaxis",
                                options = [{'label' : 'Total Cases', 'value' : "Total Cases"},
                                           {'label' : 'New Cases', 'value' : 'New Cases'}],
                                value = "Total Cases")  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),

                        ### Controls for Deaths
                        html.Div([
                            html.H6("Choose Right Y-Axis"),
                            dcc.RadioItems(id = "StatedeathsYaxis",
                                options = [{'label' : 'Total Deaths', 'value' : "Total Deaths"},
                                           {'label' : 'New Deaths', 'value' : 'New Deaths'}],
                                value = "Total Deaths")  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),


                        #### Controls for Scale
                        html.Div([
                            html.H6("Choose Scale:"),
                            dcc.RadioItems(id = "StatecasesdeathsScale",
                                           options = [{'label' : "Regular Scale", 'value' : "regular"}, 
                                                      {'label' : "Logarithmic Scale", 'value' : "log"}],
                                           value = "regular")],
                        style = {"float" : 'left', 'marginLeft' : 20}),
                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "StatedataSource2",
                                           options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                      {'label' : 'New York Times', 'value' : 'NYT'}],
                                           value = 'USAFacts')],
                            style = {"float" : 'left', 'marginLeft' : 20, 'marginRight' : 0}),


                        ### Controls for Mobility
                        html.Div([
                            html.H6("Choose Comparison Metric:"),
                            dcc.RadioItems(id = "StatemobilityMetric",
                                options = [{'label' : 'Total Cases', 'value' : "Total Cases"},
                                           {'label' : 'New Cases', 'value' : 'New Cases'},
                                           {'label' : 'Total Deaths', 'value' : "Total Deaths"},
                                           {'label' : 'New Deaths', 'value' : 'New Deaths'}],
                                value = "Total Cases",
                                labelStyle = {'display' : 'inline-block'})  
                        ], style = {"float" : 'left', 'marginLeft' : 100}),
                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "StatedataSource3",
                                           options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                      {'label' : 'New York Times', 'value' : 'NYT'}],
                                           value = 'USAFacts')],
                            style = {"float" : 'left', 'marginLeft' : 20, 'marginRight' : 0}),


                    ], className = "row")

                ]),


                ##### Comparing Cases, Deaths, and Mobility
                html.Div([

                    ### Cases & Deaths
                    html.Div([
                        dcc.Loading(id = "Stateloading45", children = [
                            dcc.Graph(id = "StateCasesDeaths", className = "six columns")])
                    ]),

                    ### Mobility
                    html.Div([
                        dcc.Loading(id = "Stateloading63", children = [
                            dcc.Graph(id = "StateMobility", className = "six columns")])
                    ])

                ]),
                
                
                
############################### Part 3 ############################################################################             
                
                ### Controls for part 2
                 html.Div([

                    html.Div(children = [

                        ### Controls for sex
                        html.Div([]),
#                             html.H6("Choose Sex:"),
#                             dcc.Dropdown(id = "StatechooseSex",
#                                 options = [{'label' : 'All', 'value' : "All"},
#                                            {'label' : 'By Sex', 'value' : 'sex'}],
#                                 value = "All",
#                                 clearable = False)  
#                         ], style = {"float" : 'left', 'marginLeft' : 20}),

                        ### Controls for race metrics
                        html.Div([
                            html.H6("Choose Metric"),
                            dcc.Dropdown(id = "StateraceMetric",
                                options = [{'label' : 'Count of COVID-19 deaths', 'value' : "Count of COVID-19 deaths"},
                                           {'label' : 'Distribution of COVID-19 deaths (%)', 'value' : 'Distribution of COVID-19 deaths (%)'},
                                           {'label' : 'Unweighted distribution of population (%)', 'value' : 'Unweighted distribution of population (%)'},
                                           {'label' : 'Weighted distribution of population (%)', 'value' : 'Weighted distribution of population (%)'}],
                                value = "Count of COVID-19 deaths",
                                clearable = False,
                                style = {'width' : '500px'})  
                        ], style = {"float" : 'right', 'marginLeft' : 0, 'marginRight' : 30}),                 

                    ], className = "row")

                 ]),

                 html.Div([

                    ### Sex bar graph
                    html.Div([
                        dcc.Loading(id = "Stateloading78", children = [
                            dcc.Graph(id = "Statesex", className = "six columns")])
                    ]),

                    ### Race bar graph
                    html.Div([
                        dcc.Loading(id = "State36loading4", children = [
                            dcc.Graph(id = "Staterace", className = "six columns")])
                    ])

                ], className = 'row'),
                
                
                ########################################## Part 4 ##############################

                html.Div([
                    html.Div(children = [

                        ### Measurement Type
                        html.Div([
                            html.H6("Choose Measurment Type"),
                            dcc.RadioItems(id = "StatehospitalMeasureType",
                                options = [{'label' : 'Regular', "value" : 'regular'},
                                           {'label' : 'Percent', 'value' : 'percent'}],
                                value = "regular",
                                labelStyle = {'display' : 'inline-block'}
                            )
                        ], style = {"float" : 'left', 'marginLeft' : 20}),

                        html.Div([
                            html.H6("Choose Metric"),
                            dcc.Dropdown(id = "StatehospitalMetric",
                                options = [{'label' : 'Hospital Inpatient Bed Occupancy', 'value' : 'InpatBeds_Occ_AnyPat'},
                                           {'label' : 'Number of Patients in an Inpatient Care Location who have Suspected or Confirmed Covid-19', 'value' : 'InpatBeds_Occ_COVID'},
                                           {'label' : 'ICU Bed Occupancy' , 'value' : 'ICUBeds_Occ_AnyPat'}],
                                value = 'InpatBeds_Occ_AnyPat',
                                clearable = False
                            ) 
                        ], style = {"float" : 'center', 'marginLeft' : 375, 'marginRight' : 450})

                    ], className = "row")
                ]),


                html.Div([

                    ### Hospital line graph
                    html.Div([
                        dcc.Loading(id = "Stateloading156", children = [
                            dcc.Graph(id = "Statehospital")])
                    ])

                ]),

                html.Div(html.H6("*One or more data points have counts between 1–9 and have been suppressed in accordance with NCHS confidentiality standards.")),
                html.Div(html.H6("**As of July 15, 2020, hospital data is no longer reported to the CDC. This data will not be updated after July 14, 2020."))
                
            ]), ### Tab 2 Ends



    ######################################################################################################################################################        
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################   







            ### County Level
            dcc.Tab(label = "County Level", value = "countyTab", children = [
                
                ####################### County Choropleth Map, Statistics, and Data Table Controls #######################
               html.Div([
                   html.Div([
                       
                       html.Div([html.H4("Choose Data Source:"),
                                 dcc.Dropdown(id = "CountyDataMaster",
                                               options = [{'label' : 'USAFacts.org', 'value' : 'USAFacts'},
                                                          {'label' : 'New York Times', 'value' : 'NYT'}],
                                               value = 'USAFacts',
                                            searchable = False,
                                            clearable = False)], style = {"float" : 'left', 'marginLeft' : 10, 'marginRight' : 30}),
                       
                       
                       
                       html.Div(html.H4('Choose State: '), style = {'float' : 'left', 'marginRight' : 0}),
                       
                       html.Div(dcc.Dropdown(id = 'StateSelect2',
                                             options = [{'label' : state, 'value' : value} for state, value in zip(stateData["State"].unique(), stateData["State"].unique())],
                                             value = "Alabama",
                                             searchable = False,
                                             clearable = False, style = {'width' : '150px'}), 
                                 style = {"float" : 'left', 'marginLeft' : 10, 'marginTop' : 10}),
                       
                       html.Div(html.H4(id = 'ChooseCounty/CityMessage'), style = {'float' : 'left', 'marginLeft' : 15, 'marginRight' : 0}),
                       html.Div(dcc.Dropdown(id = 'CountySelect', clearable = False, searchable = False, style = {'width' : '250px'}), style = {"float" : 'left', 'marginLeft' : 10, 'marginTop' : 10})
                       
                       
                   ], className = 'row')
               
               ]),
                
               html.Div(html.H2(id = "CountyStateSelected"), style = {'text-align' : 'center'}),
                
                
                
                html.Div([
                    html.Div(children = [
                        html.Div([
                            html.H6("Choose Date"),
                            dcc.DatePickerSingle(id = 'CountyMapDate')],
                        style = {"float" : 'left'}),

                        html.Div([
                            html.H6("Choose Scale:"),
                            dcc.RadioItems(id = "CountymapScale",
                                           options = [{'label' : "Regular Scale", 'value' : "regular"}, 
                                                      {'label' : "Logarithmic Scale", 'value' : "log"}],
                                           value = "regular")],
                        style = {"float" : 'left', 'marginLeft' : 20}),
                        
                        

                        html.Div([
                            html.H6("Choose Metric:"),
                            dcc.RadioItems(id = 'CountymapMetric',
                                           options = [{'label' : "Total Cases", 'value' : 'Total Cases'},
                                                      {'label' : 'Total Deaths', 'value' : 'Total Deaths'}],
                                           value = "Total Cases")],
                        style = {"float" : 'left', 'marginLeft' : 20}),


                        html.Div(html.H4(id = "CountyStats"), style = {"float" : 'right', 'marginRight' : 5, 'marginBottom' : 0, 'marginTop' : 15}),


                    ], className = "row"),

                ]),
                
                html.Div([

                    ### Map ###
                    html.Div([
                        dcc.Loading(id = "loadingMap368", children = [
                            dcc.Graph(id = "CountyMap", className = "six columns")])
                    ]),

                    #### Table ####
                    html.Div([
                        dcc.Loading(id = "loadingMap789", children = [
                            dash_table.DataTable(
                            id = "CountyTimeSummaryTable",
                            columns = [{"name" : i, "id" : i} for i in countyData.columns[[5,6,7,8,9,10,11,12]]],
                            page_action = 'none',
                            editable = False,
                            sort_action = "native",
                            style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                            style_cell = {'width' : '{}%'.format(len(countyData.columns[[5,6,7,8,9,10,11,12]]))},)
                        ])
                    ], className = "six columns") 
                ], className = "row"),
                
                
                
                
                
                ############################### Part 2 #########################################################################################################                
                
                
                html.Div([html.H3("For the plots below, click on items in the legends to hide them.", style = {'text-align' : 'center'})]),



                ### Controls for part 2
                 html.Div([

                    html.Div(children = [

                        ### Controls for Cases
                        html.Div([
                            html.H6("Choose Left Y-Axis"),
                            dcc.RadioItems(id = "CountycasesYaxis",
                                options = [{'label' : 'Total Cases', 'value' : "Total Cases"},
                                           {'label' : 'New Cases', 'value' : 'New Cases'}],
                                value = "Total Cases")  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),

                        ### Controls for Deaths
                        html.Div([
                            html.H6("Choose Right Y-Axis"),
                            dcc.RadioItems(id = "CountydeathsYaxis",
                                options = [{'label' : 'Total Deaths', 'value' : "Total Deaths"},
                                           {'label' : 'New Deaths', 'value' : 'New Deaths'}],
                                value = "Total Deaths")  
                        ], style = {"float" : 'left', 'marginLeft' : 20}),


                        #### Controls for Scale
                        html.Div([
                            html.H6("Choose Scale:"),
                            dcc.RadioItems(id = "CountycasesdeathsScale",
                                           options = [{'label' : "Regular Scale", 'value' : "regular"}, 
                                                      {'label' : "Logarithmic Scale", 'value' : "log"}],
                                           value = "regular")],
                        style = {"float" : 'left', 'marginLeft' : 20}),


                    ], className = "row")
                     
   
                ]),

                

                ### Cases & Deaths
                html.Div([
                    dcc.Loading(id = "Countyloading862", children = [
                        dcc.Graph(id = "CountyCasesDeaths")])
                ]),

  
                
                ### Controls for Mobility
                html.Div([
                    html.Div([
                        html.H6("Choose Comparison Metric:"),
                        dcc.RadioItems(id = "CountymobilityMetric",
                            options = [{'label' : 'Total Cases', 'value' : "Total Cases"},
                                       {'label' : 'New Cases', 'value' : 'New Cases'},
                                       {'label' : 'Total Deaths', 'value' : "Total Deaths"},
                                       {'label' : 'New Deaths', 'value' : 'New Deaths'}],
                            value = "Total Cases",
                            labelStyle = {'display' : 'inline-block'})  
                    ], style = {"float" : 'left', 'marginLeft' : 20}),

                ], className = 'row'),
                
                
                 ### Mobility
                html.Div([
                    dcc.Loading(id = "Countyloading456", children = [
                        dcc.Graph(id = "CountyMobility")])
                ])


            ]), ### Tab 3 Ends




    ######################################################################################################################################################        
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################           





            ### Data Tables
            dcc.Tab(label = "Data Tables", value = "dataTab", children = [
                
                ### Source: USAFacts.org
                html.Div(html.H3('Source: USAFacts.org',style = {'text-align' : 'center'})),
                
                ### National Level
                html.Div(html.H4('National Level Data')),
                html.Div(dcc.Loading(id = "usaDataloading0", children = [
                        dash_table.DataTable(
                            id = 'usaData-table',
                            columns = [{'name' : i, 'id' : i} for i in usaData.columns],
                            editable = False,
                            style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                            page_current = 0,
                            page_size = PAGE_SIZE,
                            page_action = 'custom',
                            page_count = math.ceil(usaData.shape[0]/PAGE_SIZE)
                            )])
                        ),
                
                ### State Level
                html.Div(html.H4('State Level Data')),
                html.Div(dcc.Loading(id = 'stateDataloading0', children = [
                                     dash_table.DataTable(
                                         id = 'stateData-table',
                                         columns = [{'name' : i, 'id' : i} for i in stateData.columns],
                                         editable = False,
                                         style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                         page_current = 0,
                                         page_size = PAGE_SIZE,
                                         page_action = 'custom',
                                         page_count = math.ceil(stateData.shape[0]/PAGE_SIZE)
                                     )])
                        ),
                
                
                ### County Level
                html.Div(html.H4('County Level Data')),
                html.Div(dcc.Loading(id = 'countyDataloading0', children = [
                                     dash_table.DataTable(
                                         id = 'countyData-table',
                                         columns = [{'name' : i, 'id' : i} for i in countyData.columns],
                                         editable = False,
                                         style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                         page_current = 0,
                                         page_size = PAGE_SIZE,
                                         page_action = 'custom',
                                         page_count = math.ceil(countyData.shape[0]/PAGE_SIZE)
                                     )])
                        ),
                
                

                ### Source: New York Times
                html.Div(html.H3('Source: New York Times',style = {'text-align' : 'center'})),
                
                ### National Level
                html.Div(html.H4('National Level Data')),
                html.Div(dcc.Loading(id = 'NYTusaloading0', children = [
                                    dash_table.DataTable(
                                        id = 'NYTusa-table',
                                        columns = [{'name' : i, 'id' : i} for i in NYTusa.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(NYTusa.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                ### State Level
                html.Div(html.H4('State Level Data')),
                html.Div(dcc.Loading(id = 'NYTstateloading0', children = [
                                    dash_table.DataTable(
                                        id = 'NYTstate-table',
                                        columns = [{'name' : i, 'id' : i} for i in NYTstate.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(NYTstate.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
                
                ### County Level
                html.Div(html.H4('County Level Data')),
                html.Div(dcc.Loading(id = 'NYTcountyloading0', children = [
                                    dash_table.DataTable(
                                        id = 'NYTcounty-table',
                                        columns = [{'name' : i, 'id' : i} for i in NYTcounty.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(NYTcounty.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
  
                ### Google Mobility
                html.Div(html.H3('Source: Google Community Mobility Reports',style = {'text-align' : 'center'})),
                
                ### National Level
                html.Div(html.H4('National Level Data')),
                html.Div(dcc.Loading(id = 'GoogleUsaMobilityloading0', children = [
                                    dash_table.DataTable(
                                        id = 'GoogleUsaMobility-table',
                                        columns = [{'name' : i, 'id' : i} for i in GoogleUsaMobility.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(GoogleUsaMobility.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
                ### State Level
                html.Div(html.H4('State Level Data')),
                html.Div(dcc.Loading(id = 'GoogleStateMobilityloading0', children = [
                                    dash_table.DataTable(
                                        id = 'GoogleStateMobility-table',
                                        columns = [{'name' : i, 'id' : i} for i in GoogleStateMobility.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(GoogleStateMobility.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
                
                ### County Level
                html.Div(html.H4('County Level Data')),
                html.Div(dcc.Loading(id = 'GoogleCountyMobilityloading0', children = [
                                    dash_table.DataTable(
                                        id = 'GoogleCountyMobility-table',
                                        columns = [{'name' : i, 'id' : i} for i in GoogleCountyMobility.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(GoogleCountyMobility.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
                
                
                
                ### Source CDC/National Center for Health Statistics
                html.Div(html.H3('Source: CDC - National Center for Health Statistics',style = {'text-align' : 'center'})),
                
                ### Covid-19 Deaths by Sex and Age Group
                html.Div(html.H4('Covid-19 Deaths by Sex and Age Group')),
                html.Div(dcc.Loading(id = 'demoDeathsloading0', children = [
                                    dash_table.DataTable(
                                        id = 'demoDeaths-table',
                                        columns = [{'name' : i, 'id' : i} for i in demoDeaths.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(demoDeaths.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
                
                ### Covid-19 Death Statistics by Race
                html.Div(html.H4('Covid-19 Death Statistics by Race')),
                html.Div(dcc.Loading(id = 'raceDeathsloading0', children = [
                                    dash_table.DataTable(
                                        id = 'raceDeaths-table',
                                        columns = [{'name' : i, 'id' : i} for i in raceDeaths.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(raceDeaths.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                
                
                
                ### CDC’s NHSN Hospitalization Estimates
                html.Div(html.H4('CDC’s NHSN Hospitalization Estimates')),
                html.Div(dcc.Loading(id = 'hospitalloading0', children = [
                                    dash_table.DataTable(
                                        id = 'hospital-table',
                                        columns = [{'name' : i, 'id' : i} for i in hospital.columns],
                                        editable = False,
                                        style_table = {'overflowX' : 'auto', "overflowY" : "auto", 'height': "450px"},
                                        page_current = 0,
                                        page_size = PAGE_SIZE,
                                        page_action = 'custom',
                                        page_count = math.ceil(hospital.shape[0]/PAGE_SIZE)
                                        )])
                        ),
                

            ]), ### Tabe 4 Ends 




    ######################################################################################################################################################        
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################           

            ### Data Dictionary
            dcc.Tab(label = "Data Dictionary", value = "dictTab", children = [
                
                dcc.Markdown('''
                # Source: USAFacts.org
                '''),
                
                 html.Div([
                    html.Div(children = [

                        ### National Level
                        html.Div([dcc.Markdown('''
                        ### National Level

                        * __Country__: The country where Covid-19 data comes from.
                        * __Date__: Calendar date.
                        * __Total Cases__: Cumulative total of Covid-19 cases on a given day.
                        * __Total Deaths__: Cumulative total of deaths due to Covid-19 on a given day.
                        * __Population__: Aggregated sum of 2019 county census estimates.
                        * __New Cases__: Number of new Covid-19 cases on a given day.
                        * __New Deaths__: Number of new deaths due to Covid-19 on a given day.
                        * __%Cases__: Cumulative total of Covid-19 cases by percent of population.
                        * __%Deaths__: Cumulative total of deaths due to Covid-19 by percent of population.
                        * __log(Total Cases)__: Logarithmic transformation of Total Cases.
                        * __log(Total Deaths)__: Logarithmic transformation of Total Deaths.
                        * __log(New Cases)__: Logarithmic transformation of New Cases.
                        * __log(New Deaths)__: Logarithmic transformation of New Deaths.

                        ''')], style = {"float" : 'left', 'marginLeft' : 5}),
                        
                        
                        
                        ### State Level
                        html.Div([dcc.Markdown('''
                        ### State Level
                        
                        * __Date__: Calendar date.
                        * __State__: State where Covid-19 data comes from (including D.C.).
                        * __StateABV__: Abbreviation of State name.
                        * __stateFIPS__: FIPS code for State (including D.C.).
                        * __Total Cases__: Cumulative total of Covid-19 cases on a given day.
                        * __Total Deaths__: Cumulative total of deaths due to Covid-19 on a given day.
                        * __Population__: Aggregated sum of 2019 county census estimates.
                        * __New Cases__: Number of new Covid-19 cases on a given day.
                        * __New Deaths__: Number of new deaths due to Covid-19 on a given day.
                        * __%Cases__: Cumulative total of Covid-19 cases by percent of population.
                        * __%Deaths__: Cumulative total of deaths due to Covid-19 by percent of population.
                        * __log(Total Cases)__: Logarithmic transformation of Total Cases.
                        * __log(Total Deaths)__: Logarithmic transformation of Total Deaths.
                        * __log(New Cases)__: Logarithmic transformation of New Cases.
                        * __log(New Deaths)__: Logarithmic transformation of New Deaths.

                        ''')], style = {"float" : 'left', 'marginLeft' : 15}),
                        
                        
                        ### County Level
                        html.Div([dcc.Markdown('''
                        ### County Level
                        * __County Name__: Name of County (including D.C.).                        
                        * __State__: State where Covid-19 data comes from (including D.C.).
                        * __countyFIPS__: FIPS code for County (including D.C.).
                        * __StateABV__: Abbreviation of State name.
                        * __stateFIPS__: FIPS code for State (including D.C.).
                        * __Date__: Calendar date.
                        * __Total Cases__: Cumulative total of Covid-19 cases on a given day.
                        * __Total Deaths__: Cumulative total of deaths due to Covid-19 on a given day.
                        * __Population__: Aggregated sum of 2019 county census estimates.
                        * __New Cases__: Number of new Covid-19 cases on a given day.
                        * __New Deaths__: Number of new deaths due to Covid-19 on a given day.
                        * __%Cases__: Cumulative total of Covid-19 cases by percent of population.
                        * __%Deaths__: Cumulative total of deaths due to Covid-19 by percent of population.
                        * __log(Total Cases)__: Logarithmic transformation of Total Cases.
                        * __log(Total Deaths)__: Logarithmic transformation of Total Deaths.
                        * __log(New Cases)__: Logarithmic transformation of New Cases.
                        * __log(New Deaths)__: Logarithmic transformation of New Deaths.

                        ''')], style = {"float" : 'left', 'marginLeft' : 15}),

                    ], className = "row")
                     
   
                ]),
                
                
                dcc.Markdown('''
                # Source: New York Times
                '''),
                
                
                html.Div([
                    html.Div(children = [

                        ### National Level
                        html.Div([dcc.Markdown('''
                        ### National Level

                        * __Country__: The country where Covid-19 data comes from.
                        * __Date__: Calendar date.
                        * __Total Cases__: Cumulative total of Covid-19 cases on a given day.
                        * __Total Deaths__: Cumulative total of deaths due to Covid-19 on a given day.
                        * __Population__: Aggregated sum of 2019 county census estimates.
                        * __New Cases__: Number of new Covid-19 cases on a given day.
                        * __New Deaths__: Number of new deaths due to Covid-19 on a given day.
                        * __%Cases__: Cumulative total of Covid-19 cases by percent of population.
                        * __%Deaths__: Cumulative total of deaths due to Covid-19 by percent of population.
                        * __log(Total Cases)__: Logarithmic transformation of Total Cases.
                        * __log(Total Deaths)__: Logarithmic transformation of Total Deaths.
                        * __log(New Cases)__: Logarithmic transformation of New Cases.
                        * __log(New Deaths)__: Logarithmic transformation of New Deaths.

                        ''')], style = {"float" : 'left', 'marginLeft' : 5}),
                        

                        ### State Level
                        html.Div([dcc.Markdown('''
                        ### State Level
                        
                        * __Date__: Calendar date.
                        * __State__: State where Covid-19 data comes from (including D.C.).
                        * __StateABV__: Abbreviation of State name.
                        * __stateFIPS__: FIPS code for State (including D.C.).
                        * __Total Cases__: Cumulative total of Covid-19 cases on a given day.
                        * __Total Deaths__: Cumulative total of deaths due to Covid-19 on a given day.
                        * __Population__: Aggregated sum of 2019 county census estimates.
                        * __New Cases__: Number of new Covid-19 cases on a given day.
                        * __New Deaths__: Number of new deaths due to Covid-19 on a given day.
                        * __%Cases__: Cumulative total of Covid-19 cases by percent of population.
                        * __%Deaths__: Cumulative total of deaths due to Covid-19 by percent of population.
                        * __log(Total Cases)__: Logarithmic transformation of Total Cases.
                        * __log(Total Deaths)__: Logarithmic transformation of Total Deaths.
                        * __log(New Cases)__: Logarithmic transformation of New Cases.
                        * __log(New Deaths)__: Logarithmic transformation of New Deaths.

                        ''')], style = {"float" : 'left', 'marginLeft' : 15}),
        
                        
                        ### County Level
                        html.Div([dcc.Markdown('''
                        ### County Level
                        * __County Name__: Name of County (including D.C.).                        
                        * __State__: State where Covid-19 data comes from (including D.C.).
                        * __countyFIPS__: FIPS code for County (including D.C.).
                        * __StateABV__: Abbreviation of State name.
                        * __stateFIPS__: FIPS code for State (including D.C.).
                        * __Date__: Calendar date.
                        * __Total Cases__: Cumulative total of Covid-19 cases on a given day.
                        * __Total Deaths__: Cumulative total of deaths due to Covid-19 on a given day.
                        * __Population__: Aggregated sum of 2019 county census estimates.
                        * __New Cases__: Number of new Covid-19 cases on a given day.
                        * __New Deaths__: Number of new deaths due to Covid-19 on a given day.
                        * __%Cases__: Cumulative total of Covid-19 cases by percent of population.
                        * __%Deaths__: Cumulative total of deaths due to Covid-19 by percent of population.
                        * __log(Total Cases)__: Logarithmic transformation of Total Cases.
                        * __log(Total Deaths)__: Logarithmic transformation of Total Deaths.
                        * __log(New Cases)__: Logarithmic transformation of New Cases.
                        * __log(New Deaths)__: Logarithmic transformation of New Deaths.

                        ''')], style = {"float" : 'left', 'marginLeft' : 15}),

                    ], className = "row")
                     
   
                ]),      
                
                
                dcc.Markdown('''
                # Source: Google Community Mobility Reports
                '''),
                
                html.Div([
                    html.Div(children = [
                        
                        ### National Level
                        html.Div(dcc.Markdown('''
                        ### National Level
                        * __Country__: Country from which data comes from.
                        * __Date__: Calendar date.
                        * __%Retail/Rec Change__: Percent change from baseline in mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.
                        * __%Grocery/Pharm Change__: Percent change from baseline in mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.
                        * __%Parks Change__: Percent change from basline in mobility trends for places like local parks, national parks, public beaches, marinas, dog parks, plazas, and public gardens.
                        * __%Transit Change__: Percent change from baseline in mobility trends for places like public transport hubs such as subway, bus, and train stations.
                        * __%Workplace Change__: Percent change from baseline in mobility trends for places of work.
                        * __%Residential Change__: Percent change from baseline in mobility trends for places of residence.
                        '''), style = {"float" : 'left', 'marginLeft' : 5}),
                        
                        
                        ### State Level
                        html.Div(dcc.Markdown('''
                        ### State Level
                        * __State__: State from which data comes from (including D.C.).
                        * __Date__: Calendar date.
                        * __%Retail/Rec Change__: Percent change from baseline in mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.
                        * __%Grocery/Pharm Change__: Percent change from baseline in mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.
                        * __%Parks Change__: Percent change from basline in mobility trends for places like local parks, national parks, public beaches, marinas, dog parks, plazas, and public gardens.
                        * __%Transit Change__: Percent change from baseline in mobility trends for places like public transport hubs such as subway, bus, and train stations.
                        * __%Workplace Change__: Percent change from baseline in mobility trends for places of work.
                        * __%Residential Change__: Percent change from baseline in mobility trends for places of residence.
                        '''), style = {"float" : 'left', 'marginLeft' : 5}),
                        
                        
                        ### County Level
                        html.Div(dcc.Markdown('''
                        ### County Level
                        * __County Name__: Name of county from which data comes from.
                        * __countyFIPS__: FIPS code for County (including D.C.).
                        * __Date__: Calendar date.
                        * __%Retail/Rec Change__: Percent change from baseline in mobility trends for places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters.
                        * __%Grocery/Pharm Change__: Percent change from baseline in mobility trends for places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies.
                        * __%Parks Change__: Percent change from basline in mobility trends for places like local parks, national parks, public beaches, marinas, dog parks, plazas, and public gardens.
                        * __%Transit Change__: Percent change from baseline in mobility trends for places like public transport hubs such as subway, bus, and train stations.
                        * __%Workplace Change__: Percent change from baseline in mobility trends for places of work.
                        * __%Residential Change__: Percent change from baseline in mobility trends for places of residence.
                        '''), style = {"float" : 'left', 'marginLeft' : 5}),                        
                    ], className = "row")
                ]),
                
                
                
                dcc.Markdown('''
                # Source: CDC - National Center for Health Statistics
                '''),
                
                dcc.Markdown('''
                ### Covid-19 Deaths by Sex and Age Group
                * __Data as of__: Date data was last updated.
                * __Start week__: Week when data started being recorded.
                * __End Week__: Week when data was last recorded.
                * __State__: State where data comes from (including United States).
                * __Sex__: Sex.
                * __Age group__: Age group.
                * __COVID-19 Deaths__: Number of deaths due to Covid-19.
                '''),
                
                dcc.Markdown('''
                ### Covid-19 Death Statistics by Race
                * __Date as of__: Date data was last updated.
                * __State__: State where data comes from (including United States).
                * __Race__: Race.
                * __Count of COVID-19 deaths__: Count of deaths due to Covid-19.
                * __Distribution of COVID-19 deaths (%)__: Distribution of deaths due to Covid-19 by race.
                * __Unweighted distribution of population (%)__: Unweighted distribution of population by race.
                * __Weighted distribution of population (%)__: Weighted distribution of population by race.
                
                '''),
                
                dcc.Markdown('''
                ### CDC’s NHSN Hospitalization Estimates
                * __State__: State where data comes from (including United States).
                * __Date__: Day for which estimate is made.
                * __InpatBeds_Occ_AnyPat_Est__: Hospital inpatient bed occupancy, estimate.
                * __InpatBeds_Occ_AnyPat_LoCI__: Hospital inpatient bed occupancy, lower 95% CI.
                * __InpatBeds_Occ_AnyPat_UpCI__: Hospital inpatient bed occupancy, upper 95% CI.
                * __InpatBeds_Occ_AnyPat_Est_Avail__: Hospital inpatient beds available, estimate.
                * __InBedsOccAnyPat__Numbeds_Est__: Hospital inpatient bed occupancy, percent estimate (percent of inpatient beds).
                * __InBedsOccAnyPat__Numbeds_LoCI__: Hospital inpatient bed occupancy, lower 95% CI (percent of inpatient beds).
                * __InBedsOccAnyPat__Numbeds_UpCI__: Hospital inpatient bed occupancy, upper 95% CI (percent of inpatient beds).
                * __InpatBeds_Occ_COVID_Est__: Number of patients in an inpatient care location who have suspected or confirmed COVID-19,  estimate.
                * __InpatBeds_Occ_COVID_LoCI__: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, lower 95% CI.
                * __InpatBeds_Occ_COVID_UpCI__: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, upper 95% CI.
                * __InBedsOccCOVID__Numbeds_Est__: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, percent estimate (percent of inpatient beds).
                * __InBedsOccCOVID__Numbeds_LoCI__: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, lower 95% CI (percent of inpatient beds).
                * __InBedsOccCOVID__Numbeds_UpCI__: Number of patients in an inpatient care location who have suspected or confirmed COVID-19, upper 95% CI (percent of inpatient beds).
                * __ICUBeds_Occ_AnyPat_Est__: ICU bed occupancy, estimate.
                * __ICUBeds_Occ_AnyPat_LoCI__: ICU bed occupancy, lower 95% CI.
                * __ICUBeds_Occ_AnyPat_UpCI__: ICU bed occupancy, upper 95% CI.
                * __ICUBeds_Occ_AnyPat_Est_Avail__: ICU beds available, estimate.
                * __ICUBedsOccAnyPat__N_ICUBeds_Est__: ICU bed occupancy, percent estimate (percent of ICU beds).
                * __ICUBedsOccAnyPat__N_ICUBeds_LoCI__: ICU bed occupancy, lower 95% CI (percent of ICU beds).
                * __ICUBedsOccAnyPat__N_ICUBeds_UpCI__: ICU bed occupancy, upper 95% CI (percent of ICU beds).
                ''')
                
            ]), ### Tab 5 Ends


    ######################################################################################################################################################        
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################      
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################              
    ######################################################################################################################################################           





            #### About the Data
            dcc.Tab(label = "About the Data", value = "aboutTab", children = [
                
                dcc.Markdown('''
                # USAFacts.org
                '''),
                dcc.Markdown('''
                Covid-19 data comes from the website USAFacts.org. From USAFacts.org, daily Covid-19 cases and deaths number for each county in the United States can be downloaded to csv files. These files are updated daily. USAFacts.org attempts to match each case with a county, but some cases counted at the state level are not allocated to counties due to lack of information.
                
                ###### __NOTES FROM USAFacts.org__:
                
                
                * __Note from April 28__: "On April 14, New York City began a separate count of "probable deaths" of people believed to have died as a result of COVID-19, though weren't tested. On April 28, these deaths were retroactively added to our death counts, assigned to a New York City borough if possible. In the future, USAFacts will include "probable deaths" in the overall tally if a local government chooses to report that information separately."
                                
                                
                * __Note from April 18__: "Certain states have changed their methodology in reporting deaths due to COVID-19. As a result, we are holding off on reporting death data in a few key states (New York is notable among these states due to the high number of confirmed cases and deaths). USAFacts is committed to providing official numbers confirmed by state or local health agencies, and we will appropriately backfill the death data when we receive more guidance from the CDC and relevant health departments."
                    
                    
                * __Note from April 15__: "In certain states, probable deaths are listed alongside confirmed deaths. Following the lead of the CDC, we will begin publishing death counts that combine these two totals where applicable; this might result in larger than expected increases in deaths in certain counties."
                
                
                * __Note from March 28__: "The data now includes all counties regardless of confirmed case count. Additionally, New York City data has been allotted to its five boroughs/counties, where possible."
                
                
                All other variables used in this dashboard where calculated based on what is supplied by USAFacts.org. 
                
                For the purposes of creating this dashboard, the following changes to the data were made:
                
                
                * Observations for the Wade Hampton Census Area, Alaska were dropped. This area no longer exists. It was renamed to Kusilvak Census Area.
                
                
                * Observations for New York City Unallocated/Probable were dropped. This is not a county. Observations for the NYC area are covered by the 5 counties of the metropolitan area.
                
                
                * Observations for the Grand Princess Cruise Ship were dropped. This is a cruise ship, not a county, and these cases are attributed to California.
                
                
                * For the purposes of creating national, state, and county level choropleth maps, observations for the Aleutians West Census Area, Alaska were dropped.
                
                
                The original data can be found here: https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/
                
                USAFacts.org's methodology and sources can be found here: https://usafacts.org/articles/detailed-methodology-covid-19-data/
                '''),
                
                
                dcc.Markdown('''
                # New York Times
                '''),
                dcc.Markdown('''
                Covid-19 data comes from the New York Times (NYT) github page. NYT supplies daily Covid-19 cases and deaths number in the United States on the national, state, county level, and for U.S. territories. This data can be downloaded to csv files. These files are updated daily. For this dashboard, data focusing on the 50 States, including D.C., were used.
                
                ###### __Notable Geographic Exceptions from NYT__:
                
                
                * __New York__: "All cases for the five boroughs of New York City (New York, Kings, Queens, Bronx and Richmond counties) are assigned to a single area called New York City. There is a large jump in the number of deaths on April 6th due to switching from data from New York City to data from New York state for deaths."
                
                
                * __ Kansas City, Missouri__: "Four counties (Cass, Clay, Jackson and Platte) overlap the municipality of Kansas City, Missouri. The cases and deaths that NYT shows for these four counties are only for the portions exclusive of Kansas City. Cases and deaths for Kansas City are reported as their own line."
                
                
                * __Joplin, Missouri__: "Starting June 25, cases and deaths for Joplin are reported separately from Jasper and Newton counties. The cases and deaths reported for those counties are only for the portions exclusive of Joplin. Joplin cases and deaths previously appeared in the counts for those counties or as Unknown."
                
                
                * __Alameda County, California__: "Counts for Alameda County include cases and deaths from Berkeley and the Grand Princess cruise ship."
                
                
                * __Dauglas County, Nebraska__: "Counts for Douglas County include cases brought to the state from the Diamond Princess cruise ship."
                
                
                All other variables used in this dashboard where calculated based on what is supplied by NYT. 
                
                
                For the purposes of creating this dashboard, the following changes to the data were made:
                
                
                * New York City observations are the summation of the 5 counties that make up the NYC metropolitan area. To handle this, "New York City" will be split into 5 parts, and their case and death numbers will be divided by 5. This will evenly split the information across New York, Kings, Queens, Bronx and Richmond counties. "New York City" will be kept for other parts of the dashboard. This division doesn't match reality, but for the purposes of this dashboard, it is good enough.
                
                
                The original data and other geographical exception descriptions can be found here: https://github.com/nytimes/covid-19-data

                '''),
                
                
                dcc.Markdown('''
                # Google Community Mobility Reports
                '''),
                dcc.Markdown('''
                Community mobility data comes from Google's open source Covid-19 Community Mobility Reports. These reports consist of anonymized aggregated location data that track movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential. This data can be downloaded to a csv file. Changes for each day are compared to a baseline value for that day of the week. 
                
                ###### __NOTES FROM GOOGLE__:
                
                
                * "The baseline is the median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020 (pre-pandemic)."
                
                
                * "The datasets show trends over several months with the most recent data representing approximately 2-3 days ago—this is how long it takes to produce the datasets"
                
                
                * "No personally identifiable information, such as an individual’s location, contacts or movement, is made available at any point."
                
                
                * "This data will be available for a limited time, as long as public health officials find it useful in their work to stop the spread of COVID-19."
                
                
                The data can be found here: https://www.google.com/covid19/mobility/

                '''),
                
                
                dcc.Markdown('''
                # Covid-19 Deaths by Sex & Age
                '''),
                dcc.Markdown('''
                This data comes from the Centers of Disease Control and Prevention (CDC) and is provided by the National Center for Health Statistics. It contains aggregated death data based on Country, State, Sex, and Age Group. This data can be downloaded to a csv file.
                
                ###### __NOTES FROM CDC__:
                
                
                * "Number of deaths reported in this table are the total number of deaths received and coded as of the date of analysis, and do not represent all deaths that occurred in that period. Data during this period are incomplete because of the lag in time between when the death occurred and when the death certificate is completed, submitted to NCHS and processed for reporting purposes. This delay can range from 1 week to 8 weeks or more."
                
                
                * "One or more data cells have counts between 1–9 and have been suppressed in accordance with NCHS confidentiality standards."
                
                
                The data can be found here: _Centers for Disease Control and Prevention. Provisional Death Counts for Coronavirus Disease (COVID-19): Weekly State-Specific Data Updates._ https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Sex-Age-and-S/9bhg-hcku
                
                '''),
                
                
                dcc.Markdown('''
                # Covid-19 Deaths by Race
                '''),
                dcc.Markdown('''
                This data comes from the Centers of Disease Control and Prevention (CDC) and is provided by the National Center for Health Statistics. It contains aggregated death data based on Country, State, and Race. This data can be downloaded to a csv file.
                
                ###### __NOTES FROM CDC__:
                
                
                * "The percent of deaths reported in this table are the total number of represent all deaths received and coded as of the date of analysis and do not represent all deaths that occurred in that period. Data are incomplete because of the lag in time between when the death occurred and when the death certificate is completed, submitted to NCHS and processed for reporting purposes. This delay can range from 1 week to 8 weeks or more, depending on the jurisdiction, age, and cause of death. Provisional counts reported here track approximately 1–2 weeks behind other published data sources on the number of COVID-19 deaths in the U.S. COVID-19 deaths are defined as having confirmed or presumed COVID-19, and are coded to ICD–10 code U07.1."
                
                
                * "Unweighted population percentages are based on the Single-Race Population Estimates from the U.S. Census Bureau, for the year 2018 (available from: https://wonder.cdc.gov/single-race-population.html )."
                
                
                * "Weighted population percentages are computed by multiplying county-level population counts by the count of COVID deaths for each county, summing to the state-level, and then estimating the percent of the population within each racial and ethnic group. These weighted population distributions therefore more accurately reflect the geographic locations where COVID outbreaks are occurring. Jurisdictions are included in this table if more than 100 deaths were received and processed by NCHS as of the data of analysis. 1. Race and Hispanic-origin categories are based on the 1997 Office of Management and Budget (OMB) standards (1,2), allowing for the presentation of data by single race and Hispanic origin. These race and Hispanic-origin groups—non-Hispanic single-race white, non-Hispanic single-race black or African American, non-Hispanic single-race American Indian or Alaska Native (AIAN), and non-Hispanic single-race Asian—differ from the bridged-race categories shown in most reports using mortality data. 2. Includes persons having origins in any of the original peoples of North and South America 3. Includes persons having origins in any of the original peoples of the Far East, Southeast Asia, or the Indian subcontinent. 4. Includes Native Hawaiian and Other Pacific Islander, more than one race, race unknown, and Hispanic origin unknown 5. Excludes New York City."

                
                * "One or more data cells have counts between 1–9 and have been suppressed in accordance with NCHS confidentiality standards."
                
                
                The data can be found here: _Centers for Disease Control and Prevention. Provisional COVID-19 Death Counts by Sex, Age, and State._ https://data.cdc.gov/NCHS/Provisional-Death-Counts-for-Coronavirus-Disease-C/pj7m-y5uh
                
                '''),
                
                
                
                dcc.Markdown('''
                # Hospitalization Estimates
                '''),
                dcc.Markdown('''
                This data comes from the CDC’s National Healthcare Safety Network (NHSN). It enables hospitals to report: 1) Current inpatient and intensive care unit (ICU) bed occupancy, 2) Healthcare worker staffing, and 3) Personal protective equipment (PPE) supply status and availability. This data can be downloaded to a csv file.
                
                ###### __NOTES FROM CDC__:
                
                
                * "Statistical methods were used to generate estimates of patient impact and hospital capacity measures that are representative at the national level. The estimates are based on data submitted by acute care hospitals to the NHSN COVID-19 Module. The statistical methods include weighting (to account for non-response) and multiple imputation (to account for missing data). The estimates (number and percentage) are shown along with 95% confidence intervals that reflect the statistical error that is primarily due to non-response."
                
                
                
                * "This data was submitted directly to CDC’s National Healthcare Safety Network (NHSN) and does not include data submitted to other entities contracted by or within the federal government."
                
                
                
                #### __As of July 15, 2020, hospital data is no longer reported to the CDC. It is now reported to the Department of Health and Human Services. This data will not be updated after July 14, 2020.__
                
                The data (as is) can be found here: https://www.cdc.gov/nhsn/covid19/report-overview.html#anchor_1590010579051
                
                ''')
                
            ]) ### Tab 6 Ends

        ])
    ])


    
    
### Generate dashboard
app.layout = create_layout
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
########################################################################################################################################################################################################
    
    
    
    
    
    
    
    
    
########## Callbacks for data tables tab #################### 
@app.callback(
    Output('usaData-table', 'data'),
    [Input('usaData-table', "page_current"),
     Input('usaData-table', "page_size")]
)
def update_usaData_table(page_current, page_size):
    x = usaData.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('stateData-table', 'data'),
    [Input('stateData-table', "page_current"),
     Input('stateData-table', "page_size")]
)
def update_stateData_table(page_current, page_size):
    x = stateData.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('countyData-table', 'data'),
    [Input('countyData-table', "page_current"),
     Input('countyData-table', "page_size")]
)
def update_countyData_table(page_current, page_size):
    x = countyData.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')






@app.callback(
    Output('NYTusa-table', 'data'),
    [Input('NYTusa-table', "page_current"),
     Input('NYTusa-table', "page_size")]
)
def update_NYTusa_table(page_current, page_size):
    x = NYTusa.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('NYTstate-table', 'data'),
    [Input('NYTstate-table', "page_current"),
     Input('NYTstate-table', "page_size")]
)
def update_NYTstate_table(page_current, page_size):
    x = NYTstate.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('NYTcounty-table', 'data'),
    [Input('NYTcounty-table', "page_current"),
     Input('NYTcounty-table', "page_size")]
)
def update_NYTcounty_table(page_current, page_size):
    x = NYTcounty.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')









@app.callback(
    Output('GoogleUsaMobility-table', 'data'),
    [Input('GoogleUsaMobility-table', "page_current"),
     Input('GoogleUsaMobility-table', "page_size")]
)
def update_GoogleUsaMobility_table(page_current, page_size):
    x = GoogleUsaMobility.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('GoogleStateMobility-table', 'data'),
    [Input('GoogleStateMobility-table', "page_current"),
     Input('GoogleStateMobility-table', "page_size")]
)
def update_GoogleStateMobility_table(page_current, page_size):
    x = GoogleStateMobility.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('GoogleCountyMobility-table', 'data'),
    [Input('GoogleCountyMobility-table', "page_current"),
     Input('GoogleCountyMobility-table', "page_size")]
)
def update_GoogleCountyMobility_table(page_current, page_size):
    x = GoogleCountyMobility.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')








@app.callback(
    Output('demoDeaths-table', 'data'),
    [Input('demoDeaths-table', "page_current"),
     Input('demoDeaths-table', "page_size")]
)
def update_demoDeaths_table(page_current, page_size):
    x = demoDeaths.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')


@app.callback(
    Output('raceDeaths-table', 'data'),
    [Input('raceDeaths-table', "page_current"),
     Input('raceDeaths-table', "page_size")]
)
def update_raceDeaths_table(page_current, page_size):
    x = raceDeaths.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

@app.callback(
    Output('hospital-table', 'data'),
    [Input('hospital-table', "page_current"),
     Input('hospital-table', "page_size")]
)
def update_hospital_table(page_current, page_size):
    x = hospital.iloc[(page_current*page_size):((page_current+ 1)*page_size)]
    return x.to_dict('records')

    
    
 
    
    
    
    
    
    
    
    


    
    
    
    
    
    
    
    
    


########################### CALLBACKS #########################################
###################################################################################################################################################################################
###################################################################################################################################################################################
###################################################################################################################################################################################
###################################################################################################################################################################################
###################################################################################################################################################################################

@app.callback(
    Output('updateData', 'children'),
    [Input('DataRefresh', 'n_clicks')]
)
def import_data(n_clicks):
    if n_clicks != 0:
        import import_ipynb
        import UpdateData
        UpdateData.run_all()
        
        ### Load Datasets
        global countyData 
        countyData = pd.read_csv("data/countyData.csv", dtype = "str") ### county level
        global stateData 
        stateData = pd.read_csv("data/stateData.csv", dtype = "str") ### state level
        global usaData 
        usaData = pd.read_csv("data/usaData.csv", dtype = "str") ### country level
        global demoDeaths 
        demoDeaths = pd.read_csv("data/demoDeaths.csv") ### demographic deaths data
        global raceDeaths 
        raceDeaths = pd.read_csv("data/raceDeaths.csv") ### racial deaths data
        global hospital 
        hospital = pd.read_csv("data/hospitalData.csv") ### hospitalization estimates
        global GoogleUsaMobility 
        GoogleUsaMobility = pd.read_csv('data/GoogleUsaMobility.csv')
        global GoogleStateMobility 
        GoogleStateMobility = pd.read_csv('data/GoogleStateMobility.csv')
        global GoogleCountyMobility 
        GoogleCountyMobility = pd.read_csv('data/GoogleCountyMobility.csv', dtype = "str")
        global NYTusa
        NYTusa = pd.read_csv('data/NYTusa.csv')
        global NYTstate
        NYTstate = pd.read_csv('data/NYTstate.csv')
        global NYTcounty
        NYTcounty = pd.read_csv('data/NYTcounty.csv', dtype = 'str')

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
                                        "log(New Deaths)" : "float64"})

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
                                      "log(New Deaths)" : "float64"})

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
                                  "log(New Deaths)" : "float64"})

        GoogleCountyMobility = GoogleCountyMobility.astype({"Date" : "datetime64",
                                                            "%Retail/Rec Change" : "float64",
                                                            "%Grocery/Pharm Change" : "float64",
                                                            "%Parks Change" : "float64",
                                                            "%Transit Change" : "float64",
                                                            "%Workplace Change" : "float64",
                                                            "%Residential Change" : "float64"})
        NYTcounty = NYTcounty.astype({"Date" : "datetime64",
                              "Total Cases" : "float64",
                              "Total Deaths" : "float64",
                              "Population" : "float64",
                              "New Cases" : "float64",
                              "New Deaths" : "float64",
                              "%Cases" : "float64",
                              "%Deaths" : "float64", 
                              "log(Total Cases)" : "float64",
                              "log(Total Deaths)" : "float64",
                              "log(New Cases)" : "float64", 
                              'log(New Deaths)' : "float64"})
        
        return 'Data has been updated. Refresh Page.'
                                



###################################   NATIONAL TAB   #################################################################################################     
######################################################################################################################################################      
######################################################################################################################################################      
######################################################################################################################################################      
######################################################################################################################################################              
######################################################################################################################################################              
######################################################################################################################################################              
######################################################################################################################################################   

############# USA statistics ###############
@app.callback(
    Output('usaStats', 'children'),
    [Input('USmapDate', 'date'),
     Input('USdataSource1', 'value')])
def display_usaStats(date, source):
    
    if source == "USAFacts":
        totcases = "{:,}".format(int(usaData["Total Cases"][usaData["Date"] == date]))
        totdeaths = "{:,}".format(int(usaData["Total Deaths"][usaData["Date"] == date]))
        x = 'Total Cases: {} - Total Deaths: {} - (As of {})'.format(totcases, totdeaths, date)
        return x
    
    elif source == "NYT":
        totcases = "{:,}".format(int(NYTusa["Total Cases"][NYTusa["Date"] == date]))
        totdeaths = "{:,}".format(int(NYTusa["Total Deaths"][NYTusa["Date"] == date]))
        x = 'Total Cases: {} - Total Deaths: {} - (As of {})'.format(totcases, totdeaths, date)
        return x
    
    
    
    
############################################################################################################################################################################################

############# USA data table ################
@app.callback(
    Output('StateSummaryTable', 'data'),
    [Input('USmapDate', 'date'),
     Input('USdataSource1', 'value')]
)
def update_USATable(date, source):
    
    if source == "USAFacts":
        x = stateData[stateData["Date"] == date].copy()
        x['Date'] = x["Date"].unique().astype(str)[0][:10]
        return x.to_dict("records")
    
    elif source == "NYT":
        x = NYTstate[NYTstate["Date"] == date].copy()
        x['Date'] = x["Date"].unique().astype(str)[0][:10]
        return x.to_dict("records")
    
############################################################################################################################################################################################

############### USA Map Callback ##################
@app.callback(
    Output('usaMap', 'figure'),
    [Input('USmapDate', 'date'),
     Input('USmapScale', 'value'),
     Input('USmapMetric', 'value'),
     Input('USmapView', 'value'),
     Input('USdataSource1', 'value')]
)
def display_USAMap(date, scale, metric, view, source):
    
    
    ################## USAFacts.org
    
    if source == "USAFacts":
        if view == 'County':
            if scale == "regular":
                quants = countyData[metric][countyData[metric]>0].quantile(q = [0,1])
                fig = px.choropleth(countyData[(countyData["Date"] == date) &
                                               (countyData[metric] > 0)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ['blue', 'green', 'yellow', 'orange', 'red'],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig

            elif scale == "log":

                metric = "log(" + metric + ")"
                quants = countyData[metric][countyData[metric]>=0].quantile(q = [0,1])
                fig = px.choropleth(countyData[(countyData["Date"] == date) &
                                               (countyData[metric] >= 0)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0],quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig

        elif view == 'State':
            if scale == "regular":
                quants = stateData[metric][stateData[metric]>0].quantile(q = [0,1])
                fig = px.choropleth(stateData[(stateData["Date"] == date) &
                                               (stateData[metric] > 0)], 
                                    locations = "StateABV",
                                    locationmode = "USA-states",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"StateABV":False,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (State Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig


            elif scale == "log":

                metric = "log(" + metric + ")"
                quants = stateData[metric][stateData[metric]>=0].quantile(q = [0,1])
                fig = px.choropleth(stateData[(stateData["Date"] == date) &
                                               (stateData[metric] >= 0)], 
                                    locations = "StateABV",
                                    locationmode = "USA-states",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"StateABV":False,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (State Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig    
            
        
        
        ############# New York Times ################################
        
    elif source == "NYT":
        if view == 'County':
            if scale == "regular":
                quants = NYTcounty[metric][NYTcounty[metric]>0].quantile(q = [0,1])
                fig = px.choropleth(NYTcounty[(NYTcounty["Date"] == date) &
                                               (NYTcounty[metric] > 0)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig


            elif scale == "log":

                metric = "log(" + metric + ")"
                quants = NYTcounty[metric][NYTcounty[metric]>=0].quantile(q = [0,1])
                fig = px.choropleth(NYTcounty[(NYTcounty["Date"] == date) &
                                               (NYTcounty[metric] >= 0)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig

        elif view == 'State':
            if scale == "regular":
                quants = NYTstate[metric][NYTstate[metric]>0].quantile(q = [0,1])
                fig = px.choropleth(NYTstate[(NYTstate["Date"] == date) &
                                               (NYTstate[metric] > 0)], 
                                    locations = "StateABV",
                                    locationmode = "USA-states",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"StateABV":False,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (State Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig


            elif scale == "log":

                metric = "log(" + metric + ")"
                quants = NYTstate[metric][NYTstate[metric]>=0].quantile(q = [0,1])
                fig = px.choropleth(NYTstate[(NYTstate["Date"] == date) &
                                               (NYTstate[metric] >= 0)], 
                                    locations = "StateABV",
                                    locationmode = "USA-states",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"StateABV":False,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " in U.S. as of " + str(date) + " (State Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":50,"l":0,"b":0})
                return fig   
        
            
            
            
            
            
############################################################################################################################################################################################   
       
#################### Cases and Deaths Plot ###############
@app.callback(
    Output("USACasesDeaths", 'figure'),
    [Input('USAcasesYaxis','value'),
     Input('USAdeathsYaxis','value'),
     Input("UScasesdeathsScale",'value'),
     Input('USdataSource2', 'value')]
)
def create_CasesVsDeaths_Plot_usa(casesAxis, deathsAxis, scale, source):
    
    if source == "USAFacts":

        if scale == "regular":
            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = usaData["Date"], y = usaData[casesAxis], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = usaData["Date"], y = usaData[deathsAxis], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig

        elif scale == "log":

            casesAxis = "log(" + casesAxis + ")"
            deathsAxis = "log(" + deathsAxis + ")"

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = usaData["Date"], y = usaData[casesAxis], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = usaData["Date"], y = usaData[deathsAxis], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig
        
        
        
        
    elif source == "NYT":
        if scale == "regular":
            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = NYTusa["Date"], y = NYTusa[casesAxis], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = NYTusa["Date"], y = NYTusa[deathsAxis], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig

        elif scale == "log":

            casesAxis = "log(" + casesAxis + ")"
            deathsAxis = "log(" + deathsAxis + ")"

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = NYTusa["Date"], y = NYTusa[casesAxis], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = NYTusa["Date"], y = NYTusa[deathsAxis], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})
            
            return fig
        
############################################################################################################################################################################################
    
################## Mobility Plot #####################
@app.callback(
    Output("USAMobility", 'figure'),
    [Input("USAmobilityMetric", 'value'),
     Input("USdataSource3", 'value')]
)    
def create_MobilityComparison_Plot(value, source):
    
    if source == "USAFacts":
        x = usaData[(usaData["Date"] >= np.min(GoogleUsaMobility["Date"])) & (usaData["Date"] <= np.max(GoogleUsaMobility["Date"]))]

        fig = make_subplots(specs = [[{"secondary_y" : True}]])

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x[value], name = value, line = dict(color = "black", dash = "dot", width = 4),
        ), secondary_y = False)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Retail/Rec Change'], name = "Retail/Recreation", line = dict(color = "yellow"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Grocery/Pharm Change'], name = "Grocery/Pharmacy", line = dict(color = "red"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Parks Change'], name = "Parks", line = dict(color = "green"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Transit Change'], name = "Transit Stations", line = dict(color = "blue"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Workplace Change'], name = "Workplaces", line = dict(color = "purple"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Residential Change'], name = "Residential", line = dict(color = "orange"),
        ), secondary_y = True)

        fig.update_layout(
                title = {'text' : value + " Vs. " + "Community Mobility",
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified", legend_orientation="h",
                margin={"r":0,"t":80,"l":0,"b":0}
            )
        fig.update_xaxes(title_text = "Date", title_standoff = 0)
        fig.update_yaxes(title_text = value, secondary_y = False)
        fig.update_yaxes(title_text = '% Change from Baseline', secondary_y = True)

        return fig
    
    
    
    elif source == "NYT":
        x = NYTusa[(NYTusa["Date"] >= np.min(GoogleUsaMobility["Date"])) & (NYTusa["Date"] <= np.max(GoogleUsaMobility["Date"]))]

        fig = make_subplots(specs = [[{"secondary_y" : True}]])

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x[value], name = value, line = dict(color = "black", dash = "dot", width = 4),
        ), secondary_y = False)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Retail/Rec Change'], name = "Retail/Recreation", line = dict(color = "yellow"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Grocery/Pharm Change'], name = "Grocery/Pharmacy", line = dict(color = "red"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Parks Change'], name = "Parks", line = dict(color = "green"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Transit Change'], name = "Transit Stations", line = dict(color = "blue"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Workplace Change'], name = "Workplaces", line = dict(color = "purple"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleUsaMobility["Date"], y = GoogleUsaMobility['%Residential Change'], name = "Residential", line = dict(color = "orange"),
        ), secondary_y = True)

        fig.update_layout(
                title = {'text' : value + " Vs. " + "Community Mobility",
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified", legend_orientation="h",
                margin={"r":0,"t":80,"l":0,"b":0}
            )
        fig.update_xaxes(title_text = "Date", title_standoff = 0)
        fig.update_yaxes(title_text = value, secondary_y = False)
        fig.update_yaxes(title_text = '% Change from Baseline', secondary_y = True)

        return fig
        
############################################################################################################################################################################################

######### USA Sex bar graph ##########################
@app.callback(
    Output("USAsex", 'figure'),
    [Input("USAchooseSex", 'value')]
)
def create_USAsex_plot(sex):
    
    if sex == "All":
        x = demoDeaths[(demoDeaths["State"] == "United States") & (demoDeaths["Sex"] == "All")]
        
        fig = go.Figure([go.Bar(
            x = x["Age group"], y = x["COVID-19 Deaths"],
            text = x["COVID-19 Deaths"],
            textposition = "auto")])

        fig.update_layout(
            title = {'text' : 'Covid-19 Deaths as of ' + str(x["Data as of"].unique()[0]) + " by Age Group*",
                    'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
             margin={"r":0,"t":80,"l":0,"b":0}
        )
        fig.update_yaxes(title_text = "Covid-19 Deaths")
        
        return fig

    elif sex == "sex":
        x = demoDeaths[(demoDeaths["State"] == "United States") & (demoDeaths["Sex"] != "All")]
        fig = go.Figure(data = [
            go.Bar(name = "Male", x = x["Age group"], y = x['COVID-19 Deaths'][x["Sex"] == "Male"],
                              text = x['COVID-19 Deaths'][x["Sex"] == "Male"], textposition = 'auto'),
            go.Bar(name = "Female", x = x["Age group"], y = x['COVID-19 Deaths'][x["Sex"] == "Female"],
                              text = x['COVID-19 Deaths'][x["Sex"] == "Female"], textposition = 'auto')])
        fig.update_layout(barmode = "group",
                          title = {'text' : 'Covid-19 Deaths as of ' + str(x["Data as of"].unique()[0]) + " by Age Group & Gender*",
                                    'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                          margin={"r":0,"t":80,"l":0,"b":0})
        return fig
###########################################################################################################################################################################################  
    
######### USA Race bar graph #########################
@app.callback(
    Output("USArace", 'figure'),
    [Input('USAraceMetric', 'value')]
)
def create_USArace_plot(metric):
    x = raceDeaths[raceDeaths["State"] == "United States"]
    colors = ['crimson','green','yellow','blue','orange','purple']

    fig = go.Figure(data = [go.Bar(
        x = x["Race"], y = x[metric],
        text = x[metric],
        textposition = "auto",
        marker_color = colors)],)
    
    fig.update_layout(
        title = {'text' : metric + ' as of ' + str(x["Data as of"].unique()[0]) + " by Race*",
                'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
         margin={"r":0,"t":80,"l":0,"b":0}
    )
    fig.update_yaxes(title_text = metric)

    return fig
############################################################################################################################################################################################

#### USA Hospitalization Estimate graph #######################################
@app.callback(
    Output('USAhospital', 'figure'),
    [Input("UShospitalMeasureType", 'value'),
     Input("UShospitalMetric", 'value')]
)
def create_USAHospital_plot(TYPE, metric):
    
    x = hospital[hospital["State"] == "United States"]
        
    if TYPE == "regular":
        
        if metric == "InpatBeds_Occ_AnyPat":
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_LoCI"],
                mode = "lines",
                line_color = "blue",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "blue",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_Est"],
                line_color = "black",
                name = "Estimate"
            ))
        
            ### Availability
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_Est_Avail"],
                mode = "lines",
                line_color = "red",
                name = "Estimated Availability"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Hospital Inpatient Bed Occupancy Estimation**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Hospital Inpatient Bed Occupancy**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
            
            return fig
            
            
        elif metric == "ICUBeds_Occ_AnyPat":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_LoCI"],
                mode = "lines",
                line_color = "green",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "green",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_Est"],
                line_color = "black",
                name = "Estimate"
            ))
        
            ### Availability
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_Est_Avail"],
                mode = "lines",
                line_color = "red",
                name = "Estimated Availability"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "ICU Bed Occupancy Estimation**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "ICU Bed Occupancy**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
            
            
            return fig
            
  
            
        elif metric == "InpatBeds_Occ_COVID":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_COVID_LoCI"],
                mode = "lines",
                line_color = "purple",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_COVID_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "purple",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_COVID_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Number of Patients in an Inpatient Care Location who have Suspected or Confirmed COVID-19 Estimation**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Number of Patients**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
            return fig
    
    
    elif TYPE == "percent":
        
        if metric == "InpatBeds_Occ_AnyPat":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccAnyPat__Numbeds_LoCI"],
                mode = "lines",
                line_color = "blue",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccAnyPat__Numbeds_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "blue",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccAnyPat__Numbeds_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Hospital Inpatient Bed Occupancy Estimation (%)**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Hospital Inpatient Bed Occupancy (%)**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
        
            return fig
            
            
        elif metric == "ICUBeds_Occ_AnyPat":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBedsOccAnyPat__N_ICUBeds_LoCI"],
                mode = "lines",
                line_color = "green",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBedsOccAnyPat__N_ICUBeds_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "green",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBedsOccAnyPat__N_ICUBeds_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "ICU bed occupancy Estimation (%)**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "ICU bed occupancy Occupancy (%)**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
            return fig
  
            
        elif metric == "InpatBeds_Occ_COVID":
                        
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccCOVID__Numbeds_LoCI"],
                mode = "lines",
                line_color = "purple",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccCOVID__Numbeds_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "purple",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccCOVID__Numbeds_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Number of Patients in an Inpatient Care Location who have Suspected or Confirmed COVID-19 Estimation (%)**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Number of Patients (%)",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
        
            return fig

############################################################################################################################################################################################
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
###################################   STATE TAB   ####################################################################################################     
######################################################################################################################################################      
######################################################################################################################################################      
######################################################################################################################################################      
######################################################################################################################################################              
######################################################################################################################################################              
######################################################################################################################################################              
###################################################################################################################################################### 



### Updating date range for map and table selected state #############################################
@app.callback(
    Output('StateMapDate','min_date_allowed'),
    [Input('StateSelect1', 'value'),
     Input('StatedataSource1', 'value')]
)
def set_state_minDate(state, source):
    if source == "USAFacts":
        return stateData["Date"][(stateData["Total Cases"] > 0) & (stateData["State"] == state)].unique().astype(str)[0][:10]
        
    elif source == 'NYT':
        return NYTstate["Date"][(NYTstate["Total Cases"] > 0) & (NYTstate["State"] == state)].unique().astype(str)[0][:10]
        

        
@app.callback(
    Output('StateMapDate','max_date_allowed'),
    [Input('StateSelect1', 'value'),
     Input('StatedataSource1', 'value')]
)
def set_state_maxDate(state, source):
    if source == "USAFacts":
        return stateData["Date"][(stateData["Total Cases"] > 0) & (stateData["State"] == state)].unique().astype(str)[-1][:10]
        
    elif source == 'NYT':
        return NYTstate["Date"][(NYTstate["Total Cases"] > 0) & (NYTstate["State"] == state)].unique().astype(str)[-1][:10]
    
    
    
@app.callback(
    Output('StateMapDate','initial_visible_month'),
    [Input('StateSelect1', 'value'),
     Input('StatedataSource1', 'value')]
)
def set_state_visibleMonth(state, source):
    if source == "USAFacts":
        return stateData["Date"][(stateData["Total Cases"] > 0) & (stateData["State"] == state)].unique().astype(str)[-1][:10]
        
    elif source == 'NYT':
        return NYTstate["Date"][(NYTstate["Total Cases"] > 0) & (NYTstate["State"] == state)].unique().astype(str)[-1][:10]
    

@app.callback(
    Output('StateMapDate','date'),
    [Input('StateSelect1', 'value'),
     Input('StatedataSource1', 'value')]
)
def set_state_date(state, source):
    if source == "USAFacts":
        return stateData["Date"][(stateData["Total Cases"] > 0) & (stateData["State"] == state)].unique().astype(str)[-1][:10]
        
    elif source == 'NYT':
        return NYTstate["Date"][(NYTstate["Total Cases"] > 0) & (NYTstate["State"] == state)].unique().astype(str)[-1][:10]


##############################################################################################################################################################







##### Show selected state ###############
@app.callback(
    Output('SelectedState1', 'children'),
    [Input('StateSelect1', 'value')]
)
def show_selectedState(state):
    return state + ' Covid-19 Analysis'


############# State statistics ###############
@app.callback(
    Output('StateStats', 'children'),
    [Input('StateMapDate', 'date'),
     Input('StatedataSource1', 'value'),
     Input('StateSelect1', 'value')])
def display_StateStats(date, source, state):
    
    if source == "USAFacts":
        data = stateData[stateData["State"] == state]
        totcases = "{:,}".format(int(data["Total Cases"][data["Date"] == date]))
        totdeaths = "{:,}".format(int(data["Total Deaths"][data["Date"] == date]))
        x = 'Total Cases: {} - Total Deaths: {} - (As of {})'.format(totcases, totdeaths, date)
        return x
    
    elif source == "NYT":
        
        if (NYTstate[(NYTstate["State"] == state) & (NYTstate["Date"] == date)].size) == 0:
            x = 'Total Cases: 0 - Total Deaths: 0 - (As of {})'.format(date)
            return x
        else:
            data = NYTstate[NYTstate["State"] == state]
            totcases = "{:,}".format(int(data["Total Cases"][data["Date"] == date]))
            totdeaths = "{:,}".format(int(data["Total Deaths"][data["Date"] == date]))
            x = 'Total Cases: {} - Total Deaths: {} - (As of {})'.format(totcases, totdeaths, date)
            return x
    
    
    
    
# ############################################################################################################################################################################################

############# State data table ################
@app.callback(
    Output('CountySummaryTable', 'data'),
    [Input('StateMapDate', 'date'),
     Input('StatedataSource1', 'value'),
     Input('StateSelect1', 'value')]
)
def update_StateTable(date, source, state):
    
    if source == "USAFacts":
        
        zeroIndex = list(countyData[countyData["Total Cases"]==0].index)
        y = countyData.copy()
        y = y.drop(index = zeroIndex)
        
        if (y[(y["State"] == state) & (y["Date"] == date)].size) == 0:
            x = y[(NYTcounty["Date"] == date) & (y['State'] == state)]
            return x.to_dict("records")
        
        else:
            x = y[(countyData["Date"] == date) & (y['State'] == state)].copy()
            x['Date'] = x["Date"].unique().astype(str)[0][:10]
            return x.to_dict("records")

    elif source == "NYT":

        if (NYTcounty[(NYTcounty["State"] == state) & (NYTcounty["Date"] == date)].size) == 0:
            x = NYTcounty[(NYTcounty["Date"] == date) & (NYTcounty['State'] == state)].copy()
            return x.to_dict("records")
        
        else:
            x = NYTcounty[(NYTcounty["Date"] == date) & (NYTcounty['State'] == state)].copy()
            x['Date'] = x["Date"].unique().astype(str)[0][:10]
            return x.to_dict("records")
    
# ############################################################################################################################################################################################

############### State Map Callback ##################
@app.callback(
    Output('stateMap', 'figure'),
    [Input('StateMapDate', 'date'),
     Input('StatemapScale', 'value'),
     Input('StatemapMetric', 'value'),
     Input('StatedataSource1', 'value'),
     Input('StateSelect1', 'value')]
)
def display_StateMap(date, scale, metric, source, state):
        
    ################## USAFacts.org ############
    if source == "USAFacts":
        if scale == "regular":
            
            if (countyData[(countyData["Date"] == date) & (countyData[metric] > 0) & (countyData['State'] == state)].size) == 0:
                return noneFig
            
            else:
                quants = countyData[metric][countyData['State'] == state].quantile([0,1])
                fig = px.choropleth(countyData[(countyData["Date"] == date) &
                                              (countyData[metric] > 0) &
                                              (countyData['State'] == state)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " in " + state + " as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":60,"l":0,"b":0})
                fig.update_geos(fitbounds = 'locations', visible = True)
                return fig

        elif scale == "log":
            metric = "log(" + metric + ")"
            
            if (countyData[(countyData["Date"] == date) & (countyData[metric] >= 0) & (countyData['State'] == state)].size) == 0:
                return noneFig
            
            else:
                quants = countyData[metric][(countyData['State'] == state) & (countyData[metric] >= 0)].quantile([0,1])
                fig = px.choropleth(countyData[(countyData["Date"] == date) &
                                               (countyData[metric] >= 0) &
                                               (countyData['State'] == state)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " in " + state + " as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":60,"l":0,"b":0})
                fig.update_geos(fitbounds = 'locations', visible = True)
                return fig

       
        
        ############# New York Times ################################
        
    elif source == "NYT":   
        if scale == "regular":
            
            if (NYTcounty[(NYTcounty["Date"] == date) & (NYTcounty[metric] > 0) & (NYTcounty['State'] == state)].size) == 0:
                return noneFig
            
            else: 
                quants = NYTcounty[metric][NYTcounty['State'] == state].quantile([0,1])
                fig = px.choropleth(NYTcounty[(NYTcounty["Date"] == date) &
                                               (NYTcounty[metric] > 0) &
                                              (NYTcounty['State'] == state)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " in " + state + " as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":60,"l":0,"b":0})
                fig.update_geos(fitbounds = 'locations', visible = True)
                return fig


        elif scale == "log":
            metric = "log(" + metric + ")"
            
            if (NYTcounty[(NYTcounty["Date"] == date) & (NYTcounty[metric] >= 0) & (NYTcounty['State'] == state)].size) == 0:
                return noneFig
            
            else:
                quants = NYTcounty[metric][NYTcounty['State'] == state].quantile([0,1])
                fig = px.choropleth(NYTcounty[(NYTcounty["Date"] == date) &
                                               (NYTcounty[metric] >= 0) &
                                              (NYTcounty['State'] == state)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " in " + state + " as of " + str(date) + " (County Level)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":60,"l":0,"b":0})
                fig.update_geos(fitbounds = 'locations', visible = True)
                return fig

#####################################################################################################################################################


#################### Cases and Deaths Plot State ###############
@app.callback(
    Output("StateCasesDeaths", 'figure'),
    [Input('StatecasesYaxis','value'),
     Input('StatedeathsYaxis','value'),
     Input("StatecasesdeathsScale",'value'),
     Input('StatedataSource2', 'value'),
     Input('StateSelect1', 'value')]
)
def create_CasesVsDeaths_Plot_state(casesAxis, deathsAxis, scale, source, state):
    
    if source == "USAFacts":

        if scale == "regular":
            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = stateData["Date"][stateData["State"] == state], y = stateData[casesAxis][stateData["State"] == state], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = stateData["Date"][stateData["State"] == state], y = stateData[deathsAxis][stateData["State"] == state], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig

        elif scale == "log":

            casesAxis = "log(" + casesAxis + ")"
            deathsAxis = "log(" + deathsAxis + ")"

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = stateData["Date"][stateData["State"] == state], y = stateData[casesAxis][stateData["State"] == state], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = stateData["Date"][stateData["State"] == state], y = stateData[deathsAxis][stateData["State"] == state], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig
        
        
        
        
    elif source == "NYT":
        if scale == "regular":
            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = NYTstate["Date"][NYTstate["State"] == state], y = NYTstate[casesAxis][NYTstate["State"] == state], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = NYTstate["Date"][NYTstate["State"] == state], y = NYTstate[deathsAxis][NYTstate["State"] == state], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig

        elif scale == "log":

            casesAxis = "log(" + casesAxis + ")"
            deathsAxis = "log(" + deathsAxis + ")"

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = NYTstate["Date"][NYTstate["State"] == state], y = NYTstate[casesAxis][NYTstate["State"] == state], name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = NYTstate["Date"][NYTstate["State"] == state], y = NYTstate[deathsAxis][NYTstate["State"] == state], name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})
            
            return fig

        
##################################################################################################################################
        
        
################## Mobility Plot #####################
@app.callback(
    Output("StateMobility", 'figure'),
    [Input("StatemobilityMetric", 'value'),
     Input("StatedataSource3", 'value'),
     Input('StateSelect1', 'value')]
)    
def create_MobilityComparison_Plot(value, source, state):
    
    if source == "USAFacts":
        x = stateData[(stateData["Date"] >= np.min(GoogleStateMobility["Date"])) & (stateData["Date"] <= np.max(GoogleStateMobility["Date"]))]

        fig = make_subplots(specs = [[{"secondary_y" : True}]])

        fig.add_trace(go.Scatter(
            x = x["Date"][x['State'] == state], y = x[value][x['State'] == state], name = value, line = dict(color = "black", dash = "dot", width = 4),
        ), secondary_y = False)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Retail/Rec Change'][GoogleStateMobility['State'] == state], name = "Retail/Recreation", line = dict(color = "yellow"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Grocery/Pharm Change'][GoogleStateMobility['State'] == state], name = "Grocery/Pharmacy", line = dict(color = "red"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Parks Change'][GoogleStateMobility['State'] == state], name = "Parks", line = dict(color = "green"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Transit Change'][GoogleStateMobility['State'] == state], name = "Transit Stations", line = dict(color = "blue"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Workplace Change'][GoogleStateMobility['State'] == state], name = "Workplaces", line = dict(color = "purple"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Residential Change'][GoogleStateMobility['State'] == state], name = "Residential", line = dict(color = "orange"),
        ), secondary_y = True)

        fig.update_layout(
                title = {'text' : value + " Vs. " + "Community Mobility",
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified", legend_orientation="h",
                margin={"r":0,"t":80,"l":0,"b":0}
            )
        fig.update_xaxes(title_text = "Date", title_standoff = 0)
        fig.update_yaxes(title_text = value, secondary_y = False)
        fig.update_yaxes(title_text = '% Change from Baseline', secondary_y = True)

        return fig
    
    
    
    elif source == "NYT":
        x = NYTstate[NYTstate["Date"] <= np.max(GoogleStateMobility["Date"])]

        fig = make_subplots(specs = [[{"secondary_y" : True}]])

        fig.add_trace(go.Scatter(
            x = x["Date"][x['State'] == state], y = x[value][x['State'] == state], name = value, line = dict(color = "black", dash = "dot", width = 4),
        ), secondary_y = False)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Retail/Rec Change'][GoogleStateMobility['State'] == state], name = "Retail/Recreation", line = dict(color = "yellow"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Grocery/Pharm Change'][GoogleStateMobility['State'] == state], name = "Grocery/Pharmacy", line = dict(color = "red"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Parks Change'][GoogleStateMobility['State'] == state], name = "Parks", line = dict(color = "green"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Transit Change'][GoogleStateMobility['State'] == state], name = "Transit Stations", line = dict(color = "blue"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Workplace Change'][GoogleStateMobility['State'] == state], name = "Workplaces", line = dict(color = "purple"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = GoogleStateMobility["Date"], y = GoogleStateMobility['%Residential Change'][GoogleStateMobility['State'] == state], name = "Residential", line = dict(color = "orange"),
        ), secondary_y = True)

        fig.update_layout(
                title = {'text' : value + " Vs. " + "Community Mobility",
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified", legend_orientation="h",
                margin={"r":0,"t":80,"l":0,"b":0}
            )
        fig.update_xaxes(title_text = "Date", title_standoff = 0)
        fig.update_yaxes(title_text = value, secondary_y = False)
        fig.update_yaxes(title_text = '% Change from Baseline', secondary_y = True)

        return fig
        
        
        
#########################################################################################################################################################################################################

######### State Sex bar graph ##########################
@app.callback(
    Output("Statesex", 'figure'),
    [ Input('StateSelect1', 'value')]
)
def create_Statesex_plot(state):
    
#     if sex == "All":
#         x = demoDeaths[(demoDeaths["State"] == state) & (demoDeaths["Sex"] == "All")]
        
#         fig = go.Figure([go.Bar(
#             x = x["Age group"], y = x["COVID-19 Deaths"],
#             text = x["COVID-19 Deaths"],
#             textposition = "auto")])

#         fig.update_layout(
#             title = {'text' : 'Covid-19 Deaths as of ' + str(x["Data as of"].unique()[0]) + " by Age Group*",
#                     'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
#              margin={"r":0,"t":80,"l":0,"b":0}
#         )
#         fig.update_yaxes(title_text = "Covid-19 Deaths")
        
#         return fig

#     elif sex == "sex":
        x = demoDeaths[(demoDeaths["State"] == state)]
        fig = go.Figure(data = [
            go.Bar(name = "Male", x = x["Age group"], y = x['COVID-19 Deaths'][x["Sex"] == "Male"],
                              text = x['COVID-19 Deaths'][x["Sex"] == "Male"], textposition = 'auto'),
            go.Bar(name = "Female", x = x["Age group"], y = x['COVID-19 Deaths'][x["Sex"] == "Female"],
                              text = x['COVID-19 Deaths'][x["Sex"] == "Female"], textposition = 'auto')])
        fig.update_layout(barmode = "group",
                          title = {'text' : 'Covid-19 Deaths as of ' + str(x["Data as of"].unique()[0]) + " by Age Group & Gender*",
                                    'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                          margin={"r":0,"t":80,"l":0,"b":0})
        return fig
###########################################################################################################################################################################################  
    
######### State Race bar graph #########################
@app.callback(
    Output("Staterace", 'figure'),
    [Input('StateraceMetric', 'value'),
     Input('StateSelect1', 'value')]
)
def create_Staterace_plot(metric, state):
    
    if ((state == "Alaska") | (state == 'Hawaii')):
        fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = "No Data for " + state, textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=55,
                    color="black")))
        return fig
        
    
    else:
        x = raceDeaths[raceDeaths["State"] == state]
        colors = ['crimson','green','yellow','blue','orange','purple']

        fig = go.Figure(data = [go.Bar(
            x = x["Race"], y = x[metric],
            text = x[metric],
            textposition = "auto",
            marker_color = colors)],)

        fig.update_layout(
            title = {'text' : metric + ' as of ' + str(x["Data as of"].unique()[0]) + " by Race*",
                    'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
             margin={"r":0,"t":80,"l":0,"b":0}
        )
        fig.update_yaxes(title_text = metric)

        return fig
############################################################################################################################################################################################
        
        
#### State Hospitalization Estimate graph #######################################
@app.callback(
    Output('Statehospital', 'figure'),
    [Input("StatehospitalMeasureType", 'value'),
     Input("StatehospitalMetric", 'value'),
     Input('StateSelect1', 'value')]
)
def create_USAHospital_plot(TYPE, metric, state):
    
    x = hospital[hospital["State"] == state]
        
    if TYPE == "regular":
        
        if metric == "InpatBeds_Occ_AnyPat":
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_LoCI"],
                mode = "lines",
                line_color = "blue",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "blue",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_Est"],
                line_color = "black",
                name = "Estimate"
            ))
        
            ### Availability
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_AnyPat_Est_Avail"],
                mode = "lines",
                line_color = "red",
                name = "Estimated Availability"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Hospital Inpatient Bed Occupancy Estimation**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Hospital Inpatient Bed Occupancy**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
            
            return fig
            
            
        elif metric == "ICUBeds_Occ_AnyPat":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_LoCI"],
                mode = "lines",
                line_color = "green",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "green",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_Est"],
                line_color = "black",
                name = "Estimate"
            ))
        
            ### Availability
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBeds_Occ_AnyPat_Est_Avail"],
                mode = "lines",
                line_color = "red",
                name = "Estimated Availability"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "ICU Bed Occupancy Estimation**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "ICU Bed Occupancy**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
            
            
            return fig
            
  
            
        elif metric == "InpatBeds_Occ_COVID":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_COVID_LoCI"],
                mode = "lines",
                line_color = "purple",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_COVID_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "purple",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InpatBeds_Occ_COVID_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Number of Patients in an Inpatient Care Location who have Suspected or Confirmed COVID-19 Estimation**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Number of Patients**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
            return fig
    
    
    elif TYPE == "percent":
        
        if metric == "InpatBeds_Occ_AnyPat":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccAnyPat__Numbeds_LoCI"],
                mode = "lines",
                line_color = "blue",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccAnyPat__Numbeds_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "blue",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccAnyPat__Numbeds_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Hospital Inpatient Bed Occupancy Estimation (%)**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Hospital Inpatient Bed Occupancy (%)**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
        
            return fig
            
            
        elif metric == "ICUBeds_Occ_AnyPat":
            
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBedsOccAnyPat__N_ICUBeds_LoCI"],
                mode = "lines",
                line_color = "green",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBedsOccAnyPat__N_ICUBeds_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "green",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["ICUBedsOccAnyPat__N_ICUBeds_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "ICU bed occupancy Estimation (%)**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "ICU bed occupancy Occupancy (%)**",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
            return fig
  
            
        elif metric == "InpatBeds_Occ_COVID":
                        
            fig = go.Figure()
            
            ### Lower CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccCOVID__Numbeds_LoCI"],
                mode = "lines",
                line_color = "purple",
                name = '95% CI Lower'
            ))

            ### Upper CI
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccCOVID__Numbeds_UpCI"],
                fill = "tonexty",
                mode = 'lines',
                line_color = "purple",
                name = "95% CI Upper"
            ))

            ### Estimate
            fig.add_trace(go.Scatter(
                x = x["Date"],
                y = x["InBedsOccCOVID__Numbeds_Est"],
                line_color = "black",
                name = "Estimate"
            ))
            
            fig.update_layout(hovermode = 'x', legend_orientation="h")
            fig.update_layout(
                title = {'text' : "Number of Patients in an Inpatient Care Location who have Suspected or Confirmed COVID-19 Estimation (%)**",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Number of Patients (%)",
                 margin={"r":0,"t":80,"l":0,"b":0}
            )
        
        
            return fig

############################################################################################################################################################################################
           
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
#############################################################################################################################################################
        
        
        
        
        
        
        
        
        
        
########### County Level Callbacks ###########################################        
        
### Updating Choose county/city
@app.callback(
    Output('ChooseCounty/CityMessage', 'children'),
    [Input('StateSelect2', 'value'),
     Input('CountyDataMaster', 'value')]
)
def display_choose_countyCity(state, source):
    if source == "USAFacts":
        return "Choose County:"
    
    elif source == 'NYT':
        if state == 'New York':
            return 'Choose County/City:'
            
        elif state == 'Missouri':
            return 'Choose County/City:'
            
        else:
            return 'Choose County:'
    
    
    
    
############## Updating county dropdown #####################
    
@app.callback(
    Output('CountySelect', 'options'),
    [Input('StateSelect2', 'value'),
     Input('CountyDataMaster', 'value')]
)
def set_county_Options(state, source):
    if source == 'USAFacts':
        return ([{'label' : county, 'value' : value} for county, value in zip(countyData['County Name'][countyData['State'] == state].unique(), countyData['County Name'][countyData['State'] == state].unique())])
        
    elif source == 'NYT':
        return ([{'label' : county, 'value' : value} for county, value in zip(NYTcounty['County Name'][NYTcounty['State'] == state].unique(), NYTcounty['County Name'][NYTcounty['State'] == state].unique())])
        
@app.callback(
    Output('CountySelect', 'value'),
    [Input('StateSelect2', 'value'),
     Input('CountyDataMaster', 'value')]
)    
def set_county_value(state, source):
    if source == 'USAFacts':
        return countyData['County Name'][countyData['State'] == state].unique()[0]
    
    elif source == 'NYT':
        return NYTcounty['County Name'][NYTcounty['State'] == state].unique()[0]

######################################################################################################################################################################   
    
    

#### Updating Selected County and State  
@app.callback(
    Output('CountyStateSelected', 'children'),
    [Input('StateSelect2', 'value'),
     Input('CountySelect', 'value')]
)
def display_selected_CountyState(state, county):
    if state == 'Alaska':
        return county + ', Alaska Analysis'
        
    elif county == 'New York City':
        return county + ', New York Analysis'
        
    elif county == 'Kansas City':
        return county + ', Missouri Analysis'
        
    elif county == 'Joplin':
        return county + ', Missouri Analysis'
        
    else:
        return county + ' County, ' + state + ' Analysis'
        
######################################################################################################################################################################## 

        
### Updating date range for map and table selected county #############################################
@app.callback(
    Output('CountyMapDate','min_date_allowed'),
    [Input('StateSelect2', 'value'),
     Input('CountySelect', 'value'),
     Input('CountyDataMaster', 'value')]
)
def set_county_minDate(state, county, source):
    if source == "USAFacts":
        return countyData["Date"][(countyData["Total Cases"] > 0) & (countyData["State"] == state) & (countyData['County Name'] == county)].unique().astype(str)[0][:10]
        
    elif source == 'NYT':
        
        if county == 'Unknown':
            return NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[0][:10]
            
        else:
            return NYTcounty["Date"][(NYTcounty["Total Cases"] > 0) & (NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[0][:10]
        

        
@app.callback(
    Output('CountyMapDate','max_date_allowed'),
    [Input('StateSelect2', 'value'),
     Input('CountySelect', 'value'),
     Input('CountyDataMaster', 'value')]
)
def set_county_maxDate(state, county, source):
    if source == "USAFacts":
        return countyData["Date"][(countyData["Total Cases"] > 0) & (countyData["State"] == state) & (countyData['County Name'] == county)].unique().astype(str)[-1][:10]
        
    elif source == 'NYT':
        if county == 'Unknown':
            return NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[-1][:10]
            
        else:
            return NYTcounty["Date"][(NYTcounty["Total Cases"] > 0) & (NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[-1][:10]
    
    
    
@app.callback(
    Output('CountyMapDate','initial_visible_month'),
    [Input('StateSelect2', 'value'),
     Input('CountySelect', 'value'),
     Input('CountyDataMaster', 'value')]
)
def set_county_visibleMonth(state, county, source):
    if source == "USAFacts":
        return countyData["Date"][(countyData["Total Cases"] > 0) & (countyData["State"] == state) & (countyData['County Name'] == county)].unique().astype(str)[-1][:10]
        
    elif source == 'NYT':
        if county == 'Unknown':
            return NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[-1][:10]
            
        else:
            return NYTcounty["Date"][(NYTcounty["Total Cases"] > 0) & (NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[-1][:10]
    

@app.callback(
    Output('CountyMapDate','date'),
    [Input('StateSelect2', 'value'),
     Input('CountySelect', 'value'),
     Input('CountyDataMaster', 'value')]
)
def set_county_date(state, county, source):
    if source == "USAFacts":
        return countyData["Date"][(countyData["Total Cases"] > 0) & (countyData["State"] == state) & (countyData['County Name'] == county)].unique().astype(str)[-1][:10]
        
    elif source == 'NYT':
        if county == 'Unknown':
            return NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[-1][:10]
            
        else:
            return NYTcounty["Date"][(NYTcounty["Total Cases"] > 0) & (NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)].unique().astype(str)[-1][:10]


##############################################################################################################################################################
     
        
        
        
############# County statistics ###############
@app.callback(
    Output('CountyStats', 'children'),
    [Input('CountyMapDate', 'date'),
     Input('CountyDataMaster', 'value'),
     Input('StateSelect2', 'value'),
     Input('CountySelect', 'value')]
)
def display_StateStats(date, source, state, county):
    
    if source == "USAFacts":
        data = countyData[(countyData["State"] == state) & (countyData['County Name'] == county)]
        totcases = "{:,}".format(int(data["Total Cases"][data["Date"] == date]))
        totdeaths = "{:,}".format(int(data["Total Deaths"][data["Date"] == date]))
        x = 'Total Cases: {} - Total Deaths: {} - (As of {})'.format(totcases, totdeaths, date)
        return x
    
    elif source == "NYT":
        
        if (NYTcounty[(NYTcounty["State"] == state) & (NYTcounty["Date"] == date) & (NYTcounty['County Name'] == county)].size) == 0:
            x = 'Total Cases: 0 - Total Deaths: 0 - (As of {})'.format(date)
            return x
        else:
            data = NYTcounty[(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)]
            totcases = "{:,}".format(int(data["Total Cases"][data["Date"] == date]))
            totdeaths = "{:,}".format(int(data["Total Deaths"][data["Date"] == date]))
            x = 'Total Cases: {} - Total Deaths: {} - (As of {})'.format(totcases, totdeaths, date)
            return x     
        
################################################################################################################################################################################################################
        
        
        
############# county data table ################
@app.callback(
    Output('CountyTimeSummaryTable', 'data'),
    [Input('CountyDataMaster', 'value'),
     Input('StateSelect2', 'value'),
     Input('CountySelect', 'value')]
)
def update_CountyTable(source, state, county):
    
    if source == "USAFacts":
        x = countyData[(countyData['State'] == state) & (countyData['County Name'] == county) & (countyData['Total Cases'] > 1)]
        x = x.sort_values(by = 'Date', ascending = False)
        x['Date'] = [date[:10] for date in x["Date"].unique().astype(str)]
        return x.to_dict("records")

    elif source == "NYT":
        
        if county == 'Unknown':
            x = NYTcounty[(NYTcounty['State'] == state) & (NYTcounty['County Name'] == county)]
            x = x.sort_values(by = 'Date', ascending = False)
            x['Date'] = [date[:10] for date in x["Date"].unique().astype(str)]
            return x.to_dict("records")
            
        else:
            x = NYTcounty[(NYTcounty['State'] == state) & (NYTcounty['County Name'] == county) & (NYTcounty['Total Cases'] > 1)]
            x = x.sort_values(by = 'Date', ascending = False)
            x['Date'] = [date[:10] for date in x["Date"].unique().astype(str)]
            return x.to_dict("records")

        
#################################################################################################################################################################################################################



##### County Choropleth Map
        
@app.callback(
    Output('CountyMap', 'figure'),
    [Input('CountyMapDate', 'date'),
     Input('CountymapScale', 'value'),
     Input('CountymapMetric', 'value'),
     Input('CountyDataMaster', 'value'),
     Input('StateSelect2', 'value'),
     Input('CountySelect', 'value')]
)
def display_CountyMap(date, scale, metric, source, state, county):
        
    ################## USAFacts.org ############
    if source == "USAFacts":
        if scale == "regular":
            
            if (countyData[(countyData["Date"] == date) & (countyData[metric] > 0) & (countyData['State'] == state)].size) == 0:
                return noneFig
            
            else:
                quants = stateData[metric][stateData['State'] == state].quantile([0,1])
                fig = px.choropleth(countyData[(countyData["Date"] == date) &
                                              (countyData[metric] > 0) &
                                              (countyData['State'] == state) &
                                              (countyData['County Name'] == county)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True})
                fig.update_layout(title = {'text' : metric + " as of " + str(date) + " (Color Compared to whole State)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":70,"l":0,"b":0})
                fig.update_geos(fitbounds = 'locations', visible = True)
                return fig

        elif scale == "log":
            metric = "log(" + metric + ")"
            
            if (countyData[(countyData["Date"] == date) & (countyData[metric] >= 0) & (countyData['State'] == state)].size) == 0:
                return noneFig
            
            else:
                quants = stateData[metric][(stateData['State'] == state) & (stateData[metric] >= 0)].quantile([0,1])
                fig = px.choropleth(countyData[(countyData["Date"] == date) &
                                               (countyData[metric] >= 0) &
                                               (countyData['State'] == state) &
                                               (countyData['County Name'] == county)], 
                                    geojson = counties, locations = "countyFIPS",
                                    color = str(metric),
                                    color_continuous_scale = ["blue","green","yellow","orange","red"],
                                    range_color = [quants[0], quants[1]],
                                    scope = "usa",
                                    hover_data = {"countyFIPS":False,
                                                  "County Name":True,
                                                  "State":True,
                                                  "Total Cases":True,
                                                  "Total Deaths":True,
                                                  "New Cases":True,
                                                  "New Deaths":True,
                                                  "Population":True,
                                                  "%Cases":True,
                                                  "%Deaths":True,
                                                  "log(Total Cases)":False,
                                                  "log(Total Deaths)":False})
                fig.update_layout(title = {'text' : metric + " as of " + str(date) + " (Color Compared to whole State)",
                                           'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                 margin={"r":0,"t":70,"l":0,"b":0})
                fig.update_geos(fitbounds = 'locations', visible = True)
                return fig

       
        
        ############# New York Times ################################
        
    elif source == "NYT":   
            if (NYTcounty[(NYTcounty["Date"] == date) & (NYTcounty[metric] > 0) & (NYTcounty['State'] == state)].size) == 0:
                return noneFig
            
            else:
                
                if county == 'New York City':
                    fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't map.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=55,
                    color="black")))
                    
                    return fig
                    
                elif county == 'Kansas City':
                    fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't map.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=55,
                    color="black")))
                    
                    return fig
                    
                    
                elif county == 'Joplin':
                    fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't map.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=55,
                    color="black")))
                    
                    return fig
                
                elif county == 'Unknown':
                    fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = "Data Not Assigned to a County. Can't Map.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=55,
                    color="black")))
                    
                    return fig
                    
                    
                        
                else:
                    
                    if scale == "regular":
                        quants = NYTstate[metric][NYTstate['State'] == state].quantile([0,1])
                        fig = px.choropleth(NYTcounty[(NYTcounty["Date"] == date) &
                                                       (NYTcounty[metric] > 0) &
                                                      (NYTcounty['State'] == state) &
                                                      (NYTcounty['County Name'] == county)], 
                                            geojson = counties, locations = "countyFIPS",
                                            color = str(metric),
                                            color_continuous_scale = ["blue","green","yellow","orange","red"],
                                            range_color = [quants[0], quants[1]],
                                            scope = "usa",
                                            hover_data = {"countyFIPS":False,
                                                          "County Name":True,
                                                          "State":True,
                                                          "Total Cases":True,
                                                          "Total Deaths":True,
                                                          "New Cases":True,
                                                          "New Deaths":True,
                                                          "Population":True,
                                                          "%Cases":True,
                                                          "%Deaths":True})
                        fig.update_layout(title = {'text' : metric + " as of " + str(date) + " (Color Compared to whole State)",
                                                   'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                         margin={"r":0,"t":70,"l":0,"b":0})
                        fig.update_geos(fitbounds = 'locations', visible = True)
                        return fig


                    elif scale == "log":
                        metric = "log(" + metric + ")"

                        if (NYTcounty[(NYTcounty["Date"] == date) & (NYTcounty[metric] >= 0) & (NYTcounty['State'] == state)].size) == 0:
                            return noneFig

                        else:
                            quants = NYTstate[metric][NYTstate['State'] == state].quantile([0,1])
                            fig = px.choropleth(NYTcounty[(NYTcounty["Date"] == date) &
                                                           (NYTcounty[metric] >= 0) &
                                                          (NYTcounty['State'] == state) &
                                                          (NYTcounty['County Name'] == county)], 
                                                geojson = counties, locations = "countyFIPS",
                                                color = str(metric),
                                                color_continuous_scale = ["blue","green","yellow","orange","red"],
                                                range_color = [quants[0], quants[1]],
                                                scope = "usa",
                                                hover_data = {"countyFIPS":False,
                                                              "County Name":True,
                                                              "State":True,
                                                              "Total Cases":True,
                                                              "Total Deaths":True,
                                                              "New Cases":True,
                                                              "New Deaths":True,
                                                              "Population":True,
                                                              "%Cases":True,
                                                              "%Deaths":True,
                                                              "log(Total Cases)":False,
                                                              "log(Total Deaths)":False})
                            fig.update_layout(title = {'text' : metric + " as of " + str(date) + " (Color Compared to whole State)",
                                                       'xanchor' : 'auto', 'yanchor' : 'top', 'y' : 0.9, 'x' : 0.45},
                                             margin={"r":0,"t":70,"l":0,"b":0})
                            fig.update_geos(fitbounds = 'locations', visible = True)
                            return fig

######################################################################################################################################################       




#################### Cases and Deaths Plot State ###############
@app.callback(
    Output("CountyCasesDeaths", 'figure'),
    [Input('CountycasesYaxis','value'),
     Input('CountydeathsYaxis','value'),
     Input("CountycasesdeathsScale",'value'),
     Input('CountyDataMaster', 'value'),
     Input('StateSelect2', 'value'),
     Input('CountySelect', 'value')]
)
def create_CasesVsDeaths_Plot_county(casesAxis, deathsAxis, scale, source, state, county):
    
    if source == "USAFacts":

        if scale == "regular":
            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = countyData["Date"][(countyData["State"] == state) & (countyData['County Name'] == county)], 
                           y = countyData[casesAxis][(countyData["State"] == state) & (countyData['County Name'] == county)], 
                           name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = countyData["Date"][(countyData["State"] == state) & (countyData['County Name'] == county)],
                           y = countyData[deathsAxis][(countyData["State"] == state) & (countyData['County Name'] == county)], 
                           name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig

        elif scale == "log":

            casesAxis = "log(" + casesAxis + ")"
            deathsAxis = "log(" + deathsAxis + ")"

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = countyData["Date"][(countyData["State"] == state) & (countyData['County Name'] == county)], 
                           y = countyData[casesAxis][(countyData["State"] == state) & (countyData['County Name'] == county)], 
                           name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = countyData["Date"][(countyData["State"] == state) & (countyData['County Name'] == county)],
                           y = countyData[deathsAxis][(countyData["State"] == state) & (countyData['County Name'] == county)], 
                           name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig
        
        
        
        
    elif source == "NYT":
        if scale == "regular":
            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)], 
                           y = NYTcounty[casesAxis][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)], 
                           name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)],
                           y = NYTcounty[deathsAxis][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)], 
                           name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})

            return fig

        elif scale == "log":

            casesAxis = "log(" + casesAxis + ")"
            deathsAxis = "log(" + deathsAxis + ")"

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(
                go.Scatter(x = NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)], 
                           y = NYTcounty[casesAxis][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)], 
                           name = casesAxis, line = dict(width = 4)),
                secondary_y = False)
            fig.add_trace(
                go.Scatter(x = NYTcounty["Date"][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)],
                           y = NYTcounty[deathsAxis][(NYTcounty["State"] == state) & (NYTcounty['County Name'] == county)], 
                           name = deathsAxis, line = dict(width = 4)),
                secondary_y = True)

            fig.update_layout(
                title = {'text' : casesAxis + " Vs. " + deathsAxis,
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified"
            )
            fig.update_xaxes(title_text = "Date")
            fig.update_yaxes(title_text = casesAxis, secondary_y = False)
            fig.update_yaxes(title_text = deathsAxis, secondary_y = True)
            fig.update_layout(margin={"r":0,"t":80,"l":0,"b":0})
            
            return fig

        
##################################################################################################################################
        


################## Mobility Plot #####################
@app.callback(
    Output("CountyMobility", 'figure'),
    [Input("CountymobilityMetric", 'value'),
     Input("CountyDataMaster", 'value'),
     Input('StateSelect2', 'value'),
     Input('CountySelect', 'value')]
)    
def create_CountyMobilityComparison_Plot(value, source, state, county):
    
    if source == "USAFacts":
        x = countyData[(countyData['State'] == state) & (countyData['County Name'] == county) & (countyData["Date"] <= np.max(GoogleCountyMobility["Date"]))]
        x = x.sort_values(by = 'Date', ascending = False)
        x = x.merge(GoogleCountyMobility, on = ['Date', 'countyFIPS'], how = 'left')
        
        

        fig = make_subplots(specs = [[{"secondary_y" : True}]])

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x[value], name = value, line = dict(color = "black", dash = "dot", width = 4),
        ), secondary_y = False)

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x['%Retail/Rec Change'], name = "Retail/Recreation", line = dict(color = "yellow"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x['%Grocery/Pharm Change'], name = "Grocery/Pharmacy", line = dict(color = "red"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x['%Parks Change'], name = "Parks", line = dict(color = "green"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x['%Transit Change'], name = "Transit Stations", line = dict(color = "blue"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x['%Workplace Change'], name = "Workplaces", line = dict(color = "purple"),
        ), secondary_y = True)

        fig.add_trace(go.Scatter(
            x = x["Date"], y = x['%Residential Change'], name = "Residential", line = dict(color = "orange"),
        ), secondary_y = True)

        fig.update_layout(
                title = {'text' : value + " Vs. " + "Community Mobility",
                         'y' : 0.87, 'x' : 0.45,
                         'xanchor' : 'center', 'yanchor' : 'top'},
                hovermode = "x unified", legend_orientation="h",
                margin={"r":0,"t":80,"l":0,"b":0}
            )
        fig.update_xaxes(title_text = "Date", title_standoff = 0)
        fig.update_yaxes(title_text = value, secondary_y = False)
        fig.update_yaxes(title_text = '% Change from Baseline', secondary_y = True)

        return fig
    
    
    
    elif source == "NYT":
        
        if county == 'New York City':
            fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't compare community mobility data.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=70,
                    color="black")))
                    
            return fig
            
        elif county == 'Kansas City':
            fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't compare community mobility data.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=70,
                    color="black")))
                    
            return fig
            
        elif county == 'Joplin':
            fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't compare community mobility data.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=70,
                    color="black")))
                    
            return fig
            
        elif county == 'Unknown':
            fig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = county + " is not a county. Can't compare community mobility data.", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=70,
                    color="black")))
                    
            return fig
            
        else:      
        
            x = NYTcounty[(NYTcounty['State'] == state) & (NYTcounty['County Name'] == county) & (NYTcounty["Date"] <= np.max(GoogleCountyMobility["Date"]))]
            x = x.sort_values(by = 'Date', ascending = False)
            x = x.merge(GoogleCountyMobility, on = ['Date', 'countyFIPS'], how = 'left')

            fig = make_subplots(specs = [[{"secondary_y" : True}]])

            fig.add_trace(go.Scatter(
            x = x["Date"], y = x[value], name = value, line = dict(color = "black", dash = "dot", width = 4),
            ), secondary_y = False)

            fig.add_trace(go.Scatter(
                x = x["Date"], y = x['%Retail/Rec Change'], name = "Retail/Recreation", line = dict(color = "yellow"),
            ), secondary_y = True)

            fig.add_trace(go.Scatter(
                x = x["Date"], y = x['%Grocery/Pharm Change'], name = "Grocery/Pharmacy", line = dict(color = "red"),
            ), secondary_y = True)

            fig.add_trace(go.Scatter(
                x = x["Date"], y = x['%Parks Change'], name = "Parks", line = dict(color = "green"),
            ), secondary_y = True)

            fig.add_trace(go.Scatter(
                x = x["Date"], y = x['%Transit Change'], name = "Transit Stations", line = dict(color = "blue"),
            ), secondary_y = True)

            fig.add_trace(go.Scatter(
                x = x["Date"], y = x['%Workplace Change'], name = "Workplaces", line = dict(color = "purple"),
            ), secondary_y = True)

            fig.add_trace(go.Scatter(
                x = x["Date"], y = x['%Residential Change'], name = "Residential", line = dict(color = "orange"),
            ), secondary_y = True)

            fig.update_layout(
                    title = {'text' : value + " Vs. " + "Community Mobility",
                             'y' : 0.87, 'x' : 0.45,
                             'xanchor' : 'center', 'yanchor' : 'top'},
                    hovermode = "x unified", legend_orientation="h",
                    margin={"r":0,"t":80,"l":0,"b":0}
                )
            fig.update_xaxes(title_text = "Date", title_standoff = 0)
            fig.update_yaxes(title_text = value, secondary_y = False)
            fig.update_yaxes(title_text = '% Change from Baseline', secondary_y = True)

            return fig

        
        
#########################################################################################################################################################################################################








        
        
        
        
        
        
        
        
        
        
        
        



### Run Dashboard
if __name__ == '__main__':
    app.run_server(debug=False, host='10.26.105.230', port = 8053)
