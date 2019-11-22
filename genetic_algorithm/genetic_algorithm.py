#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========== SIMPLE GENETIC ALGORITHM (SGA) ==========

Created on Wed Nov  6 19:36:44 2019

@author: Juan Camilo Díaz 
"""

import pandas as pd
import numpy as np
import seaborn as sb
from matplotlib import pyplot as plt
import random as rnd

class genetic_algorithm:

    """ SIMPLE GENETIC ALGORITHM

        * <model_class>: Should be a class that must have a 'fitness_function' function inside it. And this function
                       must return a numerical value (float or int), and it should receive as input a solution.
                    
                    EX: 
                       class XX:
                           def __init__(self):

                           def fitness_function(solution):
                               return solution^2

        * <optional_prm>: Dictionary that must follow the following structure

                optionals = {
                    "method" : "Permutation",           # Type of problem: "Permutation" or "Combinatorial"
                    "optimize" : "min",                 # "min" or "max"                     
                    "cross_prob" : 0.87,                # Probability of performing Crossover Operation
                    "mutat_prob" : 0.50,                # Probability of performing Mutation Operation
                    "cross_method" : "Order 1",         # Method of Crossover: "Order 1", "n points", "Uniform", ""
                    "mutation_method" : "swap",         # Method of mutation:  "Swap", "Scramble", "Inversion", ""
                    "selection_method" : "roulette",    # Method of selection: "Roulette", "Rank", "Tournament"
                    "generations" : 10,                 # Number of generations
                    "pop_size" : 50,                    # Population Size
                    "elitism" : False,                  # Perform elitism
                    "show_iters" : True                 # Show iterations (generations)
                }
    """

    def __init__(self, model_class, optional_prm):
        self.optional_prm = optional_prm
        self.model_class  = model_class
        
    # Create random solution 
    def random_solution(self):
        """ 
        Creates a random solution depending of the type of problem. 
        Method could be: 
            - Permutations:  Shuffle the decision variable vector. 
            - Combinatorial: Randomize values among the decision variable vector. 
        """

        if self.optional_prm["method"].lower() == "permutation":
            rnd_sol = self.model_class.decision_variables.copy()
            rnd.shuffle(rnd_sol)
            return rnd_sol
        elif self.optional_prm["method"].lower() == "combinatorial":
            decision_variables = self.model_class.decision_variables.copy() 
            rnd_sol = [decision_variables[rnd.randint(0,len(decision_variables))-1] for i in range(len(decision_variables))]
            return rnd_sol
        
    def initialize(self):
        """ Creates the initial population bag. """

        pop_bag = []
        for i in range(self.optional_prm["pop_size"]):
            pop_bag.append(self.random_solution())
            
        return np.array(pop_bag)
    
    def eval_fit_population(self, pop_bag):
        """ Evaluates the fitness of each element in population bag.  """

        result = {}
        fit_vals_lst = []
        solutions = []
        for solution in pop_bag:   
             fit_vals_lst.append(self.model_class.fitness_function(solution))
             solutions.append(solution)
             
        result["fit_vals"] = fit_vals_lst

        if self.optional_prm["optimize"].lower() == "min":
            # If the problem is minimization then the lower fitnes values should have the hieghts probability of been selected
            min_wgh = [np.max(list(result["fit_vals"]))-i for i in list(result["fit_vals"])]
            result["fit_wgh"]  = [i/sum(min_wgh) for i in min_wgh]
        elif self.optional_prm["optimize"].lower() == "max":
            result["fit_wgh"]  = [i/sum(list(result["fit_vals"])) for i in list(result["fit_vals"])]

        result["solution"] = np.array(solutions)
        
        return result
     
    def pickOne(self, pop_bag):
        """ Pick one solution from the population bag using the selection method. """

        # Evaluate the fitness of the population bag
        fit_bag_evals = self.eval_fit_population(pop_bag)

        if self.optional_prm["selection_method"].lower() == "roulette":
            
            n = len(fit_bag_evals["solution"])
            maxIts = 1000
            c = 0
            while c <= maxIts:
                rnIndex = rnd.randint(0, n-1)
                rnPick  = fit_bag_evals["fit_wgh"][rnIndex]
                r = rnd.random()
                if  r <= rnPick:
                    pickedFitness = fit_bag_evals["fit_vals"][rnIndex]
                    pickedSol     = fit_bag_evals["solution"][rnIndex]
                    #print(f"ProbRnd: {r} <= Choosen: {rnPick} | fitness : {pickedFitness}")
                    return pickedSol
                
                c += 1
        
        elif self.optional_prm["selection_method"].lower() == "rank":
            pass
        else:
            print("Method of selection not selected.")
            return []    
        
        print("It was not possible to pick one solution from the population bag.")
        return []
    
    def crossover(self, solA, solB):
        """ Perform Crossover GA Operation depending on the method. """

        # ========= For Permutations ==========
        # Order 1 Crossover Operation: Take a random subsection of the first parent, then paste that in the child and then start to
        #                              include ordered the elements of parent 2 that are not in that subsection of parent 1.
        if self.optional_prm["cross_method"].lower() == "order 1":
            n = len(solA)
            # Create an empty child -> Ch = [nan nan nan nan nan nan]
            child = [np.nan for i in range(n)] 
            # Number of elements to take as the subsection.
            blockA, str_pnt, end_pnt = self.SubSection(solA)
            #print(f"{solA} | De {str_pnt} hasta {end_pnt} => {blockA}")

            # Input that subsection to the child -> Ch = [nan nan 5 2 4 nan] 
            child[str_pnt:end_pnt] = blockA
            for i in range(n):
                if list(blockA).count(solB[i]) == 0:
                    for j in range(n):
                        if np.isnan(child[j]):
                            child[j] = solB[i]
                            break
            #print(f"Parent A: {solA} | Parent B: {solB} | Child: {child}")
            return child
    
    def mutation(self, sol):
        """ Perform Mutation GA Operation depending on method. """

        n = len(sol)

        # ========= For Permutations ==========
        # Swap : Exchange the positions between to elements. [3 4 2 1] --> [3 2 4 1]  where 4 <-> 2 
        if self.optional_prm["mutation_method"].lower() == "swap":
            pos_1 = rnd.randint(0,n-1)
            c = 0
            while c <= 1000:
                pos_2 = rnd.randint(0,n-1)
                if pos_2 != pos_1:
                    result = self.swap(sol, pos_1, pos_2)
                    return result
                    break
                c += 1

        # Scramble : Take a subsection and shuffle it.
        elif self.optional_prm["mutation_method"].lower() == "scramble":
            result = sol.copy()
            subsec, pos1, pos2 = self.SubSection(sol)
            rnd.shuffle(subsec)
            result[pos1:pos2] = subsec
            return result

        # Inversion : Take a subsection and reverse it.
        elif self.optional_prm["mutation_method"].lower() == "inversion":
            result = sol.copy()
            subsec, pos1, pos2 = self.SubSection(sol)
            subsec.reverse()
            result[pos1:pos2] = subsec
            return result

            
    def run(self):
        """ Execute the Simple Genetic Algorithm SGA"""
        
        # Initialize the population bag with random elements
        pop_bag  = self.initialize()
        
        # Iterate for all generations
        for g in range(self.optional_prm["generations"]):

            # Show step of Iteration
            perc_gen = np.round(100*g/self.optional_prm["generations"], 0)
            if self.optional_prm["show_iters"]:
                print(f"\nGeneration: {g} | {perc_gen}%")
            
            # Calculate the fitness of elements in population bag
            pop_bag_fit = self.eval_fit_population(pop_bag)
            
            # Best so far
            if self.optional_prm["optimize"].lower() == "min":
                best_fit       = np.min(pop_bag_fit["fit_vals"])
            elif self.optional_prm["optimize"].lower() == "max":
                best_fit       = np.max(pop_bag_fit["fit_vals"])
                
            best_fit_index = pop_bag_fit["fit_vals"].index(best_fit)
            best_solution  = pop_bag_fit["solution"][best_fit_index]
            
            if g == 0:
                best_fit_global      = best_fit
                best_solution_global = best_solution
            else:
                if self.optional_prm["optimize"].lower() == "min":
                    if(best_fit <= best_fit_global):
                        best_fit_global      = best_fit
                        best_solution_global = best_solution
                elif self.optional_prm["optimize"].lower() == "max":
                    if(best_fit >= best_fit_global):
                        best_fit_global      = best_fit
                        best_solution_global = best_solution
            
            if self.optional_prm["show_iters"]:
                print(f"Best solution so far -> {best_solution_global} | Fitness: {best_fit_global}")
            
            # Create the new population bag
            new_pop_bag = []
            for i in range(self.optional_prm["pop_size"]):
                
                # Pick 2 parents from bag using the method of selection
                pA = self.pickOne(pop_bag_fit)
                pB = self.pickOne(pop_bag_fit)
                
                new_element = pA 
                
                # Crossover the parents if rnd <= Rcros 
                rndCross = rnd.random()
                if rndCross <= self.optional_prm["cross_prob"]:
                    new_element = self.crossover(pA,pB)
                    
                # Mutate the child of that crossover (or the parentA) if rnd <= Rmut
                rndMutat = rnd.random()
                if rndMutat <= self.optional_prm["mutat_prob"]:
                    new_element = self.mutation(new_element)  
                
                new_pop_bag.append(new_element)
            
            pop_bag = np.array(new_pop_bag)
            
        return best_fit_global, best_solution_global
                
            
    def swap(self, sol, posA, posB):
        """ Swap positions of elements in a vector. """
        result = sol.copy()
        elA = sol[posA]
        elB = sol[posB]
        result[posA] = elB
        result[posB] = elA
        return result

    def SubSection(self, vector):
        """ Get a subsection of a vector. """
        n = len(vector)
        # Number of elements to take as the subsection. Between 10% and 90% of the elements.
        num_els = np.ceil(n*(rnd.randint(10,90)/100))
        # Starting point of the subsection
        str_pnt = rnd.randint(0, n-2)
        # Ending point of the subsection
        end_pnt = n if int(str_pnt+num_els) > n else int(str_pnt+num_els)
        # Subsection of parent A
        blockA = list(vector[str_pnt:end_pnt])
        
        return blockA, str_pnt, end_pnt



# =========================================        
