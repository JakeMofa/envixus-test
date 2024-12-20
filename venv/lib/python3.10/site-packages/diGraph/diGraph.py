import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import random as r



class Node(object):
    '''
    Node object
    '''
    def __init__(self, ID:int=-1, connections:list=None, pos:np.array=None):
        '''
        Initialize Node object.
        ID - node identifier
        connections - list of connected nodes
        pos - (x,y) position of node
        '''
        self.ID = ID
        self.connections = [] if connections == None else connections
        self.degree = 0 if connections == None else len(connections)
        self.pos = np.array([0.0,0.0]) if pos == None else pos
        self.displacement = np.array([0.0,0.0])

    def setCoord(self, pos:np.array):
        '''
        Set node position
        pos - (x,y) position of node
        '''
        self.pos = pos

    def setDisplacement(self):
        '''
        Add displacement to node position
        '''
        self.pos += self.displacement
        self.displacement = np.array([0.0,0.0])

    def addConnection(self, connection):
        '''
        Add connection to node and update the node degree
        connection - connected node
        '''
        self.connections += [connection]
        self.degree += 1

    def addConnections(self, connections:list):
        '''
        Add connection to node and update the node degree
        connection - list of connected nodes
        '''
        self.connections += connections
        self.degree += len(connections)

    def distanceTo(self, node):
        '''
        Return distance to node
        node - Node object
        '''
        return np.sqrt((self.pos[0]-node.pos[0])**2 + (self.pos[1]-node.pos[1])**2)

    # how would you check the connections being equal?
    def equals(self, node):
        '''
        Return if equal to node
        node - Node object
        '''
        boolID = self.ID == node.ID
        boolPos = all(self.pos == node.pos)
        boolDegree = self.degree == node.degree
        return boolID and boolPos and boolDegree

    def __repr__(self):
        '''
        retrurn string representation of (self) node
        '''
        return f'<Node {self.ID} @ ({round(self.pos[0],3)},{round(self.pos[1],3)})>'



class SpringBoard(object):
    '''
    SpringBoard object
    '''
    def __init__(self, nodesDict:dict, k:float, Q:float):
        '''
        nodes - an adjacency dictionary of first positive integers
        k - coefficient of spring
        Q - coefficient of electric field
        '''

        # create a bidirectional dictionary of nodes (numbers) that do not
        # contain self-maps
        graphNodesDict = {}
        for nodeA in nodesDict:
            connectedToA = lambda nodeB : (nodeA in nodesDict[nodeB]) or (nodeB in nodesDict[nodeA])
            graphNodesDict[nodeA] = [nodeB for nodeB in nodesDict if (connectedToA(nodeB) and nodeA != nodeB)]

        # initialize the list of nodes
        self.nodes = [Node(ID + 1) for ID in range(len(nodesDict))]

        # add connections to nodes using dictionary
        for nodeA in self.nodes:
            nodeA.addConnections([self.nodes[nodeB - 1] for nodeB in graphNodesDict[nodeA.ID]])

        # set spring and field constants
        self.k = k
        self.Q = Q

        # add positions to nodes
        for (node, i) in zip(self.nodes,range(len(self.nodes))):
            arg = 2 * np.pi * i / len(nodesDict)
            node.setCoord(np.array([np.cos(arg), np.sin(arg)]))

    def _increment(self, deltaT:float):
        '''
        increments the timestep simulation by one step
        deltaT - simulation time step
        '''
        for node in self.nodes:

            # add the spring forces
            for connection in node.connections:
                deltaD = deltaT**2 * self.k * (1 - node.distanceTo(connection)) / node.degree
                vec = node.pos - connection.pos
                vec *= deltaD / np.sqrt(vec[0]**2 + vec[1]**2)
                node.displacement += vec

            # add the repellant forces
            for other in self.nodes:
                if not node.equals(other):
                    deltaD = self.Q * (deltaT / node.distanceTo(other))**2 * other.degree
                    vec = other.pos - node.pos
                    vec *= deltaD / np.sqrt(vec[0]**2 + vec[1]**2)
                    node.displacement += vec

            # add universal force
            node.displacement += -1 * node.pos / np.sqrt(sum(node.pos**2)) * node.degree * .001

        # finalize displacements
        for node in self.nodes:
            node.setDisplacement()

    def move(self, deltaT:float, n:int):
        '''
        Iterate _increment()
        deltaT - simulation time step
        n - number of time steps
        '''
        for i in range(n):
            self._increment(deltaT)

    def plot(self, saveAs:str='_'):
        '''
        Plot the graph.
        saveAs - (optional) file path to save
        '''
        fig, ax = plt.subplots(figsize=(7,7))
        ax.set_aspect('equal')
        ax.autoscale()
        for node in self.nodes:
            x = [node.pos[0] for node in self.nodes]
            y = [node.pos[1] for node in self.nodes]
        ax.plot(x,y,'o');
        for node in self.nodes:
            for connection in node.connections:
                ax.annotate('', xytext=node.pos,xy=connection.pos,
                            arrowprops={'arrowstyle': '-'}, va='center')
        plt.show();
        if saveAs != '_':
            plt.savefig(saveAs)

    def move_plot_save(self, deltaT:float, n:int, saveAs:str):
        '''
        Move forward in simulation and save image after each timestep
        deltaT - simulation time step
        n - number of time steps
        saveAs - folder path to save images
        '''
        for i in range(n):
            self.plot(f'{saveAs}/{i}');
            self._increment(deltaT)
        self.plot(f'{saveAs}/{n}')

    def settle(self, deltaT:float):
        '''
        Increment timestep simulation until objects have settled
        deltaT - simulation time step
        '''
        sumDiff = 1 # > 0.05
        while sumDiff > 0.05:
            last = {node.ID: node.pos for node in self.nodes}
            self.move(deltaT,500)
            sumDiff = sum([abs(node.pos[0] - last[node.ID][0]) + abs(node.pos[1] - last[node.ID][1]) for node in self.nodes])

    def random_reset(self):
        '''
        Randomly reset node positions
        '''
        for node in self.nodes:
            node.pos = np.array([r.uniform(0,1), r.uniform(0,1)])



