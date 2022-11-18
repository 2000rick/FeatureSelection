import scipy.stats as stats

def ReadFile():
    # Load data
    data = []
    dataFile = open('CS170_Small_Data__96.txt', 'r')
    for y in dataFile:
        entry = [float(num) for num in y.split()] #one row of data
        data.append(entry)
    dataFile.close()

    for element in data: # z normalization
        element[1:] = stats.zscore(element[1:])
    return data

def NearestNeighbor(data, features, k=1):
    # features: set of features to use
    success = 0
    for i in range(len(data)):
        # find nearest neighbor
        minDist = float('inf')
        minIdx = -1
        for j in range(len(data)):
            if i != j:
                distance = 0
                for feature in features:
                    distance += abs(data[i][feature] - data[j][feature])
                if distance < minDist:
                    minDist = distance
                    minIdx = j
        # check if success or failure
        if data[i][0] == data[minIdx][0]:
            success += 1
    accuracy = success / len(data)
    return accuracy

def FowardSelection(data):
    numFeatures = len(data[0]) # number of features + 1
    currState = set() # current state of features
    best = NearestNeighbor(data, currState)
    bestState = currState
    print("Initial accuracy (default rate): ", best)
    #iteratively add/select features starting from empty set (no features-default rate)
    for i in range(1, numFeatures):
        states = list()
        accuracies = list()
        for j in range(1, numFeatures):
            if j not in currState:
                tempState = currState.copy()
                tempState.add(j)
                states.append(tempState)
        for state in states:
            accuracy = NearestNeighbor(data, state)
            accuracies.append(accuracy)
            if accuracy > best:
                best = accuracy
                bestState = state
        idx = accuracies.index(max(accuracies))
        print("For i==", i, "Best feature set: ", states[idx], "Accuracy: ", accuracies[idx])
        currState = states[idx]
    print("Best accuracy: ", best)
    print("Best state: ", bestState)
            


def main():
    data = ReadFile()
    ones = [i for i in data if i[0] == 1]
    print("Number of 1s: ", len(ones))
    twos = [i for i in data if i[0] == 2]
    print("Number of 2s: ", len(twos))
    print("Default rate should be: ", max(len(ones), len(twos)) / len(data))
    FowardSelection(data)

if __name__ == "__main__":
    main()

# print(f'Number of rows: {len(data)}')
# print(f'Number of features: {len(data[0])-1}')
