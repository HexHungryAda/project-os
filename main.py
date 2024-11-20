from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly_express as px
import dash_bootstrap_components as dbc
from figures import create_australia_chart, create_sport_chart


df = pd.read_csv("Data/athlete_events.csv")

unique_sports = sorted(df["Sport"].unique())

app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])


app.layout = html.Div([
    html.H1("Welcome to Team Raygun's Dashboard!"),
    html.Br(),
    html.Div(
        [
            html.Div(
                [
                    html.H2("Filter"),
                    html.Br(),
                    html.Label("Category:"),
                    dcc.Dropdown(
                        id="category-dropdown",
                        placeholder="Select a category",
                        options=[
                            {"label": "Australia", "value": "Australia"},
                            {"label": "Sports", "value": "Sports"}
                        ], className="custom-dropdown-field"
                    ),
                    html.Br(),

                    html.Label("Feature:"),
                    dcc.Dropdown(
                        id="feature-dropdown",
                        placeholder="Select a feature",
                        className="custom-dropdown-field"
                    ),
                ], className="col-2 mt-4"),

            html.Div(
                [
                    dcc.Graph(id="output-graph")
                ], className="col-10")

        ], className="row")

], className="custom-page")


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
        return px.bar(title="Select a Category")


if __name__ == "__main__":
    app.run(debug=True)
