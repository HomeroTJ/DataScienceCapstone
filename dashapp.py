# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options = spacex_df['Launch Site'].unique()
options_dic = {}
for value in options:
    options_dic[value] = value

options_dic['All'] = 'All'
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=options_dic, value='All'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id = 'payload-slider', min = 0, max = 10_000, step = 1_000,
                                    marks={0: '0', 
                                           1_000: '1000',
                                           2_000: '2000',
                                           3_000: '3000',
                                           3_000: '3000',
                                           4_000: '4000',
                                           5_000: '5000',
                                           6_000: '6000',
                                           7_000: '7000',
                                           8_000: '8000',
                                           9_000: '9000',
                                           10000:'10000',
                                           }, value=[min_payload,max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(enteredSite):
    filtered_df = spacex_df.groupby('Launch Site').sum()[['class']].reset_index()

    if enteredSite == 'All':
        fig = px.pie(data_frame=filtered_df,values=spacex_df.groupby('Launch Site').sum()[['class']].reset_index()['class'].tolist(),
                     names=spacex_df.groupby('Launch Site').sum()[['class']].reset_index()['Launch Site'].tolist(),
                     title='Succes Rate of all sites')
        return fig
    
    else: 
        fig = px.pie(data_frame= spacex_df[spacex_df['Launch Site'] == enteredSite]['class'].value_counts().reset_index(), values='count', names='class',
                     title=f'Success rate of {enteredSite}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure' ),
    Input(component_id='site-dropdown', component_property='value'),Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart(enteredSide, payload):
    
    if enteredSide == 'All':
        fig = px.scatter(data_frame=spacex_df[(spacex_df['Payload Mass (kg)']<payload[1]) & (spacex_df['Payload Mass (kg)']>payload[0]) ],x='Payload Mass (kg)', y='class', color='Launch Site',
                         title='Correlation between Payload and Success for all sites')
        return fig
    else:
        data_dummy = spacex_df[spacex_df['Launch Site'] == enteredSide] 
        fig = px.scatter(data_frame=data_dummy[(data_dummy['Payload Mass (kg)']<payload[1]) & (data_dummy['Payload Mass (kg)']>payload[0]) ],x='Payload Mass (kg)', y='class',
                         title=f'Correlation between Payload and Success for {enteredSide}')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()