import matplotlib.pyplot as plt
import pandas as pd

df_1 = pd.read_csv("2000.csv")
df_2 = pd.read_csv("2010.csv")

df_1["decade"] = "2000s"
df_2["decade"] = "2010s"

df = pd.concat([df_1,df_2],ignore_index=True)

print("data set uploaded")
print(df.info())
print(df.head())

#data cleaning
df.drop_duplicates(inplace = True)
df.fillna(df.mean(numeric_only= True), inplace= True)

#summary
print("summary stats")
print(df.groupby("decade")[["bpm","nrgy", "dnce", "dB","val", "acous", "spch", "pop"]].mean().round(2))

#comparission
att = ["bpm","nrgy", "dnce", "dB","val", "acous", "spch", "pop"]
mean_val = df.groupby("decade")[att].mean()

mean_val.plot(kind = "bar", figsize=(12,6))
plt.title1 = ("Average song attribute by decades")
plt.ylabel("average value", fontsize = 12)
plt.xlabel("decade", fontsize = 12)
plt.legend(title = "Attributes")
plt.grid(axis = "y", linestyle = "--", alpha = 0.6)
plt.savefig("images/average_song_attributes_by_decades.png", dpi = 300, bbox_inches = "tight")
plt.show()

#popularity
plt.figure(figsize=(8, 5))
for decade in df['decade'].unique():
    plt.hist(df[df['decade'] == decade]['pop'], bins=15, alpha=0.6, label=decade)
plt.title("Popularity Distribution (2000s vs 2010s)")
plt.xlabel("Popularity")
plt.ylabel("Number of Songs")
plt.legend()
plt.savefig("images/Popularity_Distribution_(2000s_vs_2010s).png", dpi = 300, bbox_inches = "tight")
plt.show()

#energy vs danceibility
plt.figure(figsize = (8,6))
for decade, color in zip(["2000s", "2010s"], ["blue", "orange"]):
    subset = df[df["decade"] == decade]
    plt.scatter(subset["nrgy"], subset["dnce"], alpha=0.6, label = decade, color = color)
plt.title("Energy vs Danceability (2000s vs 2010s)")
plt.xlabel("energy")
plt.ylabel("Danceablity")
plt.grid(axis = "x" , linestyle = "--", alpha = 0.6)
plt.legend()
plt.savefig("images/energy_vs_danceabilty.png", dpi = 300, bbox_inches = "tight")
plt.show()

#top 10 comparission
plt.figure(figsize=(10, 6))
df_1['top genre'].value_counts().head(10).plot(kind='barh', alpha=0.7, label='2000s', color="red")
df_2['top genre'].value_counts().head(10).plot(kind='barh', alpha=0.7, label='2010s', color = "purple")
plt.title("Top 10 Genres Comparison")
plt.xlabel("Number of Songs")
plt.legend()
plt.tight_layout()
plt.savefig("images/top10_songs.png", dpi = 300, bbox_inches = "tight")
plt.show()


#user interaction:  song recommendation by genre
print("All avaiable generes: ")
print(df["top genre"].unique())

import tkinter as tk
from tkinter import ttk, messagebox
import plotly.express as px


def recommend_songs():
    selected_genre = genre_var.get()
    if not selected_genre:
        messagebox.showwarning("No Genre", "Please select a genre.")
        return


    recs = df[df['top genre'].str.lower().str.contains(selected_genre.lower(), na=False)]
    if recs.empty:
        messagebox.showinfo("No Results", f"No songs found for genre '{selected_genre}'.")
        return


    possible_title_cols = ['track_name', 'track', 'song', 'title', 'name']
    possible_artist_cols = ['artist', 'artist_name', 'singer', 'band']
    title_col = next((col for col in possible_title_cols if col in df.columns), None)
    artist_col = next((col for col in possible_artist_cols if col in df.columns), None)

    if title_col and artist_col:
        recs['Song'] = recs[title_col] + " - " + recs[artist_col]
    elif title_col:
        recs['Song'] = recs[title_col]
    else:
        recs['Song'] = "Unknown Song"


    fig = px.bar(
        recs.sort_values('pop', ascending=False).head(10),
        x='Song',
        y='pop',
        color='decade',
        title=f" Top {selected_genre.title()} Songs by Popularity",
        labels={'pop': 'Popularity Score'},
        hover_data=['bpm', 'nrgy', 'dnce']
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()

#trinklet
root = tk.Tk()
root.title("🎶 Choose Your Favorite Genre")
root.geometry("400x200")

tk.Label(root, text="Select your favorite genre:", font=('Arial', 12)).pack(pady=10)


genres = sorted(df['top genre'].dropna().unique())
genre_var = tk.StringVar()
genre_dropdown = ttk.Combobox(root, textvariable=genre_var, values=genres, state="readonly", width=40)
genre_dropdown.pack(pady=5)


ttk.Button(root, text="Show Recommendations", command=recommend_songs).pack(pady=10)

root.mainloop()