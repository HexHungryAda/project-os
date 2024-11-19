import pandas as pd
import plotly.express as px 
from dash import Dash, html, dash_table, dcc, callback, Output, Input

df = pd.read_csv("Data/athlete_events.csv")

aus_df = df[df["NOC"] == "AUS"]

app = Dash()

app.layout = html.Div([
    html.Label("Select Feature:"),
    dcc.Dropdown(
        id="feature-dropdown",
        options=[
            {"label": "Medal per OS game", "value": "medals_per_os"},
            {"label": "Age", "value": "Age"},
            {"label": "Top 10 Medals by Sport", "value": "top_10_sports"},
            {"label": "Tug-Of-War", "value": "Tug-Of-War"},
            {"label": "Basketball", "value": "Basketball"},
            {"label": "Ski Jumping", "value": "Ski Jumping"},
            {"label": "Rowing", "value": "Rowing"}
        ],
        value="Select Feature"
    ),
    dcc.Graph(id="histogram")
])


@app.callback(
    Output("histogram","figure"),
    Input("feature-dropdown","value"),)


def update_histogram(selected_feature):
# bara australien
    if selected_feature == "medals_per_os":
        medals_per_os = aus_df.groupby("Medal")["Sport"].count().reset_index()
        fig = px.histogram(medals_per_os, x="Medal", y="Sport", histfunc="sum",
                           title="Medals per Sport")
        
        fig.update_layout(xaxis_title="Medal",yaxis_title="Count of Sport")

    elif selected_feature == "Age":

        fig = px.histogram(aus_df, x="Age", title="Age Distribution", nbins=20)

        fig.update_layout(xaxis_title="Age", yaxis_title="Frequency")
    
    elif selected_feature == "top_10_medals_sport":
        medal_count = aus_df.groupby("Sport")["Medal"].count().reset_index()
        sorted_medals = medal_count.sort_values("Medal", ascending=False)
        top_10_sports = sorted_medals.head(10)
        fig = px.histogram(top_10_sports, x="Sport", y="Medal",
                     title="Top 10 Sports with Most Medals")

# alla andra länder 
        
    elif selected_feature == "Tug-Of-War":
        tug_of_war_df = df[df["Sport"] == "Tug-Of-War"]
        fig = px.histogram(tug_of_war_df, x="Year", title="Tug-Of-War Participation Over Time")
        fig.update_layout(xaxis_title="Year", yaxis_title="Frequency")

    elif selected_feature == "Basketball":
        basketball_df = df[df["Sport"] == "Basketball"]
        fig = px.histogram(basketball_df, x="Year", title="Basketball Participation Over Time")
        fig.update_layout(xaxis_title="Year", yaxis_title="Frequency")

    elif selected_feature == "Ski Jumping":
        ski_jumping_df = df[df["Sport"] == "Ski Jumping"]
        fig = px.histogram(ski_jumping_df, x="Year", title="Ski Jumping Participation Over Time")
        fig.update_layout(xaxis_title="Year", yaxis_title="Frequency")
    
    else: 
        rowing_df = df[df["Sport"] == "Rowing"]
        fig = px.histogram(rowing_df, x="Year", title="Rowing Participation Over Time")
        fig.update_layout(xaxis_title="Year", yaxis_title="Frequency")
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)