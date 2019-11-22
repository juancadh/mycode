import os
import sys
import datetime
import time
import csv
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

def ScrapIMDB_list(range_of_pages, over_write_csv):

    global_n_movies = 0

    if over_write_csv:
        # Create CSV File
        f = open(f"C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/imdb/movies_imdb_us_1972_2016.csv", 'w', newline='')
        myFile = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        myFile.writerow(['title', 'year', 'runtime', 'genre', 'certificate', 'rating', 'director', 'cast', 'gross', 'votes'])
    else:
        f = open(f"C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/imdb/movies_imdb_us_1972_2016.csv", 'a', newline='')
        myFile = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for page in range_of_pages:
        browser = webdriver.Chrome(executable_path="C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/rotten_tomatos/chromedriver")
        wait = WebDriverWait(browser, 20)
        browser.get(f'https://www.imdb.com/list/ls057823854/?sort=alpha,asc&st_dt=&mode=detail&page={page}')
        #time.sleep(1)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ft')))
        browser.execute_script("window.stop();")

        all_items = browser.find_elements_by_css_selector("div.lister-item.mode-detail")

        n_movies = 0
        for i in all_items:
            try:
                movie_title = i.find_element_by_css_selector("div.lister-item-content").find_element_by_css_selector("h3.lister-item-header").find_element_by_css_selector("a").text.strip().replace(",","").replace(";","")
            except:
                movie_title = np.nan

            try: 
                movie_year = int(re.findall(r'\b\d+\b', i.find_element_by_css_selector("div.lister-item-content").find_element_by_css_selector("h3.lister-item-header").find_element_by_css_selector("span.lister-item-year.text-muted.unbold").text.strip().replace("(","").replace(")",""))[0])
            except:
                movie_year = np.nan

            try:    
                movie_runtime = int(re.findall(r'\b\d+\b', i.find_element_by_css_selector("div.lister-item-content").find_element_by_css_selector("span.runtime").text.strip())[0])
            except:
                movie_runtime = np.nan

            try:
                movie_genre_x = i.find_element_by_css_selector("div.lister-item-content").find_element_by_css_selector("span.genre").text.strip().split(",")
                movie_genre = [x.strip().replace(",","").replace(";","") for x in movie_genre_x]
                movie_genre_str = "|".join(movie_genre)
            except:
                movie_genre = []
                movie_genre_str = ""

            try:
                movie_certificate = i.find_element_by_css_selector("div.lister-item-content").find_element_by_css_selector("span.certificate").text.strip()
            except:
                movie_certificate = np.nan

            try:
                movie_rating = float(i.find_element_by_css_selector("div.lister-item-content").find_element_by_css_selector("span.ipl-rating-star__rating").text.strip().replace(",","."))
            except:
                movie_rating = np.nan

            try:  
                dir_and_cast = i.find_element_by_css_selector("div.lister-item-content").find_elements_by_css_selector("p.text-muted.text-small")[1].find_elements_by_css_selector("a")
                c = 0
                movie_cast = []
                for k in dir_and_cast:
                    if c == 0:
                        movie_director = k.text.strip().replace(",","").replace(";","")
                    else:
                        movie_cast.append(k.text.strip().replace(",","").replace(";",""))
                    c += 1

                movie_cast_str = "|".join(movie_cast)
            except:
                movie_director = np.nan
                movie_cast = []
                movie_cast_str = ""

            try:  
                votes_and_gross = i.find_element_by_css_selector("div.lister-item-content").find_elements_by_css_selector("p.text-muted.text-small")[2].find_elements_by_css_selector("span")
            except:
                pass

            try:
                c = 0
                movie_gross = np.nan
                movie_votes = np.nan
                for i in votes_and_gross:
                    if i.get_attribute("name") == "nv" and c == 1:
                        movie_votes = int(i.get_attribute("data-value").replace(".",""))
                    elif i.get_attribute("name") == "nv" and c == 4:
                        movie_gross = int(i.get_attribute("data-value").replace(".",""))
                    c += 1
            except:
                movie_gross = np.nan
                movie_votes = np.nan

            print(f"Page: {page} | Importing movie: {global_n_movies + 1}")
            
            n_movies += 1
            global_n_movies += 1

            myFile.writerow([movie_title, movie_year, movie_runtime, movie_genre_str, movie_certificate, movie_rating, movie_director, movie_cast_str, movie_gross, movie_votes ])
            #print(f"{movie_title} || {movie_year} || {movie_runtime} || {movie_genre} || {movie_certificate} || {movie_rating} || {movie_director} || {movie_cast} || {movie_gross} || {movie_votes}" )

        browser.close()

#================================
range_of_pages = [i for i in range(91,101)]
over_write_csv = False
ScrapIMDB_list(range_of_pages, over_write_csv)
#================================

