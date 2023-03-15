import uuid
import random
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation





class GraphInterface():
    # Create an empty graph
    
    
    def __init__(self):
        self.G = nx.Graph()

        self.infection = [True,False]
        self.weights_infection = [0.1, 0.9]

        self.no_of_children = [0,1,2,3]
        self.weights_children = [0.3, 0.2, 0.4, 0.1]

        self.sex = ['F','M']
        self.reproduction_rate = 0.23

        self.population = 0
        self.infected = 0
        


    def new_node(self, sex =  random.choices(['F','M'])[0], age = 0, is_infected = False, partner = 0, family = []):
        id = uuid.uuid1().int
        self.G.add_node(id, age=age, sex=sex, is_infected=is_infected, partner=partner)
        #connect the family
        for i in family:
            if i != id:
                self.G.add_edge(id,i, family = True)
        self.population += 1
        if is_infected:
            self.infected += 1
        return id
    
    def find_friends(self,new_friends = 2):
        # Try to give each node a new friend
        for n in list(self.G.nodes):
            for i in range(new_friends):
                # Find a random node
                random_node = random.choice(list(self.G.nodes))
                # If the random node is not already a friend
                if random_node not in list(self.G.neighbors(n)):
                    # Add a new edge
                    self.G.add_edge(n,random_node, family = False)
                    
    
    def pair(self):
        for u, v, attrs in self.G.edges(data=True):
            if attrs.get('family') == False:
                # If the nodes are not already a couple
                if self.G.nodes[u]['partner'] == 0 and self.G.nodes[v]['partner'] == 0:
                    self.G.nodes[u]['partner'] = v
                    self.G.nodes[v]['partner'] = u

    def reproduce(self):
        for i in list(self.G.nodes):
            #if node is female (to prevent duplicate children) and is has a partner
            if self.G.nodes[i]['partner'] != 0 and self.G.nodes[i]['sex'] == 'F' and random.random() < self.reproduction_rate:
                #in the future inherite the infection status from the parents
                if self.G.nodes[i]['is_infected'] and self.G.nodes[self.G.nodes[i]['partner']]['is_infected']:
                    is_infected = True
                else:
                    is_infected = False 

                family_nodes = [i,self.G.nodes[i]['partner']]
                for neighbor in self.G.neighbors(i):
                    if self.G.get_edge_data(i, neighbor).get('label') == 'family':
                        family_nodes.append(neighbor)

                child = self.new_node(family=family_nodes, is_infected=is_infected)
                #add all family nodes from both partners

    def ageing(self):
        for i in list(self.G.nodes):
            self.G.nodes[i]['age'] += 1
            if self.G.nodes[i]['age'] > 5:
                if self.G.nodes[i]['partner'] != 0:
                #change the partner status of the partner
                    p = self.G.nodes[i]['partner']
                    self.G.nodes[p]['partner'] = 0
                self.population -= 1
                if self.G.nodes[i]['is_infected']:
                    self.infected -= 1
                self.G.remove_node(i)
    def initialize(self,size):
        for i in range(size):
            self.new_node(is_infected=random.choices(self.infection, self.weights_infection)[0])
    




    
G = GraphInterface()
G.initialize(1000)
populaion_list = []
infected_list = []
for i in range (100):
    G.find_friends()
    G.pair()
    G.reproduce()
    G.ageing()
    populaion_list.append(G.population)
    infected_list.append(G.infected)

plt.plot(populaion_list)
plt.plot(infected_list)
plt.show()

"""
# Get a random edge and read its attributes
u, v = random.choice(list(G.edges()))
print(f"The random edge is ({u}, {v}) with attributes:")
for key, value in G.edges[(u, v)].items():
    print(f"  - {key}: {value}")
"""