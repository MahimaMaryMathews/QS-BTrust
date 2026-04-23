# evaluation/plot_results.py
import matplotlib.pyplot as plt
from evaluation.poisson_simulation import simulate

nodes = [1250, 2500, 3750, 5000]
latency = []

for n in nodes:
    l, _ = simulate(n)
    latency.append(l)

plt.figure()
plt.plot(nodes, latency, marker='o')
plt.xlabel("Number of Vehicles")
plt.ylabel("Latency")
plt.title("Latency vs Vehicle Density")
plt.grid()
plt.show()