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
    from smoother.code_package.single_exponential_smoothing import SES
    from smoother.code_package.double_exponential_smoothing import DES
except:
    print('------------- need to add directory smoother to $PATH or PYTHONPATH----------')
    add_to_path = str(os.path.dirname(os.path.dirname(os.getcwd()))) #str(os.getcwd()) # str(os.path.dirname(os.path.dirname(os.getcwd())))
    sys.path.append(add_to_path)
    from smoother.code_package.moving_average import MovingAverage
    from smoother.code_package.single_exponential_smoothing import SES
    from smoother.code_package.double_exponential_smoothing import DES

def process_data_dir(wdir=str(os.path.join(os.path.dirname(os.getcwd()), 'data')), smoother=None):
    '''
    Обработать данные в директории

    Parameters
    ----------
    wdir : string, optional
        Путь к директории с файлами для обработки. The default is str(os.path.join(os.path.dirname(os.getcwd()), 'data')).
    window : integer
        Окно скользящего среднего. The default is None.
    drop_outlier : boolean, optional
        Использовать ли убирание одного выброса при расчёте среднего значения подвыборки. The default is False.

    Returns
    -------
    None.

    '''
    # проверить наличие рабочей директории
    if not os.path.isdir(wdir):
        raise ValueError('Указанный путь к файлам не является директорией')
    # список файлов в рабочей директории
    data_files = os.listdir(wdir)
    # Директория сохранения
    save_dir = str(os.path.join(os.path.dirname(os.getcwd()), 'results'))
    
    # Создать обработчики
    smoother_objs = {}
    for smoother_name in smoother.keys():
        smoother_type = smoother[smoother_name]["type"]
        if smoother_type == "moving_average":
            smoother_objs.update({smoother_name: MovingAverage(smoother[smoother_name]["window"], smoother[smoother_name]["drop_outliers"])})
        elif smoother_type == "single_exponential":
            smoother_objs.update({smoother_name: SES(smoother[smoother_name]["alpha"])})
        elif smoother_type == "double_exponential":
            smoother_objs.update({smoother_name: DES(smoother[smoother_name]["alpha"], smoother[smoother_name]["gamma"])})
    
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
        
        # Инициализация фигуры графика
        fig = plt.figure(figsize=(30,10), facecolor=(1,1,1))
        # Исходные данные
        ax = fig.add_subplot(111)
        ax.plot(x, y,  marker='o', label='Исходные данные')
        # Обработанные данные, используюя ранее созданные обработчики
        for smoother_name in smoother_objs.keys():
            temp_smoother = smoother_objs[smoother_name]
            x_tr, y_tr = temp_smoother.transform(x=x, y=y)
            ax.plot(x_tr, y_tr,  marker='o', alpha=0.5, label=f"Обработанные данные: {smoother_name}")
        ax.legend(fontsize=20)
        ax.grid(axis='y')
        ax.set_title(name, fontsize=30)
        plt.savefig(os.path.join(save_dir,f'{os.path.splitext(filename)[0]}.png'))
        plt.close()
        
if __name__ == "__main__":
    smoother = {"ma_10_true": {"type": "moving_average", "window": 10, "drop_outliers": True}
                 ,"ma_10_false": {"type": "moving_average", "window": 10, "drop_outliers": False}
                 ,"des_0.3_0.3": {"type": "double_exponential", "alpha": 0.3, "gamma": 0.3}
                 ,"des_0.3_0.9": {"type": "double_exponential", "alpha": 0.3, "gamma": 0.9}
                 }
    process_data_dir(wdir=str(os.path.join(os.path.dirname(os.getcwd()), 'data')), smoother=smoother)