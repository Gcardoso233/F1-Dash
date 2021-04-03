import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import urllib.request, json 
import re
# https://htmlcheatsheet.com/css/

######################################################Data##############################################################

f1_data = pd.read_csv('F1_data.csv')

laps = pd.read_csv('lap_times.csv')
laps = pd.merge(laps,f1_data[['circuit','full_name','raceId','driverId','year','fastestLapSpeed','fastestLapTime']],on=['raceId','driverId'])

######################################################Interactive Components############################################
#years
year_slider = dcc.Slider(
        id='year_slider',
        min=f1_data['year'].min(),
        max=f1_data['year'].max(),
        marks={str(i): '{}'.format(str(i)) for i in
               [1950, 1960, 1970, 1980, 1990, 2000,2010,2020]},
        value=2020,
        step=1,
    )

#circuits
all_circuit_options={}
for year in list(f1_data['year'].unique()):
    all_circuit_options[year] = list(f1_data[f1_data['year']==year]['circuit'].unique())


circuit_dropdown = dcc.Dropdown(
    id='circuit_dropdown',
    options=[{'label': k, 'value': k} for k in all_circuit_options.keys()],
    value = 'Austrian Grand Prix',
    style={'font-family': 'Helvetica'}
)


driver_options={}
for year in list(f1_data['year'].unique()):
    driver_options[year] = list(f1_data[f1_data['year']==year]['full_name'].unique())

driver_dropdown = dcc.Dropdown(
    id='driver_dropdown',
    options=[{'label': k, 'value': k} for k in driver_options.keys()],
    value='Lewis Hamilton',
    style={'font-family': 'Helvetica'}
)


#######colors

tab_style = {
    'borderTop': '1px solid #242e3f',
    'borderRight': '1px solid #1c212a',
    'borderLeft': '1px solid #1c212a',
    'borderBottom': '1px solid #242e3f',
    'backgroundColor': '#242e3f',
    'color':'white',
    'font-family': "Helvetica",
    'font-size': '1.5em', 

}

tab_selected_style = {
    'borderTop': '4px solid rgb(138, 138, 138)',
    'borderRight': '4px solid rgb(138, 138, 138)',
    'borderLeft': '4px solid rgb(138, 138, 138)',
    'borderBottom': '1px solid #1c212a',

    'backgroundColor': '#1c212a',
    'color': 'white',
    'fontWeight': 'bold',
    'font-family': "Helvetica",
    'font-size': '1.5em', 


    
}
##################################################APP###################################################################

app = dash.Dash(__name__)
app.title = 'Formula One Dash'

server = app.server

