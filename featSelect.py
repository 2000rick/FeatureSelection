import math

def ReadFile(): # Load data
    data = []
    fileName = 'CS170_Large_Data__35.txt'
    print(f'Loading data from {fileName}...')
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
        minLocation = int(10e6)
        for j in range(len(data)):
            if i != j:
                distance = 0.0
                for feature in features:
                    distance += (data[i][feature] - data[j][feature]) ** 2
                distance = math.sqrt(distance)
                if distance < minDist:
                    minDist = distance
                    minLocation = j
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
        for state in states:
            accuracy = NearestNeighbor(data, state)
            accuracies.append(accuracy)
            print(f"\tUsing feature(s) {state}, accuracy is {round(accuracy*100, 1)}%")
            if accuracy > best:
                best = accuracy
                bestState = state
        idx = accuracies.index(max(accuracies))
        print(f"Feature set {states[idx]} was best with an accuracy of {round(accuracies[idx]*100, 1)}%")
        currState = states[idx]
    print(f"\nFinished search!\nThe best feature set is {bestState} with an accuracy of {round(100*best, 1)}%")

def TestNN(data, features):
    print("\nTesting Nearest Neighbor...")
    print('Hard coded feature set:', features)
    accuracy = NearestNeighbor(data, features)
    print(f"NearestNeighbor returned an accuracy of: {100*accuracy}%")

def main():
    data = ReadFile()
    print(f'This dataset has {len(data[0])-1} features, with {len(data)} instances.\n')
    ones = [1 for i in data if i[0] == 1.0]
    twos = [1 for i in data if i[0] == 2.0]
    defaultRate = max(len(ones), len(twos)) / len(data)
    print(f"The default rate is: {round(defaultRate*100,1)}%")
    FowardSelection(data, defaultRate)
    # TestNN(data, {1,5,4})
    # TestNN(data, {5,2,3})
    # TestNN(data, {1,4,2})

main()
