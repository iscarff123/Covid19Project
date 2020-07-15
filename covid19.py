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
from decimal import Decimal


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
noneFig = go.Figure(go.Scatter(x = [2.5], y = [1.5], text = "No Data - Cases/Deaths = 0", textposition="middle center", mode="text", textfont=dict(
                    family="ariel",
                    size=48,
                    color="black")))
    
    
    
    
    
    

################################################# Create Dashboard #######################################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


### Create Dashboard layout.
def create_layout():
    return html.Div([

        ### Header
        html.H1("Covid-19 Dashboard", style = {'text-align' : 'center'}),
        html.H6('**Data from various sources were used in the creating of this dashboard. Numbers may vary between sources.**',
               style = {'text-align' : 'center'}),
        html.H6("**Dashboard creater(s) is/are not responsible for the validity of the data.**",
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
                        ], style = {"float" : 'left', 'marginLeft' : 100}),
                        
                        html.Div([
                            html.H6("Choose Data Source:"),
                            dcc.RadioItems(id = "USdataSource3",
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
                                clearable = False)  
                        ], style = {"float" : 'center', 'marginLeft' : 800, 'marginRight' : 300}),                 

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

                html.Div(html.H6("*One or more data points have counts between 1–9 and have been suppressed in accordance with NCHS confidentiality standards."))




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
                            dcc.DatePickerSingle(id = "StatemapDate",
                                                 min_date_allowed = stateData["Date"].unique().astype(str)[0][:10],
                                                 max_date_allowed = stateData["Date"].unique().astype(str)[-1][:10],
                                                 initial_visible_month = stateData["Date"].unique().astype(str)[-1][:10],
                                                 date = usaData["Date"].unique().astype(str)[-1][:10])],
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
            dcc.Tab(label = "Data Table", value = "dataTab", children = [


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


            ]) ### Tab 6 Ends

        ])
    ])


    
    
### Generate dashboard
app.layout = create_layout
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


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
def create_CasesVsDeaths_Plot(casesAxis, deathsAxis, scale, source):
    
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
                title = {'text' : "Hospital Inpatient Bed Occupancy Estimation",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Hospital Inpatient Bed Occupancy",
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
                title = {'text' : "ICU Bed Occupancy Estimation",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "ICU Bed Occupancy",
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
                title = {'text' : "Number of Patients in an Inpatient Care Location who have Suspected or Confirmed COVID-19 Estimation",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Number of Patients",
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
                title = {'text' : "Hospital Inpatient Bed Occupancy Estimation (%)",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "Hospital Inpatient Bed Occupancy (%)",
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
                title = {'text' : "ICU bed occupancy Estimation (%)",
                        'y' : 0.87, 'x' : 0.50, 'xanchor' : 'center', 'yanchor' : 'top'},
                xaxis_title = "Date",
                yaxis_title = "ICU bed occupancy Occupancy (%)",
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
                title = {'text' : "Number of Patients in an Inpatient Care Location who have Suspected or Confirmed COVID-19 Estimation (%)",
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
    [Input('StatemapDate', 'date'),
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
    [Input('StatemapDate', 'date'),
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
    [Input('StatemapDate', 'date'),
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
                                    projection = 'mercator',
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
                fig.update_geos(fitbounds = 'locations', visible = False)
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
                                    projection = 'mercator',
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
                fig.update_geos(fitbounds = 'locations', visible = False)
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
                                    projection = 'mercator',
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
                fig.update_geos(fitbounds = 'locations', visible = False)
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
                                    projection = 'mercator',
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
                fig.update_geos(fitbounds = 'locations', visible = False)
                return fig

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        



### Run Dashboard
if __name__ == '__main__':
    app.run_server(debug=True, host='10.26.105.230', port = 8051)
