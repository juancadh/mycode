import pandas as pd
import numpy as np
import seaborn as sb
import time
import csv
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

def get_metadata_movies(url_movies_list):

    # Create CSV File
    f = csv.writer(open("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/movies_metadata.csv", "w"), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f.writerow(['href','tomatometer', 'audience_score', 'genre', 'director', 'runtime', 'studio', 'cast', 'date'])

    c = 0
    result = {}

    for url in url_movies:
        print(f"\nRecopilando info de {url} | {c+1} de {len(url_movies)}")

        browser = webdriver.Chrome(executable_path="C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/chromedriver", desired_capabilities= capa)
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

        f.writerow([url, tomatometer, audience_score, genre_str, director_str, runtime, studio, cast_str, date_tht])

        c += 1

        browser.close()

    return result



# =======================================================================
# =======================================================================


data_movies = pd.read_csv("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/movies_794406277.csv", delimiter=";")
url_movies = data_movies['URL']

movies_metadata = get_metadata_movies(url_movies)