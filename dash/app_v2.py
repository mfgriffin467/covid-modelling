import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from textwrap import dedent as d
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read data and create 
df_final = pd.read_csv("df_final.csv", parse_dates=['date'])
#country_list = pd.read_csv("country_list.csv")
#ctry_list = country_list['country'].unique()

df_filt1 = df_final[df_final.days < 20][['date','country','max_pop','beta','actual_cases','projected_infections']].melt(id_vars = ['date', 'country','max_pop','beta'], var_name = 'projection')
df_filt2 = df_final[['date','country','max_pop','beta','projected_susceptible','projected_infections', 'projected_recovered', 'projected_hospitalisation', 'projected_icu', 'projected_beds','projected_fatalities']].melt(id_vars = ['date', 'country','max_pop','beta'], var_name = 'projection')
df_filt3 = df_final[['date','country','max_pop','beta', 'projected_hospitalisation', 'projected_icu', 'projected_beds','projected_fatalities']].melt(id_vars = ['date', 'country','max_pop','beta'], var_name = 'projection')

#country_list['country'].unique()
#df_final = df_final['country'].unique()

app.layout = html.Div([
    html.H1(children='COVID-19 DASHBOARD'),

    html.Div([
    	html.Label(children='Country selection'),
        dcc.Dropdown(
		    id='ctry',
            options=[{'label': i, 'value': i} for i in df_final['country'].unique()],
            value='China'
            ),
        html.Br(),
        html.Label(children='Chart scaling'),
        dcc.RadioItems(
            id='yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
            )
        ]),

    html.Div([
        dcc.Graph(id='graphic1')
        ]),

    html.Div([
        dcc.Graph(id='graphic2')
        ]),


    html.Div([
        dcc.Graph(id='graphic3')
        ]),

    html.Div([
        dcc.Markdown(d('''
        #### NOTES
        - Data sourced from John Hopkins [dashboard](https://coronavirus.jhu.edu/map.html) - refreshed at least daily
        - Simple modelling based on SRI model, assuming mean period of contagion = 10 days, 5 perc hospitalisation rate, 2.5 perc ICU rate, 1 perc fatality rate 
        - ADD changeable R0 by time
        ''')),
    ]),


    html.Div([
        html.Label('Beta selection:'), 
        dcc.Slider(
            id='beta_select',
            min=df_final['beta'].min(),
            max=df_final['beta'].max(),
            step=2.5/100,
            value=0.20,
            marks={i: '{}'.format(i) for i in df_final['beta'].unique().round(3)}
            ),
        ]),

    html.Div([
        html.Br(),
        html.Label('Max population impacted:'), 
        dcc.Slider(
            id='max_pop',
            min=df_final['max_pop'].min(),
            max=df_final['max_pop'].max(),
            step=0.3,
            value=0.5,
            marks={i: '{}'.format(i) for i in df_final['max_pop'].unique()}
            ),
        html.Br()
        ]),


    html.Div([
        dcc.Graph(id='graphic4')
        ]),

    html.Div([
        dcc.Graph(id='graphic5')
        ]),

    html.Div([
        dcc.Graph(id='graphic6')
        ]),

], style={'columnCount': 2})


@app.callback(
	Output('graphic1', 'figure'),
    [Input('ctry', 'value'),
    Input('yaxis-type', 'value')])


def update_cases(ctry,yaxis_type):
	return {
            'data': [dict(
            	x=df_final[df_final.country == ctry]['date'][0:30],
            	y=df_final[df_final.country == ctry]['actual_cases'][0:30],
            	mode='lines+markers',
            	opacity=0.7,
            	marker={
            		'size': 10,
                    'color': 'orange',
            		'line': {'width': 0.5, 'color': 'white'}
                    },
                )
            ],
            'layout': dict(
                title="Covid cases",
                xaxis={'title': 'time'},
                yaxis={
                    'title': 'count',
                    'type': 'linear' if yaxis_type == 'Linear' else 'log'
                    },
                margin={'l': 100, 'b': 40, 't': 100, 'r': 10},
                hovermode='closest'
            )
        }


@app.callback(
    Output('graphic2', 'figure'),
    [Input('ctry', 'value'),
    Input('yaxis-type', 'value')])


def update_deaths(ctry,yaxis_type):
    return {
            'data': [dict(
                x=df_final[df_final.country == ctry]['date'][0:30],
                y=df_final[df_final.country == ctry]['actual_deaths'][0:30],
                mode='lines+markers',
                opacity=0.7,
                marker={
                    'size': 10,
                    'color': 'red',
                    'line': {'width': 0.5, 'color': 'white'}
                    },
                )
            ],
            'layout': dict(
                title="Covid deaths",
                xaxis={'title': 'time'},
                yaxis={
                    'title': 'count',
                    'type': 'linear' if yaxis_type == 'Linear' else 'log'
                    },
                margin={'l': 100, 'b': 40, 't': 100, 'r': 10},
                hovermode='closest'
            )
        }


@app.callback(
    Output('graphic3', 'figure'),
    [Input('ctry', 'value'),
    Input('beta_select', 'value')])


def update_graph(ctry,beta_select):
    return {
            'data': [dict(
                x=df_final[df_final.country == ctry]['date'][0:30],
                y=df_final[df_final.country == ctry]['fatality_rate'][0:30],
                mode='lines+markers',
                opacity=0.7,
                marker={
                    'size': 10,
                    'color': 'red',
                    'line': {'width': 0.5, 'color': 'white'}
                    },
                )
            ],
            'layout': dict(
                title="Raw fatality rate = deaths/cases",
                xaxis={'title': 'time'},
                yaxis={
                    'title': 'fatality rate',
                    'type': 'linear',
                    'tickformat': '.3%'
                    },
                margin={'l': 100, 'b': 40, 't': 100, 'r': 10},
                hovermode='closest'
            )
        }


@app.callback(
    Output('graphic4', 'figure'),
    [Input('ctry', 'value'),
    Input('beta_select', 'value'),
    Input('max_pop','value')])

def update_graph(ctry,beta_select,max_pop):
    return px.line(df_filt1[(df_filt1.country == ctry) & (df_filt1.max_pop == max_pop) & (df_filt1.beta == beta_select)],
        x='date', 
        y='value', 
        color='projection',
        title="Model projections, R0=" + str(beta_select*10))

@app.callback(
    Output('graphic5', 'figure'),
    [Input('ctry', 'value'),
    Input('beta_select', 'value'),
    Input('max_pop','value')])

def update_graph(ctry,beta_select,max_pop):
    return px.line(df_filt2[(df_filt2.country == ctry) & (df_filt2.max_pop == max_pop) & (df_filt2.beta == beta_select)],
        x='date', 
        y='value', 
        color='projection',
        title="Model projections, R0=" + str(beta_select*10))


@app.callback(
    Output('graphic6', 'figure'),
    [Input('ctry', 'value'),
    Input('beta_select', 'value'),
    Input('max_pop','value')])

def update_graph(ctry,beta_select,max_pop):
    return px.line(df_filt3[(df_filt3.country == ctry) & (df_filt3.max_pop == max_pop) & (df_filt3.beta == beta_select)],x='date',y='value',color='projection',
        title="Model projections, R0=" + str(beta_select*10))


#@app.callback(
#    Output('text', 'value'),
#    [Input('ctry', 'value'),
#    Input('beta_select', 'value')])

#def update_text(gamma):
#    return gamma

if __name__ == '__main__':
    app.run_server(debug=True)