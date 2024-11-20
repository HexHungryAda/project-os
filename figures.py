import pandas as pd
import plotly.express as px
import hashlib as hl


df = pd.read_csv("Data/athlete_events.csv")

anonymous_name = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
df.insert(1, "Anonymous Name", anonymous_name)
df = df.drop("Name", axis=1)
df = df.rename(columns={"Anonymous Name": "Name"})

aus_df = df[df["NOC"] == "AUS"]
medal_counts_by_sport = df.groupby(["Sport", "NOC", "Medal"]).size().reset_index(name="Count")

def create_australia_chart(selected_feature):
    if selected_feature == "Medal Count":
        medals_per_os = aus_df.groupby(["Games", "Medal"]).size().unstack(level=1, fill_value=0).reset_index()
        medals_per_os['Year'] = medals_per_os['Games'].str.extract(r'(\d{4})').astype(int)
        medals_per_os = medals_per_os.sort_values('Year')
        melted_medals = medals_per_os.melt(id_vars=["Games", "Year"], value_vars=["Bronze", "Gold", "Silver"],
                                           var_name="Medal", value_name="Count")

        fig = px.bar(
            melted_medals,
            x="Games",
            y="Count",
            color="Medal",
            title="Number of Medals per Olympic Games (Australia)",
            labels={"Games": "Olympic Games", "Count": "Number of Medals", "Medal": "Medal Type"},
            color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "brown"}
        )
        fig.update_layout(
            xaxis={"categoryorder": "array", "categoryarray": medals_per_os["Games"].tolist()},
            bargap=0.1, 
            legend_title="Medal Type"
        )
    elif selected_feature == "Average Age":
        fig = px.histogram(
            aus_df, x="Age", nbins=20,
            title="Age Distribution of Australian Athletes",
            labels={"Age": "Age", "count": "Number of Athletes"},
            color_discrete_sequence=["#1f77b4"]
        )
        fig.update_layout(bargap=0.1)
    else:
        fig = px.bar(title="No Data Available")

    return fig


def create_sport_chart(sport):
    sport_medals = medal_counts_by_sport[medal_counts_by_sport["Sport"] == sport]
    medal_count = sport_medals.pivot(index="NOC", columns="Medal", values="Count").fillna(0)
    medal_count["Total"] = medal_count.sum(axis=1)
    top_10_medals = medal_count.nlargest(10, "Total").reset_index()

    fig = px.bar(
        top_10_medals,
        x="NOC",
        y=["Gold", "Silver", "Bronze"],
        title=f"Top 10 Medal-Winning Countries in {sport}",
        labels={"value": "Number of Medals", "variable": "Medal Type"},
        barmode="stack",
        color_discrete_map={"Gold": "gold", "Silver": "silver", "Bronze": "#8c7853"}
    )
    return fig