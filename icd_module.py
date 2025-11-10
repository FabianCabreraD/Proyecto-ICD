import os
import json
import folium
import matplotlib.pyplot as plt

#Retorna el listado de archivos json de las mipymes
def mipymes_list():
    files = os.listdir("d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes")
    return files

#Devuelve el path del json dado su nombre
def return_path_mipymes(name):
    path = f"d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes\\{name}"
    return path

#Lee el archivo json
def read_json(path):
    with open(path,"r",encoding="utf-8") as f:
        file = json.load(f)
        return file

#Devuelve el promedio de los elementos de una lista    
def mean_list(list):
    return sum(list)/len(list)

#Muestra el mapa con las mipymes analizadas
def show_map_mipymes():    
    mapa = folium.Map(location=(23.0515757,-82.3304645),zoom_start=11)

    archivos = mipymes_list()
    for i in archivos:
        diccionario = read_json(f"d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes\\{i}")
        
        name = diccionario['name']
        lat = diccionario["location"]["lat"]
        long = diccionario["location"]["long"]            
        
        folium.Marker([lat,long],tooltip=name).add_to(mapa)
    
    return mapa