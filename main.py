import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input


# Läs in data

df = pd.read_csv("Data/athlete_events.csv")

# Filtrera data för Australien
aus_df = df[df["NOC"] == "AUS"]

# Skapa Dash app
app = Dash()

# Layout för appen
app.layout = html.Div([
    html.Label("Select Feature:"),
    dcc.Dropdown(
        id="feature-dropdown",
        placeholder="Select feature",
        options=[
            {"label": "Medal per OS game", "value": "medals_per_os"},
            {"label": "Age", "value": "Age"},
            {"label": "Top 10 Medals by Sport", "value": "top_10_medals_sport"},
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
    Output("histogram", "figure"),
    Input("feature-dropdown", "value")
)
def update_histogram(selected_feature):

# bara Australien 

    if selected_feature == "medals_per_os":
        medals_per_os = aus_df.groupby("Medal")["Sport"].count().reset_index()
        fig = px.histogram(medals_per_os, x="Medal", y="Sport", histfunc="sum",
                           title="Medals per Sport (Australia)")
        fig.update_layout(xaxis_title="Medal", yaxis_title="Count of Sport")

    elif selected_feature == "Age":
        fig = px.histogram(aus_df, x="Age", title="Age Distribution (Australia)", nbins=20)
        fig.update_layout(xaxis_title="Age", yaxis_title="Frequency")
    
    elif selected_feature == "top_10_medals_sport":
        medal_count = aus_df.groupby("Sport")["Medal"].count().reset_index()
        sorted_medals = medal_count.sort_values("Medal", ascending=False)
        top_10_sports = sorted_medals.head(10)
        fig = px.bar(top_10_sports, x="Sport", y="Medal",
                     title="Top 10 Sports with Most Medals (Australia)")
        fig.update_layout(xaxis_title="Sport", yaxis_title="Number of Medals")

# Alla andra länder 
    elif selected_feature == "Tug_Of_War":
        tug_of_war_df = df[df["Sport"] == "Tug-Of-War"]
        medal_count = tug_of_war_df.groupby("Medal")["Sport"].count().reset_index()
        fig = px.bar(tug_of_war_df, x="Sport", y="Medal",
                     title="Tug-Of-War Medal Count")
        fig.update_layout(xaxis_title="Sport", yaxis_title="Total Medal Count")

    elif selected_feature == "Basketball":
        basketball_df = df[df["Sport"] == "Basketball"]
        medal_count = basketball_df.groupby("Medal")["Sport"].count().reset_index()
        fig = px.bar(medal_count, x="Medal", y="Sport",
                     title="Basketball Medal Count")
        fig.update_layout(xaxis_title="Medal", yaxis_title="Count")

    elif selected_feature == "Ski Jumping":
        ski_jumping_df = df[df["Sport"] == "Ski Jumping"]
        medal_count = ski_jumping_df.groupby("Medal")["Sport"].count().reset_index()
        fig = px.bar(medal_count, x="Medal", y="Sport",
                     title="Ski Jumping Medal Count")
        fig.update_layout(xaxis_title="Medal", yaxis_title="Count")

 
    else:
        rowing_df = df[df["Sport"] == "Rowing"]
        medal_count = rowing_df.groupby("Medal")["Sport"].count().reset_index()
        fig = px.bar(medal_count, x="Medal", y="Sport",
                     title="Rowing Medal Count")
        fig.update_layout(xaxis_title="Medal", yaxis_title="Count")
    
    return fig



if __name__ == "__main__":
    app.run(debug=True)

