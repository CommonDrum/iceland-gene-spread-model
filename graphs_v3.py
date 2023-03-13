import uuid
import random
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation


# Create an empty graph
G = nx.Graph()

def init_graph(G,pairs, singles):

    infection = [True,False]
    weights_infection = [0.1, 0.9]

    no_of_children = [0,1,2,3]
    weights_children = [0.3, 0.2, 0.4, 0.1]

    sex = ['F','M']

    for i in range(pairs):
            id1 = uuid.uuid1().int
            id2 = uuid.uuid1().int
            G.add_node(id1, age=random.randint(2,6), sex='M', is_infected=random.choices(infection, weights_infection)[0], partner=id2,family = [])
            G.add_node(id2, age=random.randint(2,6), sex='F', is_infected=random.choices(infection, weights_infection)[0], partner=id1,family = [])
            G.add_edge(id2,id1)
            id_family = [id1,id2]
        
            for j in range(random.choices(no_of_children, weights_children)[0]):
                id_child = uuid.uuid1().int
                G.add_node(id_child, age=random.randint(0,2), sex=random.choices(sex), is_infected=random.choices(infection, weights_infection)[0], partner=None,family = [])
                id_family.append(id_child)


            for j in id_family:
                for k in id_family:
                    if j!=k:
                        G.nodes[j]["family"].append(k)
                        G.add_edge(j,k)

    for i in range(singles):
        G.add_node(uuid.uuid1().int, age=random.randint(0,2), sex=random.choices(sex), is_infected=random.choices(infection, weights_infection)[0], partner=None,family = [])
               





# use "family" variable this will ease up the process of pairing etc. 
# this can iterate through three generations of a family befor pairing


init_graph (G,10,10)
# draw the graph
nx.draw(G)

# show the graph
plt.show()
#print(G.nodes)