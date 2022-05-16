import random
import time
import sys
import threading
sys.setrecursionlimit(20000)
threading.stack_size(200000000)


# DFS
def dfs(visited, graph, node, size):
    global counter
    if node not in visited:
        stack.append(node)
        d[int(node)] = counter
        counter = counter+1
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                dfs(visited, graph, neighbour,size)
    if len(stack)!=0:
        f[int(stack.pop())] = counter
        counter = counter + 1

    if len(stack) == 0 and len(visited)<size:
        for vertex in graph.keys():
            if vertex not in visited:
                dfs(visited,graph,vertex,size)


#Creates random directed graph in matrix form
def createMatrix(size, density):
    matrix = []
    ile =0
    for row in range(size):
        matrix.append([0 for x in range(size)])

    for row in range(size):
        for el in range(size):
            if random.uniform(0,1) < density:
                matrix[row][el] =1

    for row in range(size):
        for el in range(size):
            if matrix[row][el] ==1:
               ile = ile+1
    return matrix


#converts matrix to list of angles
def createListOfAngles(matrix, size):
    loa = []
    for row in range(size):
        for el in range(size):
            if matrix[row][el] == 1:
                loa.append([row, el])
    return loa


#converts matrix to adjacency list
def createAdjacencyList(matrix, size):
    adjacencyList = {}
    for row in range(size):
        neighbours = []
        for el in range(size):
            if matrix[row][el] == 1:
                neighbours.append(el)
        adjacencyList[row] = neighbours
    return adjacencyList


#counts returning angles in adjacency list
def countAnglesAdjList(adjList,d,f):
    global  ret_angles
    for u in adjList.keys():
          for v in adjList[u]:
              if d[v] <d[u] < f[u] < f[v]:
                  ret_angles = ret_angles+1


#counts returning angles in matrix
def countAnglesMatrix(matrix, d, f,size):
    global ret_angles
    for u in range(size):
        for v in range(size):
            if matrix[u][v] == 1:
                if d[v] < d[u] < f[u] < f[v]:
                    ret_angles += 1


#counts returning angles in list of angles
def countAnglesList(loa, d, f, size):
    global ret_angles
    for a in loa:
        if d[a[1]] < d[a[0]] < f[a[0]] < f[a[1]]:
            ret_angles+=1


#Driver Code
data = {}
size = 1000
sizes = [x for x in range(size,10*size+1,size)]
density = 0.4
ret_angles = 0
visited = set() # Set to keep track of visited nodes.
stack = []
counter = 1

for s in sizes:
    data[s] = [0,0,0,0,0] #time of dfs, number of returning angles, time: matrix, adjacency list, list of angles

#DFS
for s in sizes:
    matrix = createMatrix(s, density)
    adjList = createAdjacencyList(matrix, s)
    angList = createListOfAngles(matrix,s)


    d = [0 for x in range(s + 1)]
    f = [0 for x in range(s + 1)]

    #time of dfs
    startTime = time.perf_counter()
    thread = threading.Thread(target=dfs, args=[visited, adjList, 0,s])

    thread.start()
    thread.join()

    stopTime = time.perf_counter();
    print("{} Time of DFS: {}".format(s,stopTime-startTime))
    data[s][0] = stopTime-startTime

    stopTime =0
    startTime =0

    #topology = []
    # topology sort
    # for v in sorted(f):
    #     topology.append(f.index(v))
    # topology.reverse()
    # topology = topology[:-1]

    #Count returning angles using Adjacency List
    startTime = time.perf_counter()
    countAnglesAdjList(adjList, d, f)
    stopTime = time.perf_counter()
    print("{} returning adj list:{}".format(s,ret_angles))
    data[s][3] = stopTime-startTime

    data[s][1] = ret_angles

    stopTime =0
    startTime =0
    ret_angles = 0

    #count returning angles using Adjacency Matrix
    startTime = time.perf_counter()
    countAnglesMatrix(matrix, d, f,s)
    stopTime = time.perf_counter()
    print("{} returning matrix:{}".format(s,ret_angles))
    data[s][2] = stopTime-startTime

    stopTime =0
    startTime =0
    ret_angles = 0

    #count returning angles using list of angles
    startTime = time.perf_counter()
    countAnglesList(angList,d,f,s)
    stopTime = time.perf_counter()
    print("{} returning ang:{}\n".format(s,ret_angles))
    data[s][4] = stopTime-startTime

    stopTime =0
    startTime =0
    ret_angles = 0


    visited = set()  # Set to keep track of visited nodes.
    stack = []
    counter = 1


for s in sizes:
    print(s,data[s])



#credits to Dawid Nowakowski github.com/dawidnowakowski and Bartosz Nowak
