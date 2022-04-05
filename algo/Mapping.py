# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:39:58 2022

@author: lilia
"""
import pandas as pd
import folium
import numpy as np


class mapping:
    
    def __init__(self, data_longitude, data_latitude):
                self.data_longitude = data_longitude
                self.data_latitude = data_latitude
                
    def create_map_total_prediction(self, train, test):
        
        y_pred_mlrlat=list(self.data_latitude)
        y_pred_mlrlong=list(self.data_longitude)
        
        prediction=pd.DataFrame()
        prediction["longitude"]=y_pred_mlrlong
        prediction["latitude"]=y_pred_mlrlat
                
        c = folium.Map(location=[ 44.833328, -0.56667])

        for i in range(0,len(prediction)):
           folium.Circle(
              location=[prediction.iloc[i]['latitude'], prediction.iloc[i]['longitude']],
              radius=550,
              color="red",
              weight=2,
              fill_color='orange',
              fill_opacity = 0.25,
           ).add_to(c)
        
        for i in range(0,len(train)):
           folium.Circle(
              location=[train.iloc[i]['latitude'], train.iloc[i]['longitude']],
              radius=10,
              color="#00BFFF",
              fill=False,
              
           ).add_to(c)
        
        for i in range(0,len(test)):
           folium.Circle(
              location=[test.iloc[i]['latitude'], test.iloc[i]['longitude']],
              radius=100,
              color="black",
              fill_color='black',
              fill_opacity = 1,
              fill=False,
              
           ).add_to(c)
        
        return c
    
    def create_map_prediction(self,weight):
        
        pred_lat=list(self.data_latitude)
        pred_long=list(self.data_longitude)
        
        prediction=pd.DataFrame()
        prediction["longitude"]=pred_long
        prediction["latitude"]=pred_lat
        
        c = folium.Map(location=[ 45.6500000, 0.1500000])
        
        for i in range(0,len(prediction)):
           folium.Circle(
              location=[prediction.iloc[i]['latitude'], prediction.iloc[i]['longitude']],
              radius=np.exp(float(weight.iloc[i]["weight"])*0.21429),
              color="red",
              weight=2,
              popup=folium.Popup("""<h3>This is the weight of the prediction</h3>
                                 """+str(weight.iloc[i]["weight"]), width=500),
              fill_color='orange',
              fill_opacity = 0.5,
           ).add_to(c)
        
        return c