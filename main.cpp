#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <string>
#include <sstream>
#include <chrono>
#include <unordered_set>
#include <cmath>
#include <iomanip>
using namespace std;

vector<vector<float>> readFile() {
    vector<vector<float>> data;
    string fileName= "";
    cout << "Type the name of the file to test: " << flush;
    cin >> fileName; cout << endl;
    ifstream file(fileName);
    if (!file.is_open()) { cout << "File not found" << endl; return data; }
    string line;
    while (getline(file, line)) {
        vector<float> row;
        stringstream ss(line);
        float value;
        while (ss >> value) {
            row.push_back(value);
        }
        data.push_back(row);
    }
    return data;
}

int counts(vector<vector<float>> data, float value) {
    int count = 0;
    for (int i = 0; i < (int)data.size(); i++)
        if (data[i][0] == value) count++;
    return count;
}

void printState(unordered_set<int> state) {
    stringstream ss;
    ss << "{";
    for (auto i : state) ss << i << ',';
    ss.seekp(-1, ss.cur);
    ss << "}";
    cout << ss.str();
}

double CrossValidation(auto data, auto features) { // leave-one-out cross validation or n-fold cross validation
    int success = 0;
    for (int i=0; i<(int)data.size(); i++) {
        auto minDistance = double(10e6);
        int minIndex = -1;
        for (int j=0; j<(int)data.size(); j++) {
            if (i == j) continue;
            double distance = 0.0;
            for (auto feature : features)
                distance += pow(data[i][feature] - data[j][feature], 2);
            distance = sqrt(distance);
            if (distance < minDistance) {
                minDistance = distance;
                minIndex = j;
            }
        }
        if (data[i][0] == data[minIndex][0]) success++;
    }
    return success / (double)data.size();
}

void ForwardSelection(auto data, auto defaultRate) {
    int numFeatures = data[0].size(); // number of features + 1
    unordered_set<int> currState = {};
    unordered_set<int> bestState = {};
    double bestAccuracy = defaultRate;
    for (int i = 1; i < numFeatures; i++) {
        vector<unordered_set<int>> states;
        vector<double> accuracies;
        for (int j = 1; j < numFeatures; j++)
            if (currState.find(j) == currState.end()) {
                unordered_set<int> newState = currState;
                newState.insert(j);
                states.emplace_back(newState);
            }
        for (auto state : states) {
            auto accuracy = CrossValidation(data, state);
            accuracies.emplace_back(accuracy);
            cout << "\tUsing feature(s) "; printState(state);
            cout << ", accuracy is " << 100*accuracy << '%' << endl;
            if(accuracy > bestAccuracy) {
                bestAccuracy = accuracy;
                bestState = state;
            }
        }
        int idx = max_element(accuracies.begin(), accuracies.end()) - accuracies.begin();
        currState = states[idx];
        cout << "Feature set "; printState(currState); cout << " was best with an accuracy of " << 100*accuracies[idx] << '%' << endl;
    }
    cout << "\nFinished search!!\nThe best feature set is "; printState(bestState); 
    cout << " with an accuracy of " << 100*bestAccuracy << '%' << endl;
}

void BackwardElimination(auto data, auto defaultRate) {
    int numFeatures = data[0].size(); // number of features + 1
    unordered_set<int> currState = {};
    for (int i = 1; i < numFeatures; i++) currState.insert(i);
    double accuracy_all = CrossValidation(data, currState);
    double bestAccuracy = max(defaultRate, accuracy_all);
    unordered_set<int> bestState = bestAccuracy == accuracy_all ? currState : unordered_set<int>();
    cout << "Using all features, accuracy is " << accuracy_all*100 << '%' << endl;
    for (int i = 1; i < numFeatures-1; i++) {
        vector<unordered_set<int>> states;
        vector<double> accuracies;
        for (int j=1; j<numFeatures; j++)
            if (currState.find(j) != currState.end()) {
                unordered_set<int> newState = currState;
                newState.erase(j);
                states.emplace_back(newState);
            }
        for (auto state : states) {
            auto accuracy = CrossValidation(data, state);
            accuracies.emplace_back(accuracy);
            cout << "\tUsing feature(s) "; printState(state);
            cout << ", accuracy is " << 100*accuracy << '%' << endl;
            if(accuracy > bestAccuracy) {
                bestAccuracy = accuracy;
                bestState = state;
            }
        }
        int idx = max_element(accuracies.begin(), accuracies.end()) - accuracies.begin();
        currState = states[idx];
        cout << "Feature set "; printState(currState); cout << " was best with an accuracy of " << 100*accuracies[idx] << '%' << endl;
    }
    cout << "\nFinished search!!\nThe best feature set is "; printState(bestState); 
    cout << " with an accuracy of " << 100*bestAccuracy << '%' << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);    
    cout << setprecision(3);
    cout << "Welcome to the Feature Selection Program!" << endl;
    vector<vector<float>> data = readFile();
    cout << "This dataset has " << data[0].size()-1 << " features, with "  << data.size() << " instances.\n\n" << flush;
    cout << "Type the number of the algorithm you want to use:\n1. Forward Selection\n2. Backward Elimination\n> " << flush;
    int algorithm = 0; cin >> algorithm;
    int ones = counts(data, 1); int twos = counts(data, 2);
    double defaultRate = max(ones, twos) / (float)data.size();
    cout << "The default rate is: " << (100*defaultRate) << '%' << endl;
    chrono::steady_clock::time_point begin = chrono::steady_clock::now();
    algorithm == 1 ? ForwardSelection(data, defaultRate) : BackwardElimination(data, defaultRate);
    chrono::steady_clock::time_point end = chrono::steady_clock::now();
    cout << "Time Elapsed: " << chrono::duration_cast<chrono::milliseconds>(end - begin).count() << " milliseconds or about "
    << chrono::duration_cast<chrono::seconds> (end - begin).count() << " seconds\n";
    return 0;
}
