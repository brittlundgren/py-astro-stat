def calcdev(input_matrix):
    ### function to calculate the matrix of deviations from the mean ###
    
    ncols = np.shape(input_matrix)[1]

    for col in range(ncols):
        mean = np.mean(input_matrix[:,col])
        input_matrix[:,col] -= mean

    a = input_matrix

    return a
    
    
def calc_cov(input_matrix):
    # Function to compute a'a * (1/n), the covariance matrix for A ###
    N = np.shape(input_matrix)[0]
    
    # First transform the raw grade matrix into a matrix of deviation scores ##
    a = calcdev(input_matrix)

    # Compute a'a, the n x n deviation sums of squares and x-product matrix for A ##    
    aprimea = np.dot(a.T,a)

    # Calculate the covariance matrix ##
    covA = aprimea / N
    
    return covA


    
    
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

if __name__ == "__main__":

    
    student1 = np.array([90.,60.,90.])
    student2 = np.array([90.,90.,30.])
    student3 = np.array([60.,60.,60.])
    student4 = np.array([60.,60.,90.])
    student5 = np.array([30.,30.,30.])

    # create a matrix A containing all of the grades ##
    A = np.array([student1, student2, student3, student4, student5])
    print "Entered grades (Math, English, Art):"
    print A
    print " "

    # Compute the covariance matrix of A ##
    covA = calc_cov(A)
    print "Covariance Matrix:"
    print covA

    # Generate a color-coded plot of the normalized covariance matrix ##
    diags = covA.flat[::len(covA)+1]
    covA_norm = covA/diags
    print "Normalized Covariance Matrix:"
    print covA

    fig, ax = plt.subplots()
    im = ax.imshow(covA, cmap=cm.jet, interpolation='nearest')

    numrows, numcols = covA.shape
    def format_coord(x, y):
        col = int(x+0.5)
        row = int(y+0.5)
        if col>=0 and col<numcols and row>=0 and row<numrows:
            z = covA[row,col]
            return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
        else:
            return 'x=%1.4f, y=%1.4f'%(x, y)
    ax.format_coord = format_coord

    fig.colorbar(im)
    plt.show()
