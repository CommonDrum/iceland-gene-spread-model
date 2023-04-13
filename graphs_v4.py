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
    #TODO: Fix the jump
    #TODO: Maybe implement distance
    
    
    
    def __init__(self):
        self.G = nx.Graph()

        self.infection = [True,False]
        self.weights_infection = [0.1, 0.9] #probability of being infected

        self.no_of_children = [0,1,2,3]
        self.weights_children = [0.3, 0.2, 0.4, 0.1] #probability of having a child depending on the number of children

        self.capacity = 4000

        self.sex = ['F','M']
        self.sex_weights = [0.5, 0.5] #probability of having a child depending on the number of children
        #reproduction rate 
        self.reproduction_rate = [0.38,0.31,0.14,0.03,0.02,0,0,0,0] #probability of having a child depending on the number of children
        #self.rr_age_modifier = [0.0,0.1,1,0.9,0.4,0.03,0.01]
        self.offspring_penalty = [0.2,0.20,0.3,0.4,0.5,1,1,1]
        self.age_penalty = [1,0.75,0.1,0.30,0.75,0.85,1,1,1]
        self.rural_reproduction_bonus = 0.1
        self.urban_bonus =  - 0.05

        self.age = [0,1,2,3,4,5,6,7,8]
        self.age_weights = [0.131,0.126,0.145,0.15,0.131,0.117,0.103,0.066,0.026] #TODO: ADJUST WEIGHTS
        self.death_rate = [0,0,0,0,0,0,0,0.2,0.3,0.50]

        #Statistics
        self.population = 0
        self.infected = 0
        self.no_of_children_by_parrent_age= [0,0,0,0,0,0,0,0,0]
        self.age_distribution = [0,0,0,0,0,0,0,0,0]
        self.age_of_death = [0,0,0,0,0,0,0,0,0,0]



        self.regions=[
            "Southwest" ,
            "Reykjavik North",
            "Reykjavik South",
            "South" ,
            "Northeast",
            "Northwest"]
        self.region_distribution= [0.28,0.185,0.183,0.145,0.12,0.087]
        self.region_is_rural = [False,False,False,True,True,True]
      
      
        self.both_parents_infected = [0.75, 0.25]
        self.one_parents_infected = [0.5, 0.5]

        self.reproduction_age = 2

        self.friend_limit = 5


    def new_node(self , age = 0, is_infected = False, partner = 0, family = [], no_of_children = 0, region = ""):
        id = uuid.uuid1().int
        self.G.add_node(id, age=age, sex=random.choices(self.sex,self.sex_weights)[0], is_infected=is_infected, partner=partner, no_of_children=no_of_children,region=region)
        #connect the family
        for i in family:
            if i != id:
                self.G.add_edge(id,i, family = True)
        self.population += 1
        if is_infected:
            self.infected += 1
        return id


    def initialize(self,size):
        for i in range(size):
            age = random.choices(self.age, self.age_weights)[0]
        
            chosen_region = random.choices(self.regions,self.region_distribution)[0]
            is_infected = random.choices(self.infection, self.weights_infection)[0]
            self.new_node(age=age, is_infected=is_infected,region=chosen_region)

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
                if self.G.nodes[random_node]["region"] == self.G.nodes[node]["region"] and random.random() <= 0.8:
                    self.G.add_edge(node,random_node, label='friend')
                elif self.G.nodes[random_node]["region"] != self.G.nodes[node]["region"] and random.random() <= 0.2:
                    self.G.add_edge(node,random_node, label='friend')

    def reproduce_node(self, node,penalty=0):
        no_of_children = self.G.nodes[node]['no_of_children']
        partner = self.G.nodes[node]['partner']

        reproduction_rate = 1 - penalty
        reproduction_rate -= self.offspring_penalty[self.G.nodes[node]['no_of_children']]
        reproduction_rate -= self.age_penalty[self.G.nodes[node]['age']]
        reproduction_rate *= -math.log(self.G.number_of_nodes()/self.capacity)*2

        #rural regions have a higher reproduction rate
        region_index = self.regions.index(self.G.nodes[node]['region'])
        if self.region_is_rural[region_index]:
            reproduction_rate += self.rural_reproduction_bonus

        
       
        if partner == 0 or random.random() > reproduction_rate or self.G.nodes[node]["sex"] == 'M':
            return
        
        is_infected = self.G.nodes[node]['is_infected']
        is_infected_partner = self.G.nodes[partner]['is_infected']
        is_infected_child = False
        

        
        if is_infected and is_infected_partner:
                is_infected_child = random.choices(self.infection, self.both_parents_infected)[0]
        elif is_infected or is_infected_partner:
                is_infected_child = random.choices(self.infection, self.one_parents_infected)[0]
        
        child = self.new_node(is_infected=is_infected_child,region=self.G.nodes[node]['region'])
        self.G.add_edge(node,child, label='family',)
        self.no_of_children_by_parrent_age[self.G.nodes[node]['age']] += 1

        for neighbor in self.G.neighbors(node):
            if self.G.get_edge_data(node, neighbor).get('label') == 'family':
                self.G.add_edge(neighbor,child, label='family')

        if penalty == 0:
            self.reproduce_node(node,penalty=0.01)

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
        if random.random() < self.death_rate[ self.G.nodes[node]['age']] or self.G.nodes[node]['age'] > 8:
            if self.G.nodes[node]['partner'] != 0:
            #change the partner status of the partner
                p = self.G.nodes[node]['partner']
                self.G.nodes[p]['partner'] = 0
            self.population -= 1
            if self.G.nodes[node]['is_infected']:
                self.infected -= 1
            self.age_of_death[self.G.nodes[node]['age']] += 1
            self.G.remove_node(node)

    def step(self):
        for node in list(self.G.nodes):
            self.find_friends_node(node)
            self.partner_node(node)
            self.reproduce_node(node)
            self.age_node(node)
    def step2(self):
        for node in list(self.G.nodes):
            self.find_friends_node(node)



    




for i in range (3):
    G = GraphInterface()
    G.initialize(1600)
    populaion_list = []
    infected_list = []
    average_births_per_decade = 0

    for i in range (2):
        G.step2()

    for i in range (100):
        G.step()
        populaion_list.append(G.population)
        infected_list.append(G.infected)

        
        #if G.infected == 0:
            #break

    average_births_per_decade = sum(G.no_of_children_by_parrent_age)/100
    print(average_births_per_decade)
    plt.figure("1")
    plt.plot(populaion_list)
    plt.plot(infected_list)
    sum_of_births = sum(G.no_of_children_by_parrent_age)
    print(G.no_of_children_by_parrent_age[1]/sum_of_births)
    print(G.no_of_children_by_parrent_age[2]/sum_of_births)
    print(G.no_of_children_by_parrent_age)
    print(G.age_of_death)
    #plt.figure("2")
    #ax = plt.figure().add_subplot(projection='3d')
    #ax.plot(xs = populaion_list, ys = infected_list, zs = range(100) )
    #plt.xlabel("Population")
    #plt.ylabel("Infected")
    #plt.clabel("Time")

print(G.no_of_children_by_parrent_age)
print(G.age_of_death)
plt.show()

"""
# Get a random edge and read its attributes
u, v = random.choice(list(G.edges()))
print(f"The random edge is ({u}, {v}) with attributes:")
for key, value in G.edges[(u, v)].items():
    print(f"  - {key}: {value}")
"""