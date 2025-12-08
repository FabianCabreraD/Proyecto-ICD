import os
import json
import folium
import matplotlib.pyplot as plt
import csv
import datetime
import numpy as np
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#CONSTANTES
MIPYMES_PATH = "d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes"
RICE_MEAN_PRICE_PATH = "d:\\uh\\icd\\Proyecto-ICD\\data\\rice_price.json"
SALARIES_PATH = "d:\\uh\\icd\\Proyecto-ICD\\data\\salary.json" 
AVERAGE_SALARY = 6660.1
MINIMUM_PENSION = 3056
REGULATED_RICE_PRICE_LB = 7 
STIPEND_YEAR_ONE = 200
LIKE_ICON = "d:\\uh\\icd\\Proyecto-ICD\\img\\like.png"
DISLIKE_ICON = "d:\\uh\\icd\\Proyecto-ICD\\img\\dislike.png"

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

#Retorna las fechas y el valor correspondiente del dolar y el euro
def currency_data():
    with open("d:\\uh\\icd\\Proyecto-ICD\\data\\precio_compra.csv","r") as file:
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
def rice_mean_price():
    files = mipymes_list()
    prices = []
    for i in files:
        path = return_path_mipymes(i)
        data = read_json(path)
        for j in data["product"]:
            if j["type"].lower() == "Arroz".lower():
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
    dt = AVERAGE_SALARY if data == "salary" else (MINIMUM_PENSION if data == "pension" else STIPEND_YEAR_ONE)
    values = [dt/i for i in data_currency]
    return values

def mean_price_liquids():
    soft_drink = []
    beer = []
    juice = []
    malt = []
    
    mipymes = mipymes_list()
    
    for i in mipymes:
        path = return_path_mipymes(i)
        json_file = read_json(path)
        for j in json_file['product']:
            if j['type'] == "Refresco":
                soft_drink.append(j['price'])
            elif j['type'] == "Cerveza":
                beer.append(j['price'])
            elif j['type'] == "Jugo":
                juice.append(j['price']) 
            elif j['type'] == "Malta":
                malt.append(j['price'])
    
    mean_soft_drink = mean_list(soft_drink)
    mean_beer = mean_list(beer)
    mean_juice = mean_list(juice)
    mean_malt = mean_list(malt)
    
    return [mean_soft_drink,mean_beer,mean_juice,mean_malt]

def means():
    data = currency_data()
    usd, euro = data[1], data[2]
    
    usd_mean = round(mean_list(usd))
    euro_mean = round(mean_list(euro))
    
    tx1 = f"Precio promedio de USD: {usd_mean}"
    tx2 = f"Precio promedio de EUR: {euro_mean}"
    tx3 = f"Promedio Salario Medio en USD: {round(AVERAGE_SALARY/usd_mean,2)}"
    tx4 = f"Promedio Salario Medio en EUR: {round(AVERAGE_SALARY/euro_mean,2)}"
    tx5 = f"Promedio Pensión Mínima en USD: {round(MINIMUM_PENSION/usd_mean,2)}"
    tx6 = f"Promedio Pensión Mínima en EUR: {round(MINIMUM_PENSION/euro_mean,2)}"
    tx7 = f"Promedio Estipendio 1er Año en USD: {round(STIPEND_YEAR_ONE/usd_mean,2)}"
    tx8 = f"Promedio Estipendio 1er Año en EUR: {round(STIPEND_YEAR_ONE/euro_mean,2)}"
    
    means = [tx1,tx2,tx3,tx4,tx5,tx6,tx7,tx8]
    
    print("Últimos 3 Meses")
    print("--------------------------------------------")
    for mean in means:
        print(mean)
     
def egg_mean_price():
    files = mipymes_list()
    
    price = []
    
    for i in files:
        path = return_path_mipymes(i)
        data = read_json(path)
        
        for j in data["product"]:
            if j["type"] == "Huevo":
                price.append(j["price"])
                break
        
    mean_price = mean_list(price)
    return mean_price
     
#GRÁFICOS

#Mapa de las mipymes
def soft_drink_map():    
    mapa = folium.Map(location=(23.0515757,-82.3304645),zoom_start=11)
    
    archivos = mipymes_list()
    for i in archivos:
        data = read_json(f"d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes\\{i}")
        
        name = data['name']
        lat = data["location"]["lat"]
        long = data["location"]["long"]          
        
        under_200 = False
        for j in data["product"]:
            if j["type"] == "Refresco" and j["price"] <= 200:
                under_200 = True
                break
        
        like_marker = folium.CustomIcon("d:\\uh\\icd\\Proyecto-ICD\\img\\like.png",icon_size=(30,30))
        dislike_marker = folium.CustomIcon("d:\\uh\\icd\\Proyecto-ICD\\img\\dislike.png",icon_size=(30,30))
        
        if under_200:
            folium.Marker([lat,long],tooltip=name,icon=like_marker).add_to(mapa)
        else:
            folium.Marker([lat,long],tooltip=name,icon=dislike_marker).add_to(mapa)
            
    return mapa
          
