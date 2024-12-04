# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:18:59 2024

@author: Hitriihoma
"""

import numpy as np

import json
import os
from pathlib import Path
from datetime import datetime


    
def generate_test_cases(data_dir = os.path.join(Path.cwd().parent, 'data')):
    '''
    Сохранение тестовых случаев в директорию data_dir

    Parameters
    ----------
    data_dir : str, optional
        Путь к директории, куда сохранять данные. The default is os.path.join(Path.cwd().parent, 'data').

    Returns
    -------
    None.

    '''
    def save_to_json(data_dir, filename, date_array, data_array, id_array, name):
        with open(f'{data_dir}\{filename}.json', 'w', encoding='utf-8') as f:
            json.dump({"data": {"date": dict(enumerate(date_array)), "x": dict(enumerate(data_array.tolist())), "uniq_id":dict(enumerate(id_array))}
                       , "properties": {"name": name} }
                       , f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))  # https://stackoverflow.com/a/37795053

    np.random.seed(0) 
    
    # сформировать папку data
    if not Path(data_dir).is_dir():
        Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    # вспомогательные данные
    date = np.arange(np.datetime64("2024-01-01"), np.datetime64("2024-04-10"), np.timedelta64(1, "D")).astype(datetime)
    date = list(map(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S.000'),date))
    uniq_id = np.arange(1,101,1).tolist()
    
    # базовый уровень
    base_array = np.full(100, 100)
    
    # дисперсия
    dispersion_low = np.random.rand(100)*10
    dispersion_high = np.random.rand(100)*100
    
    # тренд
    trend_linear = np.append(np.full(49,0), np.linspace(0,100,51)) # np.linspace(0,99,100)
    trend_exponential = np.exp(np.linspace(1,6,100))
    
    # выбросы
    outliers_rare = np.zeros(100)
    # сделать элементы 20? 40, 60, 80 выбросами
    outliers_rare[20] = 10
    outliers_rare[40] = -10
    outliers_rare[60] = 10
    outliers_rare[80] = -10
    
    outliers_frequently = np.zeros(100)
    # сделать каждый 5й элемент выбросом
    for i in range(4,104,5):
        if i % 2 == 0:
            outliers_frequently[i] += 10
        else:
            outliers_frequently[i] -= 10
    
    outliers_close = np.zeros(100)
    # сделать выбросами элементы 10, 11, 12, 49, 51, 73, 76
    indexes_to_change = {10:10, 11:-10, 12:10
                         , 30:10, 31:-10, 32:10, 33:-10
                         , 50:10, 51:10, 53:10, 54:10
                         , 70:10, 71:10, 73:-10, 74:-10}
    for i in indexes_to_change.keys():
        outliers_close[i] += indexes_to_change[i]
    
    # малая дисперсия
    ## нет тренда
    dl_tn_on = base_array + dispersion_low
    save_to_json(data_dir, filename='dl_tn_on', date_array=date, data_array=dl_tn_on, id_array=uniq_id, name='dispersion_low')
    dl_tn_olr = base_array + dispersion_low + outliers_rare
    save_to_json(data_dir, filename='dl_tn_olr', date_array=date, data_array=dl_tn_olr, id_array=uniq_id, name='dispersion_low + outliers_rare')
    dl_tn_olf = base_array + dispersion_low + outliers_frequently
    save_to_json(data_dir, filename='dl_tn_olf', date_array=date, data_array=dl_tn_olf, id_array=uniq_id, name='dispersion_low + outliers_frequently')
    dl_tn_olc = base_array + dispersion_low + outliers_close
    save_to_json(data_dir, filename='dl_tn_olc', date_array=date, data_array=dl_tn_olc, id_array=uniq_id, name='dispersion_low + outliers_close')
    dl_tn_ohr = base_array + dispersion_low + outliers_rare*10
    save_to_json(data_dir, filename='dl_tn_ohr', date_array=date, data_array=dl_tn_ohr, id_array=uniq_id, name='dispersion_low + outliers_rare*10')
    dl_tn_ohf = base_array + dispersion_low + outliers_frequently*10
    save_to_json(data_dir, filename='dl_tn_ohf', date_array=date, data_array=dl_tn_ohf, id_array=uniq_id, name='dispersion_low + outliers_frequently*10')
    dl_tn_ohc = base_array + dispersion_low + outliers_close*10
    save_to_json(data_dir, filename='dl_tn_ohc', date_array=date, data_array=dl_tn_ohc, id_array=uniq_id, name='dispersion_low + outliers_close*10')
    ## линейный тренд
    dl_tl_on = base_array + dispersion_low + trend_linear
    save_to_json(data_dir, filename='dl_tl_on', date_array=date, data_array=dl_tl_on, id_array=uniq_id, name='dispersion_low + trend_linear')
    dl_tl_olr = base_array + dispersion_low + trend_linear + outliers_rare
    save_to_json(data_dir, filename='dl_tl_olr', date_array=date, data_array=dl_tl_olr, id_array=uniq_id, name='dispersion_low + trend_linear + outliers_rare')
    dl_tl_olf = base_array + dispersion_low + trend_linear + outliers_frequently
    save_to_json(data_dir, filename='dl_tl_olf', date_array=date, data_array=dl_tl_olf, id_array=uniq_id, name='dispersion_low + trend_linear + outliers_frequently')
    dl_tl_olc = base_array + dispersion_low + trend_linear + outliers_close
    save_to_json(data_dir, filename='dl_tl_olc', date_array=date, data_array=dl_tl_olc, id_array=uniq_id, name='dispersion_low + trend_linear + outliers_close')
    dl_tl_ohr = base_array + dispersion_low + trend_linear + outliers_rare*10
    save_to_json(data_dir, filename='dl_tl_ohr', date_array=date, data_array=dl_tl_ohr, id_array=uniq_id, name='dispersion_low + trend_linear + outliers_rare*10')
    dl_tl_ohf = base_array + dispersion_low + trend_linear + outliers_frequently*10
    save_to_json(data_dir, filename='dl_tl_ohf', date_array=date, data_array=dl_tl_ohf, id_array=uniq_id, name='dispersion_low + trend_linear + outliers_frequently*10')
    dl_tl_ohc = base_array + dispersion_low + trend_linear + outliers_close*10
    save_to_json(data_dir, filename='dl_tl_ohc', date_array=date, data_array=dl_tl_ohc, id_array=uniq_id, name='dispersion_low + trend_linear + outliers_close*10')
    ## экспоненциальный тренд
    dl_te_on = base_array + dispersion_low + trend_exponential
    save_to_json(data_dir, filename='dl_te_on', date_array=date, data_array=dl_te_on, id_array=uniq_id, name='dispersion_low + trend_exponential')
    dl_te_olr = base_array + dispersion_low + trend_exponential + outliers_rare
    save_to_json(data_dir, filename='dl_te_olr', date_array=date, data_array=dl_te_olr, id_array=uniq_id, name='dispersion_low + trend_exponential + outliers_rare')
    dl_te_olf = base_array + dispersion_low + trend_exponential + outliers_frequently
    save_to_json(data_dir, filename='dl_te_olf', date_array=date, data_array=dl_te_olf, id_array=uniq_id, name='dispersion_low + trend_exponential + outliers_frequently')
    dl_te_olc = base_array + dispersion_low + trend_exponential + outliers_close
    save_to_json(data_dir, filename='dl_te_olc', date_array=date, data_array=dl_te_olc, id_array=uniq_id, name='dispersion_low + trend_exponential + outliers_close')
    dl_te_ohr = base_array + dispersion_low + trend_exponential + outliers_rare*10
    save_to_json(data_dir, filename='dl_te_ohr', date_array=date, data_array=dl_te_ohr, id_array=uniq_id, name='dispersion_low + trend_exponential + outliers_rare*10')
    dl_te_ohf = base_array + dispersion_low + trend_exponential + outliers_frequently*10
    save_to_json(data_dir, filename='dl_te_ohf', date_array=date, data_array=dl_te_ohf, id_array=uniq_id, name='dispersion_low + trend_exponential + outliers_frequently*10')
    dl_te_ohc = base_array + dispersion_low + trend_exponential + outliers_close*10
    save_to_json(data_dir, filename='dl_te_ohc', date_array=date, data_array=dl_te_ohc, id_array=uniq_id, name='dispersion_low + trend_exponential + outliers_close*10')
    
    # большая дисперсия
    ## нет тренда
    dh_tn_on = base_array + dispersion_high
    save_to_json(data_dir, filename='dh_tn_on', date_array=date, data_array=dh_tn_on, id_array=uniq_id, name='dispersion_high')
    dh_tn_olr = base_array + dispersion_high + outliers_rare
    save_to_json(data_dir, filename='dh_tn_olr', date_array=date, data_array=dh_tn_olr, id_array=uniq_id, name='dispersion_high + outliers_rare')
    dh_tn_olf = base_array + dispersion_high + outliers_frequently
    save_to_json(data_dir, filename='dh_tn_olf', date_array=date, data_array=dh_tn_olf, id_array=uniq_id, name='dispersion_high + outliers_frequently')
    dh_tn_olc = base_array + dispersion_high + outliers_close
    save_to_json(data_dir, filename='dh_tn_olc', date_array=date, data_array=dh_tn_olc, id_array=uniq_id, name='dispersion_high + outliers_close')
    dh_tn_ohr = base_array + dispersion_high + outliers_rare*10
    save_to_json(data_dir, filename='dh_tn_ohr', date_array=date, data_array=dh_tn_ohr, id_array=uniq_id, name='dispersion_high + outliers_rare*10')
    dh_tn_ohf = base_array + dispersion_high + outliers_frequently*10
    save_to_json(data_dir, filename='dh_tn_ohf', date_array=date, data_array=dh_tn_ohf, id_array=uniq_id, name='dispersion_high + outliers_frequently*10')
    dh_tn_ohc = base_array + dispersion_high + outliers_close*10
    save_to_json(data_dir, filename='dh_tn_ohc', date_array=date, data_array=dh_tn_ohc, id_array=uniq_id, name='dispersion_high + outliers_close*10')
    ## линейный тренд
    dh_tl_on = base_array + dispersion_high + trend_linear
    save_to_json(data_dir, filename='dh_tl_on', date_array=date, data_array=dh_tl_on, id_array=uniq_id, name='dispersion_high + trend_linear')
    dh_tl_olr = base_array + dispersion_high + trend_linear + outliers_rare
    save_to_json(data_dir, filename='dh_tl_olr', date_array=date, data_array=dh_tl_olr, id_array=uniq_id, name='dispersion_high + trend_linear + outliers_rare')
    dh_tl_olf = base_array + dispersion_high + trend_linear + outliers_frequently
    save_to_json(data_dir, filename='dh_tl_olf', date_array=date, data_array=dh_tl_olf, id_array=uniq_id, name='dispersion_high + trend_linear + outliers_frequently')
    dh_tl_olc = base_array + dispersion_high + trend_linear + outliers_close
    save_to_json(data_dir, filename='dh_tl_olc', date_array=date, data_array=dh_tl_olc, id_array=uniq_id, name='dispersion_high + trend_linear + outliers_close')
    dh_tl_ohr = base_array + dispersion_high + trend_linear + outliers_rare*10
    save_to_json(data_dir, filename='dh_tl_ohr', date_array=date, data_array=dh_tl_ohr, id_array=uniq_id, name='dispersion_high + trend_linear + outliers_rare*10')
    dh_tl_ohf = base_array + dispersion_high + trend_linear + outliers_frequently*10
    save_to_json(data_dir, filename='dh_tl_ohf', date_array=date, data_array=dh_tl_ohf, id_array=uniq_id, name='dispersion_high + trend_linear + outliers_frequently*10')
    dh_tl_ohc = base_array + dispersion_high + trend_linear + outliers_close*10
    save_to_json(data_dir, filename='dh_tl_ohc', date_array=date, data_array=dh_tl_ohc, id_array=uniq_id, name=' dispersion_high + trend_linear + outliers_close*10')
    ## экспоненциальный тренд
    dh_te_on = base_array + dispersion_high + trend_exponential
    save_to_json(data_dir, filename='dh_te_on', date_array=date, data_array=dh_te_on, id_array=uniq_id, name='dispersion_high + trend_exponential')
    dh_te_olr = base_array + dispersion_high + trend_exponential + outliers_rare
    save_to_json(data_dir, filename='dh_te_olr', date_array=date, data_array=dh_te_olr, id_array=uniq_id, name='dispersion_high + trend_exponential + outliers_rare')
    dh_te_olf = base_array + dispersion_high + trend_exponential + outliers_frequently
    save_to_json(data_dir, filename='dh_te_olf', date_array=date, data_array=dh_te_olf, id_array=uniq_id, name='dispersion_high + trend_exponential + outliers_frequently')
    dh_te_olc = base_array + dispersion_high + trend_exponential + outliers_close
    save_to_json(data_dir, filename='dh_te_olc', date_array=date, data_array=dh_te_olc, id_array=uniq_id, name='dispersion_high + trend_exponential + outliers_close')
    dh_te_ohr = base_array + dispersion_high + trend_exponential + outliers_rare*10
    save_to_json(data_dir, filename='dh_te_ohr', date_array=date, data_array=dh_te_ohr, id_array=uniq_id, name='dispersion_high + trend_exponential + outliers_rare*10')
    dh_te_ohf = base_array + dispersion_high + trend_exponential + outliers_frequently*10
    save_to_json(data_dir, filename='dh_te_ohf', date_array=date, data_array=dh_te_ohf, id_array=uniq_id, name='dispersion_high + trend_exponential + outliers_frequently*10')
    dh_te_ohc = base_array + dispersion_high + trend_exponential + outliers_close*10
    save_to_json(data_dir, filename='dh_te_ohc', date_array=date, data_array=dh_te_ohc, id_array=uniq_id, name='dispersion_high + trend_exponential + outliers_close*10')

if __name__ == "__main__":
    generate_test_cases()