# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 15:51:51 2024

@author: 123
"""

import os
import json
import pandas as pd

def process_data_dir(wdir=str(os.path.join(os.path.dirname(os.getcwd()), 'data'))):
    '''
    Обработать дан

    Parameters
    ----------
    wdir : string, optional
        Путь к директории с файлами для обработки. The default is str(os.path.join(os.path.dirname(os.getcwd()), 'data')).

    Returns
    -------
    None.

    '''
    # проверить наличие рабочей директории
    if not os.path.isdir(wdir):
        raise ValueError('Указанный путь к файлам не является директорией')
    
    # список файлов в рабочей директории
    data_files = os.listdir(wdir)
    
    # обработать каждый файл из списка
    for filename in data_files:
        data_path = os.path.join(wdir,filename)
        
        # чтение файла  
        with open(data_path, 'r') as file:
            data = json.load(file)
        df = pd.DataFrame.from_dict(data['data'])
        
        # Конвертировать строчную дату в тип дата
        df.loc[:, 'date'] = pd.to_datetime(df["date"], format='%Y-%m-%dT%H:%M:%S.%f')
        
        # Выборки для обработки
        x = df['date'].to_numpy()
        y = df['x'].to_numpy()
    
if __name__ == "__main__":
    process_data_dir(wdir=str(os.path.join(os.path.dirname(os.getcwd()), 'data')))