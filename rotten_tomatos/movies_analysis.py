import pandas as pd
import numpy as np
import seaborn as sb
from matplotlib import pyplot as plt
from rottem_srap import rotten_tomatos
import csv
import datetime as dt

# =============== USER ID OF ROTTEN TOMATOS ==============
user_id = '794406277' #'832654610' '794406277'
secs_to_sleep = 5

myRotten        = rotten_tomatos(user_id, secs_to_sleep)

#my_movies       = myRotten.get_my_movies()
#movies_metadata = myRotten.get_metadata_movies(",")
all_data        = myRotten.combine_files(";")
# ========================================================


# Add Columns
all_data["first_genre"]    = all_data["genre"].apply(lambda x : x.split("|")[0])
all_data["first_director"] = all_data["director"].apply(lambda x : x.split("|")[0])
all_data["first_actor"]    = all_data["cast"].apply(lambda x : x.split("|")[0])
all_data["runtime"]        = all_data["runtime"].apply(lambda x : int(x.replace("minutes","").strip()))
all_data["Rating_Score"]   = all_data["Rating"].apply(lambda x : (float(x) * 100) / 5)
all_data['date_of_rate']   = all_data["Date Rated"].apply(lambda x : dt.datetime.strptime(x, '%d/%m/%Y') )
all_data['year_of_rate']   = all_data['date_of_rate'].apply(lambda x : x.year )

print_all = True

# Evolution of average of rating over time
#print(all_data.groupby('year_of_rate')['Rating'].mean())

# ====================== GENERAL STATISTICS ===========
total_movies = all_data.shape[0]
total_runtime_h = '{:,}'.format(int(all_data["runtime"].sum()/60))
total_runtime_d = '{:,}'.format(int((all_data["runtime"].sum()/60)/24))
min_rate_year = all_data['year_of_rate'].min()
max_rate_year = all_data['year_of_rate'].max()

# ======================= MOST SEEN STUDIO ================
studios_cnt = all_data.groupby("studio")["Title"].count().sort_values(ascending = False)

# ======================== MOST SEEN GENRE =================
genre_data = all_data["genre"].apply(lambda x : x.split("|"))
all_genre = []
for i in genre_data:
    for j in i:
        all_genre.append(j)
all_genre = pd.DataFrame({"Genre" : all_genre})
gnr_class = all_genre["Genre"].value_counts()
top_genre = gnr_class

# ======================== MOST SEEN ACTORS =================
cast_data = all_data["cast"].apply(lambda x : x.split("|"))
all_cast = []
for i in cast_data:
    for j in i:
        all_cast.append(j)
top_cast = pd.DataFrame({"name" : all_cast})["name"].value_counts()

# ======================== MOST SEEN DIRECTOR =================
direct_data = all_data["director"].apply(lambda x : x.split("|"))
all_directors = []
for i in direct_data:
    for j in i:
        all_directors.append(j)
top_director = pd.DataFrame({"name" : all_directors})["name"].value_counts()

# ============ Number of movies by year of movie ===============
num_movies_by_year = all_data.groupby("Year")["Title"].count().reset_index()
num_movies_by_year.columns = ["Year", "n_movies"]
num_movies_by_year.sort_values("n_movies", ascending = False, inplace = True)
num_movies_by_year.set_index("Year", inplace = True)

# ============== TOP RATED FUNCTION ==================

def calculate_top_rated(cat_name):
    data = all_data[cat_name].apply(lambda x : x.split("|"))
    data_score = pd.concat([all_data["Rating_Score"], all_data["audience_score"], all_data["tomatometer"], data], axis = 1)
    list_gnr    = []
    list_you_sc = []
    list_aud_sc = []
    list_tom_sc = []

    all_vals = []
    for i in data:
        for j in i:
            all_vals.append(j)
    count_data = pd.DataFrame({"name" : all_vals})["name"].value_counts()

    for i in range(len(data)):
        your_score     = data_score.iloc[i,0]
        audience_score = data_score.iloc[i,1]
        tomatometer    = data_score.iloc[i,2]
        genre_list     = data_score.iloc[i,3]
        for j in genre_list:
            list_gnr.append(j)
            list_you_sc.append(your_score)
            list_aud_sc.append(audience_score)
            list_tom_sc.append(tomatometer)

    grn_scores = pd.DataFrame({
        "category" : list_gnr,
        "your_score" : list_you_sc,
        "audi_score" : list_aud_sc,
        "toma_score" : list_tom_sc
    })

    #grn_scores.set_index("genre", inplace = True)
    summ_gnre_score = grn_scores.groupby("category").mean().sort_values("your_score", ascending = False).round(1)
    return summ_gnre_score


# Top rated by gender
summ_gnre_score = calculate_top_rated("genre")
# Top rated by director
summ_director_score = calculate_top_rated("director")
# Top rated by actor
summ_actor_score = calculate_top_rated("cast")

