from kmeans import kmeans_clust
from kmeans import elbow_chart
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random as rnd
import seaborn as sb

# 1. === Data and Inputs ===
data_test = pd.DataFrame({
      'x' : [12,20,28,18,29,33,24,45,45,52,51,52,55,53,55,61,64,69,72]
    , 'y' : [39,36,30,52,54,46,55,59,63,70,66,63,58,23,14, 8,19, 7,24]
})

params = {
    "epsilon"     : 0.001,
    "max_iters"   : 100,
    "print_iters" : False      
}

# 2. === ELBOW CHART ===
elbowChart = elbow_chart(data_test, 10, params)
elbowPlot  = elbowChart.ploty()
plt.show()

# 3. === Best Solution (k = 3) ===
params["print_iters"] = True
cluster_best = kmeans_clust(k = 3, data = data_test, params = params)
distances, centroids, total_var = cluster_best.run()

# Plot the results for this 2 Dimensional Example
sb.set()
sb.scatterplot(data_test['x'], data_test['y'], distances['cluster'])
plt.plot(centroids['x'],  centroids['y'], 'x', c = "black")
plt.title("K-Means Clusters")
plt.show()