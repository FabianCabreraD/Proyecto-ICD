import os
import json
import folium
import matplotlib.pyplot as plt
import csv
import datetime
import numpy as np
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as mpatches

#CONSTANTES
MIPYMES_PATH = "data\\mipymes"
RICE_MEAN_PRICE_PATH = "data\\rice_price.json"
SALARIES_PATH = "data\\salary.json" 
AVERAGE_SALARY = 6660.1
MINIMUM_PENSION = 3056
REG_RICE_NATIONAL_PRICE_LB = 7 
REG_RICE_INTERNATIONAL_PRICE_LB = 10
STIPEND_YEAR_ONE = 200
LIKE_ICON = "img\\like.png"
DISLIKE_ICON = "img\\dislike.png"

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

def salary_cuba():
    data = read_json("data/salary_cuba.json")
    data_sorted = dict(sorted(data.items(),key=lambda x:x[1][0],reverse=True))
    return data_sorted
     
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
        
        products = []
        for j in data["product"]:
            if j["type"] in ["Refresco","Malta","Jugo","Cerveza"] and j["price"] <= 200:
                products.append(j["type"])
        
        like_marker = folium.CustomIcon("d:\\uh\\icd\\Proyecto-ICD\\img\\like.png",icon_size=(30,30))
        dislike_marker = folium.CustomIcon("d:\\uh\\icd\\Proyecto-ICD\\img\\dislike.png",icon_size=(30,30))
        
        products_string = ', '.join(products)
        
        html_like = f"""
            <h1>{name}</h1>
            <p>{products_string}</p>
        """
        
        html_dislike = f"""
            <h1>{name}</h1>
        """

        
        if len(products) > 0:
            folium.Marker([lat,long],tooltip=name,popup=html_like,icon=like_marker).add_to(mapa)
        else:
            folium.Marker([lat,long],tooltip=name,popup=html_dislike,icon=dislike_marker).add_to(mapa)
            
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

# #Por ciento con respecto al salario de 1kg de Arroz
def rice_and_salary_graph():
    cuba_rice = rice_mean_price()
    
    salary_and_rice_data = read_json("data/salary_and_rice.json")
    salary_and_rice_data["Cuba"]["Rice"] = cuba_rice/435
    salary_and_rice_data["Cuba"]["Salary"] = 6660.1/435
    
    data = dict(sorted(salary_and_rice_data.items(), key=lambda x: x[1]["Rice"]))
        
    countries = data.keys()
    percentage = [(i["Rice"]/i["Salary"]*100) for i in data.values()]
    rice = [-i["Rice"] for i in data.values()]
    
    fig, ax = plt.subplots(figsize=(12,6))
    
    img = mpimg.imread('img/m1.png')
    imagebox = OffsetImage(img, zoom=0.4)

    ab = AnnotationBbox(imagebox, (9, 3), frameon=False)
    ax.add_artist(ab)      
      
    ax.barh(countries,rice,color="#78aa87",edgecolor="gray", label="Precio Promedio 1kg")
    ax.barh(countries,percentage,edgecolor="gray",color="#c3854c",label="Por ciento del salario medio")
    ax.axvline(x=0,ls = "--", color="black")
    ticks = ax.get_xticks()
    ax.set_xticks(ticks)
    ax.set_xticklabels([abs(int(t)) for t in ticks])
    ax.set_title("Precio de 1kg de arroz y por ciento del salario medio")
    ax.text(x=-3,y=-3,s="Precio en USD",ha="center")
    ax.text(x=7,y=-3,s="Por ciento",ha="center")
    plt.subplots_adjust(left=0.2)
    plt.legend()
    plt.show()
    
def rice_vs_minimum_pension():
    cuba_rice = rice_mean_price()
    lb7_to_kg = round(7/2.20462,2)
    cuba_rice_rationed = round(lb7_to_kg*cuba_rice,2)
    pension = MINIMUM_PENSION
    
    percentage = round((cuba_rice_rationed/pension)*100,2)
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    x = ["Precio Mipymes", "Precio Subsidiado Importado", "Precio Subsidiado Nacional"]
    y = [cuba_rice_rationed,7*REG_RICE_INTERNATIONAL_PRICE_LB,7*REG_RICE_NATIONAL_PRICE_LB]
    
    img = mpimg.imread("img/rice.png")
    
    imagebox = OffsetImage(img, zoom=0.05)

    ab = AnnotationBbox(imagebox, (2, 2400), frameon=False)
    ax.add_artist(ab)      

    bar_container = ax.bar(x,y,color=['#aac79a','#f0c4b2','#e3d3c2'],edgecolor="gray")
    ax.bar_label(bar_container,y)
    ax.axhline(y=3056,ls="--",color="black")
    ax.set_title("Pensión mínima y costo del arroz: subsidiado vs privado (7 lb)")
    ax.text(x[0],y[0]/2,f"{percentage}%",ha='center',color='black',fontname="Arial",fontweight="bold",fontsize=20)
    ax.annotate("", xytext=(0, y[0]-100), xy=(1, 3020),arrowprops=dict(arrowstyle="->",color="black"))
    plt.show()
    
def liquids_graph():
    means = mean_price_liquids()
    products = ["Refresco", "Cerveza", "Jugo", "Malta"]
    
    fig, ax = plt.subplots(figsize=(7,5))
    
    ax.bar(products,means,color="#F0B884",edgecolor="gray")
    
    for index, mean in enumerate(means):
        ax.text(x=index,y=mean+5,s=mean,ha="center")
    
    ax.axhline(y=200,ls="--",color="#003049")
    ax.annotate("Estipendio 1er Año Mensual", xytext=(-0.2,330), xy=(0, 205),arrowprops=dict(arrowstyle="->",color="#003049",linewidth=2),weight="bold")
    ax.set_title("Precio promedio de líquidos")
    ax.set_ylabel("Precio en CUP")

def egg_employees_graph():
    mean_price = egg_mean_price()
    price_five_eggs = mean_price/5
    salary = salary_cuba()
    
    sector = salary.keys()
    percentage_thirty = [mean_price/i[0]*100 for i in salary.values()]
    percentage_employees = [i[1] for i in salary.values()]
    
    fig, ax = plt.subplots(figsize=(12,6))
    
    n = len(sector)
    index = list(range(n))
    height = 0.35
    
    x_egg = [i - height/2 for i in index]

    x_employees = [i + height/2 for i in index]
    
    color_list = ["#A8E6CF" if v > 0 else "#FF8C94" for v in percentage_employees]
    
    ax.barh(x_egg,percentage_thirty,label="Cartón (30 u)",color="#AED9E0",height=height,edgecolor="gray")
    ax.barh(x_employees, percentage_employees,height=height,color=color_list,edgecolor="gray", label="Cambio en porcentaje de trabajadores")
    
    ax.set_yticks(index)
    ax.set_yticklabels(sector)
    ax.set_xlabel("Por ciento del Salario Medio")
    ax.axvline(x=0,ls="--",color="black")
    ax.set_title("Salario vs Cartón de Huevo y Variación de empleados")
        
    positivo_patch = mpatches.Patch(color="#A8E6CF", label="Incremento trabajadores")
    negativo_patch = mpatches.Patch(color="#FF8C94", label="Decremento trabajadores")
    otro_patch = mpatches.Patch(color="#AED9E0", label="Otro dato")

    ax.legend(handles=[positivo_patch, negativo_patch, otro_patch])

    plt.subplots_adjust(left=0.4)
    plt.show()
