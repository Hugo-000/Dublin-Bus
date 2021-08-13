
from pandas import DataFrame
import sqlite3
import pandas as pd


conn = sqlite3.connect("/home/groupone/data/CSV_Sqlite/leave_times_2018.sqlite")
cur=conn.cursor()

routes: ['68', '65', '77A', '130', '66', '41', '83', '13', '27', '40', '151', '16', '75', '41C', '122', '39', '33', '46A', '67', '123', '38', '7A', '4', '150', '29A', '15', '7', '39A', '14', '27A', '145', '9', '17A', '25B', '49', '38A', '31', '54A', '15A', '63', '40D', '37', '15B', '25A', '65B', '66A', '104', '76', '27B', '31A', '18', '42', '33B', '140', '120', '44', '83A', '1', '185', '79', '47', '61', '184', '17', '32', '43', '84', '102', '11', '56A', '59', '45A', '53', '70', '69', '238', '79A', '220', '25', '270', '33A', '40B', '26', '41B', '16C', '7D', '38B', '66B', '239', '84X', '84A', '76A', '66X', '41A', '77X', '67X', '111', '39X', '33X', '7B', '236', '142', '70D', '32X', '114', '51X', '41X', '38D', '27X', '69X', '46E', '51D', '15D', '44B', '68A', '31B', '25D', '42D', '25X', '31D', '14C', '116', '118', '161', '68X', '33D', '40E', '33E', '16D', '41D']
    
    
def saving_outbound_leavetimes()
    '''Function to seperate leavetimes file by finding trips associated with route and direction
    
    Saves seperated route to csv.
    '''
    for route in routes:
        try:
            name = route + '_OB'
            df_name =DF_TRIPS.loc[(DF_TRIPS['LINEID']==route)& (DF_TRIPS['DIRECTION'] == 1) ]
            trips_list = df_name['TRIPID'].unique().tolist()
            keys = ['DAYOFSERVICE','TRIPID','PROGRNUMBER', 'STOPPOINTID', 'PTA_STOPS', 'PTD_STOPS', 'ATA_STOPS', 'ATD_STOPS']

            sql="select DAYOFSERVICE,TRIPID,PROGRNUMBER, STOPPOINTID, PLANNEDTIME_ARR AS PTA_STOPS, PLANNEDTIME_DEP AS PTD_STOPS, ACTUALTIME_ARR AS ATA_STOPS, ACTUALTIME_DEP AS ATD_STOPS from leave_times where TRIPID in ({seq})".format(
            seq=','.join(['?']*len(trips_list)))

            result = cur.execute(sql, trips_list)
            df_to_save = DataFrame(result.fetchall())
            df_to_save.columns = keys
            df_to_save.to_csv('~/data/trips/outbound/' + str(name) +'.csv', index=False)
            print(name, 'done')

        except: 
            print(name, 'error')
            

def saving_inbound_leavetimes():
       '''Function to seperate leavetimes file by finding trips associated with route and direction
    
    Saves seperated route to csv.
    '''
    for route in routes:
        try:
            name = route + '_IB'
            df_name =DF_TRIPS.loc[(DF_TRIPS['LINEID']==route)& (DF_TRIPS['DIRECTION'] == 2) ]
            trips_list = df_name['TRIPID'].unique().tolist()
            keys = ['DAYOFSERVICE','TRIPID', 'PROGRNUMER','STOPPOINTID', 'PTA_STOPS', 'PTD_STOPS', 'ATA_STOPS', 'ATD_STOPS']

            sql="select DAYOFSERVICE,TRIPID, PROGRNUMBER, STOPPOINTID, PLANNEDTIME_ARR AS PTA_STOPS, PLANNEDTIME_DEP AS PTD_STOPS,   ACTUALTIME_ARR AS ATA_STOPS, ACTUALTIME_DEP AS ATD_STOPS from leave_times where TRIPID in ({seq})".format(
            seq=','.join(['?']*len(trips_list)))

            result = cur.execute(sql, trips_list)
            df_to_save = DataFrame(result.fetchall())
            df_to_save.columns = keys
            df_to_save.to_csv('~/data/trips/' + str(name) +'.csv', index=False)
            print(name, "done")
        except:
            print(name, "error")
            
            
saving_inbound_leavetimes()           
saving_outbound_leavetimes()