import math

def ReadFile(): # Load data
    data = []
    fileName = 'CS170_Small_Data__96.txt'
    dataFile = open(fileName, 'r')
    for y in dataFile:
        entry = [float(num) for num in y.split()] #one row/instance
        data.append(entry)
    dataFile.close()
    return data

def NearestNeighbor(data, features): #using leave-one-out cross validation
    # features: the set of features to use/evaluate
    success = 0
    for i in range(len(data)):
        minDist = float('inf')
        minLocation = 10e6
        for j in range(len(data)):
            if i != j:
                distance = 0.0
                for feature in features:
                    distance += (data[i][feature] - data[j][feature]) ** 2
                distance = math.sqrt(distance)
                if distance < minDist:
                    minDist = distance
                    minLocation = j
        # check if success or failure
        if data[i][0] == data[minLocation][0]:
            success += 1
    accuracy = success / len(data)
    return accuracy

def FowardSelection(data, defaultRate):
    numFeatures = len(data[0]) # number of features + 1
    currState = set() # current state of features
    best = defaultRate
    bestState = currState
    #iteratively add/select features
    for i in range(1, numFeatures):
        states = list()
        accuracies = list()
        for j in range(1, numFeatures):
            if j not in currState: #if j isn't already added
                tempState = currState.copy()
                tempState.add(j)
                states.append(tempState)
        # print("states: ", states)
        for state in states:
            accuracy = NearestNeighbor(data, state)
            accuracies.append(accuracy)
            if accuracy > best:
                best = accuracy
                bestState = state
        idx = accuracies.index(max(accuracies))
        # print("Accuracy list:", accuracies)
        # print("index:", idx)
        print("For i ==", i, "Best feature set: ", states[idx], "Accuracy:", accuracies[idx])
        currState = states[idx]
    print("Best accuracy: ", best)
    print("Best state: ", bestState)

def testSelect(data, defaultRate):
    numFeatures = len(data[0]) # number of features + 1
    currState = set() # current state of features
    best = defaultRate
    bestState = currState
    accuracy = NearestNeighbor(data, {1,5,4})
    print("Test Accuracy: ", accuracy)
    if accuracy > best:
        best = accuracy
        bestState = {1,5,4}
    print("Best accuracy: ", best)
    print("Best state: ", bestState)       

def main():
    data = ReadFile()
    print(f'This dataset has {len(data[0])-1} features, with {len(data)} instances.')
    ones = [1 for i in data if i[0] == 1.0]
    twos = [1 for i in data if i[0] == 2.0]
    defaultRate = max(len(ones), len(twos)) / len(data)
    print("Default rate: ", defaultRate)
    # FowardSelection(data, defaultRate)
    testSelect(data, defaultRate)

if __name__ == "__main__":
    main()
