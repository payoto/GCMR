print("Starting the program")
import pandas as pd
import urllib.request
import os
import sys
import numpy as np

filePath = "./Global_Mobility_Report.csv"
# Country we are looking for : Denmark, Italy, Germany, Spain, United_Kingdom, France, Norway, Belgium, Austria, Sweden, Switzerland, Greece, Portugal, Netherlands
# let's begin the mapping for the country : Create a dictionnary with the mapping that you wish between the google name and the name in your database
# Annexe 2 there are a useful tool to look for your country 
# For example in this example the only difference is for United Kingdom
countries_list =  ['Denmark', 'Italy', 'Germany', 'Spain', 'United Kingdom', 'France', 'Norway', 'Belgium', 'Austria', 'Sweden', 'Switzerland', 'Greece', 'Portugal', 'Netherlands']

countries = {
 'Denmark': 'Denmark',
 'Italy': 'Italy',
 'Germany': 'Germany',
 'Spain': 'Spain',
 'United Kingdom': 'United_Kingdom',
 'France': 'France',
 'Norway': 'Norway',
 'Belgium': 'Belgium',
 'Austria': 'Austria',
 'Sweden': 'Sweden',
 'Switzerland': 'Switzerland',
 'Greece': 'Greece',
 'Portugal': 'Portugal',
 'Netherlands': 'Netherlands',
  }

# Regions we are looking for :  Auvergne-Rhône-Alpes, Bourgogne-Franche-Comté, Bretagne, Centre-Val de Loire, Corse, Grand Est, Hauts-de-France, Normandie, Nouvelle-Aquitaine, Occitanie, Pays de la Loire,  Provence-Alpes-Côte d'Azur, Île-de-France, France-hopitaux, France-OC19, France-EHPAD    
# let's begin the mapping for the regions : Create a dictionnary with the mapping that you wish between the google name and the name in your database
# Annexe 2 there are a useful tool to look for your regions 
# difference : Brittany, normandy, Corsica

all_france = 'France-OC19'

regions = {
    
    'Auvergne-Rhône-Alpes' : 'Auvergne-Rhône-Alpes',
    'Bourgogne-Franche-Comté' : 'Bourgogne-Franche-Comté',
    'Brittany' : 'Bretagne',
    'Centre-Val de Loire' : 'Centre-Val de Loire',
    'Corsica' : 'Corse',
    'Grand Est' : 'Grand Est',
    'Hauts-de-France' : 'Hauts-de-France',
    'Normandy' : 'Normandie',
    'Nouvelle-Aquitaine' : 'Nouvelle-Aquitaine',
    'Occitanie' : 'Occitanie',
    'Pays de la Loire' : 'Pays de la Loire',
    "Provence-Alpes-Côte d'Azur" : "Provence-Alpes-Côte d'Azur",
    'Île-de-France' : 'Île-de-France'
    
}

regions_code = {
    
    'Auvergne-Rhône-Alpes' : 84,
    'Bourgogne-Franche-Comté' : 27,
    'Bretagne' : 53,
    'Centre-Val de Loire' : 24,
    'Corse' :94,
    'Grand Est' : 44,
    'Hauts-de-France' : 32,
    'Normandie' : 28,
    'Nouvelle-Aquitaine' : 75,
    'Occitanie' : 76,
    'Pays de la Loire' : 52,
    "Provence-Alpes-Côte d'Azur" : 93,
    'Île-de-France' : 11
    
}

if os.path.isfile(filePath):
    os.remove(filePath)
else:
    print ("File not exists")


print('Start the download')

try :
    url = 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=e0c5a582159f5662'
    urllib.request.urlretrieve(url, filePath)
    print('The file have been correctly downloaded')
except Exception as e:
    print("The file have NOT been correctly downloaded")
    print(e)
    
print("Start the processing")
csv_df = pd.read_csv("./Global_Mobility_Report.csv", low_memory=False)

if len(csv_df[csv_df['country_region'].isin(countries_list)]['country_region'].unique()) != len (countries_list):
    sys.exit("Error : You haven't put the countries that you want in the format of the google community report")
    
df_countries = csv_df[csv_df['country_region'].isin(countries_list)].copy()

df_countries['country_region'].replace(countries, inplace=True)

df_countries.loc[(df_countries['country_region']=='France') & (df_countries['sub_region_1'].isnull()), 'sub_region_1'] = all_france

df_countries['sub_region_1'].replace(regions, inplace=True)

df_countries['sub_region_1_code'] = df_countries['sub_region_1'].map(regions_code)

df_countries = df_countries[['country_region_code','country_region', 'sub_region_1_code', 'sub_region_1', 'sub_region_2','date', 'retail_and_recreation_percent_change_from_baseline',
       'grocery_and_pharmacy_percent_change_from_baseline',
       'parks_percent_change_from_baseline',
       'transit_stations_percent_change_from_baseline',
       'workplaces_percent_change_from_baseline',
       'residential_percent_change_from_baseline']]

print("End of the processing")

print("Save the result with the name : Global_Mobility_Report_prepared.csv")

try : 
    df_countries.to_csv('Global_Mobility_Report_prepared.csv')
except Exception as e : 
    print("We could not save the file")
    print(e)