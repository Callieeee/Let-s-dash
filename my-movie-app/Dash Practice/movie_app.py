# Import required libraries
# import pickle
# import copy
# import pathlib
import copy
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(
    __name__, meta_tags=[{'name': 'viewport','content': 'width=device-sidth'}],
        external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
)
server = app.server

# Load data
data_path = '/Users/chongchen/Downloads/Dash Practice/data/cleaned_movie_data.csv'
movies = pd.read_csv(data_path)

# Create controls
genres = movies['Genres'].unique()
genre_options = [
    {'label': str(genre),'value': str(genre)} for genre in genres
]


# Create global chart template
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
)


# set tab styles
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


# create app layout
app.layout = html.Div(
    [
        #dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        #html.Div(id='output-clientside'),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url('movie-icon.png'),
                            id='ploty-image',
                            style={
                                'height': '60px',
                                'width': 'auto',
                                'margin-bottom': '25px',
                            },
                        )
                    ],
                    className='one-third column'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    'The Best Movie Site Ever',
                                    style = {'margin-bottom': '0px'},
                                ),
                                html.H5(
                                    'Find the right movie for you',
                                    style = {'margin-top':'0px'}
                                ),
                            ]
                        )
                    ],
                    className='one-half column',
                    id='title',
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Like it", id="like-it-button"),
                            href="https://plot.ly/dash/pricing/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id = 'header',
            className='row flex-display',
            style={'margin-bottom':'25px'},
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs-styled-with-inline", 
                    value='tab-1',
                    children = [
                        dcc.Tab(
                            label='Movie Trend Analysis',
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    'Filter by genre',
                                                    className='control_label'
                                                ),
                                                dcc.RadioItems(
                                                    id='genre_selector',
                                                    options=[
                                                        {'label':'All', 'value':'all'},
                                                        {'label':'Customize','value':'custom'},
                                                    ],
                                                    value='all',
                                                    labelStyle={'display': 'inline-block'},
                                                    className='dcc_control'
                                                ),
                                                dcc.Dropdown(
                                                    id='genres',
                                                    options=genre_options,
                                                    multi=True,
                                                    value=list(genres),
                                                    className='dcc_control'
                                                ),
                                            ],
                                            className='columns',
                                            id='filters_tab1',
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [dcc.Graph(id='count_graph'),],
                                                    className= 'pretty_container six columns',
                                                ),
                                                html.Div(
                                                    [dcc.Graph(id='rating_graph'),],
                                                    className= 'pretty_container six columns',
                                                ),
                                            ],
                                            className='row flex-display',
                                            style={'margin-bottom':'0px', 'display':'flex'},
                                        ),
                                    ],
                                    id='main_graphs',
                                    style={'display':'flex', 'flex-direction':'column'},
                                ),
                            ],
                            style=tab_style, 
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label='Find Movies...',
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P('Filter by release year',className='control_label',),
                                                dcc.RangeSlider(
                                                    id='year_slider',
                                                    min=1921,
                                                    max=2017,
                                                    value=[1921,2017],
                                                    className='dcc_control',
                                                ),
                                                html.P('Filter by ratings', className='control_label',),
                                                dcc.RangeSlider(
                                                    id='rating_slider',
                                                    min=0,
                                                    max=295,
                                                    value=[5,50],
                                                    className='dcc_control'
                                                ),
                                                html.P('Filter by genre', className='control_label'),
                                                dcc.RadioItems(
                                                    id='genre_selector_2',
                                                    options=[
                                                        {'label':'All', 'value':'all'},
                                                        {'label':'Customize','value':'custom'},
                                                    ],
                                                    value='all',
                                                    labelStyle={'display': 'inline-block'},
                                                    className='dcc_control'
                                                ),
                                                dcc.Dropdown(
                                                    id='genres_2',
                                                    options=genre_options,
                                                    multi=True,
                                                    value=list(genres),
                                                    className='dcc_control'
                                                ),
                                            ],
                                            className='columns',
                                            id='filters_tab2',
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Graph(id='movie_table'),
                                                    ],
                                                    className='pretty_container eight columns',
                                                ),
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.H4('Movie Keywords:'),
                                                                html.P(id='update_movie_keywords', children=['Click the movie title to see its keywords']),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.H4('Movie Overview:'),
                                                                html.P(id='update_movie_overview',children=['Click the movie title to see its overview']),
                                                            ],
                                                        )
                                                    ],
                                                    className='pretty_container four columns',
                                                    style={'display':'flex', 'flex-direction':'column'},
                                                ),
                                            ],
                                            className='row flex-display',
                                            style={'margin-bottom':'0px', 'display':'flex'},
                                        ),
                                    ],
                                    id='main_graphs_tab2',
                                    style={'display':'flex', 'flex-direction':'column'},
                                ),
                            ],
                            style=tab_style, 
                            selected_style=tab_selected_style
                        ),
                    ],
                    style = tabs_styles,
                ),
            ],
        ),
    ],
)