if print_all:
    # PRINT STUFF
    print("\n===============================================================")
    print("======================= GENERAL STATISTICS ====================")
    print("===============================================================\n")
    print(f"Total movies: {total_movies}")
    print(f"Range of dates: {min_rate_year} - {max_rate_year}")
    print(f"Total of hours seen: {total_runtime_h} hours")
    print(f"Total of days seen: {total_runtime_d} days")
    print("\n---- Most Seen -----\n")
    print(f"    by genre   : {top_genre.index[0]} ({top_genre[0]} movies)")
    print(f"    by actor   : {top_cast.index[0]} ({top_cast[0]} movies)")
    print(f"    by director: {top_director.index[0]} ({top_director[0]} movies)")
    print(f"    by Studio  : {studios_cnt.index[0]} ({studios_cnt[0]} movies)")
    print("\n---- Top Rated -----\n")
    print(f"    by genre   : {summ_gnre_score.index[0]} ({summ_gnre_score['your_score'][0]} Score | {summ_gnre_score['toma_score'][0]} Rotten Score)")
    #print(f"    by actor   : {summ_actor_score.index[0]} ({summ_actor_score['your_score'][0]} Score | {summ_actor_score['toma_score'][0]} Rotten Score)")
    #print(f"    by director: {summ_director_score.index[0]} ({summ_director_score['your_score'][0]} Score | {summ_director_score['toma_score'][0]} Rotten Score)")

    print("\n---- Worst Rated -----\n")
    print(f"    by genre   : {summ_gnre_score.index[-1]} ({summ_gnre_score['your_score'][-1]} Score | {summ_gnre_score['toma_score'][-1]} Rotten Score)")
    #print(f"    by actor   : {summ_actor_score.index[-1]} ({summ_actor_score['your_score'][-1]} Score | {summ_actor_score['toma_score'][-1]} Rotten Score)")
    #print(f"    by director: {summ_director_score.index[-1]} ({summ_director_score['your_score'][-1]} Score | {summ_director_score['toma_score'][-1]} Rotten Score)")


    print("\n===============================================================")
    print("========================= MOST SEEN ===========================")
    print("===============================================================")
    print("\n================= MOST SEEN BY GENRE =================\n")
    print(top_genre.head(5))
    print("\n================= MOST SEEN BY CAST =================\n")
    print(top_cast.head(5))
    print("\n================= MOST SEEN BY DIRECTOR =================\n")
    print(top_director.head(5))
    print("\n================= MOST SEEN BY YEAR =================\n")
    print(num_movies_by_year.head(5))
    print("\n================= MOST SEEN BY STUDIO =================\n")
    print(studios_cnt.head(5))

    print("\n===============================================================")
    print("========================= TOP RATED ===========================")
    print("===============================================================")
    print("\n================= TOP RATED BY GENRE =================\n")
    print(summ_gnre_score.head(5))
    #print("\n================= TOP RATED BY CAST =================\n")
    #print(summ_actor_score.head(5))
    #print("\n================= TOP RATED BY DIRECTOR =================\n")
    #print(summ_director_score.head(5))



# Chart of Evolution in rating fequency over Time
rate_series = all_data['year_of_rate'].value_counts(sort = False)
sb.set()
plt.plot(rate_series)
plt.ylabel("Number of movies")
plt.title("Evolution of rating")
plt.show()

# ============= Summary of Genre ==========================
# (Number of movies, Avg Rating, Avg Audience Rating, Avg Tomato Rating)
rating_by_gender = all_data.groupby("first_genre")[["Rating_Score","audience_score", "tomatometer"]].mean().reset_index()
rating_by_gender.columns = ["Genre", "Rating","Audience_Rating","Tomato_Rating"]
rating_by_gender = rating_by_gender.sort_values("Rating", ascending = False)

genre_anly = pd.merge(left = rating_by_gender, right = gnr_class, left_on = "Genre", right_on = "Genre")

# ======================== PLOT FINDINGS =======================
f, axes = plt.subplots(2, 2, figsize=(14, 6))
f.subplots_adjust(hspace = 0.3)
sb.despine(left=True)

# Gener by count
genre_anly.sort_values('n_movies', ascending = True, inplace = True)
genre_anly.set_index("Genre", inplace = True)
genre_anly.rename(index = {
    'Comedy' : 'Comedy',
    'Drama' : 'Drama',
    'Action & Adventure' : 'Action',
    'Art House & International' : 'Intern.',
    'Animation' : 'Animation',
    'Horror' : 'Horro',
    'Mystery & Suspense' : 'Suspense',
    'Classics' : 'Classic',
    'Documentary' : 'Documentary',
    'Kids & Family' : 'Kids',
    'Musical & Performing Arts' : 'Musical',
    'Romance' : 'Romance'
}, inplace = True)
axes[0,0].barh(list(genre_anly.index), genre_anly["n_movies"], align='center', color="lightblue")
axes[0,0].set_title("Count by Genre")

# Number of movies by year
sb.barplot(num_movies_by_year["Year"][20:], num_movies_by_year["n_movies"][20:], ax = axes[1,1])
axes[1,1].set_title("Count by Year of the Movie")
plt.ylabel("Number of movies")
plt.xticks(rotation = 90)

#plt.show()

#print(all_data[["Title", "Year", "first_genre", "first_director", "Rating", "Rating_Score", "audience_score", "tomatometer","runtime"]])