app.layout = html.Div([

    html.H1('🏁 Formula 1 History Dashboard 🏁', className='box box_title',style={'font-size': '40px',}),

    html.Div([
        #video 1
        html.Div([
            html.Video(src='/static/pilot_winners.mp4',controls = False,loop=True,width="100%", height="300",autoPlay=True,muted=True),
        ], style={'width': '50%'}, className='box box_graph'),

        html.Div([
            html.Video(src='/static/team_winners.mp4',controls = False,loop=True,width="100%", height="300",autoPlay=True,muted=True),
        ], style={'width': '50%'}, className='box box_graph'),

    ], className='row'),
    

    html.H2('Explore Statistics by Year!', className='box box_graph'),

    html.Div([
            year_slider,
            html.H2([],id='selected_year'),
                ], className='box box_graph'),


    dcc.Tabs([
        dcc.Tab(label='Year Info', children=[
            #div row 1 (inputs + mapa)
            html.Div([
                #coluna 2 (mapa)
                html.Div([
                    dcc.Graph(id='year_map')
                ], className='box box_graph',style={'width':'100%'})
                    
            ], className='row'),

            #div row 2 (posições equipa + driver)
            html.Div([
                dcc.Graph(id='driver_standings', style={'width': '50%'}, className='box box_graph'),

                dcc.Graph(id='teams_standings', style={'width': '50%'}, className='box box_graph')
            ], className='row'),
        ],selected_style = tab_selected_style, style=tab_style),

        #Separador 2
        dcc.Tab(label='Grand Prix', children=[
            #input circuito
            html.Div([
                html.Div([],style={'width':'33%'}),
                html.Div([
                    html.H3('Select the Grand Prix:'),
                    circuit_dropdown,
                ], className='',style={'width':'33%'}),
                html.Div([],style={'width':'33%'}),
            ],className='row'),
            html.Div([
                html.Div([
                    html.H1([],id='circuit_fastlap_text'),
                    html.H3('Year Fastest Lap ⏱'),
                ], style={'width': '33%'}, className='box'),

                html.Div([
                    html.H1([],id='circuit_winner_text'),
                    html.H3('Winner 🥇'),
                ], style={'width': '33%'}, className='box'),
                html.Div([
                    html.H1([],id='circuit_acidents_text'),
                    html.H3('Acidents 💥'),
                ], style={'width': '33%'}, className='box'),
            ],className="row"),

            html.Div([
                html.Div([
                    html.Div([],id='circuit_map')
                ], style={'width': '60%','object-fit': 'contain','display':'flex','justify-content':'center','align-items':'center'}, className='box box_graph'),

                html.Div([
                    html.H1('Historic Fastest Lap Record'),
                    html.Div([
                        html.Div([
                                html.H2([],id='driver_record'),
                                html.H3('Driver'),
                        ],style={'width':'50%'}, className='box'),
                        html.Div([
                            html.H2([],id='lap_record'),
                            html.H3('Lap Time'),
                        ],style={'width':'50%'}, className='box'),
                    ],className='row'),
                    html.Div([
                        html.Div([
                            html.H2([],id='speed_record'),
                            html.H3('Average Speed (Km/h)'),
                        ],style={'width':'50%'}, className='box'),
                        html.Div([
                            html.H2([],id='year_record'),
                            html.H3('Year'),
                        ],style={'width':'50%'}, className='box'),
                    ],className='row'),
                ], style={'width': '40%'}, className='box box_graph'),
            ], className='row'),

        ],selected_style = tab_selected_style, style=tab_style),

        #Separador 3 driver
        dcc.Tab(label='Driver', children=[
            html.Div([
                html.Div([],style={'width':'33%'}),
                html.Div([
                    html.H3('Select your favorite driver:'),
                    driver_dropdown,
                ], className='',style={'width':'33%'}),
                html.Div([],style={'width':'33%'}),
            ],className='row'),
            #caixa
            html.Div([
                html.Div([], style={'width': '0%'}),

                html.Div([
                        #selecionar 
                        html.Div([
                            html.Div([],style={'width': '33%'}),
                            html.Div([
                                    
                                   
                            ], className='',style={'width': '34%'}),
                            html.Div([],style={'width': '33%'}),
                        ],className='row'),
                        
                        #foto
                        html.Div([
                            html.Div([],id='driver_photo', style={'width': '34%','display':'flex','justify-content':'center'}),
                            html.Div([],id='driver_summary', className='box box_graph', style={'width': '66%', 'color':'white', 'text-align': 'justify', 'text-justify': 'inter-word','font-family': 'Helvetica','font-size':'20px'}),

                        ], className='row'),


                        #quick info
                        html.Div([
                            html.Div([
                                html.H1([],id='driver_years'),
                                html.H3('Years in F1'),
                            ], style={'width': '33%'}, className='box'),

                            html.Div([
                                html.H1([],id='driver_races'),
                                html.H3('Nº Races'),
                            ], style={'width': '33%'}, className='box'),

                            html.Div([
                                html.H1([],id='driver_wc'),
                                html.H3('World Champion Titles'),
                            ], style={'width': '33%'}, className='box'),
                        ], className='row'),
                ], style={'width': '100%'}, className='box box_graph'),

                html.Div([], style={'width': '0%'}),
                
            ], className='row'),
            
            html.Div([
                html.Div([
                    dcc.Graph(id='driver_points')
                ],style={'width': '50%'}, className='box box_graph'),
                
                html.Div([
                    dcc.Graph(id='driver_status')
                ],style={'width': '50%'}, className='box box_graph'),
            ], className='row'),
        ],selected_style = tab_selected_style, style=tab_style),    
    ]),
])
######################################################Callbacks#########################################################
@app.callback(
    Output('selected_year', 'children'),
    Input('year_slider', 'value'))
