# I got confused at how exactly all the components were supposed to be implemented so I just made my own from scratch
# Adds copy so deepcopy can be used
import copy

# Has east and west bank. Easy to multiply by -1 to swap between
east = -1
west = 1

# Sets the torch as a 0 and the rest of the people as tuples with their position and travel time
torch = 0
a = (1, 1)
b = (2, 2)
c = (3, 5)
d = (4, 8)

# Defines node class. Has a lot of goals and other extra objects so it is highly modifiable
class Node:
    def __init__(self,state,goal,parent,action,maxCost,cost):
        self.state = state
        self.goal = goal
        self.parent = parent
        self.action = action
        self.maxCost = maxCost
        self.cost = cost

# Gets the cost of p1 and p2 and adds to the previous cost. p2 defaults to 0 for return trips
def getCost(cost,p1, p2 = 0):
    # Pace through the different people set val1 equal to their travel time
    for i in [a,b,c,d]:
        if i[0] == p1:
            val1 = i[1]
    # Pace through the different people set val2 equal to their travel time unless p2 is not there
    if p2:
        for i in [a,b,c,d]:
            if i[0] == p2:
                val2 = i[1]
    else:
        val2 = 0
    # Return the higher travel time + the previous cost
    return cost+max(val1,val2)

# Changes the east or west of whatever items action specifies. Action just has a list of changed indexes for the state
def makeMove(node):
    for i in node.action:
        node.state[i] = node.state[i] * -1

# Recursively prints states and times of all nodes in the path to construct an in order process
def printSolution(node):
    if node.parent:
        printSolution(node.parent)
    print(str(node.cost) + " " + str(node.state))

# Primary function call
def makeAction(node):
    # If the node cost is equal to the max cost already then don't run and no longer continue that chain
    if node.cost < node.maxCost:
        # Possibilities used to track what can actually be moved on this turn
        possibilities = []
        # If the torch is on the east side
        if node.state[0] == east:
            # Get all other torches on the east side and append them to possibilities
            for i in range(1, 5):
                if node.state[i] == east:
                    possibilities.append(i)
            # The following two for loops get all possible unique pairings from possibilities and sets them to i and j
            for i in range(0, len(possibilities)+1):
                for j in range(i+1, len(possibilities)):
                    # Create a new node with practically all identical traits to previous node, but set the cost to an updated one and list the items whose locations will be changed in actions
                    newNode = Node(copy.deepcopy(node.state), node.goal, node, (0, possibilities[i], possibilities[j]), node.maxCost, getCost(node.cost, possibilities[i], possibilities[j]))
                    # Set state of newNode to reflect the list of items in actions
                    makeMove(newNode)
                    # If the newNode's state is the goal state and cost is less than or equal to 15, then a solution has been found
                    if newNode.state == newNode.goal and newNode.cost <= 15:
                        printSolution(newNode)
                        print()
                    # Else, pass the new node back through makeAction
                    else:
                        makeAction(newNode)
        # If the torch is instead on the west side
        else:
            # Get all other torches on the west side and append them to possibilites
            for i in range(1, 5):
                if node.state[i] == west:
                    possibilities.append(i)
            # Traverses through every possible one person return trip
            for i in possibilities:
                # Create a new node with practically all identical traits to previous node, but set the cost to an updated one and list the items whose locations will be changed in actions
                newNode = Node(copy.deepcopy(node.state), node.goal, node, (0, i), node.maxCost, getCost(node.cost, i))
                # Set state of newNode to reflect the list of items in actions
                makeMove(newNode)
                # If the newNode's state is the goal state and cost is less than or equal to 15, then a solution has been found
                if newNode.state == newNode.goal and newNode.cost <= 15:
                    printSolution(newNode)
                    print()
                # Else, pass the new node back through makeAction
                else:
                    makeAction(newNode)

# Defines the start, goal, max time allotted, and the beginning node. Then plugs into the solver
def solve():
    start = [east, east, east, east, east]
    goal = [west, west, west, west, west]
    maxTime = 15
    node = Node(start,goal,None,None,maxTime,0)
    makeAction(node)

# Calls solve function
def main():
    solve()

main()