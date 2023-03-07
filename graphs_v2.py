import uuid
import random
import numpy as np
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation

def animate_nodes(G, node_colors, pos=None, *args, **kwargs):
    # define graph layout if None given
    if pos is None:
            pos = nx.spring_layout(G, scale = 1)

    nodes = nx.draw_networkx_nodes(G, pos, *args, **kwargs)
    edges = nx.draw_networkx_edges(G, pos, *args, **kwargs)
    plt.axis('off')

    
    def update(ii):
        # nodes are just markers returned by plt.scatter;
        # node color can hence be changed in the same way like marker colors
        # draw graph
       
        nodes.set_array(node_colors[ii])
        return nodes,

    fig = plt.gcf()
    animation = FuncAnimation(fig, update, interval=50, frames=len(node_colors), blit=True)
    return animation





class Node:
    def __init__(self, neighbors,parents,sex):
        self.neighbors = neighbors # Think about using some kind of id instead of the actual node

        self.age = 0
        self.sex = sex # 1 == female 0 == male || for simplicity's sake stays constant for now
        self.partner = []
        self.parents = parents # Cannot be changed
        self.id = uuid.uuid1().int
        #generate unique id
    
    def set_parents(self, parents):
        self.parents = parents
    def set_partner(self, partner):
        self.partner = partner
    def set_age(self, age):
        self.age = age
    def add_age(self):
        self.age += 1
    def set_sex(self,sex):
        self.sex = sex
    def add_neighbor(self, node):
        self.neighbors.append(node.id)
    


class Graph:
    def __init__(self, nodes):
        
        
        self.nodes = nodes
        self.num_of_nodes = len(nodes)
        self.idClass = uuid

    def add_nodes(self, nodes):
        for node in nodes:
            self.nodes.append(node)
            self.num_of_nodes += 1

    def create_node(self,neighbors,parent,sex): #Creates a node and adds it to the graph and adds the node to the neighbors' neighbor list
        new_node = [Node(neighbors,parent,sex)]
        self.add_nodes(new_node)
        for i in neighbors:
            i.neighbors.append(new_node)
        return new_node
    
    def get_node(self, index):
        return self.nodes[index]
    def get_num_of_nodes(self):
        return self.num_of_nodes
    def get_nodes(self):
        return self.nodes
    def del_node(self, id):
        for i in self.nodes:
            if i.id == id:
                for j in i.neighbors:
                    j.neighbors.remove(i.id)
                    j.s.remove(i.id)
                    j.neighbors.remove(i.id)
                self.nodes.remove(i)
                self.num_of_nodes -= 1
                return True
        return False

    def get_males(self):
        output = []
        for i in self.nodes:
            if i.sex == 0:
                output.append(i)
        return output
    
    def get_females(self):
        output = []
        for i in self.nodes:
            if i.sex == 1:
                output.append(i)
        return output
    
    def group(self,nodes):
        output = []
        for i in nodes:
            for j in nodes:
                if i != j:
                    i.neighbors.append(j.id)
        return output
        

'''

'''


node1 = Node([],None,1)
node2 = Node([],None,0)
node3 = Node([],None,1)
node4 = Node([],None,0)

#add groups
graph = Graph([])
list_of_nodes = [node1,node2,node3,node4]
graph.group(list_of_nodes)
graph.add_nodes(list_of_nodes)

print(node1.id)





running = 0
nx_graph = nx.Graph()
list_of_graphs = []
color_frames = []

while (running)< 5:
    list_of_colors = []
    for i in graph.get_nodes():
        list_of_colors.append(i.sex)
        nx_graph.add_node(i.id)
        for j in i.neighbors:
            nx_graph.add_edge(i.id,j)
            if i.parents != None:
                nx_graph.add_edge(i.id,i.parents[0])
                nx_graph.add_edge(i.id,i.parents[1])   

    list_of_graphs.append(nx_graph)
    color_frames.append(list_of_colors)

    #Finding partners
    for i in graph.get_females():
        for j in graph.get_males():
            if i.partner == [] and j.partner == [] and j.age >= 2 and i.age >= 2:
                i.partner.append(j.id)
                j.partner.append(i.id)

# Making babies!
    for i in graph.get_females():
        if i.partner != None:
            i.add_age()
            if random.randint(0,100) < 50:
                graph.create_node([],[i.id,i.partner],random.randint(0,2))
#
    running += 1
print(graph.get_num_of_nodes())

for i in list_of_graphs:
    index = 0
    animation = animate_nodes(i, color_frames[index])
    animation.save('test'+str(index)+'.gif', writer='imagemagick', savefig_kwargs={'facecolor':'white'}, fps=1)
    
    index += 1


# To animate I need to create a list of lists of node colors
# And list of lists of nodes 
