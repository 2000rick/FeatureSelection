# Feature Selection
## Update December 9, 2022:
I have added a C++ implementation! <br> 
* Compared to my Python implementation, this C++ program is about *200 times faster* running on the large dataset. <br> 
* Specifically, running forward selection with Python took about 35 minutes, forward selection with C++ took about 10 seconds. <br> 
* Backward elimination + Python was about 64 minutes, with C++ it was about 19 seconds. <br> 

I have added two traceback files named `c++Traceback*`, the results are the same, of course. <br> The time it took for the search algorithms to run can be found at the end of the tracebacks.

## Objective
Find the best subset of features that maximizes the accuracy of a classifier given some dataset, where: <br>
* Each row is an instance. <br>
* The first column is the class label. <br>
* Each column is a feature, except the first. <br>

## Implementation
The implementation is in the `featSelect.py` file. <br>

In this project, I implemented two search algorithms in Python. <br>
The two (greedy) search algorithms implemented are:
* Forward Selection
* Backward Elimination

The **forward selection** algorithm starts with an empty set of features and iteratively adds the feature that *maximizes* the accuracy of the classifier. <br>
The **backward elimination** algorithm starts with the full set of features and iteratively removes the feature that *minimizes* the accuracy of the classifier. <br>

An empty set of features implies the use of the default rate, which is the accuracy of the classifier that always predicts the most frequent class. <br>

The evaluation function used is n-fold cross validation, or leave-one-out cross validation. <br>
The classifier used is Nearest Neighbor. <br>



