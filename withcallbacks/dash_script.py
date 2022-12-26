# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc,Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# from preprocessing import preprocess
import preprocessing as ps
app = Dash(__name__)

#Defining Colors Colors
colors = {
    'background': '#0C090A',
    'graphBackground': '#151B54',
    'text': '#7FDBFF'
}

#Import File
df = ps.preprocess()

#Layout
app.layout = html.Div(className='body',children=[
    html.Div([
        html.Div(className='dropdown',children=[
            dcc.Dropdown(
                df['Country'].unique(),
                'INDIA',
                id='dropdown_country_select',
                className='dropdown-content'
            ),
        ]),
        html.Div([
            html.Table([
                html.Tr([
                    html.Th([dcc.Graph(id='graph_1'),],style={ 'width': '40%'}),
                    html.Th([dcc.Graph(id='graph_2'),],style={ 'width': '45%'}),
                ]),
                html.Tr([
                    html.Th([dcc.Graph(id='graph_5'),],style={ 'width': '40%'}),
                    html.Th([ dcc.Graph(id='graph_4'), ],style={ 'width': '45%'})
                ]), 
            ]),
        ]),
        html.Div(className='dropdown',children=[dcc.Dropdown(id = 'countries',), ]),
        html.Div([dcc.Graph(id='graph_3'),])
    ]),
])


@app.callback(
    Output(component_id='graph_3', component_property='figure'),
    Output(component_id='graph_4', component_property='figure'),
    Output(component_id='graph_5', component_property='figure'),
    Output(component_id='graph_1', component_property='figure'),
    Output(component_id='graph_2', component_property='figure'),
    Output(component_id='countries', component_property='options'),

    [
        Input(component_id='dropdown_country_select', component_property='value'),
        Input(component_id='countries', component_property='value'),
    ]
)

def update_output_div(dropdown_country_select,countries):    
    #Player from different countries
    #graph data is taken from here
    #Graph of Most Player out on 0
    i=df[df['Country']== dropdown_country_select]
    fig2 = px.bar(i, x="Player", y="0", orientation='v',title='Player Most Out on 0 score',)
    fig2 = fig2.update_traces(marker_color='yellow')
    fig2 = fig2.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'},
    plot_bgcolor=colors['graphBackground'],
    paper_bgcolor=colors['graphBackground'],
    font_color=colors['text']
    )

    #Country wise data of players 
    #Line and bar Graph of Runs and Innings Played 
    run = i.reset_index(drop='index')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=run['Player'], y=run['Runs'], name="Total Runs"),
        secondary_y=False,)
    fig.add_trace(
        go.Scatter(x=run['Player'], y=run['Inns'], name="Total Inns"),
        secondary_y=True,)
    fig.update_layout(title_text="Players total Runs with Inns",
    plot_bgcolor=colors['graphBackground'],
    paper_bgcolor=colors['graphBackground'],
    font_color=colors['text'])
    fig.update_xaxes(title_text="Players Name")
    fig.update_yaxes(title_text="Total Runs", secondary_y=False)
    fig.update_yaxes(title_text="Total Inns", secondary_y=True)

    #double bar graph Matches and Innings Played
    fig5 = go.Figure(data=[
    go.Bar(name='Inning Played', x=run['Player'], y=run['Inns']),
    go.Bar(name='Matches Played', x=run['Player'], y=run['Mat'])
    ])
    fig5.update_layout(
        title_text="Total Innings and Matches Played by player",
    barmode='group',xaxis={'categoryorder': 'total descending'},
    plot_bgcolor=colors['graphBackground'],
    paper_bgcolor=colors['graphBackground'],
    font_color=colors['text'])
    fig5.update_xaxes(title_text="Players Name")

    #Figure for Career Span
    fig6 = go.Figure( data=[
    go.Bar(name='Inning Played', x=run['Player'], y=run['Career Span'],text=run['Career Span']),
    ])
    fig6.update_layout(
    title_text="Player Career length",
    barmode='stack',xaxis={'categoryorder': 'total descending'},
    plot_bgcolor=colors['graphBackground'],
    paper_bgcolor=colors['graphBackground'],
    font_color=colors['text'])
    fig6.update_xaxes(title_text="Players Name")
    fig6.update_yaxes(title_text="Career Span")

    #player data with waterfall graph
    play=df[df['Country']== dropdown_country_select]
    play = i.loc[:, ~i.columns.str.contains('^Unnamed')]
    
    if countries == None:
        countries = play.iloc[0]
        countries = countries['Player']
        i=df[df['Player']== countries]
        player = i.loc[:, ~i.columns.str.contains('^Unnamed')]
        ind = player['Player'].index
        i = ind[0]
        play = df.iloc[i]
        fig4 = go.Figure(go.Waterfall(
        name = "Player", orientation = "h", measure = ["relative","relative","relative","relative","absolute","absolute"],
        y = ["Runs with Fours","Runs with 6s", "Runs with 50s","Runs with 100s",'Total runs','Total Ball Faced'],
        x = [play['4s']*4,play['6s']*6,play['50']*50,play['100']*100,play['Runs'],play['BF']],
        decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
        increasing = {"marker":{"color":"white"}},
        totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}}
        ))
        runs = play['Player']
        fig4.update_layout(title = runs,
        plot_bgcolor='#66CCFF',
        paper_bgcolor=colors['graphBackground'],
        font_color=colors['text'])
    else:
        i=df[df['Player']== countries]
        player = i.loc[:, ~i.columns.str.contains('^Unnamed')]
        ind = player['Player'].index
        i = ind[0]
        play = df.iloc[i]
        fig4 = go.Figure(go.Waterfall(
        name = "Player", orientation = "h", measure = ["relative","relative","relative","relative","absolute","absolute"],
        y = ["Runs with Fours","Runs with 6s", "Runs with 50s","Runs with 100s",'Total runs','Total Ball Faced'],
        x = [play['4s']*4,play['6s']*6,play['50']*50,play['100']*100,play['Runs'],play['BF']],
        decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
        increasing = {"marker":{"color":"white"}},
        totals = {"marker":{"color":"deep sky blue", "line":{"color":"blue", "width":3}}}
        ))
        runs = play['Player']
        fig4.update_layout(title = runs,
        plot_bgcolor='#66CCFF',
        paper_bgcolor=colors['graphBackground'],
        font_color=colors['text'])
    return [fig4,fig5,fig6,fig2,fig,run['Player']]

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)



