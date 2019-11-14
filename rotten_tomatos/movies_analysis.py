import pandas as pd
import numpy as np
import seaborn as sb
from matplotlib import pyplot as plt

data_movies = pd.read_csv("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/movies_794406277.csv", delimiter=";")
metadata    = pd.read_csv("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/movies_metadata.csv", delimiter=";")

metadata.rename(columns={'href': 'URL'}, inplace = True)

data_movies = data_movies.set_index("URL")
metadata    = metadata.set_index("URL")

all_data = pd.merge(data_movies, metadata, left_on = "URL", right_on= "URL")
all_data = all_data.reset_index()

# Add Columns
all_data["first_genre"]    = all_data["genre"].apply(lambda x : x.split("|")[0])
all_data["first_director"] = all_data["director"].apply(lambda x : x.split("|")[0])
all_data["runtime"]        = all_data["runtime"].apply(lambda x : int(x.replace("minutes","").strip()))
all_data["Rating_Score"]   = all_data["Rating"].apply(lambda x : (float(x) * 100) / 5)

# Number of movies by year
num_movies_by_year = all_data.groupby("Year")["Title"].count().reset_index()
num_movies_by_year.columns = ["Year", "n_movies"]

# Summary of Genre (Number of movies, Avg Rating, Avg Audience Rating, Avg Tomato Rating)
count_by_gender = all_data.groupby("first_genre")["Title"].count().reset_index()
count_by_gender.columns = ["Genre", "n_movies"]
count_by_gender = count_by_gender.sort_values("n_movies", ascending = False)

rating_by_gender = all_data.groupby("first_genre")[["Rating_Score","audience_score", "tomatometer"]].mean().reset_index()
rating_by_gender.columns = ["Genre", "Rating","Audience_Rating","Tomato_Rating"]
rating_by_gender = rating_by_gender.sort_values("Rating", ascending = False)

genre_anly = pd.merge(left = rating_by_gender, right = count_by_gender, left_on = "Genre", right_on = "Genre")
print(genre_anly)

f, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
sb.despine(left=True)

# Joinplot of Rating vs Tomato Rating
#sb.jointplot(x = all_data["Rating_Score"], y = all_data["tomatometer"], kind="hex", color="#4CB391", ax = axes[0])
sb.barplot(num_movies_by_year["Year"], num_movies_by_year["n_movies"], ax = axes[0,0])

# Number of movies by year
sb.barplot(num_movies_by_year["Year"], num_movies_by_year["n_movies"], ax = axes[1,0])
plt.title("Number of movies by year")
plt.ylabel("Number of movies")
plt.xlabel("Year")
plt.xticks(rotation = 90)

plt.setp(axes, yticks=[])
plt.tight_layout()
plt.show()

#print(all_data[["Title", "Year", "first_genre", "first_director", "Rating", "Rating_Score", "audience_score", "tomatometer","runtime"]])
