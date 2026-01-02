from IPython.display import display

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import plotly.express as px
from src.config.genre_groups import genre_groups


def plot_songsPerCluster(df, dataset_name):
    cluster_counts = df[dataset_name].value_counts().sort_index()
    display(cluster_counts)
    plt.figure(figsize=(6, 4))
    cluster_counts.plot(kind='bar', color='skyblue')
    plt.title("Number of Songs per Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Count")
    plt.show()


def plot_clusters_heatmap(df, dataset_name):
    genres = df["track_genre"].replace(genre_groups)

    genre_cluster_table = pd.crosstab(df[dataset_name], genres)

    plt.figure(figsize=(18, 6))
    sns.heatmap(genre_cluster_table, cmap="YlGnBu", linewidths=0.5, annot=True, fmt="d")
    plt.title("Cluster–Genre Group Distribution (Top Genres)")
    plt.xlabel("Genre Group")
    plt.ylabel("Cluster ID")
    plt.show()


def plot_clusters_bubbleplot(df, dataset_name):
    df["genre_group"] = df["track_genre"].replace(genre_groups)

    genre_cluster_counts = (
        df.groupby([dataset_name, "genre_group"])
        .size()
        .reset_index(name="count")
    )

    fig = px.scatter(
        genre_cluster_counts,
        x=dataset_name,
        y="genre_group",
        size="count",
        color="genre_group",
        hover_name="genre_group",
        color_discrete_sequence=px.colors.qualitative.Vivid + px.colors.qualitative.Prism,
        size_max=70,
    )

    fig.update_traces(marker=dict(line=dict(width=1, color="DarkSlateGrey")))
    fig.update_layout(
        xaxis_title="Cluster ID",
        yaxis_title="Main Genre Group",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        height=750,
    )

    fig.show()


def cluster_genre_stats(df, cluster_col="kmeans_cluster"):
    dist = (
        df
        .groupby([cluster_col, "track_genre"])
        .size()
        .rename("count")
        .reset_index()
    )

    dist["share"] = dist["count"] / dist.groupby(cluster_col)["count"].transform("sum")
    return dist


def dominant_genres(dist, cluster_col="kmeans_cluster"):
    return (
        dist
        .sort_values("count", ascending=False)
        .groupby(cluster_col)
        .first()
        .reset_index()
    )


def show_cluster(dist, cluster_id, cluster_col="kmeans_cluster", top_n=5):
    return (
        dist
        .query(f"{cluster_col} == @cluster_id")
        .sort_values("count", ascending=False)
        .head(top_n)
    )
