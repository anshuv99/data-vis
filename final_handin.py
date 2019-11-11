import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table

external_stylesheets = ['bWLwgP.css']
unixReviewTime = ' unixReviewTime'
productID = 'asin'
rating = ' overall'
reviewerID = ' reviewerID'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/'
#     'cb5392c35661370d95f300086accea51/raw/'
#     '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
#     'indicators.csv')

df = pd.read_csv('Musical_Instruments_5.csv')

# Changing unixReviewTime in proper time

df[unixReviewTime] = pd.to_datetime(df[unixReviewTime],unit='s').dt.date

tableDf = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# print(type(df[' unixReviewTime']))

xaxis_column_name = 'Quantity'
axis_type='Linear'
yaxis_column_name = ' rating'


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []

    html_row = []

    html_row.append(html.Td(['abc','dwdwde']))
    table.append(html.Tr(html_row))
    return table



app.layout = html.Div([

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': df[productID][0]}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df[unixReviewTime].min(),
        max=df[unixReviewTime].max(),
        value=df[unixReviewTime].max(),
        marks={str(year): str(year) for year in df[unixReviewTime].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


def create_time_series_quality(dff, axis_type, title, column):
    # print(dff)
    return {
        'data': [go.Scatter(
            x=sorted(dff[unixReviewTime].unique()),
            y=dff.groupby(unixReviewTime)[column].mean(),
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

def create_time_series_quantity(dff, axis_type, title, column):
    # print(dff)
    return {
        'data': [go.Scatter(
            x=sorted(dff[unixReviewTime].unique()),
            y=dff.groupby(unixReviewTime)[column].count(),
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

# @app.callback(
#     Output('datatable-paging-page-count', 'data'),
#     [Input('datatable-paging-page-count', "page_current")
#      ])
# def update_table(page_current):
#     page_current = 1
#     page_size = 20
#     return tableDf.iloc[
#         page_current*page_size:(page_current+ 1)*page_size
#     ].to_dict('records')

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(year):
    # print(type(pd.to_datetime(df[unixReviewTime]).dt.year))
    # dff = df[pd.to_datetime(df[unixReviewTime]).dt.year <= int(year_value)]
    dff = df
    # print(dff[productID].unique())

    return {
        'data': [go.Scatter(
            y=dff.groupby(productID)[rating].mean(),
            x=dff.groupby(productID)[rating].count(),
            text=dff[productID].unique(),
            customdata=dff[productID].unique(),
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }

#Quality
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_y_timeseries(hoverData):
    # print(hoverData)
    hoverProductId = hoverData['points'][0]['customdata']
    dff = df[df[productID] == hoverProductId]
    # dff = dff[rating]
    title = '<b>{}</b><br>{}'.format(hoverProductId, yaxis_column_name)
    return create_time_series_quality(dff, axis_type, title, rating)

#quantity
@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_x_timeseries(hoverData):

    dff = df[df[productID] == hoverData['points'][0]['customdata']]
    # dff = dff.groupby(unixReviewTime).count()
    return create_time_series_quantity(dff, axis_type, xaxis_column_name, rating)



if __name__ == '__main__':

    app.run_server(debug=False)