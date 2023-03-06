import uuid
import random




class Node:
    def __init__(self, neighbors,parent,sex):
        self.neighbors = neighbors # Think about using some kind of id instead of the actual node

        self.age = 0
        self.sex = sex # 1 == female 0 == male || for simplicity's sake stays constant for now
        self.partner = None
        self.parent = parent # Cannot be changed
        self.id = uuid.uuid4()
        #generate unique id
        



    def set_parent(self, parent):
        self.parent = parent
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

    def add_node(self, node):
        self.nodes.append(node)
        self.num_of_nodes += 1

    def create_node(self,neighbors,parent,sex): #Creates a node and adds it to the graph and adds the node to the neighbors' neighbor list
        new_node = Node(neighbors,parent,sex)
        self.add_node(new_node)
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
        


node1 = Node([],None,1)
node2 = Node([],None,0)
node3 = Node([],None,1)
node4 = Node([],None,0)

graph = Graph([])
list_of_nodes = [node1,node2,node3,node4]
graph.group(list_of_nodes)
print(node1.neighbors)
print(node2.neighbors)
print(node3.neighbors)

running = True

while (running):
    #Finding partners
    for i in graph.get_females:
        for j in graph.get_males:
            if i.partner == None and j.partner == None:
                i.partner = j
                j.partner = i

    for i in graph.get_females:
        if i.partner == None:
            i.add_age()
            if i.age >= 5:
                graph.del_node(i.id)       
    if random.random() < 0.5:
        running = False
    
