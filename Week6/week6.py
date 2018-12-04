#
# week6
# COMP450Lab
#
# Created by Nehir Poyraz on 2.11.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.


from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

np.random.seed(42)  # random w/ constant seed gets the same randomization each time

digits = load_digits()  # Load and return the digits dataset (classification).
data = scale(digits.data)   # Data attribute of data
# Standardization of datasets is a common requirement for many machine learning estimators implemented in scikit-learn;
# they might behave badly if the individual features do not more or less look like standard normally distributed data:
# Gaussian with zero mean and unit variance.

n_samples, n_features = data.shape  # dimensions of the data matrix
# n_samples = number of samples (rows), n_features (columns)
n_digits = len(np.unique(digits.target))    # number of unique digits (different classes - clusters)
labels = digits.target  # class labels (list of designated labels for each sample in digits set)

sample_size = 300

print("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_digits, n_samples, n_features))

print(82 * '_')
print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')




def bench_k_means(estimator, name, data):   #
    t0 = time()
    estimator.fit(data)     #Compute k-means clustering.

    # Print different metrics for the analysis of various applications with k-means clustering
# e.g.:
# Homogeneity metric of a cluster labeling given a ground truth.
# score between 0.0 and 1.0. |  1.0 stands for perfectly homogeneous labeling
# homogeneity: each cluster contains only members of a single class.


    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

def kmeansdemo():

    """ Main body of the scikit demo of K-means clustering
    """

# The KMeans algorithm clusters data by trying to separate samples in n groups of equal variance,
# minimizing a criterion known as the inertia or within - cluster sum - of - squares.
# This algorithm requires the number of clusters to be specified.


# init: method for initialization
# 'k-means++' selects initial cluster centers for k-mean clustering in a smart way to speed up the convergence
    bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
                  name="k-means++", data=data)

# 'random': choose k observations(rows) at random from data for the initial centroids
    bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
                  name="random", data=data)

    pca = PCA(n_components=n_digits).fit(data)  # Principal Component Analysis
# Linear dimensionality reduction using Singular Value Decomposition of the data
# to project it to a lower dimensional space.

# in this case the seeding of the centers is deterministic, hence we run the kmeans algorithm only once with n_init=1
    bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
                  name="PCA-based",
                  data=data)
    print(82 * '_')

    # #############################################################################
    # Visualize the results on PCA-reduced data

    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()

def task1b():
    """ Plot the following items in the dataset
    [3, 23, 43, 63, 83, 103]"""


    for i in [3, 23, 43, 63, 83, 103]:
        print(i)
        plt.matshow(digits.images[i-1])
        print(digits.images[i-1])
        plt.title(i)
        plt.gray()
    plt.show()



def task1c():
    """Create your own image"""
    mydigit = np.zeros(shape=(8, 8))    # Create a zero array (all array elements are 0)
    for i in [3, 4]:
        mydigit[1:7, i] = 1             # Assigned the value 1 to the elements in specified locations
    print(mydigit)
    plt.gray()
    plt.matshow(mydigit)                # Display an array as a matrix in a new figure window.
    plt.show()

def task2a():
    sscores = []
    k = [i for i in range(2, 21)]
    for i in k:
        estimator = KMeans(init='k-means++', n_clusters=i, n_init=10)
        estimator.fit(data)
        sscore = metrics.silhouette_score(data, estimator.labels_,
                                 metric='euclidean',
                                 sample_size=sample_size)
        print("Sscore for k = %d is %f" %(i, sscore))
        sscores.append(sscore)
    plt.title("Silhouette scores for different k values in k-means")
    plt.xticks(k)
    plt.plot(k, sscores)
    plt.grid(True)
    plt.xlabel("K value")
    plt.ylabel("Silhouette Score")
    plt.show()

#kmeansdemo()
#task1b()

#task1c()

#task2a()

