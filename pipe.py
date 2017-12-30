from pygame import *
from pygame import gfxdraw
from random import sample, choice
from time import time as now
from util import *
import math
import wx

app = wx.App()
start_time = now()

window = wx.Frame(None, title="ai path finder by mmd.sad.97@gmail.com", size=(800, 400))
panel = wx.Panel(window)
labelFont = wx.Font(16, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
textFont = wx.Font(14, wx.SCRIPT , wx.NORMAL, wx.NORMAL)

init()
FONT = font.Font(font.get_default_font(), 100)


class Case(Rect):
    ''
    CASE = Surface((60, 60))
    CASE.set_colorkey((1, 1, 1))
    CASERECT = CASE.get_rect()
    gfxdraw.filled_circle(CASE, 30, 30, 30, (200, 200, 200))
    gfxdraw.aacircle(CASE, 30, 30, 30, (200, 200, 200))

    def __init__(self, x, y, joncs):
        self.jonction = [0, 0, 0, 0]
        self.marqueur = False
        self.image = Case.CASE.copy()
        S = sample(((Case.CASERECT.midtop, 0), (Case.CASERECT.midright, 1), (Case.CASERECT.midbottom, 2),
                    (Case.CASERECT.midleft, 3)), 3)[:choice((2, 3))]
        if joncs[0] == 1:
            draw.line(self.image, (1, 1, 1), (30, 30), Case.CASERECT.midtop, 9)
            self.jonction[0] = 1
        if joncs[1] == 1:
            draw.line(self.image, (1, 1, 1), (30, 30), Case.CASERECT.midright, 9)
            self.jonction[1] = 1
        if joncs[2] == 1:
            draw.line(self.image, (1, 1, 1), (30, 30), Case.CASERECT.midbottom, 9)
            self.jonction[2] = 1
        if joncs[3] == 1:
            draw.line(self.image, (1, 1, 1), (30, 30), Case.CASERECT.midleft, 9)
            self.jonction[3] = 1

        Rect.__init__(self, SCREEN.blit(self.image, (x, y)))

    def rotate(self, dir):
        dir -= 2
        if dir == 1:
            self.jonction.insert(0, self.jonction.pop())
        else:
            self.jonction.append(self.jonction.pop(0))
        display.update(self)
        time.wait(40)
        self.image = transform.rotate(self.image, -90 * dir)
        # print self


class Node:
    def __init__(self, Id, rotation, connection, parent=None, cost=0, depth=0):
        self.id = Id
        self.rotation = rotation
        self.parent = parent
        self.connection = connection
        self.cost = cost
        self.depth = depth


def checkConnection(state, firstConnection, secondConnection):
    if (state == 1 and firstConnection[0] == 1 and secondConnection[2] == 1):
        return True
    elif (state == 2 and firstConnection[1] == 1 and secondConnection[3] == 1):
        return True
    elif (state == 3 and firstConnection[2] == 1 and secondConnection[0] == 1):
        return True
    elif (state == 4 and firstConnection[3] == 1 and secondConnection[1] == 1):
        return True
    return False


def mapArrayayRotation(l, r):
    n = 2 - r
    return l[n:] + l[:n]


def checkMoves(firstNode, rotation, secondNode, map):
    parent = mapArrayayRotation(map[firstNode], rotation)
    possibleMoveList = []
    diffNodes = secondNode - firstNode

    if diffNodes == 1:
        if (parent[1] == 1):
            if (parent[1] == map[secondNode][3]):
                possibleMoveList.append((secondNode, 2))
            if (parent[1] == map[secondNode][0]):
                possibleMoveList.append((secondNode, 1))
            if (parent[1] == map[secondNode][2]):
                possibleMoveList.append((secondNode, 3))
            if (parent[1] == map[secondNode][1]):
                possibleMoveList.append((secondNode, 4))

    elif diffNodes == -1:
        if (parent[3] == 1):
            if (parent[3] == map[secondNode][1]):
                possibleMoveList.append((secondNode, 2))
            if (parent[3] == map[secondNode][0]):
                possibleMoveList.append((secondNode, 3))
            if (parent[3] == map[secondNode][2]):
                possibleMoveList.append((secondNode, 1))
            if (parent[3] == map[secondNode][3]):
                possibleMoveList.append((secondNode, 4))

    elif diffNodes > 1:
        if (parent[2] == 1):
            if (parent[2] == map[secondNode][0]):
                possibleMoveList.append((secondNode, 2))
            if (parent[2] == map[secondNode][3]):
                possibleMoveList.append((secondNode, 3))
            if (parent[2] == map[secondNode][1]):
                possibleMoveList.append((secondNode, 1))
            if (parent[2] == map[secondNode][2]):
                possibleMoveList.append((secondNode, 4))

    else:
        if (parent[0] == 1):
            if (parent[0] == map[secondNode][2]):
                possibleMoveList.append((secondNode, 2))
            if (parent[0] == map[secondNode][3]):
                possibleMoveList.append((secondNode, 1))
            if (parent[0] == map[secondNode][1]):
                possibleMoveList.append((secondNode, 3))
            if (parent[0] == map[secondNode][0]):
                possibleMoveList.append((secondNode, 4))

    return possibleMoveList



# BFS
def breadthFirstSearch(start, end, mapArray):
    global x, y
    pushCounter, popCounter = 0.0, 0.0
    nodeQueue = Queue()
    startNode = Node(start, 2, mapArray[start])
    endNode = Node(end, 2, mapArray[end])
    finishflag = True
    path = []
    rotArr = [2, 1, 4, 3]
    visitedNodes = set()
    nodeQueue.push(startNode)
    pushCounter += 1

    while not nodeQueue.isEmpty() and finishflag:
        currentNode = nodeQueue.pop()
        popCounter += 1
        visitedNodes.add(currentNode.id)

        if (currentNode.id == endNode.id):
            while currentNode.parent != None:
                path.append(currentNode)
                currentNode = currentNode.parent
                finishflag = False

        else:
            if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes)):
                state = 1

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode)
                        nodeQueue.push(childNode)
                        pushCounter += 1

            if ((currentNode.id + 1) % x != 0 and (currentNode.id + 1 not in visitedNodes)):
                state = 2

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode)
                        nodeQueue.push(childNode)
                        pushCounter += 1

            if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes)):
                state = 3

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode)
                        nodeQueue.push(childNode)
                        pushCounter += 1

            if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes)):
                state = 4

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode)
                        nodeQueue.push(childNode)
                        pushCounter += 1

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel,
                                              label=str(int(pushCounter)) + " / " + str(int(popCounter)) + " = " + str(
                                                  pushCounter / popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


# DFS
def depthFirstSearch(start, end, mapArray):
    global x, y
    pushCounter , popCounter = 0.0,0.0
    nodeStack = Stack()
    startNode = Node(start, 2, mapArray[start])
    endNode = Node(end, 2, mapArray[end])
    finishflag = True
    path = []
    rotArr = [2, 1, 4, 3]
    visitedNodes = set()
    nodeStack.push(startNode)
    pushCounter += 1

    while not nodeStack.isEmpty() and finishflag:
        currentNode = nodeStack.pop()
        popCounter += 1
        visitedNodes.add(currentNode.id)

        if (currentNode.id == endNode.id):
            while currentNode.parent != None:
                path.append(currentNode)
                currentNode = currentNode.parent
                finishflag = False

        else:
            if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes)):
                state = 1

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode)
                        nodeStack.push(childNode)
                        pushCounter += 1


            if ((currentNode.id + 1) % x != 0 and (currentNode.id + 1 not in visitedNodes)):
                state = 2

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode)
                        nodeStack.push(childNode)
                        pushCounter += 1

            if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes)):
                state = 3

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode)
                        nodeStack.push(childNode)
                        pushCounter += 1

            if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes)):
                state = 4

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode)
                        nodeStack.push(childNode)
                        pushCounter += 1

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel,
                                              label=str(int(pushCounter)) + " / " + str(int(popCounter)) + " = " + str(
                                                  pushCounter / popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


# UCS
def uniformCostSearch(start, end, mapArray):
    global x, y
    pushCounter, popCounter = 0.0, 0.0
    nodeQueue = PriorityQueue()
    startNode = Node(start, 2, mapArray[start])
    endNode = Node(end, 2, mapArray[end])
    finishflag = True
    cost = 0
    path = []
    rotArr = [2, 1, 4, 3]
    visitedNodes = set()
    nodeQueue.push(startNode, startNode.cost)
    pushCounter += 1

    while not nodeQueue.isEmpty() and finishflag:
        currentNode = nodeQueue.pop()
        popCounter += 1
        visitedNodes.add(currentNode.id)

        if (currentNode.id == endNode.id):
            while currentNode.parent != None:
                path.append(currentNode)
                currentNode = currentNode.parent
                finishflag = False

        else:
            if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes)):
                state = 1

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode, childNode.cost)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0
            if ((currentNode.id + 1) % x != 0 and (currentNode.id + 1 not in visitedNodes)):
                state = 2

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode, childNode.cost)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes)):
                state = 3

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode, childNode.cost)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes)):
                state = 4

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode, childNode.cost)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel, label=str(int(pushCounter)) + " / " + str(int(popCounter)) + " = " + str(
        pushCounter / popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


# IDS
def IterativeDeepeningSearch(start, end, mapArray):
    global x, y
    pushCounter, popCounter = 0.0, 0.0
    flag = True
    depth = 0

    while (flag):

        nodeStack = Stack()
        startNode = Node(start, 2, mapArray[start])
        endNode = Node(end, 2, mapArray[end])
        finishflag = True
        path = []
        rotArr = [2, 1, 4, 3]
        visitedNodes = set()
        nodeStack.push(startNode)
        pushCounter +=1

        for i in range(depth + 1):
            localdepth = 0
            currentNode = nodeStack.pop()
            popCounter += 1
            visitedNodes.add(currentNode.id)

            if (currentNode.id == endNode.id):
                flag = False
                while currentNode.parent != None:
                    path.append(currentNode)
                    currentNode = currentNode.parent
                    finishflag = False

            else:

                # CheckLeft
                if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes) and currentNode.depth <= i):
                    state = 4
                    for i in range(4):
                        temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                        if checkConnection(state, currentNode.connection, temp):
                            localdepth = currentNode.depth + 1
                            childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode, 0, localdepth)
                            nodeStack.push(childNode)
                            pushCounter += 1

                            # CheckDown
                if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes) and currentNode.depth <= i):
                    state = 3

                    for i in range(4):
                        temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                        if checkConnection(state, currentNode.connection, temp):
                            localdepth = currentNode.depth + 1
                            childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode, 0, localdepth)
                            nodeStack.push(childNode)
                            pushCounter += 1

                # CheckRight
                if ((currentNode.id + 1) % x != 0 and (
                                currentNode.id + 1 not in visitedNodes) and currentNode.depth <= i):
                    state = 2

                    for i in range(4):
                        temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                        if checkConnection(state, currentNode.connection, temp):
                            localdepth = currentNode.depth + 1
                            childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode, 0, localdepth)
                            nodeStack.push(childNode)
                            pushCounter += 1

                            # CheckUp
                if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes) and currentNode.depth <= i):
                    state = 1

                    for i in range(4):
                        temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                        if checkConnection(state, currentNode.connection, temp):
                            localdepth = currentNode.depth + 1
                            childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode, 0, localdepth)
                            nodeStack.push(childNode)
                            pushCounter += 1

            if (not flag):
                break

        depth = depth + 1

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel, label=str(int(pushCounter)) + " / " + str(int(popCounter)) + " = " + str(
        pushCounter / popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


# heuristic helper functions

def h(node):
    global END
    global x, y

    endY = END / x
    endX = END % x

    nodeY = node.id / x
    nodeX = node.id % x

    distance = math.sqrt((endY - nodeY) ** 2 + (endX - nodeX) ** 2)

    return distance

def g(node):
    return node.cost

def f(node):
    return g(node) + h(node)

def modifiedF(node, gFactor=3, hFactor=2):
    return gFactor*g(node) + hFactor*h(node)


# heuristic search functions

def aStarSearch(start, end, mapArray):
    global END
    global x, y
    pushCounter , popCounter = 0.0,0.0

    nodeQueue = PriorityQueueWithFunction(f)
    startNode = Node(start, 2, mapArray[start])
    endNode = Node(end, 2, mapArray[end])
    finishflag = True
    cost = 0
    path = []
    rotArr = [2, 1, 4, 3]
    visitedNodes = set()
    nodeQueue.push(startNode)
    pushCounter += 1

    while not nodeQueue.isEmpty() and finishflag:
        currentNode = nodeQueue.pop()
        popCounter += 1
        visitedNodes.add(currentNode.id)
        localDepth = 0

        if (currentNode.id == endNode.id):
            while currentNode.parent != None:
                path.append(currentNode)
                currentNode = currentNode.parent
                finishflag = False

        else:
            if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes)):
                state = 1

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localDepth = 0
                    cost = 0
            if ((currentNode.id + 1) % x != 0 and (currentNode.id + 1 not in visitedNodes)):
                state = 2

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes)):
                state = 3

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes)):
                state = 4

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel, label=str(int(pushCounter)) + " / " + str(int(popCounter)) + " = " + str(
        pushCounter / popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


def manhattanHeuristicSearch(start, end, mapArray):
    global END
    global x, y
    pushCounter , popCounter = 0.0,0.0

    nodeQueue = PriorityQueueWithFunction(g)
    startNode = Node(start, 2, mapArray[start])
    endNode = Node(end, 2, mapArray[end])
    finishflag = True
    cost = 0
    path = []
    rotArr = [2, 1, 4, 3]
    visitedNodes = set()
    nodeQueue.push(startNode)
    pushCounter += 1

    while not nodeQueue.isEmpty() and finishflag:
        currentNode = nodeQueue.pop()
        popCounter += 1
        visitedNodes.add(currentNode.id)
        localDepth = 0

        if (currentNode.id == endNode.id):
            while currentNode.parent != None:
                path.append(currentNode)
                currentNode = currentNode.parent
                finishflag = False

        else:
            if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes)):
                state = 1

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localDepth = 0
                    cost = 0
            if ((currentNode.id + 1) % x != 0 and (currentNode.id + 1 not in visitedNodes)):
                state = 2

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes)):
                state = 3

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes)):
                state = 4

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel, label=str(int(pushCounter)) + " / " + str(int(popCounter)) + " = " + str(
        pushCounter / popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


def myHeuristicSearch(start, end, mapArray):
    global END
    global x, y
    pushCounter , popCounter = 0.0,0.0

    nodeQueue = PriorityQueueWithFunction(modifiedF)
    startNode = Node(start, 2, mapArray[start])
    endNode = Node(end, 2, mapArray[end])
    finishflag = True
    cost = 0
    path = []
    rotArr = [2, 1, 4, 3]
    visitedNodes = set()
    nodeQueue.push(startNode)
    pushCounter += 1

    while not nodeQueue.isEmpty() and finishflag:
        currentNode = nodeQueue.pop()
        popCounter += 1
        visitedNodes.add(currentNode.id)
        localDepth = 0

        if (currentNode.id == endNode.id):
            while currentNode.parent != None:
                path.append(currentNode)
                currentNode = currentNode.parent
                finishflag = False

        else:
            if (currentNode.id - y >= 0 and (currentNode.id - y not in visitedNodes)):
                state = 1

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localDepth = 0
                    cost = 0
            if ((currentNode.id + 1) % x != 0 and (currentNode.id + 1 not in visitedNodes)):
                state = 2

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id + y < x * y and (currentNode.id + y not in visitedNodes)):
                state = 3

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id + y], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id + y, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

            if (currentNode.id % x != 0 and (currentNode.id - 1 not in visitedNodes)):
                state = 4

                for i in range(4):
                    temp = mapArrayayRotation(mapArray[currentNode.id - 1], rotArr[i])
                    if checkConnection(state, currentNode.connection, temp):
                        localdepth = currentNode.depth + 1
                        if (rotArr[i] == 4):
                            cost = cost + 2
                        elif (rotArr[i] != 2):
                            cost = cost + 1
                        childNode = Node(currentNode.id - 1, rotArr[i], temp, currentNode,
                                         currentNode.cost + cost + localdepth, localdepth)
                        nodeQueue.push(childNode)
                        pushCounter += 1
                    localdepth = 0
                    cost = 0

    pathTuple = []
    for i in range(len(path) - 1, -1, -1):
        pathTuple.append((path[i].id, path[i].rotation))

    print "\nthe number of nodes"
    print int(pushCounter)
    print "\neffective Branching factor: "
    print "%d / %d = %f" % (pushCounter, popCounter, pushCounter / popCounter)
    nodeNumberLabel = wx.StaticText(panel, label="node numbers:", pos=(200, 120))
    nodeNumberText = wx.StaticText(panel, label=str(int(pushCounter)), pos=(210, 150))
    nodeNumberLabel.SetFont(labelFont)
    nodeNumberText.SetFont(textFont)
    nodeNumberText.SetForegroundColour((0, 50, 255))
    effectiveBranchFactorLabel = wx.StaticText(panel, label="effective Branching factor:", pos=(400, 120))
    effectiveBranchFactorText = wx.StaticText(panel, label=str(int(pushCounter))+" / "+str(int(popCounter))+" = " + str(pushCounter/popCounter), pos=(410, 150))
    effectiveBranchFactorLabel.SetFont(labelFont)
    effectiveBranchFactorText.SetFont(textFont)
    effectiveBranchFactorText.SetForegroundColour((0, 50, 255))
    return pathTuple


