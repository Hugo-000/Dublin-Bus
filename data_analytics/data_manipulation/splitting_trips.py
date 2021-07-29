def splitting_trips_to_routes_per_direction(df):
    '''We will split the dataframe into each route and direction 
    
    IB(NORTH/EAST) is 2, OB(SOUTH/WEST) is 1 
    
    '''

    List_Routes = list(df['LINEID'].unique())
 

    for route in List_Routes:
       
        df_route = df.loc[df['LINEID'] == route]
        df_IB =df_route.loc[df_route['DIRECTION'] == 2]
        df_OB = df_route.loc[df_route['DIRECTION'] == 1]
        
        if df_IB.shape[0] != 0 :
            name_IB=route+ '_IB' +'.csv'
            size_IB = df_IB.shape[0]
            dfs[route + '_IB_' + str(size_IB)]= df_IB
            df_IB.to_csv('~/Model_Testing/Directions/' + name_IB,  index=False)
        else:
            name_IB=route+ '_IB' +'.csv'
            empty_dfs.append(name_IB)
            
        if df_OB.shape[0] != 0:
            name_OB=route+ '_OB' +'.csv'
            size_OB = df_OB.shape[0]
            dfs[route + '_OB_' + str(size_OB)]= df_OB
            df_OB.to_csv('~/Model_Testing/Directions/' + name_OB,  index=False)
            
        else:
            name_OB=route+ '_IB' +'.csv'
            empty_dfs.append(name_OB)
   
splitting_trips_to_routes_per_direction(df)