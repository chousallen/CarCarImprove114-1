import csv
import logging
import math
from enum import IntEnum
from typing import List

import numpy as np
import pandas

from node import Direction, Node

log = logging.getLogger(__name__)


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath: str):
        # TODO : read file and implement a data structure you like
        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.node_dict = dict()  # key: index, value: the correspond node
        for i in self.raw_data:
            self.nodes.append(Node(int(i[0])))
            for j in range(4):
                if(np.isnan(i[j+1])==False):
                    self.nodes[int(i[0])-1].set_successor(i[j+1],j+1,i[j+5])
            self.node_dict[int(i[0])] = self.nodes[int(i[0])-1]

    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict
    
    def get_UID_point(self, node: Node):
        point = dict()
        for i in self.nodes:
            if (len(i.successors)==1 and i.get_index()!=node):
                path = self.BFS_2(node,i.get_index())
                x=0
                y=0
                for j in range(len(path)-1):
                    if (self.node_dict[(path[j+1])].get_direction(path[j])==1):
                        y=y+1
                    elif (self.node_dict[(path[j+1])].get_direction(path[j])==2):
                        y=y-1
                    elif (self.node_dict[(path[j+1])].get_direction(path[j])==3):
                        x=x+1
                    elif (self.node_dict[(path[j+1])].get_direction(path[j])==4):
                        x=x-1
                point[i.get_index()] = abs(x)+abs(y)
        return point

    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        ans = dict()
        for i in self.nodes:
            if i.get_index()!=node and len(i.successors)==1:
                path = self.BFS_2(node,i.get_index())
                ans[i.get_index()] = len(path)-1
        
        return ans

    def BFS_2(self, node_from: Node, node_to: Node):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        for i in self.nodes:
            i.previous = []
        queue = []
        queue.append(node_from)
        seen = set()
        seen.add(node_from)
        self.node_dict[node_from].previous.append(None)
        
        while(len(queue)>0):
            vertex = queue.pop(0)
            successors = (self.node_dict[vertex]).get_successors()
            for i in successors:
                if i[0] not in seen:
                    queue.append(i[0])
                    seen.add(i[0])
                    (self.node_dict[i[0]]).previous.append(vertex)
        ans = []  
        ans.append(node_to)
        before = self.node_dict[node_to].previous[0]
        while(before != None):
            ans.append(before)
            before = self.node_dict[before].previous[0]
        ans.reverse()
        return ans
    
    def treasure_hunt(self, node_from: Node, node_to: Node):
        ans = self.actions_to_str(self.getActions(self.BFS_2(node_from,node_to)))
        length = len(ans)
        ans = ans[1:length]
        ans = ans + 'b'        
        return ans
    
    def getAction(self, car_dir, node_from: Node, node_to: Node):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the node_to is the Successor of node_to
        # If not, print error message and return 0
        to = (self.node_dict[node_from]).get_direction(node_to)
        if (car_dir == to):
            return 1    
        if (car_dir == 1 and to == 2):
            return 2
        if(car_dir == 1 and to == 3):
            return 4
        if(car_dir == 1 and to == 4):
            return 3
        if (car_dir == 2 and to == 1):
            return 2
        if(car_dir == 2 and to == 3):
            return 3
        if(car_dir == 2 and to == 4):
            return 4
        if (car_dir == 3 and to == 1):
            return 3
        if(car_dir == 3 and to == 2):
            return 4
        if(car_dir == 3 and to == 4):
            return 2
        if (car_dir == 4 and to == 1):
            return 4
        if(car_dir == 4 and to == 2):
            return 3
        if(car_dir == 4 and to == 3):
            return 2
        return None

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        ans = []
        dir = (self.node_dict[nodes[0]]).get_direction(nodes[1])
        for i in range(len(nodes)-1):
            action = self.getAction(dir,nodes[i],nodes[i+1])
            ans.append(action)
            if(dir == 1 and action == 2):
                dir = 2
            elif(dir == 2 and action == 2):
                dir = 1
            elif(dir == 3 and action == 2):
                dir = 4
            elif(dir == 4 and action == 2):
                dir = 3
            elif(dir == 1 and action == 3):
                dir = 4
            elif(dir == 2 and action == 3):
                dir = 3
            elif(dir == 3 and action == 3):
                dir = 1
            elif(dir == 4 and action == 3):
                dir = 2
            elif(dir == 1 and action == 4):
                dir = 3
            elif(dir == 2 and action == 4):
                dir = 4
            elif(dir == 3 and action == 4):
                dir = 2
            elif(dir == 4 and action == 4):
                dir = 1
        return ans

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action - 1]
        log.info(cmds)
        return cmds

    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)