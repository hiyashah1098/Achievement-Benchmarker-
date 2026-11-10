# Achievement Benchmarker

My app helps a small indie studio decide whether to include Steam achievements in an upcoming game by comparing ratings, average playtime, and estimated ownership for games in the same genre with and without achievements.

> A course project for **MIST 4600: Computer Programming in Business** at the University of Georgia's Terry College of Business (Fall 2026).

## Problem
Small indie studios have to decide how to spend limited development time, including whether to build achievements into a new game. It can be hard to know how games with achievements compare to similar games without them. This app gives studios data they can use as a benchmark.

## What it does
My app answers three questions:
1. **Ratings:** Among games in a selected genre, how do average positive-review percentages compare for games with zero achievements versus at least one? Groq also labels a small sample of game descriptions by play mode so ratings can be compared by achievement group and play mode.
2. **Playtime:** How does average playtime compare between those two achievement groups?
3. **Estimated ownership:** How does the lower-bound estimate of ownership compare between those two groups?

## Data
The [Steam Games Dataset](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset) on Kaggle, collected in March 2025. The dataset is shared under the MIT License by its creator, artermiloff. This repo uses `steam_games.csv`, a smaller file made for the course: the 1,000 games with the most reviews.

## Built with
- Python and pandas, in Google Colab
- Groq API for labeling game descriptions by play mode

## How to run it
1. Open `Achievement_Benchmarker.ipynb` in Google Colab.
2. Place `steam_games.csv` in the `MIST4600` folder in your Google Drive.
3. In Colab Secrets, add your Groq API key as `GROQ_API_KEY` and allow notebook access.
4. Run the notebook cells from top to bottom.

## Example output
For the Action genre, the notebook reports:

- **Average positive-review percentage:** 84.90% for games with achievements; 81.52% for games without achievements.
- **Average playtime:** 26.97 hours for games with achievements; 25.20 hours for games without achievements.
- **Average estimated ownership lower bound:** 3,643,738.32 for games with achievements; 4,679,347.83 for games without achievements.

The Groq-powered comparison also returns average positive-review percentages grouped by achievement status and play mode for the sampled games.

## AI Use Disclosure
I used ChatGPT to help explain and draft parts of the code and README. The Groq API labels a small sample of game descriptions as Single-player, Multiplayer, Both, or Unclear. These AI-generated labels may not always be accurate.

## Author
Hiya Shah
