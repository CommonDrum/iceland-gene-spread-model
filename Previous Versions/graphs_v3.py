import uuid
import random
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation


# Create an empty graph
G = nx.Graph()

          



infection = [True,False]
weights_infection = [0.1, 0.9]

no_of_children = [0,1,2,3]
weights_children = [0.3, 0.2, 0.4, 0.1]

sex = ['F','M']

new_friends = 2

reproduction_rate = 0.9

def test_init(G):
    id1 = uuid.uuid1().int
    id2 = uuid.uuid1().int
    id3 = uuid.uuid1().int
    id4 = uuid.uuid1().int

    G.add_node(id1, age=random.randint(2,6), sex='M', is_infected=random.choices(infection, weights_infection)[0], partner=0,family = [],children = [])
    G.add_node(id2, age=random.randint(2,6), sex='F', is_infected=random.choices(infection, weights_infection)[0], partner=0,family = [],children = [])
    G.add_node(id3, age=random.randint(2,6), sex='M', is_infected=random.choices(infection, weights_infection)[0], partner=0,family = [],children = [])
    G.add_node(id4, age=random.randint(2,6), sex='F', is_infected=random.choices(infection, weights_infection)[0], partner=0,family = [],children = [])
    G.add_edge(id2,id1)
    G.add_edge(id3,id4)
    G.add_edge(id1,id3)
    G.add_edge(id2,id4)




def init_graph(G,pairs, singles):

  
    for i in range(pairs):
            id1 = uuid.uuid1().int
            id2 = uuid.uuid1().int
            #TODO:
            # - add regions/cities to simulate the population distribution
            # - 
            G.add_node(id1, age=random.randint(2,6), sex='M', is_infected=random.choices(infection, weights_infection)[0], partner=id2,family = [],children = [])
            G.add_node(id2, age=random.randint(2,6), sex='F', is_infected=random.choices(infection, weights_infection)[0], partner=id1,family = [],children = [])
            G.add_edge(id2,id1)
            id_family = [id1,id2]
        
            for j in range(random.choices(no_of_children, weights_children)[0]):
                id_child = uuid.uuid1().int
                G.add_node(id_child, age=random.randint(0,2), sex=random.choices(sex), is_infected=random.choices(infection, weights_infection)[0], partner=0,family = [],children = [])
                id_family.append(id_child)


            for j in id_family:
                for k in id_family:
                    if j!=k:
                        G.nodes[j]["family"].append(k)
                        G.add_edge(j,k)

    for i in range(singles):
        G.add_node(uuid.uuid1().int, age=random.randint(0,2), sex=random.choices(sex), is_infected=random.choices(infection, weights_infection)[0], partner=0,family = [],children = [])
    
    #for each node find 5 random nodes and create an edge between them.
    # Without duplicates and self loops
    for i in G.nodes:
        for j in random.sample(list(G.nodes),3):
            if i!=j:
               G.add_edge(i,j)

def find_partners(G):
    #iterate through all the nodes
    for i in list(G.nodes):
        if G.nodes[i]["partner"] == 0:
            print(list(G.neighbors(i)))
            for neighbor in list(G.neighbors(i)):
                if neighbor not in G.nodes[i]["family"] and G.nodes[neighbor]["partner"] == 0 and G.nodes[i]["sex"] != G.nodes[neighbor]["sex"]:
                    #print (neighbor,i)
                    G.nodes[neighbor]["partner"] = int(i)
                    G.nodes[i]["partner"] = int(neighbor)
                    
                


def make_children(G):
    weights_infected_parents = [1,0]
    for i in list(G.nodes):
        #is a woman and has a partner
        if G.nodes[i]["sex"] == 'F' and G.nodes[i]["partner"] != 0 and random.random() < reproduction_rate and G.nodes[i]["age"] > 1:
                #if either of the parents is infected, the child is infected
                id = uuid.uuid1().int
                if G.nodes[i]["is_infected"]:
                    G.add_node(id, age=0, sex=random.choices(sex)[0], is_infected=True, partner=0,family = [i,G.nodes[i]["partner"]],children = [])
                else:
                    G.add_node(id, age=0, sex=random.choices(sex)[0], is_infected=False, partner=0,family = [i,G.nodes[i]["partner"]],children = [])
                G.add_edge(i,id)
                G.add_edge(G.nodes[i]["partner"],id)    
                G.nodes[i]["children"].append(id)
                G.nodes[G.nodes[i]["partner"]]["children"].append(id)
                print(id)







                

def ageing(G):
    infected = 0
    for node in list(G.nodes):
        G.nodes[node]["age"] += 1
        partner = G.nodes[node]["partner"]
        if G.nodes[node]["age"] > 6:
            for n in G.neighbors(node):
                if n in G.nodes[node]["family"]:
                    G.nodes[n]["family"].remove(node)
                #if n in G.nodes[node]["children"]:
                 #   G.nodes[n]["children"].remove(node)
                if n == partner:
                    G.nodes[n]["partner"] = 0
            G.remove_node(node)
            
        elif G.nodes[node]["is_infected"]:
            infected += 1
    return infected

def find_friends(G):
    #adjust the number of friends according to the age (the older the less likely to make new friends)
    for i in G.nodes:
        for j in random.sample(list(G.nodes),new_friends):
            if i!=j:
                G.add_edge(i,j)



#change color of nodes based on sex and infection
def color_nodes(G):
    colors = []
    for i in G.nodes:
        if G.nodes[i]["sex"] == 'M':
            colors.append("green")
        elif G.nodes[i]["is_infected"] == True:
            colors.append("red")
        else:
            colors.append("blue")
    return colors


#init_graph (G,0,0)
test_init(G)
infected_population = []
population = []

#for i in range(1000):
'''   find_partners(G)
    make_children(G)
    infected_population.append(ageing(G))
    population.append(len(list(G.nodes)))
'''

# draw the graph
#x.draw(G,node_color=color,node_size=2,width=0.05)


#color = color_nodes(G)
# show the graph
#plt.show()



def update(ii):
    find_partners(G)
    make_children(G)
    find_friends(G)
    infected_population.append(ageing(G))
    population.append(len(list(G.nodes)))
    plt.clf()
    pos = nx.spring_layout(G)
    nx.draw(G, pos)
    plt.title('Frame %d' % ii)

# create the animation
animation = FuncAnimation(plt.gcf(), update, frames=range(1000), interval=1500)

# show the animation
plt.show()


#animation.save('test.gif', writer='imagemagick', savefig_kwargs={'facecolor':'white'}, fps=1)