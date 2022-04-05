from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import time

class regression:

        def __init__(self, data_base):
                self.data_base = data_base
                
        def long_reg(self):
            data_base=self.data_base.dropna()
            x = data_base[["postcode","total_weight","epci_weight","postcode_weight","town_weight","county_weight","num_county","num_epci","num_town"]]
            y = data_base["longitude"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

            mlr =HistGradientBoostingRegressor()
            mlr.fit(x_train, y_train)

            y_pred_mlr=mlr.predict(x_test)

            r2 = r2_score(y_test, y_pred_mlr)
            rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)
            
            return mlr,r2,rmse,y_pred_mlr,y_train,y_test

        def lat_reg(self):
            data_base=self.data_base.dropna()
            x = data_base[["postcode","total_weight","epci_weight","postcode_weight","town_weight","county_weight","num_county","num_epci","num_town"]]
            y = data_base["latitude"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

            mlr = HistGradientBoostingRegressor()
            mlr.fit(x_train, y_train)

            y_pred_mlr=mlr.predict(x_test)

            r2 = r2_score(y_test, y_pred_mlr)
            rmse = mean_squared_error(y_test, y_pred_mlr, squared=False)

            return mlr,r2,rmse,y_pred_mlr,y_train,y_test
        
        def weight_regression(self):
            data_base=self.data_base.dropna()
            x = data_base[["latitude","longitude"]]
            y = data_base["total_weight"]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.15, random_state = 42, shuffle=True)

            mlr = HistGradientBoostingRegressor()
            mlr.fit(x_train, y_train)

            weight=mlr.predict(x_test)

            r2 = r2_score(y_test, weight)
            rmse = mean_squared_error(y_test, weight, squared=False)
            
            return mlr,r2,rmse

        def opti_regression(self):

            start_time = time.time()
            
            mlr=pd.DataFrame(columns=["mlr_lat","mlr_long",'r2_lat','r2_long'])
            
            for i in range(5):
                mlrlat,r2lat,rmselat,y_pred_mlrlat,y_trainlat,y_testlat=self.lat_reg()
                mlrlong,r2long,rmselong,y_pred_mlrlong,y_trainlong,y_testlong=self.long_reg()
                mlr=mlr.append({"mlr_lat" :mlrlat ,"mlr_long" : mlrlong, 'r2_lat' :float(r2lat), 'r2_long' :float(r2long), 'rmselat' :float(rmselat), 'rmselong' :float(rmselong) } , ignore_index=True)
            
            best_mlr_lat = mlr['mlr_lat'][mlr["r2_lat"].idxmax()]
            best_mlr_long = mlr['mlr_long'][mlr["r2_long"].idxmax()]
            rmselat = mlr['rmselat'][mlr["r2_lat"].idxmax()]
            rmselong = mlr['rmselong'][mlr["r2_long"].idxmax()]
        
            interval = time.time() - start_time
            
            print("loading time : "+str(interval)+" sec !" )
            
            return best_mlr_lat,best_mlr_long,rmselat,rmselong,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat,y_testlat,y_testlong

