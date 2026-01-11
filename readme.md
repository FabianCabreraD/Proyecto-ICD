> **¿Para qué alcanza lo que ganamos? - Proyecto ICD**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Static Badge](https://img.shields.io/badge/Matplotlib-black?style=for-the-badge)

## Problemática

Si estás leyendo esto, lo más probable es o que seas un estudiante como yo, o un simple trabajador estatal
o una persona retirada.

En cualquiera de los 3 casos, el estado nos entrega un dinero: un estipendio, un salario o una pensión.

Y aunque sea repetitivo, en cualquiera de los 3 casos, no nos alcanza.

Este proyecto lo demuestra, anímate a echarle un vistazo

## Fuentes de Datos

- **ONEI:** Nos aporta informes estadísticos de salarios, pensiones, estipendios.
- **elTOQUE:** 'Seguramente nadie sabe qué es, esa 'increíble' página que nos dice cuánto vale nuestra moneda.
- **MIPYMES:** Nuestras 'bodegas' particulares, donde hay de todo, pero a qué precios!

## Estructura

```text
├── data/                    # Todos los datos usados: Mipymes, informes de la ONEI, datos de la web.
│   ├── mipymes/             # JSON de las mipymes.
│   ├── cuba_salary.json     # Salarios medios en Cuba por sectores.
│   ├── indicadores.pdf      # Informe de la ONEI.
│   ├── selling_price.csv    # Datos de cambio de la moneda extraídos de elTOQUE.
│   ├── salary_and_rice.json # Salarios medio y precio promedio de arroz en países de América.
|   ├── sources.txt          # Fuente de datos obtenidos.
│
├── evidencia/               # Fotos de las mipymes que visité.
│
├── img/                     # Imágenes usadas en el Jupyter.
│
├── main.ipynb               #Jupyter Notebook para mostrar la historia y las gráficas.
│
├── icd_module.py            # Archivos con las funciones utilizadas para procesar la información y crear gráficos.
├── readme.md                # Para explicar un poquito el proyecto.
├── report.pdf               # Se profundiza en la problemática y etapas del trabajo.
└── requeriments.txt         # Requisitos para reproducir el proyecto
```
