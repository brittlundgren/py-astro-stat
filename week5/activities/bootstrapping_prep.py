#!/usr/bin/python

''' Data preparation script for boostrapping activity.
'''

import scipy
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt





w = scipy.random.weibull(1.5, 5000)
plt.hist(w, bins=30)
plt.show()

np.save('./data/bootstrap_distribution', w)

n = len(w)

num_samples = 50

indexes = npr.randint(0, n, (num_samples, n))

samples = w[indexes]







