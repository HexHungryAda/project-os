from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly_express as px
import dash_bootstrap_components as dbc
from figures import create_australia_chart, create_sport_chart


df = pd.read_csv("Data/athlete_events.csv")

unique_sports = sorted(df["Sport"].unique())

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])


app.layout = html.Div([
    html.Div([
        html.H1(
            "Welcome to Team Raygun's Dashboard!", 
                style={"fontSize": "34px"}
        )
    ], className="text-light p-5", style={"backgroundColor": "#214652"}
    ),
    html.Div([
        html.Div([
            html.H2("Filter", style={"fontSize": "28px"}),
            html.Br(),
            html.Label("Category:"),
            dcc.Dropdown(
                id="category-dropdown",
                placeholder="Select a category",
                options=[
                    {"label": "Australia", "value": "Australia"},
                    {"label": "Sports", "value": "Sports"}
                ], style={"maxWidth": "200px"}),

            html.Br(),

            html.Label("Feature:"),
            dcc.Dropdown(
                id="feature-dropdown",
                placeholder="Select a feature",
                style={"maxWidth": "200px"}
            ),

            html.Img(
                src="assets/raygun.png", 
                style={"width": "100%", "marginTop": "10px"}
            )
        ], style={"minHeight": "calc(100vh - 145px)"}, className="col-2 p-5 border border-bottom-0"),

            html.Div(
                [
                    dcc.Graph(id="output-graph")
                ], className="col-9 mt-3")
    ], className="row")
], style={"minWidth": "100%", "minHeight": "100vh", "overflow-x": "hidden"})


@app.callback(
    Output("feature-dropdown", "options"),
    Input("category-dropdown", "value")
)
def update_feature_dropdown(selected_category):
    if selected_category == "Australia":
        return [
            {"label": "Medal Count", "value": "Medal Count"},
            {"label": "Average Age in Olympics", "value": "Average Age"}
        ]
    elif selected_category == "Sports":
        return [{"label": sport, "value": sport} for sport in unique_sports]
    else:
        return []


@app.callback(
    Output("output-graph", "figure"),
    [Input("category-dropdown", "value"),
     Input("feature-dropdown", "value")]
)
def update_graph(selected_category, selected_feature):
    if selected_category == "Australia":
        return create_australia_chart(selected_feature)
    elif selected_category == "Sports" and selected_feature:
        return create_sport_chart(selected_feature)
    else:
        return px.bar(title="Select a filter")


if __name__ == "__main__":
    app.run(debug=True)
