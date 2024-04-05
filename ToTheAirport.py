import math

# Adds nodes for locs. Has connections to other nodes
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = []

# Keep list of nodes
class Order:
    def __init__(self, prev, node):
        self.prev = prev
        self.val = node

# Add nodes to one another's connections
def connecter(n1, n2):
    n1.connections.append(n2)
    n2.connections.append(n1)

# Create all nodes with locs
loc1 = Node(14, 9)
loc2 = Node(0, 1)
loc3 = Node(5, 1)
loc4 = Node(11, 0)
loc5 = Node(18, 0)
loc6 = Node(23, 0)
loc7 = Node(11, 2)
loc8 = Node(18, 2)
loc9 = Node(11, 9)
loc10 = Node(16, 10)
loc11 = Node(18, 10)
loc12 = Node(22, 7)
loc13 = Node(5, 17)
loc14 = Node(10, 17)
loc15 = Node(16, 17)
loc16 = Node(18, 17)
loc17 = Node(24, 17)
loc18 = Node(11, 23)
loc19 = Node(16, 23)
loc20 = Node(18, 23)
loc21 = Node(24, 23)

# Have start and destination defined and easily editable
start = loc1
destination = loc2

# Add connections between all nodes that need it
def makeConnections():
    connecter(loc1, loc10)
    connecter(loc1, loc9)
    connecter(loc2, loc3)
    connecter(loc3, loc4)
    connecter(loc3, loc7)
    connecter(loc4, loc7)
    connecter(loc4, loc5)
    connecter(loc7, loc8)
    connecter(loc5, loc8)
    connecter(loc5, loc6)
    connecter(loc6, loc12)
    connecter(loc12, loc17)
    connecter(loc8, loc11)
    connecter(loc11, loc12)
    connecter(loc10, loc11)
    connecter(loc11, loc16)
    connecter(loc16, loc17)
    connecter(loc10, loc15)
    connecter(loc15, loc16)
    connecter(loc16, loc20)
    connecter(loc20, loc21)
    connecter(loc17, loc21)
    connecter(loc19, loc20)
    connecter(loc15, loc19)
    connecter(loc18, loc19)
    connecter(loc18, loc14)
    connecter(loc14, loc15)
    connecter(loc14, loc9)
    connecter(loc9, loc7)
    connecter(loc3, loc13)
    connecter(loc13, loc14)
makeConnections()

# Get crow flies distance between two points
def getSquareDistance(node, destination):
    return math.sqrt((max(node.x, destination.x)-(min(node.x, destination.x)))**2+(max(node.y, destination.y)-(min(node.y, destination.y)))**2)

# Check if node has already been closed with short distance
def checkClosed(n1, newDist):
    # Iterate through closed/popped nodes
    for i in popped:
        # If n1, node that may be added to pQueue, is already on there and the new distance is larger than previously found, return False (which will not add to pQueue)
        if i[0] == n1 and i[1] < newDist:
            return False
    # If n1 not already in pQueue and/or the new distance is shorter, return True (which will add to pQueue)
    return True

# Have pQueue to grab future point from, and popped to track already visited nodes
pQueue = []
popped = []
# Append the start node to pQueue and set solution empty
pQueue.append([start, 0, getSquareDistance(start, destination), Order(None, start)])
solution = None

# While solution isn't found
while solution == None:
    # Sort pQueue by heuristic distance
    pQueue = sorted(pQueue, key=lambda x: x[2])
    # Remove first item from sorted pQueue
    vals = pQueue.pop(0)
    # If the newly popped value is not equal to destination coords
    if vals[0].x != destination.x and vals[0].y != destination.y:
        # Add the newly popped value to popped
        popped.append(vals)
        # Iterate through the new value's connections
        for i in vals[0].connections:
            # Get distance from previous node to this one
            fromPrev = getSquareDistance(vals[0], i) + vals[1]
            # Check if already closed. If not and/or isn't needed to be opened, add to pQueue
            if checkClosed(i, fromPrev):
                # Has structure of [node, actual distance, heuristic distance to end, order list]
                pQueue.append([i, fromPrev, fromPrev + getSquareDistance(i, destination), Order(vals[3], i)])
    else:
        # Set solution equal to the newest node
        solution = vals

# Print the traversed order
def printOrder(chain):
    # Get total cost by heuristic of node before final
    print("Total cost is " + str(chain[2]))
    # Traverse recursively so prints from first node down
    traverseOrder(chain[3])
    # Print final node
    print("(" + str(destination.x) + ", " + str(destination.y) + ")")
def traverseOrder(chain):
    if chain:
        traverseOrder(chain.prev)
        print("(" + str(chain.val.x) + ", " + str(chain.val.y) + ")")

# Print order of nodes for solution
printOrder(solution)