# Create callbacks


# Radio -> multi dropdown tab1
@app.callback(
    Output('genres','value'),
    [Input('genre_selector', 'value')]
)
def display_status(genre_selector):
    if genre_selector == 'all':
        return list(genres)
    else:
        return []

# genre_filter -> count graph tab1
@app.callback(
    Output('count_graph','figure'),
    [Input('genres','value'),],
)
def generate_count_graph(genres):

    layout_count = copy.deepcopy(layout)

    counts = movies.groupby(by=['Release year','Genres'])['ID'].count()
    df = counts.to_frame()
    df.reset_index(inplace=True)

    traces = []
    for genre in genres:
        dff = df[df['Genres']==genre]

        data = dict(
            type='bar',
            x=dff['Release year'],
            y=dff['ID'], # count of movies
            name=genre
        ) 

        traces.append(data)

    layout_count["title"] = "Movie Production Trend"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = True
    layout_count["autosize"] = True
    
    figure = dict(data=traces, layout=layout_count)
    return figure


# genre filter -> rating graph tab1
@app.callback(
    Output('rating_graph','figure'),
    [Input('genres','value')],
)
def generate_rating_graph(genres):

    layout_count = copy.deepcopy(layout)

    avg_rating = movies.groupby(by=['Release year','Genres'])['Popularity'].mean()
    df = avg_rating.to_frame()
    df.reset_index(inplace=True)

    traces=[]
    for genre in genres:
        dff = df[df['Genres']==genre]

        data = dict(
            type='markers+line',
            x=dff['Release year'],
            y=dff['Popularity'], # average rating
            name=genre
        ) 

        traces.append(data)

    layout_count["title"] = "Trend of popularity of movies"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = True
    layout_count["autosize"] = True
    
    figure = dict(data=traces, layout=layout_count)
    return figure


# Radio -> multi dropdown tab2
@app.callback(
    Output('genres_2','value'),
    [Input('genre_selector_2', 'value')]
)
def display_status(genre_selector):
    if genre_selector == 'all':
        return list(genres)
    else:
        return []


# year & rating & genre -> movie_tables
@app.callback(
    Output('movie_table','figure'),
    [
        Input('year_slider','value'),
        Input('rating_slider','value'),
        Input('genres_2','value'),
    ],
)
def generate_tables(years,ratings,genres):
    
    #layout_table = copy.deepcopy(layout)

    df = movies[(movies['Release year']>=years[0])&
                (movies['Release year']<= years[1])&
                (movies['Popularity']>= ratings[0])&
                (movies['Popularity']<= ratings[1])&
                (movies['Genres'].isin(genres))][['Title', 'Collection','Spoken Languages','Release year', 'Director','Popularity']]

    data = [
        dict(
            type='table',
            header=dict(
                values=list(df.columns),
                fill=dict(color='#07A3EA'),
                align='left'),
            cells=dict(
                values=[df['Title'], df['Collection'], df['Spoken Languages'], df['Release year'], df['Director'], df['Popularity']],
                fill=dict(color='#E0F1F9'),
                align='left'),
        ),
    ]

    layout = dict(title='Movies Searching Results:')

    figure = dict(data=data, layout=layout)
    return figure

# movie table -> movie keywords
@app.callback(
    Output('update_movie_keywords','children'),
    [Input('movie_table','selectedData')]
)
def update_keywords(selected_data):

    keywords = movies[movies['Title']==selected_data]['Keywords']
    if selected_data is None:
        return 'Click the movie title to see its keywords'
    else:
        return keywords

# movie table -> movie overview
@app.callback(
    Output('update_movie_overview','children'),
    [Input('movie_table','selectedData')],
)
def update_overview(selected_data):

    overview = movies[movies['Title']==selected_data]['Overview']
    if selected_data is None:
        return 'Click the movie title to see its overview'
    else:
        return overview




# Main
if __name__ == "__main__":
    app.run_server(debug=True)