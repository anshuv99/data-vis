import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['bWLwgP.css']
unixReviewTime = ' unixReviewTime'
productID = 'asin'
rating = ' overall'
reviewerID = ' reviewerID'
metaProductId = 'Product ID'
metaDescription = 'Description'
metaPrice = 'price'
metaCategory = 'Category'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/'
#     'cb5392c35661370d95f300086accea51/raw/'
#     '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
#     'indicators.csv')
global df
if len(sys.argv) == 3:
    df = pd.read_csv(sys.argv[1])
else:
    df = pd.read_csv('Musical_Instruments_5.csv')

# Changing unixReviewTime in proper time

df[unixReviewTime] = pd.to_datetime(df[unixReviewTime], unit='s').dt.date
global metaDf

if(len(sys.argv) == 3):
    metaDf = pd.read_csv(sys.argv[2])
else:
    metaDf = pd.read_csv('Music_Instruments_meta_5.csv')
available_categories = sorted(metaDf[metaCategory].unique())
available_categories.insert(0, 'All')
# print(type(df[' unixReviewTime']))

xaxis_column_name = 'Quantity'
axis_type = 'Linear'
yaxis_column_name = ' rating'

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Distribution', children=[
            html.Div([
                dcc.Upload(id='upload-data',
                           children=html.Button('Upload Data File')),
                dcc.Upload(id='upload-metadata',
                           children=html.Button('Upload Metadata File')),
            ]),
            html.Div([
                dcc.Dropdown(
                    id='category',
                    options=[{'label': i, 'value': i} for i in
                             available_categories],
                    value='All'
                )
            ],
                style={'width': '100%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='crossfilter-indicator-scatter',
                    hoverData={'points': [{'customdata': df[productID][0]}]}
                )
            ], style={'width': '49%', 'display': 'inline-block',
                      'padding': '0 20'}),

            html.Div([
                dcc.Graph(id='x-time-series'),
                dcc.Graph(id='y-time-series'),
            ], style={'display': 'inline-block', 'width': '49%'}),



            html.Div([html.H2(["Product Details"]), html.Table([
                html.Tr([html.Td('Product ID'), html.Td(id='Product ID')]),
                html.Tr([html.Td('Description'), html.Td(id='Description')]),
                html.Tr([html.Td('Price'), html.Td(id='Price')]),
                html.Tr([html.Td('Category'), html.Td(id='Category')]),
            ]),
                      ])
        ]),
        dcc.Tab(label='Trending', children=[

            html.Div([
                dcc.Graph(
                    id='active-reviewers'
                )
            ], style={'width': '49%', 'display': 'inline-block',
                      'padding': '0 20'}),
            html.Div([
                dcc.Graph(
                    id='trending-items-product'
                )
            ], style={'width': '49%', 'display': 'inline-block',
                      'padding': '0 20'}),
            html.Div([
                dcc.Graph(
                    id='customer-low-ratings'
                )
            ], style={'width': '49%', 'display': 'inline-block',
                      'padding': '0 20'}),
            html.Div([
                dcc.Graph(
                    id='customer-high-ratings'
                )
            ], style={'width': '49%', 'display': 'inline-block',
                      'padding': '0 20'}),
        ]),
        dcc.Tab(label='Product Analysis', children=[
            html.Div([
                dcc.Dropdown(
                    id='category-3rd-tab',
                    options=[{'label': i, 'value': i} for i in
                             available_categories],
                    value='All'
                )
            ],
                style={'width': '100%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='product-behaviour'
                )
            ], style={'width': '100%', 'display': 'inline-block',
                      'align': 'center',
                      'padding': '0 20'}),
            html.Div(id='none', children=[], style={'display': 'none'})
        ]),
    ])
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
                'text': 'Rating distribution of the product across time'
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
                'text': 'Review distribution of the product across time'
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('category', 'value')])
def update_graph(category):
    # print(type(pd.to_datetime(df[unixReviewTime]).dt.year))
    # dff = df[pd.to_datetime(df[unixReviewTime]).dt.year <= int(year_value)]
    if (category == 'All'):
        dff = df
    else:
        metaDff = metaDf[metaDf[metaCategory] == category]
        dff = pd.merge(df, metaDff, left_on=productID, right_on=metaProductId)

    return {
        'data': [go.Scatter(
            y=dff.groupby(productID)[rating].mean(),
            x=dff.groupby(productID)[rating].count(),
            text=dff[productID].unique(),
            customdata=dff[productID].unique(),
            mode='markers',
            name='Product Id',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Total no. of reviews',
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'Average rating of the product',
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 30, 'r': 0},
            height=450,
            hovermode='closest',
            showlegend=False,
            title="Rating and Review correlation of the products",
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#000000"
            )
        )
    }


# Quality
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


# quantity
@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_x_timeseries(hoverData):
    dff = df[df[productID] == hoverData['points'][0]['customdata']]
    # dff = dff.groupby(unixReviewTime).count()
    return create_time_series_quantity(dff, axis_type, xaxis_column_name,
                                       rating)


