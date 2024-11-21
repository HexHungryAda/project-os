from dash import Dash, html, dcc, Output, Input
import pandas as pd
from figures import create_empty_figure, create_sports_figure, create_australia_chart

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

    html.Label("Choose Subfeature:"),
    dcc.Dropdown(
        id="subfeature-dropdown",
        placeholder="Select a feature",
    ),
    html.Br(),

    dcc.Graph(id="output-graph")
])

@app.callback(
    [Output("feature-dropdown", "options"),
     Output("subfeature-dropdown", "options")],
    [Input("category-dropdown", "value")]
)
def update_feature_dropdown(selected_category):
    feature_options = []
    subfeature_options = []

    if selected_category == "Australia":
        feature_options = [
            {"label": "Medal Count", "value": "Medal Count"},
            {"label": "Average Age in Olympics", "value": "Average Age"}
        ]
    elif selected_category == "Sports":
        feature_options = [
            {"label": "Judo", "value": "Judo"},
            {"label": "Tug-Of-War", "value": "Tug-Of-War"}
        ]
        subfeature_options = [
            {"label": "Top10 Medals", "value": "Top10 Medals"},
            {"label": "Medals vs Weight", "value": "Medals vs Weight"},
            {"label": "Medals vs Age", "value": "Medals vs Age"},
            {"label": "Medals vs Height", "value": "Medals vs Height"},
        ]
    
    return feature_options, subfeature_options


@app.callback(
    Output("output-graph", "figure"),
    [Input("category-dropdown", "value"),
     Input("feature-dropdown", "value"),
     Input("subfeature-dropdown", "value")]
)
def update_graph(selected_category, selected_feature, selected_subfeature):
    if selected_category == "Australia":
        return create_australia_chart(selected_feature)
    elif selected_category == "Sports" and selected_feature:
        return create_sports_figure(selected_feature, selected_subfeature)
    else:
        return create_empty_figure("Empty")
        
if __name__ == "__main__":
    app.run(debug=True, port=8047)

# there is error when pick sports vs first and then pick australia again. or did I accidentally fix it, can't recreate???
# maybe (speculation) something about not clearing the figures after switch back australia?