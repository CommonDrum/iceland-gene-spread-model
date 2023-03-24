import uuid
import random
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation
import math





class GraphInterface():
    # Create an empty graph
    
    
    def __init__(self):
        self.G = nx.Graph()

        self.infection = [True,False]
        self.weights_infection = [0.2, 0.8] #probability of being infected

        self.no_of_children = [0,1,2,3]
        self.weights_children = [0.3, 0.2, 0.4, 0.1] #probability of having a child depending on the number of children

        self.capacity = 4000

        self.sex = ['F','M']
        self.sex_weights = [0.5, 0.5] #probability of having a child depending on the number of children
        self.reproduction_rate = [0.38,0.31,0.14,0.03,0.02,0] #probability of having a child depending on the number of children

        self.age = [0,1,2,3,4,5,6]
        self.age_weights = [0.1,0.2,0.3,0.2,0.1,0.05,0.05] #probability of having a child depending on the number of children

        self.population = 0
        self.infected = 0

        self.both_parents_infected = [0.75, 0.25]
        self.one_parents_infected = [0.5, 0.5]

        self.reproduction_age = 2

        self.friend_limit = 4


    def new_node(self , age = 0, is_infected = False, partner = 0, family = [], no_of_children = 0):
        id = uuid.uuid1().int
        self.G.add_node(id, age=age, sex=random.choices(self.sex,self.sex_weights)[0], is_infected=is_infected, partner=partner, no_of_children=no_of_children)
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
        new_children = 0
        for i in list(self.G.nodes):
            #if node is female (to prevent duplicate children) and is has a partner
            no_of_children = self.G.nodes[i]['no_of_children']
            if self.G.nodes[i]['partner'] != 0 and self.G.nodes[i]['sex'] == 'F' and random.random() < self.reproduction_rate[no_of_children]:
                #in the future inherite the infection status from the parents
                is_infected = self.infection_spread(i)

                family_nodes = [i,self.G.nodes[i]['partner']]
                for neighbor in self.G.neighbors(i):
                    if self.G.get_edge_data(i, neighbor).get('label') == 'family':
                        family_nodes.append(neighbor)

                child = self.new_node(family=family_nodes, is_infected=is_infected)
                new_children += 1
                #add all family nodes from both partners
        return new_children

    def infection_spread(self, i):
        if self.G.nodes[i]['is_infected'] and self.G.nodes[self.G.nodes[i]['partner']]['is_infected']:
            is_infected = random.choices(self.infection, self.both_parents_infected)[0]
        elif self.G.nodes[i]['is_infected'] and self.G.nodes[self.G.nodes[i]['partner']]['is_infected']:
            is_infected = random.choices(self.infection, self.one_parents_infected)[0]
        else:
            is_infected = False

        return is_infected

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
            age = random.choices(self.age, self.age_weights)[0]
            is_infected = random.choices(self.infection, self.weights_infection)[0]
            self.new_node(age=age, is_infected=is_infected)

    def count_friends(self, node):
        friends = 0
        for neighbor in self.G.neighbors(node):
            if self.G.get_edge_data(node, neighbor).get('label') == 'friend':
                friends += 1
        return friends
            
    def find_friends_node(self, node, new_friends = 2):
        if self.count_friends(node) >= self.friend_limit: 
            return
        # Try to give each node a new friend
        for i in range(new_friends):
            # Find a random node
            random_node = random.choice(list(self.G.nodes))
            # If the random node is not already a friend
            if random_node not in list(self.G.neighbors(node)) and random_node != node:
                # Add a new edge
                self.G.add_edge(node,random_node, label='friend')

    def reproduce_node(self, node):
        no_of_children = self.G.nodes[node]['no_of_children']
        partner = self.G.nodes[node]['partner']

        reproduction_rate = self.reproduction_rate[no_of_children] * -math.log(len(self.G.nodes)/self.capacity)
       
        if partner == 0 or random.random() > reproduction_rate or self.G.nodes[node]["sex"] == 'M':
            return
        
        is_infected = self.G.nodes[node]['is_infected']
        is_infected_partner = self.G.nodes[partner]['is_infected']
        is_infected_child = False
        

        
        if is_infected and is_infected_partner:
                is_infected_child = random.choices(self.infection, self.both_parents_infected)[0]
        elif is_infected or is_infected_partner:
                is_infected_child = random.choices(self.infection, self.one_parents_infected)[0]
        
        child = self.new_node(is_infected=is_infected_child)
        self.G.add_edge(node,child, label='family')

        for neighbor in self.G.neighbors(node):
            if self.G.get_edge_data(node, neighbor).get('label') == 'family':
                self.G.add_edge(neighbor,child, label='family')
        return
    

    def partner_node(self, node):
        if self.G.nodes[node]['partner'] == 0:
            for neighbor in self.G.neighbors(node):
                if self.G.nodes[neighbor]['partner'] == 0 and self.G.nodes[neighbor]["sex"] != self.G.nodes[node]["sex"]:
                    self.G.nodes[node]['partner'] = neighbor
                    self.G.nodes[neighbor]['partner'] = node
                    return
                
    def age_node(self, node):
        self.G.nodes[node]['age'] += 1
        if self.G.nodes[node]['age'] > 6:
            if self.G.nodes[node]['partner'] != 0:
            #change the partner status of the partner
                p = self.G.nodes[node]['partner']
                self.G.nodes[p]['partner'] = 0
            self.population -= 1
            if self.G.nodes[node]['is_infected']:
                self.infected -= 1
            self.G.remove_node(node)

    def step(self):
        for node in list(self.G.nodes):
            self.find_friends_node(node)
            self.partner_node(node)
            self.reproduce_node(node)
            self.age_node(node)




    




for i in range (1):
    G = GraphInterface()
    G.initialize(600)
    populaion_list = []
    infected_list = []
    for i in range (1000):
        G.step()
        populaion_list.append(G.population)
        infected_list.append(G.infected)
        if G.infected == 0:
            break

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