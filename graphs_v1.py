import numpy as np
import matplotlib.pyplot as plt; plt.close('all')
import networkx as nx
from matplotlib.animation import FuncAnimation

def animate_nodes(G, node_colors, pos=None, *args, **kwargs):
    plt.figure(2)
    # define graph layout if None given
    if pos is None:
        pos = nx.spring_layout(G, scale = 1)

    # draw graph
    nodes = nx.draw_networkx_nodes(G, pos, *args, **kwargs)
    edges = nx.draw_networkx_edges(G, pos, *args, **kwargs)
    plt.axis('off')

    def update(ii):
        # nodes are just markers returned by plt.scatter;
        # node color can hence be changed in the same way like marker colors
        nodes.set_array(node_colors[ii])
        return nodes,

    fig = plt.gcf()
    animation = FuncAnimation(fig, update, interval=50, frames=len(node_colors), blit=True)
    return animation



def main(total_nodes = 50,time_steps = 20):


    num_of_red = []
    num_of_blue = []
    graph = nx.gnp_random_graph(total_nodes, p = 0.75, seed=None, directed=False) 
    node_colors = np.random.randint(0, 2, size=(total_nodes))
    color_frames= np.empty([1, total_nodes])
    color_frames[0] = node_colors
    print(color_frames) 
    counter = 0

    while (len(np.unique(node_colors)) != 1 and counter <= 50000):
        
        index1 = np.random.randint (0,total_nodes)
        index2 = np.random.randint(0,len(graph[index1]))
        node_colors[index2] = node_colors[index1]
        color_frames = np.vstack([color_frames, node_colors])
        node_colors[index1] = node_colors[index2]
        counter +=1
        print(counter)
        
    
    color_frames = np.vstack([color_frames, node_colors])

    for i in color_frames:
        red = 0
        blue = 0
        for j in i:
            if(j == 0):
                    red += 1
            else:
                 blue += 1
        num_of_blue.append(blue)
        num_of_red.append(red)
        
    
    #nimation = animate_nodes(graph, color_frames)
    #animation.save('Documents/test.gif', writer='imagemagick', savefig_kwargs={'facecolor':'white'}, fps=1)
    plt.figure(1)

    plt.plot(num_of_blue,color="blue")
    plt.plot(num_of_red,color="red")
    plt.show()


main()