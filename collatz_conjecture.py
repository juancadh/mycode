"""
======== COLLATZ CONJECTURE ========
The Collatz conjecture is a conjecture in mathematics that concerns a sequence defined as follows: start with any positive integer n. 
Then each term is obtained from the previous term as follows: if the previous term is even, the next term is one half the previous term. 
If the previous term is odd, the next term is 3 times the previous term plus 1. The conjecture is that no matter what value of n, 
the sequence will always reach 1.

"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random as rnd
import seaborn as sb

def collatz_step(n):
    r = np.nan
    if np.mod(n,2) == 0:
        r = int(n/2)
    else:
        r = int(3 * n + 1)
    return r

def collatz(n):
    collatz_lst = []
    n_steps = 0
    r = n
    collatz_lst.append(r)
    while r != 1:
        n_steps += 1
        r = collatz_step(r)
        collatz_lst.append(r)
    return n_steps, collatz_lst

sb.set()
for i in range(2,100):
    print(i)
    n_steps, gr = collatz(i)
    max_val = max(gr)
    plt.plot(i, max_val, linestyle = '-', marker = 'o')
plt.show()