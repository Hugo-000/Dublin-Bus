import datetime
import os.path
import pickle
import numpy as np

def getPickleModel(path):
    """
        Function to retreive a pickle file from modelsNew based on a 
        user provided path. 

        Requires a relative path pointing to the pickle file to work.

        If the file does not exist it will return an error.
    """
    print('*************************')
    print()
    print('getPickleModel')
    print()
    print('*************************')
    print()
    print('path', path)
    print()
    print('*************************')
    
    # filename = str(route) + "_" + str(direction) + "B"
    # filename = str(route) + str(direction)
    # path = "../modelsNew/"+filename

    cwd = os.getcwd()
    print("CWD", cwd)
    # Load the Model back from file
    if os.path.isfile(path):
        print("success")
        with open(path, 'rb') as file:  
            model = pickle.load(file)
            return model

    else:
        print("failed")
        return "Error: Couldn't compute the prediction"

