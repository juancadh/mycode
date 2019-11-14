from selenium import webdriver
import os
import sys
import datetime
import time
import csv

# =============== USER ID OF ROTTEN TOMATOS ==============
user_id = '794406277' #'832654610'
secs_to_sleep = 180
# ========================================================

browser = webdriver.Chrome(executable_path="C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/chromedriver")
browser.get(f'https://www.rottentomatoes.com/user/id/{user_id}/ratings')
time.sleep(secs_to_sleep)

all_items = browser.find_elements_by_xpath("//*[@id='col_right_index']/section/div/ul/li")

# Create CSV File
f = csv.writer(open("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/misc_code/rotten_tomatos/movies_" + user_id + ".csv", "w"), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
f.writerow(['Title','Year', 'Rating', 'Date Rated', 'URL', 'Poster URL'])

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

        f.writerow([title, year, rating, date_rated_2, href, url_poster])
    except:
        print(f"Error charging this movie: {title}")
        pass

    c += 1

browser.close()

print(f"========= TOTAL PELICULAS IMPORTADAS: {c}")
#print(movies)

