import pandas as pd
import numpy as np

class database:

        def __init__(self, url):
                self.url = url

        def create_data(self):
            data_fichier=pd.read_json(self.url)
            df=data_fichier[:]

            county = pd.DataFrame(df.pivot_table(index = ['county'], aggfunc ='size') , columns=["nb"])
            town = pd.DataFrame(df.pivot_table(index = ['town'], aggfunc ='size') , columns=["nb"])
            epci = pd.DataFrame(df.pivot_table(index = ['epci'], aggfunc ='size'), columns=["nb"])  
            postcode=pd.DataFrame(df.pivot_table(index = ['postcode'], aggfunc ='size'), columns=["nb"])

            county["num_county"]=np.arange(1,len(county)+1)
            epci["num_epci"]=np.arange(1,len(epci)+1)
            town["num_town"]=np.arange(1,len(town)+1)

            county["weight"]=county["nb"]/len(county)
            town["weight"]=town["nb"]/len(town)
            epci["weight"]=epci["nb"]/len(epci)
            postcode["weight"]=postcode["nb"]/len(postcode)

            county["county"]=county.index
            town["town"]=town.index
            epci["epci"]=epci.index
            postcode["postcode"]=postcode.index

            df["total_weight"]=np.zeros(len(df))
            df["epci_weight"]=np.zeros(len(df))
            df["postcode_weight"]=np.zeros(len(df))
            df["town_weight"]=np.zeros(len(df))
            df["county_weight"]=np.zeros(len(df))
            
            df["num_county"]=np.zeros(len(df))
            df["num_epci"]=np.zeros(len(df))
            df["num_town"]=np.zeros(len(df))

            for index, row in df.iterrows():
                for index2, row2 in county.iterrows():
                    if row["county"]==row2["county"]:
                        df["total_weight"][index]=row["total_weight"]+row2["weight"]
                        df["county_weight"][index]=row2["weight"]
                        df["num_county"][index]=row2["num_county"]
            
            for index, row in df.iterrows():
                for index2, row2 in postcode.iterrows():
                    if row["postcode"]==row2["postcode"]:
                        df["total_weight"][index]=row["total_weight"]+row2["weight"]
                        df["postcode_weight"][index]=row2["weight"]

            for index, row in df.iterrows():
                for index2, row2 in town.iterrows():
                    if row["town"]==row2["town"]:
                        df["total_weight"][index]=row["total_weight"]+row2["weight"]
                        df["town_weight"][index]=row2["weight"]
                        df["num_town"][index]=row2["num_town"]

            for index, row in df.iterrows():
                for index2, row2 in epci.iterrows():
                    if row["epci"]==row2["epci"]:
                        df["total_weight"][index]=row["total_weight"]+row2["weight"]
                        df["epci_weight"][index]=row2["weight"]
                        df["num_epci"][index]=row2["num_epci"]

            del df['images']

            df.to_csv ('D:/Shit/PPE Project ING4/algo/regression.csv', index = False, header=True)
        

            return df
        
        def find_thx_county(self,county,data):
            finder=pd.DataFrame(columns=data.columns)
            for index, row in data.iterrows():
                if row["county"]==county:
                    arr=row.values
                    arr=arr.reshape((1, 14))
                    arr=pd.DataFrame(arr,columns=data.columns)
                    finder=finder.append(arr, ignore_index=True)
            del finder["county"]
            del finder["town"]
            del finder["epci"]
            del finder["latitude"]
            del finder["longitude"]
            
            return finder
        
        def find_thx_epci(self,epci,data):
            finder=pd.DataFrame(columns=data.columns)
            for index, row in data.iterrows():
                if row["epci"]==epci:
                    arr=row.values
                    arr=arr.reshape((1, 14))
                    arr=pd.DataFrame(arr,columns=data.columns)
                    finder=finder.append(arr, ignore_index=True)
            del finder["county"]
            del finder["town"]
            del finder["epci"]
            del finder["latitude"]
            del finder["longitude"]
            return finder
        
        def all_epci(self, df):
            epci = pd.DataFrame(df.pivot_table(index = ['epci'], aggfunc ='size'))
            epci_data=pd.DataFrame(columns=["epci"])
            epci_data["epci"]=epci.index
            #epci_data.to_csv(r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\PPE\PPE\all_epci.csv', index = False, header=True)
            return epci_data
        
        def all_county(self, df):
            county = pd.DataFrame(df.pivot_table(index = ['county'], aggfunc ='size'))
            county_data=pd.DataFrame(columns=["county"])
            county_data["county"]=county.index
            #county_data.to_csv(r'C:\Users\lilia\OneDrive\Documents\Lilian\ING4_S2\PPE\PPE\all_county.csv', index = False, header=True)
            return county_data
        
        



