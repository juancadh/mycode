from genetic_algorithm import genetic_algorithm 
import numpy as np
import pandas as pd
import random as rnd
import seaborn as sb
from matplotlib import pyplot as plt

class SalesmanProblem:
    def __init__(self, decision_variables, coordinates):
        self.decision_variables = decision_variables 
        self.coordinates = coordinates
        self.distance = self.calculate_matrix_distances()
        
    def fitness_function(self, solution):
        tot_distance = 0
        for i in range(len(solution)-1):
            tot_distance += self.distance[self.decision_variables.index(solution[i]), self.decision_variables.index(solution[i+1])]
        return tot_distance
    
    def distance_btn_pnt(self, x1, y1, x2, y2):
        d = np.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)
        return d
    
    def calculate_distance(self, p1, p2):
        x1 = self.coordinates.iloc[p1,0]
        y1 = self.coordinates.iloc[p1,1]
        x2 = self.coordinates.iloc[p2,0]
        y2 = self.coordinates.iloc[p2,1]
        d = self.distance_btn_pnt(x1, y1, x2, y2)
        return d
    
    def calculate_matrix_distances(self):
        n = len(decision_variables)
        result = np.eye(n)*np.nan
        for i in range(n):
            for j in range(n):
                result[i,j] = self.calculate_distance(i, j)
                
        return result


n_cities = 10

# DECISION VARIABLES
decision_variables = [i for i in range(n_cities)]

# COORDINATES 
x = pd.Series([rnd.randint(0,100) for i in range(n_cities)])
y = pd.Series([rnd.randint(0,100) for i in range(n_cities)])
coordinates = pd.DataFrame(pd.concat([x,y], axis = 1))
coordinates.columns = ['x','y']

# Create Travel Salesman Problem
SMP = SalesmanProblem(decision_variables, coordinates)
table_of_distances = SMP.distance
print("\n =================== COORDENADAS ===================\n")
print(coordinates)
#print("\n =================== TABLA DE DISTANCIAS (EUCLIDIAN DISTANCES MATRIX) ===================\n")
#print(table_of_distances)

# Optimization TSP using SGA
optionals = {
            "method" : "Permutation",           # Type of problem: "Permutation" or "Combinatorial" 
            "optimize" : "min",                 # "min" or "max"                   
            "cross_prob" : 0.87,                # Probability of performing Crossover Operation
            "mutat_prob" : 0.70,                # Probability of performing Mutation Operation
            "cross_method" : "Order 1",         # Method of Crossover: "Order 1", "n points", "Uniform", ""
            "mutation_method" : "Inversion",         # Method of mutation:  "Swap", "Scramble", "Inversion", ""
            "selection_method" : "roulette",    # Method of selection: "Roulette", "Rank", "Tournament"
            "generations" : 300,                # Number of generations
            "pop_size" : 30,                    # Population Size
            "elitism" : False,                  # Perform elitism
            "show_iters" : True                 # Show iterations (generations)
        }
        
sga = genetic_algorithm(SMP, optionals) 

int_pop_bag = sga.initialize()
print("\n ==========> Bolsa Inicial:\n")
print(int_pop_bag)
eval_fit_pop = sga.eval_fit_population(int_pop_bag)
print("\n ==========> Bolsa Inicial Evaluada:\n")
fit_vals_pd = pd.DataFrame({"fit_vals" : eval_fit_pop["fit_vals"]})
fit_vals_pd_str = fit_vals_pd.sort_values("fit_vals", ascending = False)
print(list(fit_vals_pd_str.index))

pickA = sga.pickOne(int_pop_bag)
pickB = sga.pickOne(int_pop_bag)
print("\n ==========> Parent 1:\n")
print(pickA)
print("\n ==========> Parent 2:\n")
print(pickB)
cx = sga.crossover(pickA, pickB)
print("\n ==========> Crossover:\n")
print(cx)
mut = sga.mutation(cx)
print("\n ==========> Mutation:\n")
print(mut)

""" 
fit, sol = sga.run()

def connectpoints(x,y,p1,p2):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    plt.plot([x1,x2],[y1,y2],'b--')
    
sb.set()
plt.figure(figsize = (10,6))
sb.scatterplot(coordinates.x, coordinates.y)

for i in range(coordinates.shape[0]):
    x = coordinates.iloc[i,0]
    y = coordinates.iloc[i,1]
    plt.text(x+0.3, y+0.3, i, fontsize=12)

for i in range(len(sol)-1):
    p1, p2 = sol[i], sol[i+1]
    connectpoints(coordinates.x,coordinates.y,p1,p2)
    
print(sol, fit) 

plt.axis('equal')
plt.show()
 """
