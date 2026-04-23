# evaluation/poisson_simulation.py
import numpy as np
from scipy.stats import poisson

AREA = 2000
TIME = 300
LAMBDA = 0.1

def simulate(num_nodes):
    total_msgs = 0

    for _ in range(TIME):
        events = poisson.rvs(LAMBDA * num_nodes)
        total_msgs += events

    latency = total_msgs * num_nodes * 1e-7
    return latency, total_msgs