class Graph(object):
    '''
    Graph object
    '''
    def __init__(self, nodesDict:dict):
        '''
        Construct Graph object
        nodesDict - adjacency of first positive integers
        '''

        # check to make sure that the keys and values are not skipping any
        # positive integers and that they are the first positive integers
        testIDs = []
        for key in nodesDict:
            testIDs += [key] + [value for value in nodesDict[key]]
        if set(testIDs) != set(range(1,len(list(set(testIDs))) + 1)):
            raise ValueError('Error in node keys and values: ' +
                             'missing number or disallowed character.')

        # make sure that the nodes dictionary is bidirectional
        graphNodesDict = {}
        connectedToA = lambda nodeB : (nodeA in nodesDict[nodeB]) or (nodeB in nodesDict[nodeA])
        for nodeA in nodesDict:
            graphNodesDict[nodeA] = [nodeB for nodeB in nodesDict if (connectedToA(nodeB) and nodeA != nodeB)]

        # make adjacency matrix
        self.adjacencyMatrix = np.vstack([np.array([1 if nodeB in graphNodesDict[nodeA] else 0 for nodeB in graphNodesDict]) for nodeA in graphNodesDict]).T

        # use SpringBoard to find good coordinates
        self.springBoard = SpringBoard(graphNodesDict, 1, -1)
        self.springBoard.move(0.1, 8000)
        self._normalize_pos()

    def _normalize_pos(self):
        '''
        Normalize the positions springboard nodes for plotting
        '''
        # collect all X and Y coordinates
        X = [node.pos[0] for node in self.springBoard.nodes]
        Y = [node.pos[1] for node in self.springBoard.nodes]
        # sutract out minmum of each
        for node in self.springBoard.nodes:
            node.pos -= np.array([min(X), min(Y)])
        # recollect all X and Y coordinates
        X = [node.pos[0] for node in self.springBoard.nodes]
        Y = [node.pos[1] for node in self.springBoard.nodes]
        # Scale by a little more than the max of each collection, X and Y
        for node in self.springBoard.nodes:
            node.pos = np.array([node.pos[0]/(max(X) + 1), node.pos[1]/(max(Y) + 1)])

    def plot(self, saveAs:str='_'):
        '''
        Plot the Graph
        saveAs - (optional) a file path to save the plot
        '''
        fig, ax = plt.subplots(figsize=(7,7))
        plt.axis('off')
        ax.set_aspect('equal')
        r = 0.04
        for node in self.springBoard.nodes:
            X1, Y1 = node.pos[0], node.pos[1]
            # TODO: structure allows for other names, but circles won't adjust
            # add circle
            ax.add_artist(plt.Circle((X1,Y1), r, color='b', fill=False, clip_on=False))
            ax.text(X1, Y1, str(node.ID), fontsize=15, horizontalalignment='center', verticalalignment='center')
            # add lines per circle
            for connection in node.connections:
                # this makes each connection only graph once
                if node.ID < connection.ID:
                    X2, Y2 = connection.pos[0], connection.pos[1]
                    d = np.sqrt((X2-X1)**2 + (Y2-Y1)**2)
                    x = r * ((X2 - X1) / d)
                    y = r * ((Y2 - Y1) / d)
                    ax.annotate('', xytext=(X1 + x, Y1 + y), xy=(X2 - x, Y2 - y),  arrowprops={'arrowstyle': '-'})
        if saveAs != '_':
            plt.savefig(saveAs)

    def force(self, n:int):
        '''
        Move forward time step simulation
        n - number of time steps
        '''
        self.springBoard.move(0.1, n)
        self._normalize_pos()

    def random_reset(self):
        '''
        Randomly reset node positions and let time step simulation resettle
        '''
        self.springBoard.random_reset()
        self.springBoard.settle(0.1)
        self._normalize_pos()



