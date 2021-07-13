import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
%matplotlib inline
from patsy import dmatrices
import warnings
warnings.filterwarnings('ignore')
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import sklearn
from sklearn.model_selection import train_test_split
import pickle
import os
import csv
import glob
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

XBGMAE={}
RFMAE={}
XBGr2={}
RFr2={}

def open_csv_create_models(path):
    '''takes in a path, opens corresponding csv files
    
    prepares data and creates model for each bus line/csv, prints accuracy metrics to csv and saves model as pickle
    
    '''
    cols_to_delete = ['TRIPID','LINEID','ROUTEID', 'DIRECTION', 'PLANNEDTIME_ARR',
       'PLANNEDTIME_DEP', 'ACTUALTIME_ARR', 'ACTUALTIME_DEP', 
       'DelayedArr', 'DelayedDep',]
    #declare continous and cat cols
    cat_cols = ['weather_main']
    numeric = ['JourneyTime','temp','humidity','wind_speed','rain_1h','clouds_all']
   

    try:
        #open each file
        for filename in glob.glob(os.path.join(path, '*.csv')):

            with open(filename, 'r') as file: 
                bus_line=(filename[13:-4])
                print(bus_line, "Starting...")

                #read files in as dataframes
                df=pd.read_csv(file)
                #delete necessary cols and change to cat or cont
                for col in cols_to_delete:
                    del df[col]
                for column in numeric:
                    df[column]= df[column].astype('float32')

                for column in cat_cols:   
                     df[column]= df[column].astype('category')

                #create new cols for modelling
                df['Dates']=df['Dates'].apply(pd.to_datetime)
                df['Weekday']= df['Dates'].dt.day_name()
                df['Hour']= df['Dates'].dt.hour
                df['Month']= df['Dates'].dt.month



                df = df.drop(["Dates"], axis = 1)

                df=sklearn.utils.shuffle(df)

                df["Weekday"].replace(
                    {"Monday": 1, "Tuesday": 2,"Wednesday": 3,"Thursday": 4,"Friday": 5,"Saturday": 6,"Sunday": 7,}, inplace=True)

                df["weather_main"].replace(
                    {"Rain": 1, "Clouds": 2,"Drizzle": 3,"Clear": 4,"Fog": 5,"Mist": 6,"Snow": 7,"Smoke": 8}, inplace=True)



                df_modelling = df.drop(['Weekday','weather_main'],axis=1)

                cols=['Hour','Month']
                for column in cols:
                    df_modelling[column]= df_modelling[column].astype('int32')


                y = df_modelling["JourneyTime"]            
                X = df_modelling.drop(["JourneyTime"],1)

                #Split into test train 70/30

                X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1,  test_size=0.3)

                print("Data range is: ",df_modelling.shape[0])

                X_train.reset_index(drop=True, inplace=True)
                y_train.reset_index(drop=True, inplace=True)
                X_test.reset_index(drop=True, inplace=True)
                y_test.reset_index(drop=True, inplace=True)


                model = XGBRegressor().fit(X_train, y_train)

                xgb_train_predictions = model.predict(X_train)
                #get predictions on test set
                XGB_predictions_test = model.predict(X_test)

                #get accuracy results
                mae_train = metrics.mean_absolute_error(y_train, xgb_train_predictions)
                mae= metrics.mean_absolute_error(y_test, XGB_predictions_test)
                mse = metrics.mean_squared_error(y_test, XGB_predictions_test)
                rmse = np.sqrt(metrics.mean_squared_error(y_test, XGB_predictions_test))
                r2 = metrics.r2_score(y_test, XGB_predictions_test)
                mpe = np.mean((y_test - XGB_predictions_test)/y_test)
                XBGMAE[bus_line]=(mae)
                XBGr2[bus_line]=r2
                

                RFM = RandomForestRegressor(n_estimators=32).fit(X_train, y_train)
                train_predictions = RFM.predict(X_train)      
                rf_predictions_test = RFM.predict(X_test)

                    #get results
                MAE_TRAIN= metrics.mean_absolute_error(y_train, train_predictions)
                MAE = metrics.mean_absolute_error(y_test, rf_predictions_test)
                MSE=metrics.mean_squared_error(y_test, rf_predictions_test)
                RMSE = "RMSE",np.sqrt(metrics.mean_squared_error(y_test, rf_predictions_test))
                R2= metrics.r2_score(y_test, rf_predictions_test)
                MPE=np.mean((y_test - rf_predictions_test)/y_test)
                RFMAE[bus_line]=(MAE)
                RFr2[bus_line]=R2

                #write results to csv file for evaluation per route
                with open('XGB_ACC_models_new.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([bus_line, mae_train, mae, mse, rmse, r2, mpe])
                with open('rfc_ACC_models_new.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([bus_line, MAE_TRAIN, MAE, MSE, RMSE, R2, MPE])

                with open("./models/" +  bus_line, "wb") as f:
                    pickle.dump(model, f)
                print(bus_line, "Done.")
    except:
        print(bus_line, "Error")

