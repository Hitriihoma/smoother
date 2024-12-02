# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 15:51:51 2024

@author: 123
"""

import os
import sys
import json
import pandas as pd
from matplotlib import pyplot as plt

try:
    from smoother.code_package.moving_average import MovingAverage
except:
    print('------------- need to add directory smoother to $PATH or PYTHONPATH----------')
    add_to_path = str(os.path.dirname(os.path.dirname(os.getcwd()))) #str(os.getcwd()) # str(os.path.dirname(os.path.dirname(os.getcwd())))
    sys.path.append(add_to_path)
    from smoother.code_package.moving_average import MovingAverage

def process_data_dir(wdir=str(os.path.join(os.path.dirname(os.getcwd()), 'data')), window=None, drop_outlier=False):
    '''
    Обработать данные в директории

    Parameters
    ----------
    wdir : string, optional
        Путь к директории с файлами для обработки. The default is str(os.path.join(os.path.dirname(os.getcwd()), 'data')).
    drop_outlier : boolean, optional
        Использовать ли убирание одного выброса при расчёте среднего значения подвыборки. The default is False.

    Returns
    -------
    None.

    '''
    # проверить наличие рабочей директории
    if not os.path.isdir(wdir):
        raise ValueError('Указанный путь к файлам не является директорией')
    # проверить корректность введённых параметров
    if window is None:
        raise ValueError('Задайте параметры для обработки (окно)')
    
    # создать обработчик данных
    smoother = MovingAverage(window)
    
    # список файлов в рабочей директории
    data_files = os.listdir(wdir)
    
    # обработать каждый файл из списка
    for filename in data_files:
        data_path = os.path.join(wdir,filename)
        
        # чтение файла  
        with open(data_path, 'r') as file:
            data = json.load(file)
        df = pd.DataFrame.from_dict(data['data'])
        name = data['properties']['name']
        
        # Конвертировать строчную дату в тип дата
        df.loc[:, 'date'] = pd.to_datetime(df["date"], format='%Y-%m-%dT%H:%M:%S.%f')
        
        # Выборки для обработки
        x = df['date'].to_numpy()
        y = df['x'].to_numpy()
        
        # Обработать выборки
        x_tr, y_tr = smoother.transform(x=x, y=y, drop_outlier=drop_outlier)
        
        # построить график, сохранить в ./results
        save_dir = str(os.path.join(os.path.dirname(os.getcwd()), 'results'))
        fig = plt.figure(figsize=(30,10))
        ax = fig.add_subplot(111)
        ax.plot(x, y,  marker='o', label='Исходные данные')
        ax.plot(x_tr, y_tr,  marker='o', label='Обработанные данные')
        ax.legend()
        ax.set_title(name)
        plt.savefig(os.path.join(save_dir,f'{os.path.splitext(filename)[0]}.png'))
        plt.close()
        
if __name__ == "__main__":
    window = int(input('Введите окно скользящего среднего:\n'))
    drop_outlier_input = input('Требуется ли убирать выброс в подвыборках [True, False]:\n')
    if drop_outlier_input == 'True':
        drop_outlier = True
    elif drop_outlier_input == 'False':
        drop_outlier = False
    else:
        raise ValueError('Некорректное значение drop_outlier_input (требуется ли убирать выбросы')
    process_data_dir(wdir=str(os.path.join(os.path.dirname(os.getcwd()), 'data')), window=window, drop_outlier=drop_outlier)