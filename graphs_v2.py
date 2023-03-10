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
#Does this work now?
    
    plt.axis('off')

    
    def update(ii):
        # clear current graph
        print("lol")
        # nodes are just markers returned by plt.scatter;
        # node color can hence be changed in the same way like marker colors
        # draw graph
        
        nodes = nx.draw_networkx_nodes(G[ii], pos, *args, **kwargs)
        edges = nx.draw_networkx_edges(G[ii], pos, *args, **kwargs)
        nodes.set_array(node_colors[ii])
        plt.clf()
        fig = plt.gcf()
        return nodes, edges

    fig = plt.gcf()
    animation = FuncAnimation(fig, update, interval=1, frames=len(node_colors), blit=True)
    return animation





class Node:
    def __init__(self, neighbors,parents=[],sex = random.randint(0,2)):
        self.neighbors = neighbors # Think about using some kind of id instead of the actual node

        self.age = 0
        self.sex = sex # 1 == female 0 == male || for simplicity's sake stays constant for now
        self.partner = None
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


node1 = Node([],[],1)
node2 = Node([],[],0)
node3 = Node([],[],1)
node4 = Node([],[],0)
node5 = Node([],[],1)
node6 = Node([],[],0)
node7 = Node([],[],1)
node8 = Node([],[],0)

#add groups
graph = Graph([])
list_of_nodes = [node3,node4,node1,node2]
graph.group(list_of_nodes)
graph.add_nodes(list_of_nodes)

#print(node1.id)





running = 0

list_of_graphs = []
color_frames = []


while (running)< 10:
    nx_graph = nx.Graph()
    list_of_colors = []
    
    list_of_graphs.append(nx_graph)
    color_frames.append(list_of_colors)
    for i in graph.get_nodes():
        list_of_colors.append(i.sex)
        nx_graph.add_node(i.id)
        for j in i.neighbors:
            nx_graph.add_edge(i.id,j)
        if i.parents != None:
            for j in i.parents:  
                nx_graph.add_edge(i.id,j)   


    #Finding partners
    for i in graph.get_females():
        for j in graph.get_males():
            if i.partner == None and j.partner ==None and j.id in i.neighbors:
                i.partner = j.id
                j.partner = i.id

    # Making babies!
    for i in graph.get_females():
        if i.partner != None:
            i.add_age()
            if random.randint(0,100) < 50:
                print(i.id,i.partner)
                graph.create_node([],[i.id,i.partner],random.randint(0,2))

                # com

    
    running += 1
print(graph.get_num_of_nodes())

for i in list_of_graphs:
    plt.clf()
    pos = nx.spring_layout(i, scale = 1)
    nx.draw(i, pos)
    plt.show()
    
# To animate I need to create a list of lists of node colors
# And list of lists of nodes 
