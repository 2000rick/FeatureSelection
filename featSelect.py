import math
import time
def ReadFile(): # Load data
    data = []
    fileName = input('Type the name of the file to test: ')
    print(f'Loading data from {fileName}...\n')
    dataFile = open(fileName, 'r')
    for y in dataFile:
        entry = [float(num) for num in y.split()] #one row/instance
        data.append(entry)
    dataFile.close()
    return data

def NearestNeighbor(data, features): #using leave-one-out cross validation
    success = 0
    for i in range(len(data)):
        minDist = float('inf')
        minLocation = int(10e6)
        for j in range(len(data)):
            if i != j:
                distance = 0.0
                for feature in features: # features: the set of features to use/evaluate
                    distance += (data[i][feature] - data[j][feature]) ** 2
                distance = math.sqrt(distance)
                if distance < minDist:
                    minDist = distance
                    minLocation = j
        if data[i][0] == data[minLocation][0]:
            success += 1
    accuracy = success / len(data)
    return accuracy

def ForwardSelection(data, defaultRate):
    numFeatures = len(data[0]) # number of features + 1
    currState = set() # current state of features
    best = defaultRate
    bestState = currState
    for i in range(1, numFeatures): #iteratively add/select features
        states = list()
        accuracies = list()
        for j in range(1, numFeatures):
            if j not in currState: #if j isn't already added
                tempState = currState.copy()
                tempState.add(j)
                states.append(tempState)
        for state in states:
            accuracy = NearestNeighbor(data, state)
            accuracies.append(accuracy)
            print(f"\tUsing feature(s) {state}, accuracy is {round(accuracy*100, 1)}%")
            if accuracy > best:
                best = accuracy
                bestState = state
        idx = accuracies.index(max(accuracies))
        currState = states[idx]
        print(f"Feature set {states[idx]} was best with an accuracy of {round(accuracies[idx]*100, 1)}%")
    print(f"\nFinished search!\nThe best feature set is {bestState} with an accuracy of {round(100*best, 1)}%")

def BackwardElimination(data, defaultRate):
    numFeatures = len(data[0]) # number of features + 1
    currState = {i for i in range(1, numFeatures)} # current set of features (all)
    accuracy_all = NearestNeighbor(data, currState) # accuracy using all features
    best = max(defaultRate, accuracy_all)
    bestState = set() if best==defaultRate else currState
    print(f"Using all features, accuracy is {round(accuracy_all*100, 1)}%")
    for i in range(1, numFeatures-1): # -1 to exclude the empty set (already computed default rate)
        states = list()
        accuracies = list()
        for j in range(1, numFeatures):
            if j in currState: #if j is in currrent feature set, try removing it.
                tempState = currState.copy()
                tempState.remove(j)
                states.append(tempState)
        for state in states:
            accuracy = NearestNeighbor(data, state)
            accuracies.append(accuracy)
            print(f"\tUsing feature(s) {state}, accuracy is {round(accuracy*100, 1)}%")
            if accuracy > best:
                best = accuracy
                bestState = state
        idx = accuracies.index(max(accuracies))
        currState = states[idx]
        print(f"Feature set {states[idx]} was best with an accuracy of {round(accuracies[idx]*100, 1)}%")
    print(f"\nFinished search!\nThe best feature set is {bestState} with an accuracy of {round(100*best, 1)}%")

def main():
    print('Welcome to the Feature Selection Program!')
    data = ReadFile()
    print(f'This dataset has {len(data[0])-1} features, with {len(data)} instances.\n')
    algorithm = input('Type the number of the algorithm you want to use:\n1. Forward Selection\n2. Backward Elimination\n> ')
    ones = [1 for i in data if i[0] == 1.0]
    twos = [1 for i in data if i[0] == 2.0]
    defaultRate = max(len(ones), len(twos)) / len(data)
    print(f"\nThe default rate is: {round(defaultRate*100,1)}%")
    begin = time.time()
    ForwardSelection(data, defaultRate) if algorithm == '1' else BackwardElimination(data, defaultRate)
    end = time.time()
    print(f"Runtime: {round(end-begin, 2)} seconds or {round((end-begin)/60, 2)} minutes")
    
main()
