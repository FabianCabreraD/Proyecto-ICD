#Para obtener los archivos de una carpeta
import os
#Para leer archivos
import json
import csv
#Para mapa
import folium
#Para gráfico
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patches as mpatches
#Para mostrar tabla
from prettytable import PrettyTable

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
def path_mipyme(name):
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
        path = path_mipyme(i)
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

#Retorna el precio promedio de los líquidos
def liquids_mean_price():    
    prices = {
        "Refresco": [],
        "Cerveza": [],
        "Jugo": [],
        "Malta": []
    }
    
    mipymes = mipymes_list()
    
    for i in mipymes:
        path = path_mipyme(i)
        json_file = read_json(path)
        for j in json_file['product']:
            if j["type"] in prices:
                prices[j["type"]].append(j["price"])
    
    mean_soft_drink = mean_list(prices["Refresco"])
    mean_beer = mean_list(prices["Cerveza"])
    mean_juice = mean_list(prices["Jugo"])
    mean_malt = mean_list(prices["Malta"])
    
    return [mean_soft_drink,mean_beer,mean_juice,mean_malt]

def beer_price():
    national = []
    imported = []
    
    mipymes = mipymes_list()
    for i in mipymes:
        path = path_mipyme(i)
        data = read_json(path)
        products = data["product"]
        for product in products:
            if product["type"] == "Cerveza":
                price = product["price"]
                national.append(price) if product["origin"] == "Nacional" else imported.append(price)
                
    national_mean = mean_list(national)
    imported_mean = mean_list(imported)
    return national_mean, imported_mean

#Devuelve promedios usados
def means_table():
    data = currency_data()
    usd, euro = data[1], data[2]
    
    usd_mean = round(mean_list(usd))
    euro_mean = round(mean_list(euro))
    
    sectors = ["Salario Medio", "Pensión Mínima", "Estipendio 1er Año"]
    constants = [AVERAGE_SALARY, MINIMUM_PENSION, STIPEND_YEAR_ONE]
    
    table = PrettyTable()
    for i in ["Últimos 3 meses", "USD", "EURO"]:
        table.add_column(i,[])
    for sector,constant in zip(sectors, constants):
        table.add_row([sector,round(constant/usd_mean,2),round(constant/euro_mean,2)])
    
    print(table)
    
 
#Retorna el precio promedio del huevo     
def egg_mean_price():
    files = mipymes_list()
    
    price = []
    
    for i in files:
        path = path_mipyme(i)
        data = read_json(path)
        
        for j in data["product"]:
            if j["type"] == "Huevo":
                price.append(j["price"])
                break
        
    mean_price = mean_list(price)
    return mean_price

#Lee el archivo de los salarios en Cuba y los devuelve ordenados
def cuba_salary():
    data = read_json("data/cuba_salary.json")
    data_sorted = dict(sorted(data.items(),key=lambda x:x[1][0],reverse=True))
    return data_sorted

#Retorna el valor del usd del último día
def last_usd_price():
    usd = currency_data()[1]
    last_usd = usd[-1]
    return last_usd

def last_currency_date():
    date = currency_data()[0]
    last_date = date[-1]
    return last_date
    
#GRÁFICOS

