# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Chapter 6

# <codecell>

# Kernel Density estimation

import matplotlib.pyplot as plt
import numpy as np

# Example data
data = [1.1,2.3,3.1,2.8,3,4.4,3,
        4.5,3.6,4.2,3.9,2.4,3.3,
        6.9,5.1,7.5,8.9,7.3,8.3,
        9.3,6.6,5.2,4.1,5.7,0.3]

data = np.append(np.random.randn(20) * 1. + 0.,
                 np.random.randn(10) * 0.5 + 1.)

data = np.array(data)
plt.scatter(data, np.ones(data.shape), alpha=0.8, s=50)
plt.show()

# <codecell>

# Function definitions

# Define 'distance' function
def dist(x1, x2):
    return np.abs(x1 - x2)


# Plotting convenience function
def show_data(data):
    for dat in data:
        plt.plot([dat,dat],[0,0.01],'-k')
        
# Kernel Density Estimator function
def estimator(location, data, kernel, distance):
    pdf = np.zeros(location.shape) # output                                             
    for i, loc in enumerate(location):
        for j, dat in enumerate(data):
            pdf[i] = pdf[i] + kernel(dist(loc, dat))
    return pdf / len(data)

        
        

# <codecell>

        ###########
        # Kernels #
        ###########
        
def gauss_kernel(sigma=0.2):
    return lambda x: np.exp(-(x)**2/2./sigma**2) / sigma / np.sqrt(2 * 3.141592)

def tophat_kernel(width=0.5):
    return lambda x: 1./width if (x) < width / 2. else 0.

#def your_kernel():

# <codecell>

# Plot some example kernel density estimators


# Example usage:
x = np.arange(-5,5,0.01)
pdf_gaussian = estimator(x, data, gauss_kernel(0.1),dist)
pdf_tophat = estimator(x, data, tophat_kernel(0.5), dist)
#pdf_yourkernel = 


plt.plot(x,pdf_gaussian, label = 'Gaussian kernel')
plt.plot(x,pdf_tophat, label='Tophat kernel')
plt.plot(x,pdf_yourkernel, label='Your kernel')

plt.xlabel('Data value')
plt.ylabel('Probability Density')
plt.legend(loc=0)
show_data(data)
plt.show()

# <codecell>

# Define Likelihood-based cross validation
# (Equation 6.5)

def Likelihood_CV(h, kernel, data, dist, cv_type='bootstrap'):
    N = len(data)
    index = np.arange(N)
    P = np.array(0.0)

    if cv_type == 'leave-one-out':       
        for i in range(N):
            oos_index = index != i
            logsample = np.log(estimator(data, data[oos_index], kernel(h), dist))
            P = P + np.sum(logsample)/N

    elif cv_type == 'bootstrap':
        for i in range(20):
            oos_index = np.random.randint(0,N,N)
            logsample = np.log(estimator(data, data[oos_index], kernel(h), dist))
            P = P + np.sum(logsample)/N/20*N
            
    return -P


print Likelihood_CV(0.09, gauss_kernel, data, dist, cv_type='bootstrap')

print Likelihood_CV(0.09, gauss_kernel, data, dist, cv_type='leave-one-out')

# <codecell>

def train_h(kernel, data, hrange=[-2, 2, 50], cv_type='bootstrap'):
    h_list = np.logspace(*hrange)
    cv_list = np.zeros(h_list.shape)
    print 'Training for h...'
    for i,h in enumerate(h_list):
        print i
        cv_list[i] = Likelihood_CV(h, kernel, data, dist, cv_type=cv_type)
    
    plt.plot(h_list, cv_list)
    plt.xscale('log')
    plt.xlabel('Gaussian Sigma $\\sigma$')
    plt.ylabel('$-\\rm \mathscr{L}_{\\rm CV}$')
    plt.show()
    hmin = h_list[np.argmin(cv_list)]
    return hmin


best_sigma = train_h(gauss_kernel, data, cv_type='bootstrap')
print 'Maximum Likelihood Sigma: ', best_sigma
print '(Try out this value above)'

# <codecell>


