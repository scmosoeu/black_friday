# IMPORTING DASH PACKAGES
import dash
import dash_daq as dq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

# IMPORTING PLOTLY PACKAGES
import plotly.graph_objs as go
import plotly.figure_factory as ff

# IMPORTING OTHER PACKAGES
import pandas as pd
import numpy as np

# LOAD CSV FILE
df = pd.read_csv('data/BlackFriday.csv')

# Changed Marital_Status and Gender for more readability
df['Marital_Status'] = ['Single' if x == 0 else 'Married' for x in df['Marital_Status']]
df['Gender'] = ['Male' if x == 'M' else 'Female' for x in df['Gender']]

# Since the data has blanks representing no purchase of the product by User_ID
# took place, these blanks will be replaced by zero

df.fillna(value=0,inplace=True)

# To convert some of the data to their appropiate format

df['User_ID'] = df['User_ID'].apply(lambda x: str(x))
df['Product_Category_2'] = df['Product_Category_2'].astype(int)
df['Product_Category_3'] = df['Product_Category_3'].astype(int)

# Groupby approach can not be implemented because one customer purchased
# products with different Product_Categories, therefore droping the duplicates
# to get demographics of the database is the way to go

# DEMOGRAPHICS data
demo_df = df.drop_duplicates('User_ID')
demo_df.reset_index(drop=True, inplace=True)

# DASHBOARD APPLICATION
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([
        dcc.RadioItems(
            id='radio_items',
            options=[
                {'label':'Count','value':'counter'},
                {'label':'Purchase','value':'purchase'},
                {'label':'Product Counter','value':'products'}
            ],
            value='counter',
            labelStyle={'display':'inline-block'}
        )
    ],className='overview_header'),

    html.Div([
        html.Div([
            html.Div(id='pie-chart-1',className='charts'),
            html.Div(id='pie-chart-2',className='charts'),
            html.Div(id='bar-chart-1',className='charts')
        ]),

        html.Div([
            html.Div(
                id='bar-chart-2',
                style={'width':'30%','display':'inline-block'}),
            html.Div(
                id='bar-chart-3',
                style={'width':'67%','display':'inline-block'})
        ])
    ])
])

@app.callback(Output('pie-chart-1','children'),
             [Input('radio_items','value')]
)

def gender_count(method):

    if method == 'counter':

        data = [
            go.Pie(
                values=demo_df['Gender'].value_counts(),
                labels=demo_df['Gender'].value_counts().index
            )
        ]

        layout = go.Layout(
            title='Gender Distribution'
        )

    elif method == 'purchase':

        data = [
            go.Pie(
                values=df.groupby('Gender')['Purchase'].sum(),
                labels=df.groupby('Gender')['Purchase'].sum().index
            )
        ]

        layout = go.Layout(
            title='Gender Purchase Distribution'
        )

    else:

        data = [
            go.Pie(
                values=df.groupby('Gender')['Gender'].count(),
                labels=df.groupby('Gender')['Gender'].count().index
            )
        ]

        layout = go.Layout(
            title='Gender Product counter Distribution'
        )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

@app.callback(Output('pie-chart-2','children'),
             [Input('radio_items','value')]
)

def marital_status_count(method):

    if method == 'counter':

        data = [
            go.Pie(
                values=demo_df['Marital_Status'].value_counts(),
                labels=demo_df['Marital_Status'].value_counts().index
            )
        ]

        layout = go.Layout(
            title='Marital Status Distribution'
        )

    elif method == 'purchase':

        data = [
            go.Pie(
                values=df.groupby('Marital_Status')['Purchase'].sum(),
                labels=df.groupby('Marital_Status')['Purchase'].sum().index
            )
        ]

        layout = go.Layout(
            title='Marital Status Purchase Distribution'
        )

    else:

        data = [
            go.Pie(
                values=df.groupby('Marital_Status')['Marital_Status'].count(),
                labels=df.groupby('Marital_Status')['Marital_Status'].count().index
            )
        ]

        layout = go.Layout(
            title='Marital Status Product counter Distribution'
        )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

@app.callback(Output('bar-chart-1','children'),
             [Input('radio_items','value')]
)

def age_count(method):

    if method == 'counter':

        data = [
            go.Bar(
                x= demo_df['Age'].value_counts().index,
                y= demo_df['Age'].value_counts()
            )
        ]

        layout = go.Layout(
            title='Age Distribution'
        )

    elif method == 'purchase':

        data = [
            go.Bar(
                x= df.groupby('Age')['Purchase'].sum().index,
                y= df.groupby('Age')['Purchase'].sum()
            )
        ]

        layout = go.Layout(
            title='Age Purchase Distribution'
        )

    else:

        data = [
            go.Bar(
                x= df['Age'].value_counts().index,
                y= df['Age'].value_counts()
            )
        ]

        layout = go.Layout(
            title='Age Product counter Distribution'
        )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

@app.callback(Output('bar-chart-2','children'),
             [Input('radio_items','value')]
)

def city_category_count(method):

    if method == 'counter':

        data = [
            go.Bar(
                x= demo_df['City_Category'].value_counts().index,
                y= demo_df['City_Category'].value_counts()
            )
        ]

        layout = go.Layout(
            title='City Category Distribution'
        )

    elif method == 'purchase':

        data = [
            go.Bar(
                x= df.groupby('City_Category')['Purchase'].sum().index,
                y= df.groupby('City_Category')['Purchase'].sum()
            )
        ]

        layout = go.Layout(
            title='City Category Purchase Distribution'
        )

    else:

        data = [
            go.Bar(
                x= df['City_Category'].value_counts().index,
                y= df['City_Category'].value_counts()
            )
        ]

        layout = go.Layout(
            title='City Category Product counter Distribution'
        )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

@app.callback(Output('bar-chart-3','children'),
             [Input('radio_items','value')]
)

def occupation_count(method):

    if method == 'counter':

        data = [
            go.Bar(
                x= demo_df['Occupation'].value_counts().index,
                y= demo_df['Occupation'].value_counts()
            )
        ]

        layout = go.Layout(
            title='Occupation Distribution'
        )

    elif method == 'purchase':

        data = [
            go.Bar(
                x= df.groupby('Occupation')['Purchase'].sum().index,
                y= df.groupby('Occupation')['Purchase'].sum()
            )
        ]

        layout = go.Layout(
            title='Occupation Purchase Distribution'
        )

    else:

        data = [
            go.Bar(
                x= df['Occupation'].value_counts().index,
                y= df['Occupation'].value_counts()
            )
        ]

        layout = go.Layout(
            title='Occupation Product counter Distribution'
        )

    return dcc.Graph(
        figure={
            'data':data,
            'layout':layout
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
