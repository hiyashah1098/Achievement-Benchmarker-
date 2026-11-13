from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Achievement Benchmarker",
    page_icon="🏆",
    layout="wide",
)


@st.cache_data
def load_games() -> pd.DataFrame:
    """Load the course dataset stored alongside this app."""
    return pd.read_csv(Path(__file__).with_name("steam_games.csv"))


def prepare_genre_data(games: pd.DataFrame, genre: str) -> pd.DataFrame:
    """Filter games by genre and label their achievement status."""
    genre_games = games[
        games["genres"].str.contains(genre, case=False, na=False, regex=False)
    ].copy()
    genre_games["achievement_group"] = "Has achievements"
    genre_games.loc[
        genre_games["achievements"] == 0, "achievement_group"
    ] = "No achievements"
    return genre_games


def comparison_table(
    games: pd.DataFrame, value_column: str, result_column: str
) -> pd.DataFrame:
    """Calculate an average for each achievement group."""
    return (
        games.groupby("achievement_group", as_index=False)[value_column]
        .mean()
        .rename(columns={value_column: result_column})
        .round(2)
    )


games = load_games()
genres = sorted(
    {
        genre.strip()
        for genre_list in games["genres"].dropna()
        for genre in genre_list.split(",")
        if genre.strip()
    }
)

st.title("🏆 Achievement Benchmarker")
st.write(
    "Compare Steam games in the same genre to see how ratings, playtime, and "
    "estimated ownership differ for games with and without achievements."
)

genre = st.selectbox(
    "Choose a genre",
    genres,
    index=genres.index("Action") if "Action" in genres else 0,
)
genre_games = prepare_genre_data(games, genre)

st.caption(
    f"Analyzing {len(genre_games):,} of the 1,000 most-reviewed games in the "
    f"course dataset that include the {genre} genre."
)

ratings = comparison_table(
    genre_games, "pct_pos_total", "Average positive reviews (%)"
)
playtime = comparison_table(
    genre_games, "avg_playtime_hours", "Average playtime (hours)"
)
ownership = comparison_table(
    genre_games, "owners_low", "Average estimated owners (lower bound)"
)


def show_comparison(
    title: str, explanation: str, table: pd.DataFrame, value_column: str, unit: str
) -> None:
    st.subheader(title)
    st.write(explanation)

    values = table.set_index("achievement_group")[value_column]
    columns = st.columns(2)
    for column, group in zip(
        columns, ["Has achievements", "No achievements"], strict=False
    ):
        value = values.get(group)
        display_value = "N/A" if pd.isna(value) else f"{value:,.2f}{unit}"
        column.metric(group, display_value)

    chart_data = table.set_index("achievement_group")[[value_column]]
    st.bar_chart(chart_data, color="#7C3AED")


tab_ratings, tab_playtime, tab_ownership = st.tabs(
    ["Ratings", "Playtime", "Estimated ownership"]
)

with tab_ratings:
    show_comparison(
        "Average positive-review percentage",
        "A higher value means a larger share of reviews are positive.",
        ratings,
        "Average positive reviews (%)",
        "%",
    )

with tab_playtime:
    show_comparison(
        "Average playtime",
        "Average hours played for games in the selected genre.",
        playtime,
        "Average playtime (hours)",
        " hours",
    )

with tab_ownership:
    show_comparison(
        "Average estimated ownership",
        "Uses the lower bound of each game's estimated-owner range.",
        ownership,
        "Average estimated owners (lower bound)",
        "",
    )

with st.expander("About the data"):
    st.write(
        "This app uses a 1,000-game subset of the Steam Games Dataset collected "
        "in March 2025. These comparisons show associations in this dataset and "
        "do not prove that achievements cause a game to perform differently."
    )
    st.markdown(
        "[View the dataset source on Kaggle]"
        "(https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)"
    )
