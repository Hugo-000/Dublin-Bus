def combining_trips_and_leavetimes(route, direction, df_trips, df_leave):
    '''
    takes in a route, direction and two dataframes
    
    combines them on tripid and dates and returns the combined df
    
    '''
    try:
    
    

        print('Starting...', route )    
        #change to appropriate datatypes
        df_leave['DATEOFSERVICE'] = pd.to_datetime(df_leave['DAYOFSERVICE'], format='%d-%b-%y %H:%M:%S').dt.date
        df_trips['DATEOFSERVICE'] = pd.to_datetime(df_trips['Dates'], format='%Y-%m-%d %H:%M:%S').dt.date

        #merge the dataframes
        final_df = pd.merge( df_trips, df_leave,how='inner', on=['TRIPID','DATEOFSERVICE'])
        #create a full journey column 
        final_df['FullJourney'] = (final_df['ACTUALTIME_ARR'] - final_df['ACTUALTIME_DEP'])/60
        #calculate time of the journey completed per stop 
        final_df['TimeSinceBeginning'] = (final_df['ATA_STOPS'] - final_df['ACTUALTIME_DEP'])/60

        #delete unnecessary cols
        cols_to_delete = [ 'PLANNEDTIME_ARR',
           'PLANNEDTIME_DEP', 'ACTUALTIME_ARR', 'ACTUALTIME_DEP','DelayedArr', 'DelayedDep', 'Dates', 'temp', 'feels_like', 'humidity',
           'wind_speed', 'rain_1h', 'clouds_all', 'weather_main', 'DATEOFSERVICE',
            'DAYOFSERVICE','PTA_STOPS',
           'PTD_STOPS', 'ATA_STOPS', 'ATD_STOPS']

        for col in cols_to_delete:
            del final_df[col]
        final_df.to_csv('./final_dfs/' +route + '_' + direction + '_final_df.csv', index=False)
        
    except:
        print("Error with ", route + direction)
        traceback.print_exc()

    
