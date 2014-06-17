# cheapEM
#
# This is a very quick and dirty (and ugly!) implementation of
# Expectation-Maximization algorithm. Hopefully it is a fairly
# transparent implementation of the book's algorithm.  Ideally, the
# model parameters should converge upon the correct values regarless
# of the initialization values.
#
# Karen Lewis (June 10, 2014)

from matplotlib import pyplot as plt
import numpy as np
from sklearn.mixture import GMM

#------------------------------------------------------------
#  Set up the dataset.  We'll use scikit-learn's Gaussian Mixture
#  Model to sample data from a mixture of Gaussians.  The usual way of
#  using this involves fitting the mixture to data: we'll see that
#  below.  Here we'll set the internal means, covariances, and weights
#  by-hand.

np.random.seed(1)
Ndata=10000
gmm = GMM(3, n_iter=1)
gmm.means_ = np.array([[-1], [0], [3]])
gmm.covars_ = np.array([[1.5], [0.3], [0.5]]) ** 2
gmm.weights_ = np.array([0.3, 0.5, 0.2])

X = gmm.sample(Ndata)

#Plot histogram of data so we know what we're dealing with
plt.hist(X, 50, normed=True, histtype='stepfilled', alpha=0.4)
plt.show()

#Initialize the variables. 

# Note on weights: The w's are the so-called responsibilities. 
# Each is an array with Ndata elements that effectively states
# what fraction of that data point can be contributed to each
# of the components in the model. The responsibility for a
# particular component should be quite large for data points close to
# its mean and progressively smaller farther away from the mean.

# There are really two alternatives for initilizing. 
# 1) Select an initial guess for
# the mu's, variances, and alphas and then calculate an initial 
# set of w's.

# 2) Or, if you wanted to run this more "hands-off" on data, you might
# not want to specify initial values and simply set every w_i equal
# to 1/M where M is the number of model components.

# Right now this is set to option 1 and I encourage you to try both
# ways and see if it makes any practical difference.

# Choose sensible mu
mu1=-0.9
mu2=0.1
mu3=2.9

# Choose sensible variance
var1=1.3**2
var2=0.25**2
var3=0.55**2

# Choose sensible coefficients
a1=0.25
a2=0.55
a3=0.25

# Use these values to calculate weights following 4.21. 
# The following are the numerators in 4.21. 

tmp1=(a1/np.sqrt(2*np.pi*var1))*np.exp(-(X-mu1)**2/(2*var1))
tmp2=(a2/np.sqrt(2*np.pi*var2))*np.exp(-(X-mu2)**2/(2*var2))
tmp3=(a3/np.sqrt(2*np.pi*var3))*np.exp(-(X-mu3)**2/(2*var3))

# The following is essentially the current model prediction for 
# each data point. It is also the deonomicator in 4.21             
tmp=tmp1+tmp2+tmp3
              
# Now we have everything to calculate the weights.                   
w1=tmp1/tmp
w2=tmp2/tmp
w3=tmp3/tmp

# Print a sample of the the weights
print "End of 1st iteration sample w's"
for i in range(0,10,1):
    print X[i],w1[i],w2[i],w3[i]

# Now that we've gotten everything initialized, enter a loop
# to iterate on the maximization and estimation steps

Niteration=21    

for k in range(0,Niteration,1):
    
# Update mus according to 4.26

    mu1=np.sum(w1*X)/np.sum(w1)
    mu2=np.sum(w2*X)/np.sum(w2)
    mu3=np.sum(w3*X)/np.sum(w3)

# Update variances according to 4.27

    var1=np.sum(w1*(X-mu1)**2)/np.sum(w1)
    var2=np.sum(w2*(X-mu2)**2)/np.sum(w2)
    var3=np.sum(w3*(X-mu3)**2)/np.sum(w3)

# Calculate new scale factors, following 4.28

    a1=np.sum(w1)/Ndata
    a2=np.sum(w2)/Ndata
    a3=np.sum(w3)/Ndata

# Use these values to calculate new weights following 4.21, as above

    tmp1=(a1/np.sqrt(2*np.pi*var1))*np.exp(-(X-mu1)**2/(2*var1))
    tmp2=(a2/np.sqrt(2*np.pi*var2))*np.exp(-(X-mu2)**2/(2*var2))
    tmp3=(a3/np.sqrt(2*np.pi*var3))*np.exp(-(X-mu3)**2/(2*var3))

    tmp=tmp1+tmp2+tmp3
                                 
    w1=tmp1/tmp
    w2=tmp2/tmp
    w3=tmp3/tmp

# Output results of every 5th iteration. The % action is the modulo
# operator.

    if (k%5 == 0):
    # the %i means insert a variable that is an integer    
        print "Iteration %i done" % (k)
#        print ""
#        for i in range(0,5,1):
#            print w1[i],w2[i],w3[i]
    
        print "mu:", mu1,mu2,mu3
        print "variance:", var1, var2, var3
        print "scale:",a1, a2, a3 
        print ""

# Show progress on responsibilities
        plt.scatter(X,w1,color='red')
        plt.scatter(X,w2,color='blue')
        plt.scatter(X,w3,color='green')
        plt.show()
    
                                 
