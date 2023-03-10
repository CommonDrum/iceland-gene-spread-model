import uuid
import random
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation


# Create an empty graph
G = nx.Graph()

# Generate nodes with attributes
for i in range(1, 1001):
    age = random.randint(18, 65)
    gender = random.choice(["Male", "Female"])
    occupation = random.choice(["Student", "Engineer", "Teacher", "Doctor", "Lawyer"])
    location = random.choice(["City A", "City B", "City C"])
    interests = random.choice(["Sports", "Music", "Travel", "Reading"])
    personality = random.choice(["Introverted", "Extroverted", "Analytical", "Emotional"])
    G.add_node(i, age=age, gender=gender, occupation=occupation, location=location, interests=interests, personality=personality)

# Generate relationships
for i in range(1, 1001):
    if G.edges(i) < 1:
        for j in range(i+1, 1001):
            if G.number_of_edges(j) < 1:
                if random.random() < 0.1: # 10% probability of forming a connection
                    G.add_edge(i, j)

# Set node and edge attributes
node_size = 20
edge_width = 0.2

# Visualize the graph
pos = nx.spring_layout(G, k = 2)
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="lightblue")
nx.draw_networkx_edges(G, pos, width=edge_width, edge_color="gray")
plt.axis("off")
plt.show()