# TODO : simplify this to just depend on the Graph Class
class DiGraph(object):
    '''
    DiGraph object
    '''
    def __init__(self, nodesDict:dict):
        '''
        Construct DiGraph object
        nodesDict - adjacency dictionary of first positive integers
        '''

        # check to make sure that the keys and values are not skipping any
        # positive integers and that they are the first positive integers
        testIDs = []
        for key in nodesDict:
            testIDs += [key] + [value for value in nodesDict[key]]
        if set(testIDs) != set(range(1,len(list(set(testIDs))) + 1)):
            raise ValueError('Error in node keys and values: ' +
                             'missing number or disallowed character.')

        self.nodesDict = nodesDict

        # make adjacency matrix
        self.adjacencyMatrix = np.vstack([np.array([1 if nodeB in nodesDict[nodeA] else 0 for nodeB in nodesDict]) for nodeA in nodesDict]).T

        # use SpringBoard to find good coordinates
        self.springBoard = SpringBoard(nodesDict, 1, -1)
        self.springBoard.move(0.1, 8000)
        self._normalize_pos()

    def _normalize_pos(self):
        '''
        Normalize the positions springboard nodes for plotting
        '''
        # collect all X and Y coordinates
        X = [node.pos[0] for node in self.springBoard.nodes]
        Y = [node.pos[1] for node in self.springBoard.nodes]
        # sutract out minmum of each
        for node in self.springBoard.nodes:
            node.pos -= np.array([min(X), min(Y)])
        # recollect all X and Y coordinates
        X = [node.pos[0] for node in self.springBoard.nodes]
        Y = [node.pos[1] for node in self.springBoard.nodes]
        # Scale by a little more than the max of each collection, X and Y
        for node in self.springBoard.nodes:
            node.pos = np.array([node.pos[0]/(max(X) + 1), node.pos[1]/(max(Y) + 1)])

    def plot(self, saveAs:str='_'):
        '''
        Plot the Graph
        saveAs - (optional) a file path to save the plot
        '''
        fig, ax = plt.subplots(figsize=(7,7))
        plt.axis('off')
        ax.set_aspect('equal')
        r = 0.04
        for node in self.springBoard.nodes:
            X1, Y1 = node.pos[0], node.pos[1]
            # TODO: structure allows for other names, but circles won't adjust
            # add circle
            ax.add_artist(plt.Circle((X1,Y1), r, color='b', fill=False, clip_on=False))
            ax.text(X1, Y1, str(node.ID), fontsize=15, horizontalalignment='center', verticalalignment='center')
            # add lines per circle, only the ones that the node connects to
            for connectionIDNumber in self.nodesDict[node.ID]:
                connection = self.springBoard.nodes[connectionIDNumber - 1]
                X2, Y2 = connection.pos[0], connection.pos[1]
                d = np.sqrt((X2 - X1)**2 + (Y2 - Y1)**2)
                ax.annotate('', xytext=(X1, Y1), xy=(X2, Y2),  arrowprops={'width':.3, 'shrink': 1.2 * r / d})
        if saveAs != '_':
            plt.savefig(saveAs)

    def force(self, n:int):
        '''
        Move forward time step simulation
        n - number of time steps
        '''
        self.springBoard.move(0.1, n)
        self._normalize_pos()

    def random_reset(self):
        '''
        Randomly reset node positions and let time step simulation resettle
        '''
        self.springBoard.random_reset()
        self.springBoard.settle(0.1)
        self._normalize_pos()