@app.callback(
    dash.dependencies.Output('product-behaviour', 'figure'),
    [dash.dependencies.Input('category-3rd-tab', 'value')])
def display_product_analysis(category):
    if (category == 'All'):
        catDf = df
        metaDff = metaDf
    else:
        metaDff = metaDf[metaDf[metaCategory] == category]
        catDf = pd.merge(df, metaDff, left_on=productID, right_on=metaProductId)

    AverageRating = catDf.groupby(productID)[rating].mean()
    # AverageRating.reset_index(inplace=True)
    TotalReviews = catDf.groupby(productID, as_index=False)[rating].count()

    dff = pd.merge(AverageRating, TotalReviews, left_on=productID,
                   right_on=productID)
    finalMerge = pd.merge(dff, metaDff, left_on=productID,
                          right_on=metaProductId)
    # finalMerge.reset_index(inplace=True, col)
    return {
        'data': [go.Parcoords(
            line=dict(color=finalMerge.iloc[:, 1],
                      colorscale=[[0, 'purple'], [0.5, 'lightseagreen'],
                                  [1, 'gold']]),

            customdata=finalMerge[productID].unique(),


            dimensions=list([
                dict(range=[finalMerge['price'].min(),
                            finalMerge['price'].max()],
                     label='Price', values=finalMerge['price']),
                dict(range=[finalMerge.iloc[:, 2].min(),
                            finalMerge.iloc[:, 2].max()],
                     label='Quantity sold',
                     values=finalMerge.iloc[:, 2]),

                dict(range=[finalMerge.iloc[:, 1].min(),
                            finalMerge.iloc[:, 1].max()],
                     label="Average Rating", values=finalMerge.iloc[:, 1]),




            ]),

        )],

        'layout': go.Layout(

            # margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest',
            title="Correlation among multiple dimensions of a product",
            font=dict(
                family="Courier New, monospace",
                size=20,
                color="#000000"
            )
        )
    }


@app.callback(
    Output('active-reviewers', 'figure'),
    [Input('none', 'children')]
)
def active_reviewers(none):
    innerDf = df.groupby(reviewerID, as_index=False).count()
    innerDdf = innerDf.sort_values(by=[productID], ascending=False)
    return {
        'data': [go.Scatter(
            y=innerDdf.iloc[:, 1].head(),
            x=innerDdf[reviewerID].head(),

            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }

        )],
        'layout': go.Layout(

            xaxis={
                'title': 'Reviewer Id',

            },
            yaxis={
                'title': 'Review Count',

            },
            title="Most active reviewers",
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#000000"
            )

        )
    }


@app.callback(
    Output('trending-items-product', 'figure'),
    [Input('none', 'children')]
)
def trending_product(none):
    innerDf = df.groupby(productID, as_index=False).count()
    innerDdf = innerDf.sort_values(by=[rating], ascending=False)
    return {
        'data': [go.Scatter(
            x=innerDdf.iloc[:, 0].head(),
            y=innerDdf[rating].head(),

            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(

            xaxis={
                'title': 'Product Id',

            },
            yaxis={
                'title': 'Quantity Sold',

            },
            title="Most trending product",
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#000000"
            )

        )
    }


@app.callback(
    Output('customer-low-ratings', 'figure'),
    [Input('none', 'children')]
)
def customer_low_ratings(none):
    innerDf = df.groupby(reviewerID, as_index=False).mean()
    innerDdf = innerDf.sort_values(by=[rating], ascending=True)
    return {
        'data': [go.Scatter(
            x=innerDdf.iloc[:, 0].head(),
            y=innerDdf.iloc[:, 1].head(),

            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(

            xaxis={
                'title': 'Customer Id',

            },
            yaxis={
                'title': 'Average rating',

            },
            title="Customers frequently giving low ratings",
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#000000"
            )

        )
    }


@app.callback(
    Output('customer-high-ratings', 'figure'),
    [Input('none', 'children')]
)
def customer_low_ratings(none):
    innerDf = df.groupby(reviewerID, as_index=False).mean()
    innerDdf = innerDf.sort_values(by=[rating], ascending=False)
    return {
        'data': [go.Scatter(
            x=innerDdf.iloc[:, 0].head(),
            y=innerDdf.iloc[:, 1].head(),

            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(

            xaxis={
                'title': 'Customer Id',

            },
            yaxis={
                'title': 'Average rating',

            },
            title="Customers frequently giving high ratings",
            font=dict(
                family="Courier New, monospace",
                size=10,
                color="#000000"
            )

        )
    }


@app.callback(
    [Output('Product ID', 'children'),
     Output('Description', 'children'),
     Output('Price', 'children'),
     Output('Category', 'children')],
    [Input('crossfilter-indicator-scatter', 'hoverData')])
def display_details(hoverData):
    hoverProductId = hoverData['points'][0]['customdata']
    metaDff = metaDf[metaDf[metaProductId] == hoverProductId]
    return hoverProductId, metaDff[metaDescription], metaDff[metaPrice], \
           metaDff[metaCategory]


if __name__ == '__main__':
    app.run_server(debug=False)
