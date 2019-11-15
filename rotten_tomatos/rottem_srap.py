import os
import sys
import datetime
import time
import csv
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

# =============== USER ID OF ROTTEN TOMATOS ==============
#user_id = '794406277' #'832654610'
#secs_to_sleep = 180

#myRotten        = rotten_tomatos(user_id, secs_to_sleep)
#my_movies       = myRotten.get_my_movies()
#movies_metadata = get_metadata_movies()
# ========================================================

class rotten_tomatos():

    def __init__(self, user_id, secs_to_sleep):
        self.user_id = user_id
        self.secs_to_sleep = secs_to_sleep

    # ===================================================================
    # GET MOVIES OF AN SPECIFIC USER ID
    # ====================================================================
    def get_my_movies(self):

        browser = webdriver.Chrome(executable_path="C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/chromedriver")
        browser.get(f'https://www.rottentomatoes.com/user/id/{self.user_id}/ratings')
        print("(!) REALIZA EL SCROLL EN LA PAGINA HASTA LLEGAR A LA ULTIMA PELICULA.")
        time.sleep(self.secs_to_sleep)

        all_items = browser.find_elements_by_xpath("//*[@id='col_right_index']/section/div/ul/li")

        # Create CSV File
        f = open("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/movies_" + self.user_id + ".csv", 'w', newline='')
        theFile = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        theFile.writerow(['Title','Year', 'Rating', 'Date Rated', 'URL', 'Poster URL'])

        movies = {}
        c = 0
        for i in all_items:
            print(f". . . Getting movie {c+1} of {len(all_items)}")

            try:
                # Get the title
                title = i.find_element_by_css_selector("a.ratings__movie-title").text.strip().capitalize().replace(",","")
                # Get the Hyperlink
                href  = i.find_element_by_css_selector("a.ratings__movie-title").get_attribute("href")
                # Get the Year
                year  = i.find_element_by_css_selector("span.small.subtle").text.strip().capitalize().replace("(","").replace(")","")
                # Get the Rating Stars
                rating_obj = i.find_element_by_css_selector("span.star-display").find_elements_by_css_selector("span")
                rating = 0
                for start in rating_obj:
                    class_name = start.get_attribute("class").strip()
                    if class_name == "star-display__filled":
                        rating = rating + 1
                    elif class_name == "star-display__half":
                        rating = rating + 0.5
                    else:
                        rating = rating + 0

                # Get the URL of the picture 
                url_poster = i.find_element_by_css_selector("img.media-object.rating__posterArt").get_attribute("src")

                # Get the time when it was seen
                date_of_rated = i.find_element_by_css_selector("a.ratings__age").text.strip().capitalize()
                value, unit = date_of_rated.split()[0:2]

                if (unit == "minute") or (unit == "hour") or (unit == "day"):
                    unit = unit + "s"

                if (unit == "month") or (unit == "months"):
                    unit = "days"
                    value = int(value) * 30

                if (unit == "year") or (unit == "years"):
                    unit = "days"
                    value = int(value) * 365

                dt = datetime.timedelta(**{unit: float(value)})
                date_rated_2 = datetime.datetime.now() - dt
                date_rated_2 = date_rated_2.strftime("%d-%m-%Y")

                movies[c] = {"title"  : title,
                            "year"   : year, 
                            "rating" : rating, 
                            "date_of_rated" : date_rated_2, 
                            "href"   : href,
                            "url_poster" : url_poster}

                theFile.writerow([title, year, rating, date_rated_2, href, url_poster])
            except:
                print(f"Error charging this movie: {title}")
                pass

            c += 1

        f.close()
        browser.close()

        print(f"========= TOTAL PELICULAS IMPORTADAS: {c} ===========")
        return movies

    # ============================================================================
    # GET THE METADATA OF MY MOVIES
    # ============================================================================
    def get_metadata_movies(self, CSVdelimeter = ";"):

        data_movies = pd.read_csv(f"C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/movies_{self.user_id}.csv", delimiter=CSVdelimeter)
        url_movies = data_movies['URL']

        # Create CSV File
        f = open(f"C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/movies_metadata_{self.user_id}.csv", 'w', newline='')
        myFile = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        myFile.writerow(['href','tomatometer', 'audience_score', 'genre', 'director', 'runtime', 'studio', 'cast', 'date'])

        c = 0
        result = {}

        for url in url_movies:
            print(f"\nRecopilando info de {url} | {c+1} de {len(url_movies)}")

            browser = webdriver.Chrome(executable_path="C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/chromedriver", desired_capabilities= capa)
            wait = WebDriverWait(browser, 20)
            browser.get(url)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mop-ratings-wrap__half')))
            browser.execute_script("window.stop();")

            try:
                # Tomato Meter
                tomatometer = browser.find_element_by_css_selector("div.mop-ratings-wrap__half").find_element_by_css_selector("span.mop-ratings-wrap__percentage").text.strip().replace("%","")
            except:
                tomatometer = ''

            try:
                # Audience Score
                audience_score = browser.find_element_by_css_selector("div.mop-ratings-wrap__half.audience-score").find_element_by_css_selector("span.mop-ratings-wrap__percentage").text.strip().replace("%","")
            except:
                audience_score = ''

            try:
                # List of meta data
                list_meta_data = browser.find_element_by_css_selector("ul.content-meta.info").find_elements_by_css_selector("li.meta-row.clearfix")
            except:
                list_meta_data = []
            
            for i in list_meta_data:
                meta_label = i.find_element_by_css_selector("div.meta-label.subtle").text.strip()

                try:
                    # Genre
                    if meta_label == "Genre:":
                        genre_obj = i.find_element_by_css_selector("div.meta-value").find_elements_by_css_selector("a")
                        genre = []
                        for gnr in genre_obj:
                            genre.append(gnr.text.strip().replace(",",""))
                        
                        genre_str = "|".join(genre)
                except:
                    genre = []
                    genre_str = ""

                try:
                    # Director
                    if meta_label == "Directed By:":
                        dir_obj = i.find_element_by_css_selector("div.meta-value").find_elements_by_css_selector("a")
                        director = []
                        for d in dir_obj:
                            director.append(d.text.strip().replace(",",""))
                        director_str = "|".join(director)
                except:
                    director = []
                    director_str = ""

                try:
                    # Runtime
                    if meta_label == "Runtime:":
                        runtime = i.find_element_by_css_selector("div.meta-value").find_element_by_css_selector("time").text.strip()
                except:
                    runtime = ''

                try:
                    # Studio 
                    if meta_label == "Studio:":
                        studio = i.find_element_by_css_selector("div.meta-value").text.strip()
                except:
                    studio = ''

                try: 
                    # In Theaters
                    if meta_label == "In Theaters:":
                        date_tht = i.find_element_by_css_selector("div.meta-value").find_element_by_css_selector("time").get_attribute("datetime")
                except:
                    date_tht = ''
            
            try:
                # Cast
                cast_obj = browser.find_elements_by_css_selector("div.cast-item.media.inlineBlock")
                cast = []
                for i in cast_obj:
                    actor_name = i.find_element_by_css_selector("div.media-body").find_element_by_css_selector("span").text.strip().replace(",","")
                    if len(actor_name) > 0:
                        cast.append(actor_name)
                    cast_str = "|".join(cast)
            except: 
                cast = []
                cast_str = ""

            result[c] = {
                "href" : url,
                "tomatometer" : tomatometer,
                "audience_score" : audience_score,
                "genre" : genre,
                "director" : director,
                "runtime" : runtime,
                "studio" : studio,
                "cast" : cast,
                "date_tht" : date_tht
            }

            myFile.writerow([url, tomatometer, audience_score, genre_str, director_str, runtime, studio, cast_str, date_tht])

            c += 1

            browser.close()

        f.close()
        return result

    def combine_files(self, CSVdelimeter = ";"):
        data_movies = pd.read_csv(f"C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/movies_{self.user_id}.csv", delimiter=CSVdelimeter)
        metadata    = pd.read_csv(f"C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/movies_metadata_{self.user_id}.csv", delimiter=CSVdelimeter)

        metadata.rename(columns={'href': 'URL'}, inplace = True)

        data_movies = data_movies.set_index("URL")
        metadata    = metadata.set_index("URL")

        all_data = pd.merge(data_movies, metadata, left_on = "URL", right_on= "URL")
        all_data = all_data.reset_index()

        return all_data





