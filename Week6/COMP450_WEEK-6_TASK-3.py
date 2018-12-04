


"""
========================================================================================================================
======================= Classification applications on the handwritten digits data =====================================
========================================================================================================================
In this example, you will see two different applications of Naive Bayesian Algorithm on the
digits dataset.
"""

#import pylab as pl
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from time import time
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
#import pylab as plt
 
########################################################################################################################
##################################### GETTING THE DATA & PREPARATIONS ##################################################
########################################################################################################################
 
np.random.seed(42)  # gets the same randomization each time
digits = load_digits()  # the whole dataset with the labels and other information are extracted
data = scale(digits.data)  # the data is scaled with the use of z-score
n_samples, n_features = data.shape  # the no. of samples and no. of features are determined with the help of shape
n_digits = len(np.unique(digits.target))  # the number of labels are determined with the aid of unique formula
labels = digits.target  # get the ground-truth labels into the labels
print(digits.keys())  # this command will provide you the key elements in this dataset
print(digits.DESCR) # to get the descriptive information about this dataset
 
########################################################################################################################
########################################################################################################################
 
from sklearn.model_selection import train_test_split  # some documents still include the cross-validation option but it no more exists in version 18.0
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
#import pylab as plt
y = digits.target
X = digits.data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)
 
########################################################################################################################
########################################################################################################################
 
gnb = GaussianNB()      # GaussianNB implements the Gaussian Naive Bayes algorithm for classification.
# The likelihood of the features is assumed to be Gaussian

fit = gnb.fit(X_train, y_train)     # Fit Gaussian Naive Bayes according to X_train, y_train
predicted = fit.predict(X_test)     # Perform classification on an array of test vectors X_test


print("Confusion matrix\n", confusion_matrix(y_test, predicted))   # confusion matrix
# The confusion_matrix function evaluates classification accuracy
# by computing the confusion matrix with each row corresponding to the true class
# A confusion matrix C is such that C[i,j] = number of observations known to be in group i but predicted in group j.


print("Accuracy: \t", accuracy_score(y_test, predicted))    # Accuracy classification score. (normalize = True)
# accuracy_score computes either the fraction (default) or the count (normalize=False) of correct predictions.
# The method above returns the fraction of correctly classified samples.

print("Number of correct predictions:\t",accuracy_score(y_test, predicted, normalize=False))  # correct predictions count

print("Number of all the predictions:\t",len(predicted))   # the number of all of the predictions
 
########################################################################################################################
########################################################################################################################
 
gnb = GaussianNB()              # Gaussian Naive Bayes
fit2 = gnb.fit(X, y)            # Fit Gaussian Naive Bayes
predictedx = fit2.predict(X)    # Perform classification
print("Confusion Matrix\n", confusion_matrix(y, predictedx))   # confusion matrix
print("Accuracy:\t", accuracy_score(y, predictedx))       # the fraction of correct predictions
print("Number of correct predictions:\t",accuracy_score(y, predictedx, normalize=False))  # the number of correct predictions
print("Number of all the predictions:\t",len(predictedx))  # the number of all of the predictions
 
unique_y, counts_y = np.unique(y, return_counts=True)
print(unique_y, counts_y)
 
unique_p, counts_p = np.unique(predictedx, return_counts=True)
print(unique_p, counts_p)
print((predictedx == 0).sum())
########################################################################################################################
########################################################################################################################


"""
TASK - 3A   |||     explain test-train split
Train_test_split method splits the data into two subsets (one for training and the other for test) and returns 
two vectors for each subset (X: feature, y: target)
with given param test_size in range (0-1) indicating the portion of the test data.
Splitting the data before training the model is a highly recommended method in order to avoid overfitting 
and build a more accurate system. 
Overfitting occurs when the model learns the training dataset perfectly, but when tested with new examples 
it could not perform that well.



TASK - 3B   |||     analyze & discuss the outputs (accuracy)
There are two function calls for Gaussian Naive Bayes 
The first one uses the splitted data whereas the latter one uses the data as a whole.
We observed that the accuracy increases (from 0.81 to 0.85) when the model is trained on the data without splitting it. 
One of the reasons might be that the data is familiar to the system (tested with the training data), 
so the predictions are more likely to be correct.
Number of samples in the training is also higher in the second system, which also might have had an impact on the learning. 


TASK - 3C   |||     compare two different runs of GNB what is the difference how does it affect? 
It can be inferred that the model has learned the data better in the second one, which might be the result of overfitting. 
Although the accuracy is higher in the second model When two models compared with a new set of data it may perform 
worse than expected. 
"""