def full_currency_graph():
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,6))
    
    dates, usd, euro = currency_data()
    
    ax1.plot(dates,usd,label="USD",color="#EC2E30",linewidth=2)
    ax1.plot(dates,euro,label="EUR",color="#FA620F",linewidth=2)
    ax1.set_xticks(dates[::15])
    ax1.tick_params(axis="x",rotation=45)
    ax1.set_title("Tasa de Cambio Últimos 3 meses")
    ax1.set_ylabel("cambio en CUP")
    ax1.legend()
    
    usd_vs_salary = currency_vs_data("salary",usd)
    euro_vs_salary = currency_vs_data("salary",euro)

    usd_vs_pension = currency_vs_data("pension",usd)
    euro_vs_pension = currency_vs_data("pension",euro)
    
    usd_vs_stipend = currency_vs_data("stipend",usd)
    euro_vs_stipend = currency_vs_data("stipend",euro)
    
    ax2.plot(dates,usd_vs_salary,label="Salario Medio USD",color="#EC2E30")
    ax2.plot(dates,euro_vs_salary,label="Salario Medio EUR",color="#fa620f")
    ax2.plot(dates,usd_vs_pension, label="Pensión Mínima USD",color="#fdc401")
    ax2.plot(dates,euro_vs_pension, label="Pensión Mínima EUR",color="#549044")
    ax2.plot(dates,usd_vs_stipend,label="Estipendio 1er Año USD",color="#1564a3")
    ax2.plot(dates,euro_vs_stipend,label="Estipendio 1er Año Euro",color="#5f3c8c")
    ax2.set_xticks(dates[::15])
    ax2.tick_params(axis="x",rotation=45)
    ax2.legend(loc="upper left", bbox_to_anchor=(1, 1))
    
    plt.show()
    
    
    
#Precio promedio del arroz en países de América
def rice_mean_price_graph(ax):
    data = read_json(RICE_MEAN_PRICE_PATH)
    cuba_price = rice_mean_price()
    
    #Implementar que coja la tasa de cambio del dia
    data["Cuba"] = cuba_price/435
    
    tuples_sorted = sorted(data.items(),key=lambda x: x[1])
    countries = [i[0] for i in tuples_sorted]
    prices = [i[1] for i in tuples_sorted]
    
    bar_color = ["#78aa87" if country == "Cuba" else "#c3854c" for country in countries]
   
    ax.barh(countries,prices,color=bar_color)
    ax.set_title("Precio promedio de 1kg de arroz")

#Por ciento con respecto al salario de 1kg de Arroz
def rice_salary_percentage(ax):
    rice = read_json(RICE_MEAN_PRICE_PATH)
    cuba_rice = rice_mean_price()
    rice["Cuba"] = cuba_rice
    
    salary = read_json(SALARIES_PATH)
    
    data_countries_rice = []
    
    for country in rice:
        salary_country = salary[country]["Salario"]
        rice_price = rice[country]
        percentage = (rice_price/salary_country) * 100
        
        data_countries_rice.append((country,percentage))
    
    sorted_dcr = sorted(data_countries_rice,key=lambda x: x[1])

    countries = [i[0] for i in sorted_dcr]
    percentages = [i[1] for i in sorted_dcr]
    
    bar_color = ["#78aa87" if country == "Cuba" else "#c3854c" for country in countries]
       
    img = mpimg.imread('img/m1.png')
    imagebox = OffsetImage(img, zoom=0.4)

    ab = AnnotationBbox(imagebox, (9, 3), frameon=False)
    ax.add_artist(ab)          
    ax.barh(countries,percentages, color=bar_color)
    ax.set_title("Costo de 1kg de arroz con respecto al salario medio (por ciento)")
    ax.set_yticks(range(len(countries)))
    ax.set_yticklabels(["Cuba" if i == "Cuba" else "" for i in countries])
    ax.tick_params(axis="y")
    
  
def full_rice_graph():  
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    rice_mean_price_graph(ax1)
    rice_salary_percentage(ax2)

    plt.show()
    
def rice_vs_minimum_pension():
    cuba_rice = rice_mean_price()
    lb7_to_kg = round(7/2.20462,2)
    cuba_rice_rationed = round(lb7_to_kg*cuba_rice,2)
    pension = MINIMUM_PENSION
    
    percentage = round((cuba_rice_rationed/pension)*100,2)
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    x = ["Pensión Mínima", "Precio Mipymes", "Precio Subsidiado"]
    y = [pension,cuba_rice_rationed,7*REGULATED_RICE_PRICE_LB]
    
    img = mpimg.imread("img/rice.png")
    
    imagebox = OffsetImage(img, zoom=0.05)

    ab = AnnotationBbox(imagebox, (2, 2500), frameon=False)
    ax.add_artist(ab)      

    bar_container = ax.bar(x,y,color=['#aac79a','#f0c4b2','#e3d3c2'])
    ax.bar_label(bar_container,y)
    ax.set_title("Pensión mínima y costo del arroz: subsidiado vs privado (7 lb)")
    ax.text(x[1],y[1]/2,f"{percentage}%",ha='center',color='black',fontname="Arial",fontweight="bold",fontsize=20)
    ax.annotate("", xytext=(0.8, (y[1]/2)+70), xy=(0, y[0]/2),arrowprops=dict(arrowstyle="->"))
    plt.show()
    
def liquids_graph():
    means = mean_price_liquids()
    products = ["Refresco", "Cerveza", "Jugo", "Malta"]
    
    fig, ax = plt.subplots()
    
    ax.bar(products,means,color="#F0B884")
    ax.axhline(y=200,ls="--",color="#003049")
    ax.annotate("Estipendio 1er Año Mensual", xytext=(0.6,270), xy=(0, 205),arrowprops=dict(arrowstyle="->",color="#003049",linewidth=2))
    ax.set_title("Precio promedio de líquidos")
    ax.set_ylabel("Precio en CUP")

def egg_graph():
    mean_price = egg_mean_price()
    price_five_eggs = mean_price/5
    x_axis = ["Salario Medio", "Jubilación Mínima"]
    y_axis = [price_five_eggs/i for i in [AVERAGE_SALARY,MINIMUM_PENSION]]
    
    fig, ax = plt.subplots()
    
    ax.bar(x_axis,y_axis)
    
    plt.show()
    
egg_graph()