import os
import json
import folium
import matplotlib.pyplot as plt
import csv
import datetime

#CONSTANTS
MIPYMES_PATH = "d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes"
RICE_MEAN_PRICE_PATH = "d:\\uh\\icd\\Proyecto-ICD\\data\\rice_price.json" 
AVERAGE_SALARY = 6660.1
MINIMUM_PENSION = 3056

#Retorna el listado de archivos json de las mipymes
def mipymes_list():
    files = os.listdir(MIPYMES_PATH)
    return files

#Devuelve el path del json dado su nombre
def return_path_mipymes(name):
    path = f"{MIPYMES_PATH+"\\"+name}"
    return path

#Lee el archivo json
def read_json(path):
    with open(path,"r",encoding="utf-8") as f:
        file = json.load(f)
        return file

#Devuelve el promedio de los elementos de una lista    
def mean_list(list):
    return round(sum(list)/len(list),2)

def currency_data():
    with open("d:\\uh\\icd\\Proyecto-ICD\\data\\tasa copy.csv","r") as file:
        data = csv.reader(file)
        data_list = [i for i in data]
        
    data_list = data_list[1:]
    data_list_final = []
    for i in data_list:
        row = [i[0],float(i[1]),float(i[2])]
        data_list_final.append(row)
    
    dates = [i[0] for i in data_list_final]
    usd = [i[1] for i in data_list_final]
    euro = [i[2] for i in data_list_final]
    
    return dates, usd, euro

#Precio promedio de 1kg de arroz en las mipymes
def product_mean_price(product):
    files = mipymes_list()
    prices = []
    for i in files:
        path = return_path_mipymes(i)
        data = read_json(path)
        for j in data["product"]:
            if j["type"].lower() == product.lower():
                #Si la mipyme no vende un 1kg de arroz, se le aplica una proporción
                if j["unity"] == "1 kg":
                    prices.append(j["price"])
                else:
                    unity = j["unity"].replace(" kg", "")
                    proportion = j["price"]/float(unity)
                    prices.append(proportion)
                    
    mean = mean_list(prices)
    return mean
    
def currency_vs_data(data,data_currency):
    dt = AVERAGE_SALARY if data == "salary" else MINIMUM_PENSION
    values = [dt/i for i in data_currency]
    return values
    
#GRAPHS

#Mapa de las mipymes
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
    
#Tasa cambiaria    
def currency_graph():
    dates, usd, euro = currency_data()
    
    plt.figure()
    plt.plot(dates,usd,label="USD")
    plt.plot(dates,euro,label="EUR")
    plt.xticks(dates[::15],rotation=45)
    plt.title("Tasa cambiaria en los últimos 3 meses")
    plt.xlabel("fecha")
    plt.ylabel("cambio en CUP")
    plt.legend()
    plt.show()
        
#Salario medio y pensión mínima contra usd y euro
def salary_and_pension_graph():
    dates, usd, euro = currency_data()
    
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,6))

    usd_vs_salary = currency_vs_data("salary",usd)
    euro_vs_salary = currency_vs_data("salary",euro)

    ax1.plot(dates,usd_vs_salary,label="USD")
    ax1.plot(dates,euro_vs_salary,label="EUR")
    ax1.set_xticks(dates[::15])
    ax1.set_xlabel("fecha")
    ax1.tick_params(axis="x",rotation=45)
    ax1.legend()
    ax1.set_title("Salario Promedio en USD y EUR")
    
    usd_vs_pension = currency_vs_data("pension",usd)
    euro_vs_pension = currency_vs_data("pension",euro)


    ax2.plot(dates,usd_vs_pension, label="USD")
    ax2.plot(dates,euro_vs_pension, label="EUR")
    ax2.set_xticks(dates[::15])
    ax2.set_xlabel("fecha")
    ax2.tick_params(axis="x",rotation=45)
    ax2.legend()
    ax2.set_title("Pensión mínima en USD y EUR")

    plt.show()
    
#Precio promedio del arroz en países de América
def rice_mean_price_graph():
    data = read_json(RICE_MEAN_PRICE_PATH)
    cuba_price = product_mean_price("Arroz")
    data["Cuba"] = cuba_price/435
    
    tuples_sorted = sorted(data.items(),key=lambda x: x[1])
    countries = [i[0] for i in tuples_sorted]
    prices = [i[1] for i in tuples_sorted]
    
    bar_color = ["red" if country == "Cuba" else "#1f77b4" for country in countries]

    fig, ax = plt.subplots()
    
    ax.barh(countries,prices,color=bar_color)
    ax.set_title("Precio promedio de 1kg de arroz")
    plt.show()
