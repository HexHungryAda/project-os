import pandas as pd
import plotly.express as px 
from dash import Dash, html, dash_table, dcc, callback, Output, Input

df = pd.read_csv('Data/athlete_events.csv')

df_aus = pd.read_csv('~/aus_data.csv')

# Medaljer för enbart Australien
medals_per_os = df_aus.groupby('Medal')['Sport'].count().reset_index()

app = Dash()

app.layout = [
    html.Div#(children='Dashbaord'),
    #dash_table.DataTable(data=df.to_dict('records'), page_size=20),
    #html.Div
    ([
        html.Label('Select Feature:'),
        dcc.Dropdown(
            id='feature-dropdown',
            options=[
                {'label': 'Medal - Sport Count', 'value': 'medals_per_os'}], 
                #[{'label': col, 'value': col} for col in df.columns],
                value='Medal'
        )
    ]),
    dcc.Graph(id='histogram')
]

@app.callback(
    Output(component_id='histogram', component_property='figure'),
    Input(component_id='feature-dropdown', component_property='value'),

)

def update_histogram(selected_feature):

    if selected_feature == 'medals_per_os':
        fig = px.histogram(medals_per_os, x='Medal', y='Sport', histfunc='sum',
                           title='Medals per Sport')
        fig.update_layout(xaxis_title='Medal', yaxis_title='Count of Sport')
    else:
        fig = px.histogram(df, x=selected_feature)
        fig.update_layout(title=f'Histogram of {selected_feature}',
                          xaxis_title=selected_feature,
                          yaxis_title='Frequency')
    
    return fig 

if __name__ == '__main__':
    app.run(debug=True)