def ret_year(year):
    return html.H4(year)

@app.callback(
    Output('circuit_dropdown', 'options'),
    Input('year_slider', 'value'))
def set_cities_options(selected_year):
    return [{'label': i, 'value': i} for i in all_circuit_options[selected_year]]

@app.callback(
    Output('circuit_dropdown', 'value'),
    Input('circuit_dropdown', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('driver_dropdown', 'options'),
    Input('year_slider', 'value'))
def set_cities_options(selected_year):
    return [{'label': i, 'value': i} for i in driver_options[selected_year]]

@app.callback(
    Output('driver_dropdown', 'value'),
    Input('driver_dropdown', 'options'))
def set_cities_value(available_options):
    return available_options[5]['value']

@app.callback(
    [
        Output("year_map", "figure"),
        Output("driver_standings", "figure"),
        Output("teams_standings", "figure"),
    ],
    [
        Input("year_slider", "value"),
    ]
)
def plots(year):
    ############################################map##########################################################
    plot_data = f1_data[f1_data['year']==year].drop_duplicates(subset=['country'])
    prix_plot_data = f1_data[f1_data['year']==(year)]
    prix = len(prix_plot_data['circuit'].drop_duplicates())
    data_choropleth = dict(type='choropleth',
                           locations=plot_data['country'],
                           locationmode='country names',
                           z=plot_data['round'],
                           colorscale=['red'] * (len(plot_data['round'])+1),
                           showscale= False
                          )

    layout_choropleth = dict(geo=dict(
                                      projection=dict(type='equirectangular'
                                                     ),
                                      showland=True,   
                                      landcolor='white',
                                      lakecolor='#242e3f',
                                      showocean=True,
                                      oceancolor='#242e3f',
                                      showframe=False
                                     ),
                            #autosize=False,
                            #width=500,
                            #height=500,
                            margin=dict(
                                        l=0,
                                        r=0,
                                        b=20,
                                        t=50,
                                            ),
                            dragmode = False,
                            plot_bgcolor = '#242e3f',
                            paper_bgcolor = '#242e3f',
                            font= {'color': 'white','size':15},         
                            title=dict(text=f'{year} Grand Prix Locations ({prix} circuits)',
                                    x=.5 # Title relative position according to the xaxis, range (0,1)
                                    )
                            )
    year_map_plot = go.Figure(data=data_choropleth, layout=layout_choropleth)
    #############################################Driver######################################################

    plot_data = f1_data[f1_data['year']==year]
    plot_data = plot_data[plot_data['round']==plot_data['round'].max()]

    plot_data_1 = f1_data[f1_data['year']==(year-1)]
    plot_data_1 = plot_data_1[plot_data_1['round']==plot_data_1['round'].max()]

    plot_data_2 = f1_data[f1_data['year']==(year-2)]
    plot_data_2 = plot_data_2[plot_data_2['round']==plot_data_2['round'].max()]

    fig_driver = go.Figure()
    fig_driver.add_trace(go.Bar(
        x=plot_data['code'],
        y=plot_data['total_points'],
        name=f'{year}',
        marker_color='#ff0000'
    ))
    fig_driver.add_trace(go.Bar(
        x=plot_data_1['code'],
        y=plot_data_1['total_points'],
        name=f'{year-1}',
        marker_color='#2C4562'
    ))

    fig_driver.update_layout(barmode='group',
                             xaxis_tickangle=-45,
                             xaxis_title="Driver Code",
                             yaxis_title="Points",
                             title={'text':"Driver Standings",
                                    'x':0.5},
                            plot_bgcolor = '#242e3f',
                            paper_bgcolor = '#242e3f',
                            font= {'color': 'white','size':15},
                             )
    driver_stands_plot = fig_driver
    ############################################Teams######################################################

    plot_data = f1_data[f1_data['year']==(year)]
    plot_data = plot_data.groupby('constructor')['points'].sum()
    plot_data = plot_data.sort_values()
    colors = {'Alfa Romeo': '#910002',
              'Ferrari': '#ff0000',
              'AlphaTauri': '#2C4562',
              'Haas F1 Team': '#FFFFFF',
              'McLaren': '#ff9900',
              'Mercedes': '#00D2BE',
              'Racing Point': '#ff00ff',
              'Red Bull': '#1401EE',
              'Renault': 'yellow',
              'Williams': '#015BFF',
              'BMW Sauber': '#010076',
              'Toro Rosso': '#2C4562',
              'Toyota': '#d0003e',
              'Honda': '#030001',
              'Force India': '#ff00ff',
              'Brawn': '#ffff00',
              'Sauber': '#1401EE',
              'Lotus F1': '#cccc00',
              'Jordan': '#ffcc00',
              'BAR': 'white',
              'Benetton': '#003300',
              'Super Aguri': '#cc0000',
              'Marussia': '#800000',
              'Manor Marussia': '#800000',
              'MF1': '#ff3300',
              'Minardi': '#333399',
              'Arrows': '#3366cc',
              'Prost': 'red',
              'Caterham': '#669900',
              'Lotus': '#cccc00',
              'Virgin': '#ff6600',
              'HRT': '#669999',
              'Spyker': '#f5f5f0',
              'Jaguar':'#669900'
             }
    try:
        colors = [colors[k] for k in plot_data.index]
    except:
        colors = px.colors.qualitative.Light24

    fig_team = go.Figure()


    fig_team.add_trace(go.Bar(
        x=plot_data.values,
        y=plot_data.index,
        name=f'{year} World Championship',
        marker_color=colors,
        orientation='h'
    ))

    fig_team.update_layout(barmode='group', xaxis_tickangle=-45,
                            xaxis_title="Points",
                            title={'text':"Team Standings",'x':0.5},
                            plot_bgcolor = '#242e3f',
                            paper_bgcolor = '#242e3f',
                            font= {'color': 'white','size':15},)
                                                                    
    teams_stands_plot = fig_team

    return year_map_plot, \
           driver_stands_plot, \
           teams_stands_plot

@app.callback(
    [           
        Output("circuit_map", "children"),
        Output("circuit_winner_text", "children"),
        Output("circuit_fastlap_text", "children"),
        Output("circuit_acidents_text", "children"),
        Output("driver_record", "children"),
        Output("lap_record", "children"),
        Output("speed_record", "children"),
        Output("year_record", "children"),

    ],
    [
        Input("year_slider", "value"),
        Input("circuit_dropdown", "value"),
    ]
)

def circuit_info(year,gp):
    if gp == 'Eifel Grand Prix':
        lk= 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/N%C3%BCrburgring_-_Grand-Prix-Strecke.svg/600px-N%C3%BCrburgring_-_Grand-Prix-Strecke.svg.png'
        img_link = html.Img(src=lk, style={'height':'100%', 'width':'100%','object-fit': 'contain' }),
    elif gp == 'Tuscan Grand Prix':
        lk= 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Mugello_Racing_Circuit_track_map_15_turns.svg/600px-Mugello_Racing_Circuit_track_map_15_turns.svg.png'
        img_link = html.Img(src=lk, style={'height':'100%', 'width':'100%','object-fit': 'contain' }),
    elif gp == 'Styrian Grand Prix':
        lk= 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Circuit_Red_Bull_Ring.svg/600px-Circuit_Red_Bull_Ring.svg.png'
        img_link = html.Img(src=lk, style={'height':'100%', 'width':'100%','object-fit': 'contain' }),  
    else:
        link_gp_replace = gp.replace(' ', '%20')
        link = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=thumbnail&pithumbsize=600&titles={link_gp_replace}"
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
        
        img_link = html.Img(src=data['query']['pages'][0]['thumbnail']['source'], style={'height':'100%', 'width':'100%','object-fit': 'contain',})

    ###############
    winner = f1_data[(f1_data['year']==year)&(f1_data['circuit']==gp)]
    winner = winner[winner['position']=='1']
    winner_name = winner['full_name'].values[0]
    #####
    fastest = f1_data[(f1_data['year']==year)&(f1_data['circuit']==gp)]
    fastest = fastest[fastest['fastestLapTime'] == fastest['fastestLapTime'].min()]['fastestLapTime'].values[0]
    

    #####
    accidents = f1_data[(f1_data['year']==year)&(f1_data['circuit']==gp)]
    accidents = accidents[(accidents['status']=='Accident')|(accidents['status']=='Collision')|(accidents['status']=='Fatal accident')|(accidents['status']=='Collision damage')]
    accidents = len(accidents)

    ####

    laps_circuit = laps[laps['circuit']==gp]
    laps_circuit['time'] = laps_circuit['time'].replace('\\N','0')
    laps_circuit['time'] = laps_circuit['time'].str.replace(':','').astype(float)

    fastest_ever = laps_circuit[laps_circuit['time']==laps_circuit['time'].min()]

    
    driver_record = fastest_ever['full_name'].values[0]
    lap_record = fastest_ever['fastestLapTime'].values[0]
    speed_record = fastest_ever['fastestLapSpeed'].values[0]
    year_record = fastest_ever['year'].values[0]

    return img_link, \
            winner_name, \
            fastest, \
            accidents, \
            driver_record, \
            lap_record,\
            speed_record,\
            year_record,  


@app.callback(
    [           
        Output("driver_points", "figure"),
        Output("driver_status", "figure"),
        Output("driver_photo", "children"),
        Output("driver_summary", "children"),
        Output("driver_years", "children"),
        Output("driver_races", "children"),
        Output("driver_wc", "children"),


    ],
    [
        Input("driver_dropdown", "value"),
    ]
)
def driver_info(name):
    driver = f1_data[(f1_data['full_name']==name)]
    driver['position'] = driver['position'].replace('\\N','0')
    driver['position'] = driver['position'].astype(int)
    wins = driver[driver['position']==1]
    wins = wins.groupby('year')['position'].sum()

    fig_points = go.Figure()

    fig_points.add_trace(go.Bar(
        x=wins.index,
        y=wins.values,
        name=f'Wins per year',
        marker_color='red',
    ))

    fig_points.update_layout(barmode='group', xaxis_tickangle=-45,
                        yaxis_title="Races Won",
                        title={'text':"Driver wins per year"},
                        plot_bgcolor = '#242e3f',
                        paper_bgcolor = '#242e3f',
                        font= {'color': 'white','size':15},)
#########
    driver = f1_data[(f1_data['full_name']==name)]
    status = driver.groupby('status')['status'].count()

    labels = status.index
    values = status.values

    fig_status = px.pie(values=values, names=labels,
                 title='Most common status by the end a race',
                )
    fig_status.update_traces(textposition='inside', textinfo='percent+label',)
    fig_status.update_layout(plot_bgcolor = '#242e3f',paper_bgcolor = '#242e3f',font= {'color': 'white','size':15})
#########
    link_name_replace = name.replace(' ', '%20')
    link = f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=thumbnail&pithumbsize=500&redirects=1&titles={link_name_replace}"
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
    
    photo_link = html.Img(src=data['query']['pages'][0]['thumbnail']['source'], style={'max-height':'330px', 'width':'auto','object-fit': 'contain',}),
#########

    x = name.replace(' ', '%20')
    link = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={x}"
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        data = data['query']['pages']
        
        values_view = data.values()

        value_iterator = iter(values_view)
        first_value = next(value_iterator)
        summary = first_value['extract']
        text = ' '.join(re.split(r'(?<=[.])\s', summary)[:5])
        text = html.P([text])
##########

    first_year = f1_data[f1_data['full_name']==name]['year'].min()
    last_year = f1_data[f1_data['full_name']==name]['year'].max()
    total_years = last_year - first_year
##########

    n_races = len(f1_data[f1_data['full_name']==name])   
#########
    champions = f1_data.groupby('year')['total_points'].max().to_frame().reset_index().merge(f1_data[['full_name','year','total_points']],on=['year','total_points']).drop_duplicates(subset='year')['full_name'].value_counts()
    try:
        champion = champions[name]
    except:
        champion = 0
    return fig_points, \
            fig_status,\
            photo_link, \
            text, \
            total_years, \
            n_races,\
            champion


if __name__ == '__main__':
    app.run_server(debug=True)
