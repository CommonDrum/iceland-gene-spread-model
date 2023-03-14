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

new_friends = 4

reproduction_rate = 0.9


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
                G.add_node(id_child, age=random.randint(0,2), sex=random.choices(sex), is_infected=random.choices(infection, weights_infection)[0], partner=None,family = [])
                id_family.append(id_child)


            for j in id_family:
                for k in id_family:
                    if j!=k:
                        G.nodes[j]["family"].append(k)
                        G.add_edge(j,k)

    for i in range(singles):
        G.add_node(uuid.uuid1().int, age=random.randint(0,2), sex=random.choices(sex), is_infected=random.choices(infection, weights_infection)[0], partner=None,family = [])
    
    #for each node find 5 random nodes and create an edge between them.
    # Without duplicates and self loops
    for i in G.nodes:
        for j in random.sample(list(G.nodes),3):
            if i!=j:
               G.add_edge(i,j)

def find_partners(G):
    #iterate through all the nodes
    for i in list(G.nodes):
        if G.nodes[i]["partner"] == None:
            for neighbor in G.neighbors(i):
                if G.nodes[neighbor]["partner"] == None and G.nodes[i]["sex"] != G.nodes[neighbor]["sex"]:
                    #print (neighbor,i)
                    G.nodes[neighbor]["partner"] = int(i)
                    G.nodes[i]["partner"] = int(neighbor)
                    
                


def make_children(G):
    weights_infected_parents = [1,0]
    all_children = []
    for i in list(G.nodes):
        #add dependence on age and no_of_children
        print (G.nodes[i]["partner"])
        if G.nodes[i]["partner"] != None and G.nodes[i]["sex"] == "F":
            print("making children")
            partner = G.nodes[i]["partner"]
            if random.random() < reproduction_rate:
                id_child = uuid.uuid1().int
                all_children.append(id_child)

                family =G.nodes[i]["family"]
                family.append(G.nodes[partner]["family"])
                if G.nodes[partner]["is_infected"] or G.nodes[i]["is_infected"]:
                    G.add_node(id_child, age=0, sex=random.choices(sex), is_infected=True, partner=None,family = family)
                else:
                    G.add_node(id_child, age=0, sex=random.choices(sex), is_infected=False, partner=None,family = family)
    print (len(all_children))


                

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
                    G.nodes[n]["partner"] = None
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


init_graph (G,100,0)
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
animation = FuncAnimation(plt.gcf(), update, frames=range(10), interval=1000)

# show the animation
plt.show()


#animation.save('test.gif', writer='imagemagick', savefig_kwargs={'facecolor':'white'}, fps=1)