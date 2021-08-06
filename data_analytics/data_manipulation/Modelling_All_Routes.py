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
import traceback
from sklearn.neural_network import MLPRegressor

dict_for_subs = {'102_IB': '102_9',
 '102_OB': '102_8',
 '104_IB': '104_16',
 '104_OB': '104_15',
 '111_IB': '111_8',
 '111_OB': '111_7',
 '114_IB': '114_6',
 '114_OB': '114_5',
 '116_IB': '116_3',
 '116_OB': '116_1',
 '118_IB': '118_4',
 '11_IB': '11_42',
 '11_OB': '11_40',
 '120_IB': '120_9',
 '120_OB': '120_7',
 '122_IB': '122_20',
 '122_OB': '122_18',
 '123_IB': '123_36',
 '123_OB': '123_34',
 '130_IB': '130_11',
 '130_OB': '130_10',
 '13_IB': '13_67',
 '13_OB': '13_60',
 '140_IB': '140_21',
 '140_OB': '140_19',
 '142_IB': '142_9',
 '142_OB': '142_8',
 '145_IB': '145_105',
 '145_OB': '145_102',
 '14C_IB': '14C_18',
 '14C_OB': '14C_17',
 '14_IB': '14_16',
 '14_OB': '14_15',
 '150_IB': '150_9',
 '150_OB': '150_8',
 '151_IB': '151_17',
 '151_OB': '151_15',
 '15A_IB': '15A_84',
 '15A_OB': '15A_83',
 '15B_IB': '15B_61',
 '15B_OB': '15B_60',
 '15D_IB': '15D_63',
 '15D_OB': '15D_62',
 '15_IB': '15_17',
 '15_OB': '15_16',
 '161_IB': '161_51',
 '161_OB': '161_50',
 '16C_IB': '16C_28',
 '16C_OB': '16C_29',
 '16D_OB': '16D_30',
 '16_IB': '16_24',
 '16_OB': '16_20',
 '17A_IB': '17A_17',
 '17A_OB': '17A_15',
 '17_IB': '17_15',
 '17_OB': '17_10',
 '184_IB': '184_28',
 '184_OB': '184_29',
 '185_IB': '185_56',
 '185_OB': '185_53',
 '18_IB': '18_4',
 '18_OB': '18_3',
 '1_IB': '1_40',
 '1_OB': '1_37',
 '220_IB': '220_12',
 '220_OB': '220_10',
 '236_IB': '236_10',
 '236_OB': '236_9',
 '238_IB': '238_15',
 '238_OB': '238_11',
 '239_IB': '239_28',
 '239_OB': '239_26',
 '25A_IB': '25A_270',
 '25A_OB': '25A_273',
 '25B_IB': '25B_271',
 '25B_OB': '25B_274',
 '25D_IB': '25D_275',
 '25D_OB': '25D_277',
 '25X_IB': '25X_11',
 '25X_OB': '25X_10',
 '25_IB': '25_269',
 '25_OB': '25_272',
 '26_IB': '26_29',
 '26_OB': '26_28',
 '270_IB': '270_44',
 '270_OB': '270_42',
 '27A_IB': '27A_5',
 '27A_OB': '27A_4',
 '27B_IB': '27B_34',
 '27B_OB': '27B_23',
 '27X_IB': '27X_42',
 '27X_OB': '27X_43',
 '27_IB': '27_17',
 '27_OB': '27_19',
 '29A_IB': '29A_15',
 '29A_OB': '29A_14',
 '31A_IB': '31A_26',
 '31A_OB': '31A_25',
 '31B_IB': '31B_46',
 '31B_OB': '31B_44',
 '31D_IB': '31D_51',
 '31D_OB': '31D_50',
 '31_IB': '31_18',
 '31_OB': '31_15',
 '32X_IB': '32X_76',
 '32X_OB': '32X_77',
 '32_IB': '32_58',
 '32_OB': '32_57',
 '33A_IB': '33A_25',
 '33A_OB': '33A_22',
 '33B_IB': '33B_58',
 '33B_OB': '33B_56',
 '33D_IB': '33D_62',
 '33D_OB': '33D_61',
 '33E_OB': '33E_74',
 '33X_IB': '33X_49',
 '33X_OB': '33X_46',
 '33_IB': '33_70',
 '33_OB': '33_44',
 '37_IB': '37_15',
 '37_OB': '37_14',
 '38A_IB': '38A_32',
 '38A_OB': '38A_20',
 '38B_IB': '38B_44',
 '38B_OB': '38B_40',
 '38D_IB': '38D_61',
 '38D_OB': '38D_68',
 '38_IB': '38_14',
 '38_OB': '38_9',
 '39A_IB': '39A_43',
 '39A_OB': '39A_40',
 '39X_IB': '39X_3',
 '39X_OB': '39X_1',
 '39_IB': '39_21',
 '39_OB': '39_20',
 '40B_IB': '40B_65',
 '40B_OB': '40B_63',
 '40D_IB': '40D_104',
 '40D_OB': '40D_102',
 '40E_IB': '40E_91',
 '40E_OB': '40E_90',
 '40_IB': '40_31',
 '40_OB': '40_27',
 '41A_IB': '41A_22',
 '41B_IB': '41B_53',
 '41B_OB': '41B_52',
 '41C_IB': '41C_79',
 '41C_OB': '41C_78',
 '41D_IB': '41D_27',
 '41D_OB': '41D_26',
 '41X_IB': '41X_125',
 '41X_OB': '41X_121',
 '41_IB': '41_7',
 '41_OB': '41_3',
 '42D_IB': '42D_51',
 '42D_OB': '42D_50',
 '42_IB': '42_44',
 '42_OB': '42_42',
 '43_IB': '43_88',
 '43_OB': '43_84',
 '44B_IB': '44B_61',
 '44B_OB': '44B_60',
 '44_IB': '44_36',
 '44_OB': '44_40',
 '45A_IB': '45A_64',
 '45A_OB': '45A_60',
 '46A_IB': '46A_67',
 '46A_OB': '46A_74',
 '46E_IB': '46E_94',
 '47_IB': '47_136',
 '47_OB': '47_139',
 '49_IB': '49_28',
 '49_OB': '49_27',
 '4_IB': '4_12',
 '4_OB': '4_10',
 '51D_IB': '51D_51',
 '51D_OB': '51D_50',
 '51X_IB': '51X_64',
 '53_IB': '53_21',
 '53_OB': '53_20',
 '54A_IB': '54A_12',
 '54A_OB': '54A_11',
 '56A_IB': '56A_30',
 '56A_OB': '56A_31',
 '59_IB': '59_11',
 '59_OB': '59_10',
 '61_IB': '61_108',
 '61_OB': '61_106',
 '63_IB': '63_30',
 '63_OB': '63_26',
 '65B_IB': '65B_66',
 '65B_OB': '65B_65',
 '65_IB': '65_77',
 '65_OB': '65_74',
 '66A_IB': '66A_38',
 '66A_OB': '66A_37',
 '66B_IB': '66B_59',
 '66B_OB': '66B_58',
 '66X_IB': '66X_102',
 '66X_OB': '66X_92',
 '66_IB': '66_18',
 '66_OB': '66_17',
 '67X_IB': '67X_46',
 '67X_OB': '67X_43',
 '67_IB': '67_6',
 '67_OB': '67_4',
 '68A_IB': '68A_87',
 '68A_OB': '68A_86',
 '68X_IB': '68X_88',
 '68_IB': '68_83',
 '68_OB': '68_81',
 '69X_IB': '69X_60',
 '69X_OB': '69X_59',
 '69_IB': '69_47',
 '69_OB': '69_45',
 '70D_IB': '70D_71',
 '70D_OB': '70D_70',
 '70_IB': '70_67',
 '70_OB': '70_60',
 '75_IB': '75_19',
 '75_OB': '75_17',
 '76A_IB': '76A_29',
 '76A_OB': '76A_28',
 '76_IB': '76_37',
 '76_OB': '76_36',
 '77A_IB': '77A_28',
 '77A_OB': '77A_29',
 '77X_IB': '77X_61',
 '79A_IB': '79A_28',
 '79A_OB': '79A_27',
 '79_IB': '79_11',
 '79_OB': '79_10',
 '7A_IB': '7A_87',
 '7A_OB': '7A_85',
 '7B_IB': '7B_93',
 '7B_OB': '7B_91',
 '7D_IB': '7D_121',
 '7D_OB': '7D_120',
 '7_IB': '7_70',
 '7_OB': '7_72',
 '83A_IB': '83A_23',
 '83A_OB': '83A_17',
 '83_IB': '83_22',
 '83_OB': '83_16',
 '84A_IB': '84A_3',
 '84A_OB': '84A_1',
 '84X_IB': '84X_62',
 '84X_OB': '84X_57',
 '84_IB': '84_30',
 '84_OB': '84_27',
 '9_IB': '9_7',
 '9_OB': '9_5'}


