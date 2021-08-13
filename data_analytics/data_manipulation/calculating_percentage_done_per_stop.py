import pandas as pd
import os
import glob
import traceback
from collections import OrderedDict
import csv

def calculating_percent_done(route, direction, df):
    ''' Takes in route, direction and a dataframe
    
    Returns percentage of Journey completed per stop per route and saves to CSV
    
    '''
    try:
    

        print('Starting...', route )    
        
        #get the most commong sub route from dict
        key = route + '_' + direction
        sub = dict_for_subs.get(key)
        
        
        if sub is not None:
            print(sub)
            df = df.loc[df['ROUTEID']== sub]
            #get a percentage of the journey done     
            df['PERCENTAGE'] = ((df['TimeSinceBeginning']) / (df['FullJourney'])) * 100
            #sort by progrnumber so stops are in sequence
            df = df.sort_values('PROGRNUMBER')
            #store all the stops for the route
            stops=df['STOPPOINTID'].unique().tolist()
            #create a dictionary of progrnumbers and stops that are in order                                                                        
            #pairs the progrnumber and stopid into an ordered dictionary by progrnumber
            stops_dict={}
            PROGRNUMBERs= df['PROGRNUMBER'].unique().tolist()
            STOPPOINTID=  df['STOPPOINTID'].unique().tolist()
            for prog, stop in zip(PROGRNUMBERs,STOPPOINTID ):
                stops_dict[prog]=stop
            dict1 = OrderedDict(sorted(stops_dict.items()))
            stops_dict =dict(dict1)

            #create a dict of the stops and the corresponding percentage of journey done
            percent_dict={}
            for stop in stops:
                df_temp= df.loc[df['STOPPOINTID'] == stop]
                #calculate the mean percentage of the journey done per stop on a route
                mean_percent=df_temp["PERCENTAGE"].mean()

                
                if mean_percent <= 1:
                    percent_dict[stop]=0
                #round to the closes 2 decimel places
                percent_dict[stop]=round(mean_percent,2)
            #sort the dictionary by percentages 
            templist = sorted(percent_dict.items(), key=lambda x:x[1])
            sortdict = dict(templist)
            
            #store percentages, order of stops and stop id in csv for insertion into db
            percentss = sortdict.values()
            order_of_stops = stops_dict.keys()
            stopid =stops_dict.values()
            route_list=[route] * len(order_of_stops)
            direction_list = [direction] * len(order_of_stops)
            zipped = zip(route_list,direction_list,order_of_stops, stopid, percentss)
            print('done')
            #write data to csv
            try:
                with open('./accuracies/Journey_Percents_Correct_Sub_routes.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(zipped)

                print(route, "Done")       
            except:
                print("Error saving...",route)
                traceback.print_exc()
        
    except:
        print("Error with ", route + direction)
        traceback.print_exc()

                                
                        