# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df.groupby(['Launch Site'], as_index=False).first()
site_list = []
site_list = ['All'] + launch_sites['Launch Site'].tolist()
site_success = spacex_df[['Launch Site','class']].groupby('Launch Site', as_index=False).count()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': '40px'}),
                                # TASK 1: Add a dropdown list to enable Launch Site
                                # selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div('Launch Site Selection',
                                    style={'color': '#503D36',
                                            'font-weight': 'bold',
                                            'font-size': '16px',
                                            'padding-bottom': '5px',
                                    },
                                ),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label':i, 'value':i} for i in site_list
                                    ],
                                    style={'width': '400px'},
                                    placeholder='Select a Launch Site (Default = All Sites)',
                                    searchable=True,
                                    value='All',
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for 
                                # all sites. If a specific launch site was selected, show the
                                # Success vs. Failed counts for the site

                                html.Div(
                                    id='output_div'
                                    ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0',
                                                        2500: '2500',
                                                        5000: '5000',
                                                        7500: '7500',
                                                        10000: '10000',
                                                        },
                                                value=[0,10000]
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    id='success-payload-scatter-chart'),
                            ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='output_div', component_property='children'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_output_div(input_value):
    if input_value == 'All':
        site_success = spacex_df[['Launch Site','class']].groupby('Launch Site', as_index=False).sum()

        pie_graph = dcc.Graph(
            style={'textAlign': 'center', 'color': '#503D36',
                    'width': '60%'},
            id='success-pie-chart',
            figure=px.pie(site_success,
            title='Total Success Launches by Site',
            names='Launch Site',
            values='class'
            ),
        )
    else:
        site_success = spacex_df[spacex_df['Launch Site'] == input_value]
        site_success = site_success[['Launch Site','class']].groupby('class',as_index=False).count()

        pie_graph = dcc.Graph(
            style={'textAlign': 'center', 'color': '#503D36',
                    'width': '60%'},
            id='success-pie-chart',
            figure=px.pie(site_success,
            title='Success Launches at ' + input_value,
            names='class',
            color=[0,1],
            color_discrete_map={0:'red',
                                1:'blue'},
            values='Launch Site',
            ),
        )

    return pie_graph
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='children'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider',component_property='value')]
)
def update_output_div(site,payload):
    if site == 'All':
        # TODO: select payload by payload input
        site_payload = spacex_df[['Payload Mass (kg)','class','Booster Version Category']]
        site_payload = site_payload[site_payload['Payload Mass (kg)'].between(payload[0],payload[1])]

        scatter_g = dcc.Graph(
            style={'textAlign': 'center', 'color': '#503D36',
                    'width': '95%'},
            id='payload_graph',
            figure= px.scatter(site_payload,
                x=site_payload['Payload Mass (kg)'],
                y=site_payload['class'],
                title='Correlation between Payload and Success for All Sites',
                color=site_payload['Booster Version Category']
            )

        )
    else:
        # TODO: Select site and payload
        #site_success = spacex_df[spacex_df['Launch Site'] == input_value]
        site_payload = spacex_df[spacex_df['Launch Site'] == site]
        site_payload = site_payload[['Payload Mass (kg)','class','Booster Version Category']]
        site_payload = site_payload[site_payload['Payload Mass (kg)'].between(payload[0],payload[1])]

        scatter_g = dcc.Graph(
            style={'textAlign': 'center', 'color': '#503D36',
                    'width': '95%'},
            id='payload_graph',
            figure=px.scatter(site_payload,
                x=site_payload['Payload Mass (kg)'],
                y=site_payload['class'],
                title='Correlation between Payload and Success for All Sites',
                color=site_payload['Booster Version Category']
            ),

        )

    return scatter_g

# Run the app
if __name__ == '__main__':
    app.run_server()
