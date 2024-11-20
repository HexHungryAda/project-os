from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly_express as px
from figures import create_australia_chart, create_sport_chart


df = pd.read_csv("Data/athlete_events.csv")

unique_sports = sorted(df["Sport"].unique())

app = Dash()

app.layout = html.Div([
    html.Label("Choose Category:"),
    dcc.Dropdown(
        id="category-dropdown",
        options=[
            {"label": "Australia", "value": "Australia"},
            {"label": "Sports", "value": "Sports"}
        ],
        placeholder="Select a category"
    ),
    html.Br(),

    html.Label("Choose Feature:"),
    dcc.Dropdown(
        id="feature-dropdown",
        placeholder="Select a feature"
    ),
    html.Br(),

    dcc.Graph(id="output-graph")
])

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
        return px.bar(title="Select a Category and Feature")

if __name__ == "__main__":
    app.run(debug=True)