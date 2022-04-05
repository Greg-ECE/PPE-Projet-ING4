from Database import database
from Regression import regression
from Mapping import mapping
import pandas as pd


df=pd.read_csv('C:/Users/grego/OneDrive/Documents/ECE/Annee_2021-2022_-_ING4/S2/PPE-Projet-ING4/algo/regression.csv')
d=database('C:/Users/grego/OneDrive/Documents/ECE/Annee_2021-2022_-_ING4/S2/PPE-Projet-ING4/algo/Clean2gether.json')

epci_data=d.all_epci(df)
county_data=d.all_county(df)

r=regression(df)

mlrlat,mlrlong,rmselat,rmselong,y_trainlat,y_trainlong,y_pred_mlrlong,y_pred_mlrlat,y_testlat,y_testlong=r.opti_regression()
mlr_weight,r2,rmse=r.weight_regression()

print(rmselat)
print(rmselong)
print(r2)



"""
plot the total predictions thanks to the Clean2Gether dataset
"""

train=pd.DataFrame()
train["latitude"]=y_trainlat
train["longitude"]=y_trainlong
train=train.dropna()

test=pd.DataFrame()
test["latitude"]=y_testlat
test["longitude"]=y_testlong
test=test.dropna()

m=mapping(y_pred_mlrlong,y_pred_mlrlat)

c=m.create_map_total_prediction(train,test)

c.save("map_total_prediction.html")

"""
plot the predictions thanks to the epci
"""

finder=d.find_thx_epci("CC du Rouillacais", df)

pred_lat=mlrlat.predict(finder)
pred_long=mlrlong.predict(finder)

coord=pd.DataFrame(columns=["latitude","longitude"])
coord["latitude"]=pred_lat
coord["longitude"]=pred_long

weight=pd.DataFrame(mlr_weight.predict(coord),columns=["weight"])

m=mapping(pred_long,pred_lat)

c=m.create_map_prediction(weight)

c.save("map_prediction_finder_epci.html")


"""
plot the predictions thanks to the county
"""

finder=d.find_thx_county("Charente", df)

pred_lat=mlrlat.predict(finder)
pred_long=mlrlong.predict(finder)

coord=pd.DataFrame(columns=["latitude","longitude"])
coord["latitude"]=pred_lat
coord["longitude"]=pred_long

weight=pd.DataFrame(mlr_weight.predict(coord),columns=["weight"])

m=mapping(pred_long,pred_lat)

c=m.create_map_prediction(weight)
   
c.save("map_prediction_finder_county.html")
