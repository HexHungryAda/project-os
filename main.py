from dash import Dash, html, dcc, Output, Input
import pandas as pd
from figures import create_australia_chart, create_sport_chart, create_athlete_medal_scatter


df = pd.read_csv("Data/athlete_events.csv")

unique_sports = sorted(df["Sport"].unique())

app = Dash()

app.layout = html.Div([
    html.Label("Choose Category:"),
    dcc.Dropdown(
        id="category-dropdown",
        options=[
            {"label": "Australia", "value": "Australia"},
            {"label": "Sports", "value": "Sports"},
            {"label": "Test", "value": "Test" }
        ],
        placeholder="Select a category",
        value="Australia" # default 
    ),
    html.Br(),

    html.Label("Choose Feature:"),
    dcc.Dropdown(
        id="feature-dropdown",
        placeholder="Select a feature",
        value="Medal Count"
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
    elif selected_category == "Test":
        return [{"label": "Medals vs Weight", "value": "Medals vs Weight"}]
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
    elif selected_category == "Test":
        return create_athlete_medal_scatter("Judo", "Weight")
    else:
        raise Exception("Error: Empty figure selection.") # doesn't quit the app or really display. maybe log it?

if __name__ == "__main__":
    app.run(debug=True, port=8047) # maybe can try except here to get it to show?