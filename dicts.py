#this was originally just to create dictionaries but now is used to save background funtions to keep main code clean
import numpy as np

coordsList = [20,140,260,380,500,620,740,860]

def nodeDictMaker():

    a = 0
    nodes = {}
    for i in coordsList:
        for j in coordsList:
            nodes[a] = [i,j]
            a+=1

    return nodes

nodeList = nodeDictMaker()
keyList = list(nodeList.keys())
valueList = list(nodeList.values())

def graphMaker():
    graph = {}
    for key in keyList:
        coords = nodeList[key]
        neighbourCoords = [[coords[0]-120,coords[1]],
                           [coords[0]+120,coords[1]],
                           [coords[0],coords[1]-120],
                           [coords[0],coords[1]+120]]
        
        neighbours = {}
        for i in neighbourCoords:
            if i in valueList:
                neighbours[keyList[valueList.index(i)]] = 120

        graph[key] = neighbours
    
    return graph

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))