def soft_drink_map():    
    mapa = folium.Map(location=(23.07088,-82.43847),zoom_start=12)
    
    archivos = mipymes_list()
    for i in archivos:
        data = read_json(f"d:\\uh\\icd\\Proyecto-ICD\\data\\mipymes\\{i}")
        
        name = data['name'] if data["name"] is not None else data["location"]["address"]
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
            <p>No alcanza para ningún líquido</p>
        """

        if len(products) > 0:
            folium.Marker([lat,long],tooltip=name,popup=html_like,icon=like_marker).add_to(mapa)
        else:
            folium.Marker([lat,long],tooltip=name,popup=html_dislike,icon=dislike_marker).add_to(mapa)
            
    return mapa
          
def currency_graph():
    fig, ax = plt.subplots()
    
    dates, usd, euro = currency_data()
    
    ax.plot(dates,usd,label="USD",color="#EC2E30",linewidth=2)
    ax.plot(dates,euro,label="EUR",color="#FA620F",linewidth=2)
    ax.set_xticks(dates[::15])
    ax.tick_params(axis="x",rotation=45)
    ax.set_title("Tasa de Cambio Últimos 3 meses")
    ax.set_ylabel("cambio en CUP")
    ax.legend()
    plt.show()
    
def salary_graph():
    dates, usd, euro = currency_data()
    
    usd_vs_salary = currency_vs_data("salary",usd)
    euro_vs_salary = currency_vs_data("salary",euro)

    usd_vs_pension = currency_vs_data("pension",usd)
    euro_vs_pension = currency_vs_data("pension",euro)
    
    usd_vs_stipend = currency_vs_data("stipend",usd)
    euro_vs_stipend = currency_vs_data("stipend",euro)
    
    fig, ax = plt.subplots()
    
    ax.plot(dates,usd_vs_salary,label="Salario Medio USD",color="#EC2E30")
    ax.plot(dates,euro_vs_salary,label="Salario Medio EUR",color="#fa620f")
    ax.plot(dates,usd_vs_pension, label="Pensión Mínima USD",color="#fdc401")
    ax.plot(dates,euro_vs_pension, label="Pensión Mínima EUR",color="#549044")
    ax.plot(dates,usd_vs_stipend,label="Estipendio 1er Año USD",color="#1564a3")
    ax.plot(dates,euro_vs_stipend,label="Estipendio 1er Año Euro",color="#5f3c8c")
    ax.set_xticks(dates[::15])
    ax.tick_params(axis="x",rotation=45)
    #Arreglar posicion lygenda
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.show()
    
#Terminar gráfico
def salary_cuba_vs_america():
    usd = last_usd_price()
    date = last_currency_date()
    usd_vs_salary_cuba = AVERAGE_SALARY/usd
    
    data = read_json("data/salary_and_rice.json")
    data["Cuba"]["Salary"] = round(usd_vs_salary_cuba,2)
    
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1]["Salary"]))
    x = sorted_data.keys()
    y = [i["Salary"] for i in sorted_data.values()]
    
    fig, ax = plt.subplots(figsize=(10,6))
    
    color = ["#1564a3" if i != "Cuba" else "#EC2E30" for i in x]

    ax.barh(x,y,color=color,edgecolor="black")
    ax.set_xticks(list(range(0,4100,1000)))
    index_cuba = list(range(len(x)))[0]
    ax.annotate(f"Cambio: 1 USD - {usd} ({date})", (300,index_cuba),(1000,index_cuba-0.1),arrowprops=dict(arrowstyle="->",color="black"))
    ax.set_title("Salario en varios países de América en USD")
    for i in enumerate(x):
        index = i[0]
        ax.text(y[index]+3,index-0.2,s=f"{y[index]}")
        
    
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
    usd_price = last_usd_price()
    
    salary_and_rice_data = read_json("data/salary_and_rice.json")
    salary_and_rice_data["Cuba"]["Rice"] = cuba_rice/usd_price
    salary_and_rice_data["Cuba"]["Salary"] = 6660.1/usd_price
    
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
    ax.axvline(x=0, color="black")
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
    
    ax.bar(x,y,color=['#aac79a','#f0c4b2','#e3d3c2'], edgecolor="gray")
    ax.axhline(y=3056,ls="--",color="black")
    ax.set_title("Pensión mínima y costo del arroz: subsidiado vs privado (7 lb)")
    ax.text(x[0],y[0]/2,f"{percentage}%",ha='center',color='black',fontname="Arial",fontweight="bold",fontsize=20)
    for index in enumerate(x):
        ind = index[0]
        if index != 0:
            s = f"{y[ind]} ({round(y[ind]/MINIMUM_PENSION*100,2)}%)"
        else:
            s = y[ind]
        ax.text(x=x[ind], y=y[ind]+20,s=s,ha="center")
    ax.annotate("", xytext=(0, y[0]-100), xy=(1, 3020),arrowprops=dict(arrowstyle="->",color="black"))
    ax.set_yticks(list(range(0,3600,500)))
    ax.text(x=1,y=3100,s="Pensión Mínima")
    plt.show()
    
def milk_beans_minpens():
    files = mipymes_list()
       
    milk_kg = []
    bean_kg = []
       
    for i in files:
        path = path_mipyme(i)
        data = read_json(path)
           
        for j in data["product"]:
            if j["type"] == "Frijol" and j["unity"] == "1 kg":
                bean_kg.append(j["price"])
            if j["type"] == "Leche" and j["unity"] == "1 kg":
                milk_kg.append(j["price"])
        
    mean_milk = mean_list(milk_kg)
    mean_bean = mean_list(bean_kg)
    surplus = MINIMUM_PENSION - (mean_milk + mean_bean)
    
    fractions = [i/MINIMUM_PENSION*100 for i in [mean_milk,mean_bean,surplus]]
    labels = ["Leche 1 kg","Frijoles 1 kg","Resto"]
    
    fig, ax = plt.subplots()

    colors = ["#006494","#0582ca","#00a6fb"]
    ax.pie(x=fractions,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        wedgeprops={"edgecolor":"#003366","linewidth":1},
        textprops={"fontsize":12,"color":"black"},
    )
    plt.show()
    
def liquids_graph():
    means = liquids_mean_price()
    products = ["Refresco", "Cerveza", "Jugo", "Malta"]
    
    fig, ax = plt.subplots(figsize=(7,5))
    
    ax.bar(products,means,color="#F0B884",edgecolor="gray")
    
    for index, mean in enumerate(means):
        ax.text(x=index,y=mean+5,s=mean,ha="center")
    
    ax.axhline(y=200,ls="--",color="#003049")
    ax.annotate("Estipendio 1er Año Mensual", xytext=(-0.2,330), xy=(0, 205),arrowprops=dict(arrowstyle="->",color="#003049",linewidth=2),weight="bold")
    ax.set_title("Precio promedio de líquidos")
    ax.set_ylabel("Precio en CUP")
    plt.show()
    
def beer_graph():
    national, imported = beer_price()
    x = ["Nacional", "Importada"]
    y = [national, imported]
    
    fig, ax = plt.subplots(figsize=(6,4))
    
    ax.bar(x, y, color="#F0B884",edgecolor="gray")
    ax.axhline(y=200,ls="--",color="#003049")
    ax.set_title("Precios de la cerveza nacional e importada vs. estipendio universitario")
    for i in range(len(x)):
        inf = 200
        sup = y[i]
        ax.annotate("",(i,inf),(i,sup),arrowprops=dict(arrowstyle="<->"))
        porcentage = round((sup-inf)/200*100,2)
        ax.text(x=i+0.2,y=(inf+sup)/2,s=f"{porcentage}%",ha="center",fontsize="large")
    plt.show()
    

def egg_employees_graph():
    mean_price = egg_mean_price()
    salary = cuba_salary()
    
    sector = salary.keys()
    percentage_thirty = [mean_price/i[0]*100 for i in salary.values()]
    percentage_employees = [i[1] for i in salary.values()]
    
    fig, ax = plt.subplots(figsize=(14,6))
    
    n = len(sector)
    index = list(range(n))
    height = 0.35
    
    x_egg = [i - height/2 for i in index]

    x_employees = [i + height/2 for i in index]
    
    color_list = ["#A8E6CF" if v > 0 else "#FF8C94" for v in percentage_employees]
    
    edgecolor = ["gray" if i != "Educación" else "red" for i in sector]
    
    ax.barh(x_egg,percentage_thirty,label="Cartón (30 u)",color="#AED9E0",height=height,edgecolor=edgecolor)
    ax.barh(x_employees, percentage_employees,height=height,color=color_list,edgecolor="gray")
    
    ax.set_yticks(index)
    ax.set_yticklabels(sector)
    ax.set_xlabel("Por ciento del Salario Medio")
    ax.axvline(x=0,color="black")
    ax.set_title("Salario vs Cartón de Huevo y Variación de empleados")
        
    positivo_patch = mpatches.Patch(color="#A8E6CF", label="Incremento trabajadores")
    negativo_patch = mpatches.Patch(color="#FF8C94", label="Decremento trabajadores")
    otro_patch = mpatches.Patch(color="#AED9E0", label="Cartón de Huevo vs Salario (%)")

    ax.legend(handles=[positivo_patch, negativo_patch, otro_patch],fontsize="small")
    
    ax.set_xticks(list(range(-20,90,10)))
    ax.tick_params(axis="y",labelsize="small")
    
        
    for i in range(len(sector)):
        if percentage_employees[i] > 0:
            x = percentage_employees[i] + 2
        else:
            x = percentage_employees[i] - 6
        ax.text(x,y=i,s=round(percentage_employees[i],2),fontsize="small")
        
        ax.text(x=percentage_thirty[i]+2, y=i-0.35,s=round(percentage_thirty[i],2),fontsize="small")

    plt.subplots_adjust(left=0.4)
    plt.show()