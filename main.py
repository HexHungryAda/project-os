from dash import Dash, html, dcc, Output, Input
import pandas as pd
import dash_bootstrap_components as dbc
from figures import create_empty_figure, create_sports_figure, create_australia_chart


app = Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server

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
                ], style={"maxWidth": "200px"}
            ),
            html.Br(),

            html.Label("Feature:"),
            dcc.Dropdown(
                id="feature-dropdown",
                placeholder="Select a feature",
                style={"maxWidth": "200px"},
                disabled=True
            ),
            html.Br(),

            html.Label("Subfeature:"),
            dcc.Dropdown(
                id="subfeature-dropdown",
                placeholder="Select a sub-feature",
                style={"maxWidth": "200px"},
                disabled=True
            ),

            html.Img(
                src="assets/raygun.png",
                style={"width": "100%", "max-width": "180px", "marginTop": "10px"}
            )
        ], style={"minHeight": "calc(100vh - 145px)"}, className="col-2 p-5 border border-2 border-end custom-filter"),

        html.Div(
            [
                dcc.Graph(id="output-graph")
            ], className="col-9 mt-3")
    ], className="row")
], style={"minWidth": "100%", "maxHeight": "100vh", "overflow-x": "hidden"})


@app.callback(
    Output("feature-dropdown", "disabled"),
    Input("category-dropdown", "value"),
)
def toggle_feature_dropdown(selected_category):
    return selected_category is None


@app.callback(
    Output("subfeature-dropdown", "disabled"),
    Input("category-dropdown", "value"),
    Input("feature-dropdown", "value"),
)
def toggle_subfeature_dropdown(selected_category, selected_feature):
    return not (selected_category == "Sports" and selected_feature)


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
            {"label": "Avg. Age in Olympics", "value": "Average Age"},
            {"label": "Season", "value": "Season"}
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
        if not selected_feature:
            return create_empty_figure("Please select a feature for Australia.")
        return create_australia_chart(selected_feature)

    elif selected_category == "Sports":
        if not selected_feature:
            return create_empty_figure("Please select a feature for Sport.")
        
        if selected_feature and not selected_subfeature:
            return create_empty_figure(f"Please select a sub-feature for {selected_feature}.")
        return create_sports_figure(selected_feature, selected_subfeature)

    else:
        return create_empty_figure("Please select a category.")


if __name__ == "__main__":
    app.run(debug=True)