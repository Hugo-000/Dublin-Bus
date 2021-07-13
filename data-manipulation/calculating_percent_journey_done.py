def calculating_percent_done(route, direction, df):
    ''' Takes in route, direction and a dataframe
    
    Returns percentage of Journey completed per stop per route and saves to CSV
    
    '''
    try:
    

        print('Starting...', route )    
        
        
        dict_for_max={}
        num_sub_routes = df['ROUTEID'].unique().tolist()
        
        if len(num_sub_routes) >1:
            for sub in num_sub_routes:
                temp = df.loc[df['ROUTEID'] == sub]
                progrs = temp['PROGRNUMBER'].unique().tolist()
                dict_for_max[sub] = len(progrs)
                max_key = max(dict_for_max, key=dict_for_max.get)
                df = df.loc[df['ROUTEID']== max_key]
                
        #get a percentage of the journey done     
        df['PERCENTAGE'] = ((df['TimeSinceBeginning']) / (df['FullJourney'])) * 100
        #sort by progrnumber so stops are in sequence
        final_df.sort_values('PROGRNUMBER')

        stops=df['STOPPOINTID'].unique().tolist()
        #create a dictionary of progrnumbers and stops that are in order                                                                        
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
            mean_percent=df_temp["PERCENTAGE"].mean()


            if mean_percent <= 1:
                percent_dict[stop]=0

            percent_dict[stop]=round(mean_percent,2)

        templist = sorted(percent_dict.items(), key=lambda x:x[1])
        sortdict = dict(templist)

        percentss = sortdict.values()
        order_of_stops = stops_dict.keys()
        stopid =stops_dict.values()

        zipped = zip(order_of_stops, stopid, percentss)

        try:
            with open('./accuracies/' + route + '_' + direction + '_Percents.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(('StopOrder', 'StopID', 'PercentDone'))
                writer.writerows(zipped)

            print(route, "Done")       
        except:
            print("Error saving...",route)
            traceback.print_exc()
        
    except:
        print("Error with ", route + direction)
        traceback.print_exc()

                                
                        