def run(algorithm, start, end, array):
    if algorithm == 'BFS':
        return breadthFirstSearch(start, end, array)
    elif algorithm == 'DFS':
        return depthFirstSearch(start, end, array)
    elif algorithm == 'A*':
        return aStarSearch(start, end, array)
    elif algorithm == 'UCS':
        return uniformCostSearch(start, end, array)
    elif algorithm == 'IDS':
        return IterativeDeepeningSearch(start, end, array)
    elif algorithm == 'MANHATAN':
        return manhattanHeuristicSearch(start, end, array)
    elif algorithm == 'HEURISTIC':
        return myHeuristicSearch(start, end, array)


score = 0
x = 6  # Number of blocks in x
y = 6  # Number of blocks in y
# Each block is 60*60
SCREEN = display.set_mode((60 * x, 60 * y))
SRECT = SCREEN.get_rect()
with open('input.dat') as file:
    array2d = [[int(digit) for digit in line.split()] for line in file]  # get sequences of input.dat
ALLS = []
for i in range(x * y):
    ALLS.append(Case(60 * (i % x), 60 * (i / x), array2d[i]))
# choice(range(x*y)[::x])
START = choice(range(x * y)[::x])
END = choice(range(x * y)[x - 1::x])
# set color circle of start
gfxdraw.filled_circle(ALLS[START].image, 30, 30, 30, (200, 0, 0))  # fill
gfxdraw.aacircle(ALLS[START].image, 30, 30, 30, (200, 0, 0))  # border
SCREEN.blit(ALLS[START].image, ALLS[START])
ALLS[START].jonction = [1, 1, 1, 1]
# choice(range(x*y)[x-1::x])
array2d[START] = [1, 1, 1, 1]
array2d[END] = [1, 1, 1, 1]
# set color circle of end
gfxdraw.filled_circle(ALLS[END].image, 30, 30, 30, (0, 0, 200))
gfxdraw.aacircle(ALLS[END].image, 30, 30, 30, (0, 0, 200))
SCREEN.blit(ALLS[END].image, ALLS[END])
ALLS[END].jonction = [1, 1, 1, 1]
for i in sample(ALLS, x * y):  # Animation
    time.wait(10)
    display.update(i)

