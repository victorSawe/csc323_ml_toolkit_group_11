import numpy as np
import random
import math

""" 
    utility functions 
"""
# 2D array normalization, between 0 - 1
def normalize(arr):
    i = 0
    while i < np.size(arr,1): # while i < cols
        j = 0
        temp_lst = list() # temp array to hold column values
        while j < np.size(arr,0): # while j < rows
            temp_lst.append(arr[j][i]) # copy column values per row to list
            j += 1

        temp_max = max(temp_lst) # find maximum value in column data
        temp_min = min(temp_lst) # find minimum value in column data

        k = 0
        while k < np.size(arr,0): # while k < rows
            arr[k][i] = (arr[k][i]-temp_min)/(temp_max-temp_min) # normalize function
            k += 1

        i += 1
    return arr

# sigmoid function
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# neuron function
def neuron(arr, w):
    
    # summation function
    summation = np.matmul(arr, w) # add all the (input * weights)

    # activation function
    output = np.full_like(summation, 0)
    l = 0
    while l < np.size(summation,0) :
        output[l] = sigmoid(summation[l]) # pass all values through the sigmoid function
        l += 1

    return output

""" 
    main function 
"""
def main():
    # read data from .txt file into 2D array
    diabetes = np.loadtxt('diabetes.data.txt') 

    # normalize 2D array
    diabetes = normalize(diabetes) 

    # split data into train[], test[] sets
    # train set = total_sizhl_Eof_dataset - 200
    # test set = 200
    train,test = diabetes[:(np.size(diabetes,0)-200),:], diabetes[(np.size(diabetes,0)-200):,:]

    # for each row of train[]
    k = 0
    while k < np.size(train,0): # while k < row
        """
            propagation utilities
        """
        row = train[k] # save all data to new array (row)
        # data classes (expected output)
        expected = row[np.size(row)-1]
        
        # data attributes (inputs)
        attributes = row[1:9:1]

        # hidden layer randomized weights
        hl_weights = np.random.rand(np.size(attributes),2)

        # output layer randomized weights
        ol_weights = np.random.rand(2,1)

        # back propagation attributes
        lr = 0.6 # learning rate

        epoch = 0
        while epoch < 1000:
            """ 
                forward propagation
            """
            # input layer
            il_output = attributes
            
            # hidden layer
            hl_output = neuron(il_output, hl_weights) # pass through neuron function
            
            # output layer
            system = np.asscalar(neuron(hl_output, ol_weights)) # pass through neuron function

            # loss fuction
            error = 0.5 * pow(expected-system,2) # calculate error

            """ 
                backpropagation
            """
            """ output layer weights adjustment """
            # calculate change in weight for output layer weights - nEX
            ol_E = system * (1 - system) * (expected - system)
            nEX = np.reshape(lr * ol_E * hl_output, (2, 1))

            # update the output layer weights
            ol_weights = ol_weights + nEX

            """ hidden layer weights adjustment """
            # calculate change in weight for hidden layer weights - nEX
            hl_E = np.full_like(ol_weights, 0)
            
            hl_E[0][0] = (ol_weights[0][0] * ol_E) * (hl_output[0]) * (1 - hl_output[0]) # a x g x (1-g)
            hl_E[1][0] = (ol_weights[1][0] * ol_E) * (hl_output[1]) * (1 - hl_output[1]) # b x h x (1-h)
            
            n = 0
            while n < np.size(ol_weights[0]): # while n < row
                hl_weights[n][0] = hl_weights[n][0] + (lr * hl_E[0][0] * il_output[n]) # w + nEX
                hl_weights[n][1] = hl_weights[n][1] + (lr * hl_E[1][0] * il_output[n]) # w + nEX
                n += 1

            epoch += 1
        print("The error of dataset {0} is {1}.".format(k+1, error))

        k += 1

if __name__ == "__main__":
    main()
