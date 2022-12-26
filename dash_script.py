# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from doubleaxisgraph import graph
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
app = Dash(__name__)

#Import File
df = pd.read_csv('D:/JMM/03/most_runs_in_cricket.csv')

# Figure 1
run = df[df.Runs>20000][['Player','Runs']].reset_index(drop='index')
fig1 = px.bar(run, x='Runs', y='Player',title='Player Score 20k+ runs in his Career',orientation = 'h')

#Figure 2
runs = df[df['0']>35][['Player','0']].reset_index(drop='index')
fig2 = px.bar(runs, x="Player", y="0", orientation='v',title='Player Most Out on 0 score')

#Figure 3
player = df.iloc[0]
data = dict(
    number=[player['Runs'], player['4s']*4,  player['100']*100,player['50']*50,player['6s']*6,],
    stage=["Total Runs", "Runs with Fours", "Runs with 100s", "Runs with 50s", "Runs with 6s"])
fig3 = px.funnel(data, x='number', y='stage',title=player['Player'])

#Figure 4
fig4 = graph.doubleaxisgraph(df)

#Figure 5
run = df[df.Runs>20000][['Player','Runs','Inns','Mat']].reset_index(drop='index')
fig5 = go.Figure(data=[
    go.Bar(name='Inning Played', x=run['Player'], y=run['Inns']),
    go.Bar(name='Matches Played', x=run['Player'], y=run['Mat'])
])
fig5 = fig5.update_layout(barmode='group')

#Layout
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Most Runs in Cricket'),

    html.Div(children='''
        Player Score Most Runs
    '''),

    dcc.Graph(
        id='Figure1',
        figure=fig1
    )
    ]),

    html.Div([
        
        html.Div(
            children = '''Player who Out Mostly on 0 runs'''
        ),
        dcc.Graph(
            id = 'Figure2',
            figure = fig2
            ),
    ]),

    html.Div([
        dcc.Graph(
            id = 'Figure3',
            figure = fig3
            ),
    ]),

    html.Div([
        dcc.Graph(
            id = 'Figure4',
            figure = fig4
            ),
    ]),
    html.Div([
        dcc.Graph(
            id = 'Figure4',
            figure = fig5
            ),
    ]),
])



# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)