event.clear()
event.post(event.Event(MOUSEBUTTONDOWN, {'button': 1, 'pos': (0, 0)}))
event.post(event.Event(MOUSEBUTTONUP, {'button': 1, 'pos': (0, 0)}))
display.set_caption('AI Project by Amirmohammad Moradi')
time.wait(999)
timeDiff = (now() - start_time)

# algorithms are : BFS , DFS , UCS , IDS , A* , MANHATAN , HEURISTIC
path = run("HEURISTIC", START, END, array2d)


print "rotations:"
print path
print "\n path length:"
print len(path)
print "\n execution time:"
print(" %s seconds" % timeDiff)

# find path on window
for c in path:
    ALLS[c[0]].rotate(c[1])
    for i in ALLS:
        i.marqueur = False
        SCREEN.fill(0, i)
        SCREEN.blit(i.image, i)
    temp = [START]
    ALLS[START].marqueur = True
    while temp:
        for case in temp:
            for e, j in enumerate(ALLS[case].jonction):
                if j and SRECT.contains(ALLS[case].move(((0, -60), (60, 0), (0, 60), (-60, 0))[e])) \
                        and ALLS[case + (-x, 1, x, -1)[e]].marqueur == False \
                        and ALLS[case + (-x, 1, x, -1)[e]].jonction[e - 2] \
                        and case != END:
                    temp.append(case + (-x, 1, x, -1)[e])
                    ALLS[case + (-x, 1, x, -1)[e]].marqueur = True
                    SCREEN.fill(0xf00000, ALLS[case + (-x, 1, x, -1)[e]])
                    SCREEN.blit(ALLS[case + (-x, 1, x, -1)[e]].image, ALLS[case + (-x, 1, x, -1)[e]])
            temp.remove(case)
    display.update()
    time.wait(99)


pathLabel = wx.StaticText(panel, label="rotations:", pos=(20, 50))
pathText = wx.StaticText(panel, label=str(path), pos=(30, 80))
pathLenLabel = wx.StaticText(panel, label="path length: ", pos=(20, 120))
pathLenText = wx.StaticText(panel, label=str(len(path)), pos=(30, 150))
timeLabel = wx.StaticText(panel, label="execution time: ", pos=(20, 190))
timeText = wx.StaticText(panel, label=str(timeDiff), pos=(30, 220))
pathLabel.SetFont(labelFont)
pathText.SetFont(textFont)
pathText.SetForegroundColour((0,50,255))
pathLenLabel.SetFont(labelFont)
pathLenText.SetFont(textFont)
pathLenText.SetForegroundColour((0,50,255))
timeLabel.SetFont(labelFont)
timeText.SetFont(textFont)
timeText.SetForegroundColour((255,50,0))
window.Show(True)
app.MainLoop()

# close pygame
for i in sample(ALLS, len(ALLS)):
    SCREEN.fill(0, i)
    time.wait(10)
    display.update(i)
