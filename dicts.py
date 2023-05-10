#this was originally just to create dictionaries but now is used to save background funtions to keep main code clean
import numpy as np

coordsList = [20,140,260,380,500,620,740,860]

def nodeDictMaker():

    a = 0
    nodes = {}
    for i in coordsList:
        for j in coordsList:
            nodes[a] = [j,i]
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
                neighbours[keyList[valueList.index(i)]] = 1

        graph[key] = neighbours
    
    return graph
