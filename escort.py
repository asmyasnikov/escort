import pandas as pd
import numpy as np
import heapq
from operator import itemgetter
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from som import SOM

# Размер надписей на графиках
PLOT_LABEL_FONT_SIZE = 14 
# Генерация цветовой схемы
# Возвращает список цветов
def getColors(n):
    COLORS = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        COLORS.append(cm(i))
    return COLORS

def dict_sort(my_dict):
    keys = []
    values = []
    my_dict = sorted(my_dict.items(), key=lambda x:x[1], reverse=True)
    for k, v in my_dict:
        keys.append(k)
        values.append(v)
    return (keys,values)

def metro_stations(df):
    metro_count = pd.value_counts(list(m.strip(" \xa0") for m in np.hstack(list(map(lambda m: m.split(","), list(m.strip("\"") for m in df['Metro'].values if isinstance(m, str)))))))
    metro_count_keys, _ = dict_sort(dict(heapq.nlargest(100, metro_count.items(), key=itemgetter(1))))
    return metro_count_keys

def metro_price(df, m):
    return df.query('"'+m+'" in Metro')[['Price_USD']].mean().Price_USD

def metro_boobs(df, m):
    return df.query('"'+m+'" in Metro')[['Boobs']].mean().Boobs

def metro_age(df, m):
    return df.query('"'+m+'" in Metro')[['Age']].mean().Age

def metro(df):
    metro_count = pd.value_counts(list(m.strip(" \xa0") for m in np.hstack(list(map(lambda m: m.split(","), list(m.strip("\"") for m in df['Metro'].values if isinstance(m, str)))))))
    metro_count_keys, metro_count_values = dict_sort(dict(heapq.nlargest(100, metro_count.items(), key=itemgetter(1))))
    TOP_METRO = len(metro_count_keys)
    PLOT_LABEL_FONT_SIZE = 8
    plt.title('Количество предложений эскорт услуг по станциям метро', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(np.arange(TOP_METRO), metro_count_values, color=getColors(TOP_METRO))
    plt.xticks(np.arange(TOP_METRO), metro_count_keys, rotation=90, fontsize=6)
    plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
    plt.ylabel('Количество наблюдений', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.show()

def price(df, limit):
    prices = list(p for p in df['Price_USD'].values if isinstance(p, float) and p < limit)
    n, bins, patches = plt.hist(prices, 20, facecolor='blue', alpha=30)
    plt.xlabel('Стоимость услуг')
    plt.ylabel('Количество предложений')
    plt.title('Распределение количества предложений экскорт услуг по стоимости')
    plt.show()

def price_by_metro(df):
    stations = metro_stations(df)
    stations, prices = dict_sort({m: metro_price(df, m) for m in stations})
    print({m: metro_price(df, m) for m in stations})
    # TOP_METRO = len(stations)
    # PLOT_LABEL_FONT_SIZE = 8
    # plt.title('Средняя цена эскорт-услуг по станциям метро', fontsize=PLOT_LABEL_FONT_SIZE)
    # plt.bar(np.arange(TOP_METRO), prices, color=getColors(TOP_METRO))
    # plt.xticks(np.arange(TOP_METRO), stations, rotation=90, fontsize=6)
    # plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
    # plt.ylabel('Средняя цена', fontsize=PLOT_LABEL_FONT_SIZE)
    # plt.show()


def boobs_by_metro(df):
    stations = metro_stations(df)
    stations, boobs = dict_sort({m: metro_boobs(df, m) for m in stations})
    TOP_METRO = len(stations)
    PLOT_LABEL_FONT_SIZE = 8
    plt.title('Средний размер груди по станциям метро', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(np.arange(TOP_METRO), boobs, color=getColors(TOP_METRO))
    plt.xticks(np.arange(TOP_METRO), stations, rotation=90, fontsize=6)
    plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
    plt.ylabel('Средний размер груди', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.show()

def age_by_metro(df):
    stations = metro_stations(df)
    stations, age = dict_sort({m: metro_age(df, m) for m in stations})
    TOP_METRO = len(stations)
    PLOT_LABEL_FONT_SIZE = 8
    plt.title('Средний возраст по станциям метро', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.bar(np.arange(TOP_METRO), age, color=getColors(TOP_METRO))
    plt.xticks(np.arange(TOP_METRO), stations, rotation=90, fontsize=6)
    plt.yticks(fontsize=PLOT_LABEL_FONT_SIZE)
    plt.ylabel('Средний возраст', fontsize=PLOT_LABEL_FONT_SIZE)
    plt.show()

def age_price(df):
    plt.figure(figsize=(12,10), dpi= 80)
    sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
    plt.show()

df = pd.read_csv('./escort.csv', escapechar='`', low_memory=False)
price_by_metro(df)