def calculating_subroutes(route, direction, df):
    ''' Takes in route, direction and a dataframe
    
    Returns a csv containing the sub routes data: rows, number of stops and mean journey time
    
    '''
    try:
    
        mean_route_time = df['JourneyTime'].mean()
        sub_routes = df['ROUTEID'].unique().tolist()
        amount_of_stops=[]
        amount_of_rows=[]
        avg_journey=[]      
        for subroute in sub_routes:
            t = df.loc[df['ROUTEID'] == subroute]
            df_Tt= df.loc[df['ROUTEID'] == subroute]
            num_stops= (t['STOPPOINTID'].unique().tolist())     
            amount_of_stops.append(len(num_stops))
            amount_of_rows.append(df_Tt.shape[0])
            avg_journey.append(df_Tt['JourneyTime'].mean())      
            


        zipped = zip(sub_routes,amount_of_stops,amount_of_rows,avg_journey)
    
        try:
            with open('./sub_routes/' + route +  '_subroute_variation.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(('Mean Time for All Trips', mean_route_time))
                writer.writerow(('SubRouteID', 'No. of Stops', 'No. of Rows', 'Mean Journey Time'))
                
                writer.writerows(zipped)

            print(route, "Done")       
        except:
            print("Error saving...",route)
            traceback.print_exc()
        
    except:
        print("Error with ", route + direction)
        traceback.print_exc()

                                
for route in glob.glob(os.path.join('./final_df/outbound', '*.csv')): 
  
    routes = (route[20:-13])
    with open(route, 'r') as t:            
        df = pd.read_csv(t)
        calculating_subroutes(routes, 'OB', df) 

        
for route in glob.glob(os.path.join('./final_df/inbound', '*.csv')):   
    routes = (route[20:-13])   
    with open(route, 'r') as t:            
        df = pd.read_csv(t)
        calculating_subroutes(routes, 'IB', df)
