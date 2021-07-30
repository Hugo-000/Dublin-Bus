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
    print('***** getPickleModel ****')
    print()
    print('path', path)
    
    pickleModel={}

    cwd = os.getcwd()
    print("CWD", cwd)

    if 'Error' in path:
        error = "Couldn't compute the prediction"
        pickleModel['Error'] = error
        return pickleModel

    # Load the Model back from file
    elif os.path.isfile(path):
        print("success")
        print()
        with open(path, 'rb') as file:  
            model = pickle.load(file)
            pickleModel['ok'] = model
            return pickleModel

    else:
        print("failed")
        print()
        error = "Couldn't compute the prediction"
        pickleModel['Error'] = error
        return pickleModel

