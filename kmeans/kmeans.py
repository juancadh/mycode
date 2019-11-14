import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random as rnd
import seaborn as sb

class kmeans_clust:

    def __init__(self, k, data, params):
        self.k      = k
        self.data   = data
        self.params = params
    
    def select_randomly(self):
        m = self.data.shape[1]
        maxs = np.max(self.data, axis = 0)
        mins = np.min(self.data, axis = 0)
        
        rnd_point = {}
        for i in range(m):
            col_name = self.data.columns[i]
            rnd_point[col_name] = [rnd.uniform(mins[i], maxs[i]) for j in range(self.k)]
        
        return pd.DataFrame(rnd_point)

    def run(self):
        # Select First Centroids Randomly
        centroids = self.select_randomly()

        epsilon     = self.params["epsilon"]   # 0.001
        max_iters   = self.params["max_iters"] # 100
        print_iters = self.params["print_iters"]

        n = 0
        while n <= max_iters:
            # Compute the distances between centroids and each data point
            distances, total_var = self.calculate_distances(centroids, self.data)
            if print_iters:
                print(f"\nIteration: {n}")            
                print(f"Total Variation: {total_var}")

            # Calculate the new centroid (Avg of data points)
            centroids = self.new_centroids(distances, centroids)
            
            if n == 0:
                old_centroids = centroids
            else:
                diff_vect = np.abs(np.array(old_centroids)-np.array(centroids))
                total_diference = np.sum(diff_vect)
                if print_iters:
                        print(f"Diff in centroids: {np.round(total_diference,3)}")
                if total_diference <= epsilon:
                    if print_iters:
                        print(f"\nTotal number of iterations: {n}")
                    return distances, centroids, total_var
                else:    
                    old_centroids = centroids
            n += 1
        
        if print_iters:
            print(f"\nTotal number of iterations: {n} - Maximun Reached!")
        return distances, centroids, total_var


    def new_centroids(self, distances, old_centroids):
        all_data = pd.concat([self.data, distances], axis = 1)
        means_by_cluster = all_data.groupby('cluster')[self.data.columns].mean()        
        means_by_cluster.reset_index(drop = True, inplace = True)
        # Check if all the centroids exist, if not input the previous one. 
        # (This could happend when none of the points matches with the centroid)
        if means_by_cluster.shape[0] != self.k :
            for i in range(self.k):
                if list(means_by_cluster.index).count(i) == 0:       
                    flt = list(old_centroids.iloc[i,:])
                    means_by_cluster.loc[i] = flt

        return means_by_cluster

    def calculate_distances(self, centroids, points):
        n = points.shape[0]
        
        # Calculate the distance between centroids and cluster
        distances = {}
        for cent in range(self.k):            
            cent_point = list(centroids.iloc[cent,:])
            dist_vec   = []
            for i in range(n):
                data_point = list(points.iloc[i,:])
                data_dist  = np.linalg.norm(np.array(cent_point)-np.array(data_point))
                dist_vec.append(data_dist)
                #print(f"Centroid: {cent_point} | Data: {data_point} => Distance: {data_dist}")

            distances["cluster_" + str(cent)] = dist_vec

        distances = pd.DataFrame(distances)

        # Closest centroid for each point
        clost_cnt = distances.idxmin(1)
        distances = pd.concat([distances, clost_cnt], axis = 1)
        distances.rename(columns = {0 : 'cluster'}, inplace = True)

        clost_cnt_val = distances.min(1)
        distances = pd.concat([distances, clost_cnt_val], axis = 1)
        distances.rename(columns = {0 : 'vari_cluster'}, inplace = True)

        total_var = distances['vari_cluster'].sum()

        return distances, total_var

# ============================================================================
# ============================================================================


class elbow_chart():

    def __init__(self, data, n_clusts, params):
        self.data     = data
        self.n_clusts = n_clusts
        self.params   = params
    
    def ploty(self):
        total_vars_vect = []
        for i in range(1,self.n_clusts):
            cluster_ex1 = kmeans_clust(i, self.data, self.params)
            distances, centroids, total_var = cluster_ex1.run()
            total_vars_vect.append(total_var)

        sb.set()
        f = plt.figure()
        sp = f.add_subplot(111)
        sp.plot([i for i in range(1,self.n_clusts)], total_vars_vect, 'o-')
        plt.title("Elbow Chart")
        plt.xlabel("Number of clusters (k)")
        plt.ylabel("Total variation")
        return f