def create_models_common_subs(route, direction , df):
    '''takes in a route, direction and df
    
    prepares data and performs grid search to create model for each route and direction, prints accuracy metrics to csv and saves model as pickle for Random forest, XGBoost and Neural net
    
    '''
    cols_to_delete = ['TRIPID','LINEID','ROUTEID', 'DIRECTION', 'PlannedJourneyTime','PlanVSAct']
    #declare continous and cat cols
    cat_cols = ['weather_main']
    numeric = ['JourneyTime','temp','humidity','wind_speed','rain_1h','clouds_all']
   

    try:
            print("Starting",route)
            #get corresponding most common sub route for each route
            key = route + '_' + direction
            sub_to_segment = dict_for_subs.get(key)

            #segment df to only include longest sub route
            df = df.loc[df['ROUTEID'] ==sub_to_segment]



            #delete necessary cols and change to cat or cont
            for col in cols_to_delete:
                del df[col]
            for column in numeric:
                df[column]= df[column].astype('float32')

            for column in cat_cols:   
                 df[column]= df[column].astype('category')

            #create new cols for modelling - Weekday, hour, month, time of day, seasons, rush hour
            df['Dates']=df['Dates'].apply(pd.to_datetime)
            
            df['Weekday']= df['Dates'].dt.day_name()
            
            df['Hour']= df['Dates'].dt.hour
            
            df['Month']= df['Dates'].dt.month
            
            #set conditions for time of day
            choices=['Morning','Afternoon','Evening']
            conditions=[(df['Hour'] > 7) & (df['Hour'] < 11), (df['Hour'] >= 11) & (df['Hour'] < 15),(df['Hour'] >= 15) & (df['Hour'] < 23)]        
            df['TimeOfDay']= np.select(conditions, choices, default='Night')
            
            #set conditions for seasons 
            choices_more=['Summer','Winter','Spring']
            conditions_more=[(df['Month'] >= 6) & (df['Month'] < 9), (df['Month'] >= 11) & (df['Month'] <=1),(df['Month'] >= 2) & (df['Month'] <= 5)]
            
            df['Seasons']= np.select(conditions_more, choices_more, default='Autumn')
            
            df['RushHour']=np.where(((df['Hour'] >=7) &(df['Hour']<=9)| (df['Hour'] >=16) &(df['Hour']<=19)), 1,0)


            #drop dates
            df = df.drop(["Dates"], axis = 1)

            df=sklearn.utils.shuffle(df)
            
            #convert categorical data to numerical
            df["TimeOfDay"].replace(
                {"Morning": 1, "Afternoon": 2,"Evening": 3,"Night": 4}, inplace=True)                
            df["Seasons"].replace(
                {"Spring": 1, "Summer": 2,"Autumn": 3,"Winter": 4}, inplace=True)
            df["Weekday"].replace(
                {"Monday": 1, "Tuesday": 2,"Wednesday": 3,"Thursday": 4,"Friday": 5,"Saturday": 6,"Sunday": 7,}, inplace=True)
            df["weather_main"].replace(
                {"Rain": 1, "Clouds": 2,"Drizzle": 3,"Clear": 4,"Fog": 5,"Mist": 6,"Snow": 7,"Smoke": 8}, inplace=True)

            cols=['Hour','Month','TimeOfDay','Seasons','RushHour']
            for column in cols:
                df[column]= df[column].astype('int32')

            #set target value
            y = df["JourneyTime"]            
            X = df.drop(["JourneyTime"],1)

            #Split into test train 70/30
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1,  test_size=0.3)
            
            #display corresponding data range and sizes
            print("Data range is: ",df.shape[0])
            trainingsize= X_train.shape[0]
            testsize = X_test.shape[0]
            
            #display features being used
            features = X.columns
            print('Features' , features)

            X_train.reset_index(drop=True, inplace=True)
            y_train.reset_index(drop=True, inplace=True)
            X_test.reset_index(drop=True, inplace=True)
            y_test.reset_index(drop=True, inplace=True)
            
            #perform a grid search for XGboost models to find ideal parameters
            param_grid_ = {'learning_rate': [0.001, 0.01, 0.1, 1], 'max_depth' : [5, 10, 15], 'n_estimators' : [50, 100, 150, 200]}
            grid_search = Pipeline(steps=[
                                    ('grid_search', GridSearchCV(XGBRegressor(), param_grid_, cv = 5))])
            #fit a model on the results
            xg =grid_search.fit(X_train, y_train)
            #get predictions on training set
            xgb_train_predictions__ = xg.predict(X_train)
            #get predictions on test set
            XGB_predictions_test__ = xg.predict(X_test)
            #get accuracy
            mae_train = metrics.mean_absolute_error(y_train, xgb_train_predictions__)
            mae= metrics.mean_absolute_error(y_test, XGB_predictions_test__)
            mse = metrics.mean_squared_error(y_test, XGB_predictions_test__)
            rmse = np.sqrt(metrics.mean_squared_error(y_test, XGB_predictions_test__))
            r2 = metrics.r2_score(y_test, XGB_predictions_test__)
            mpe = np.mean((y_test - XGB_predictions_test__)/y_test)

            #perform a grid search for RF models to find ideal parameters
            param_grid = {
                'bootstrap': [True],
                'max_depth': [80, 90, 100, 110],
                'max_features': [2, 3],
                'min_samples_leaf': [3, 4, 5],
                'min_samples_split': [8, 10, 12],
                'n_estimators': [100, 200, 300, 1000]
            }
            # Create a based model
            rf = RandomForestRegressor()
            # Instantiate the grid search model
            grid_search_rf = GridSearchCV(estimator = rf, param_grid = param_grid, 
                                      cv = 3, n_jobs = -1, verbose = 2)
            model_testin_RF = grid_search_rf.fit(X_train, y_train)
            mm_rf = model_testin_RF.predict(X_train)
            mm___rf = model_testin_RF.predict(X_test)
      
            #get results
            MAE_TRAIN= metrics.mean_absolute_error(y_train, mm_rf)
            MAE = metrics.mean_absolute_error(y_test, mm___rf)
            MSE=metrics.mean_squared_error(y_test, mm___rf)
            RMSE = np.sqrt(metrics.mean_squared_error(y_test, mm___rf))
            R2= metrics.r2_score(y_test, mm___rf)
            MPE=np.mean((y_test - mm___rf)/y_test)

            #Train a neural net
            nn_model = MLPRegressor(random_state=1, max_iter=500).fit(X_train, y_train)
            #training set predictions
            nn_predictions_train = nn_model.predict(X_train)
            #get predictions on test set
            nn_predictions_test = nn_model.predict(X_test)

            #get results
            nn_MAE_train = metrics.mean_absolute_error(y_train, nn_predictions_train)
            nn_MAE_test =  metrics.mean_absolute_error(y_test, nn_predictions_test)
            nn_MSE_test =  metrics.mean_squared_error(y_test, nn_predictions_test)
            nn_RMSE_test = np.sqrt(metrics.mean_squared_error(y_test, nn_predictions_test))
            nn_R2_test = metrics.r2_score(y_test, nn_predictions_test)
            nn_MPE = np.mean((y_test - nn_predictions_test)/y_test)


            #write results to csv file for evaluation per route
            with open('./comparing/ComparingModels_CommonSubs__.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['XGBoost',trainingsize,testsize, sub_to_segment,bus_line, direction, mae_train, mae, mse, rmse, r2, mpe,[features]])
                writer.writerow(['RandomForest',trainingsize,testsize,sub_to_segment,bus_line,direction, MAE_TRAIN, MAE, MSE, RMSE, R2, MPE,[features]])
                writer.writerow(['NeuralNet',trainingsize,testsize, sub_to_segment,bus_line, direction,nn_MAE_train,nn_MAE_test,nn_MSE_test,nn_RMSE_test,nn_R2_test,nn_MPE,[features]])


            with open("./comparing/" +  bus_line + 'RF', "wb") as f:
                pickle.dump(grid_search_rf, f)

            with open("./comparing/" +  bus_line + 'XG', "wb") as f:
                pickle.dump(xg, f)
            print(route,'_',direction ,"Done.")

    except:
         traceback.print_exc()





with open('./comparing/ComparingModels_CommonSubs__.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Model','TrainingSize','TestSize','SubUsed','Route','Direction','MAE TRAIN','MAE','MSE','RMSE','R2','MPE','Features'])
            



path = './Directions'
try:
    for filename in glob.glob(os.path.join(path, '*.csv')):
            with open(filename, 'r') as file: 
                
                bus_line=(filename[13:-4])
                print(bus_line)
                route = bus_line[0:-3]

                df=pd.read_csv(file)
                if 'IB' in bus_line:
                    create_models_with_outliers(route, 'IB', df)
                elif 'OB' in bus_line:
                    create_models_with_outliers(route, 'OB', df)
except:
    traceback.print_exc()
                
                

            