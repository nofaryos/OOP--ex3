
# Directed Weighted Graph

### Ex_3 in OOP

This project designed to model data structures and algorithms on directional weighted graphs,
this project consists of three parts.

## The first part:
 This part consists of two classes:

### 1.NodeData class:
This class is an internal class in DiGraph class and is designed to create a
vertex in the graph. Each node in the graph has a unique key, weight, tag and info, the last three used 
to define properties of the node through which it will be possible to check whether the graph is connected, find connected components of the graph and
in addition, to calculate shortest paths weights in the graph.

### 2. DiGraph class:
This class implements the interface of GraphInterface. Each graph has a 3 collections in the form of dictionary:
the first for keeping the nodes of the graph, the second for keeping the out edges and the last for keeping the enter edges. 
Changes in the graph such as: add/remove a node/edge can be made in this class. 
Dictionary data structure in Python: In dictionary, each value has a unique key, in this way we can access to value, 
add a value, or delete an value, with an O(1) time. 
Hence, we chose this data structure so that graph changes would be made quickly, even when it comes to a graph with A lots of nodes.

## The second part:
This part consists of one class:

### 3. GraphAlgo class: 
This class implements the interface of GraphAlgoInterface, this class implements algorithms that can be run on the graph:
finding the path with the minimum weight between two nodes, find connected component of specific node,
find  connected components of the whole graph and plot the graph- to plot the graph we used matplotlib Python library.
In this class we used Dijkstra's algorithm to calculate minimum  path weights in the graph- 
This algorithm scans the graph using the info and the weight of each node, at each stage of the algorithm each node is marked in black or white,
by which it is possible to know whether the algorithm has already visited a particular node in the graph, 
white node- node we have not yet been able to reach, black node- a node we were able to reach.
Moreover, to know the minimum weight of the path between the start node to particular node, we use the weight of each node.
In this algorithm we used in priority queue data structure,
In this data structure, the organ that is extracted at each stage is the organ with the minimal key. We put the nodes in a priority queue, the key to each node was its weight. In this way we found at each stage the node with the minimum weight and thus we found the path with the minimum weight
This algorithm return dictionary of predecessors nodes of the src node.
Moreover, we used BFS algorithm to find connected components in the graph- This algorithm scans the graph from 
the src node and marks each node we were able to reach in black,
then we "turn" the edges in the graph and again check which nodes we are able to reach from the same src node.
The connected component of the src node is the intersection between the above two groups.
In this way we found connected component of one node.
To find connected components for the whole graph we repeated the process for each node in the graph,
only if it no longer belongs to a particular connected component,
a node that already belongs to some connected component has a tag of (-1).

## The third part:
In this part we have made comparisons between the implementations in Python, Java, and NetworkX for of the following functions:
Dijkstra, BFS,  connected components,  connected component and shortest path.
We checked that the three implementations return the same results for each run and in addition, 
we compared the run times, the results are shown in graphs and explained in the wiki.




