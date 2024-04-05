# Adds copy so deepcopy can be used
import copy

# Faucet just tracked as another bucket
maxA = 12
maxB = 8
maxC = 3
faucet = 50
maxVals = (maxA, maxB, maxC, faucet)
optimalVal = 1

# Keep list of nodes
class Order:
    def __init__(self, prev, node):
        self.prev = prev
        self.val = node

# Pours any amount from any index to another. Will fill up to limit of any index and no more
def fill(order, i1, i2):
    # As long as both buckets are unique
    if i1 != i2:
        # Get the array and find maximum value that could be added to it
        array = copy.deepcopy(order.val)
        max = maxVals[i2] - array[i2]
        # If that max is more than the filling bucket, empty filling bucket completely
        if max >= array[i1]:
            array[i2] += array[i1]
            array[i1] = 0
        # If that max is less than the filling bucket, fill as much as possible
        else:
            array[i2] += max
            array[i1] -= max
        # Return a new order object with the new array
        return Order(order, array)
    # If the buckets are the same, just return the same object (Which should be detected as duplicate and not re-added to queue)
    return Order(order, copy.deepcopy(order.val))

# Checks if any of the buckets has a value of one gallon
def solutionChecker(array, val):
    for i in array:
        if i == val:
            return True
    return False

# Iterate through all the fill options for an object
def discoverer(order, toCheck, discovered, solutions):
    array = order.val
    for i in range(0, len(array)):
        for j in range(0, len(array)):
            # Get the new object with new values
            new = fill(order, i, j)
            # Check if it is a solution
            isSolution = solutionChecker(new.val, optimalVal)
            # If it is a new array, hasn't been discovered, and is not a solution, add to the queue
            if new.val not in discovered and not isSolution:
                discovered.append(new.val)
                toCheck.append(new)
            # If it is a solution append to solutions and do not add to queue
            if isSolution:
                solutions.append(new)

# Go through the order and print in a way to demonstrate the order of actions
def iterateOrder(order):
    if order:
        iterateOrder(order.prev)
        print(order.val)

# Iterate through the toCheck queue until it is empty
def solve(toCheck, discovered, solutions):
    while len(toCheck) > 0:
        discoverer(toCheck.pop(0), toCheck, discovered, solutions)

# Return an integer for the number of actions within an order
def getDepth(order):
    if order:
        return getDepth(order.prev) + 1
    else:
        return -1

# Get different pieces of information from the solution queue
def solutionRanker(sol):
    # Set the objects for different rankings equal to the first object of solutions
    mostw, leastw, mosta, fewa = sol[0], sol[0], sol[0], sol[0]
    # Set the values for all rankings equal to the first objects values
    mw, lw = sol[0].val[3], sol[0].val[3]
    ma, fa = getDepth(sol[0]), getDepth(sol[0])
    # Make comparisons and update based on values of solutions for every solution
    for i in sol:
        currw = i.val[3]
        curra = getDepth(i)
        if currw < mw:
            mw = currw
            mostw = i
        if currw > lw:
            lw = currw
            leastw = i
        if curra > ma:
            ma = curra
            mosta = i
        if curra < fa:
            fa = currw
            fewa = i
    return mostw, leastw, mosta, fewa

def main():
    # Create queue, discovered, and solutions lists that will be used throughout
    toCheck = [Order(None, [0, 0, 0, 50])]
    discovered = [[0, 0, 0, 50]]
    solutions = []
    # Solve the problem by passing the queues and lists
    solve(toCheck, discovered, solutions)
    # Rank solutions to use for printing
    mostWater,leastWater,mostActions,fewActions = solutionRanker(solutions)
    # Print the interesting results from the program
    print("Most water used from faucet: " + str(50 - mostWater.val[3]))
    iterateOrder(mostWater)
    print("Least water used from faucet: " + str(50 - leastWater.val[3]))
    iterateOrder(leastWater)
    print("Most actions: " + str(getDepth(mostActions)))
    iterateOrder(mostActions)
    print("Fewest actions: " + str(getDepth(fewActions)))
    iterateOrder(fewActions)
    print("Total unique solutions: " + str(len(solutions)))

main()