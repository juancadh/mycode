import pandas as pd
import numpy as np
from matplotlib import pyplot as plot


# Read the csv file that contains the data
data_csv = pd.read_csv("C:/Users/Juan Camilo Díaz/Dropbox/Project_VSC/python_projects/imdb/movies_imdb_us_1972_2016.csv", delimiter= ";")

print(data_csv.columns)

# Summary by year
sum_date = data_csv.groupby("year")["title"].count()
print(sum_date)

# Summary by year
sum_date = data_csv.groupby("year")["title"].count()
print(sum_date)

