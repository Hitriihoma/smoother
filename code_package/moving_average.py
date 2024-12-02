# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:01:54 2024

@author: 123
"""

import numpy as np
import copy

class MovingAverage():
    def __init__(self, window, direction='both'):
        self.window = window
        self.direction = direction
        
    def _calculate_sma(self, n, insert_list, k):
        '''
        Внтуренний метод расчёта единичного значения для применения к списку
        Посчитать simple moving average - среднее предыдущих k точек данных

        Parameters
        ----------
        n : integer
            Индекс в списке, для которого считаем sma. Начинается с 0.
        insert_list : list
            Список данных.
        k : integer
            окно скользящего срежнего, по скольки точкам считаем среднее.

        Returns
        -------
        float
            Значение simple moving average.

        '''
        if n >= k-1:
            sma_sum = 0
            start_index = n-k
            for offset in range(1,k+1):
                sma_sum += insert_list[start_index+offset]
            return sma_sum / k
        else:
            return None
        
    def _calculate_nextsma(self):
        '''
        https://en.wikipedia.org/wiki/Moving_average
        SMA_k,next = SMA_k,prev + 1/k * (p_n+1 - p_n-k+1)
        This means that the moving average filter can be computed quite cheaply on real time data with a FIFO / circular buffer and only 3 arithmetic steps.
        '''
        
    def _calculate_sma_outlier(self, n, insert_list, k, iqr_coef=1.5):
        '''
        Внтуренний метод расчёта единичного значения для применения к списку
        Посчитать simple moving average - среднее предыдущих k точек данных
        Учитывать, что при расчёте среднего может быть в выборке может быть один выброс. Определять его как точку за границами mean + IQR * IQR_coef

        Parameters
        ----------
        n : integer
            Индекс в списке, для которого считаем sma. Начинается с 0.
        insert_list : list
            Список данных.
        k : integer
            окно скользящего срежнего, по скольки точкам считаем среднее.
        iqr_coef : float
           Коэффициент межквартильного размаха. IQR = Q_0.75 - Q_0.25. The default is 1.5.

        Returns
        -------
        float
            Значение simple moving average.
        '''
        if n >= k-1:
            # сформировать тестовую выборку
            temp_array = np.array(insert_list[n-k+1:n+1])
            # посчитать верхнюю и нижнюю границу
            # на малых выборках iqr_range с большим выбросом сильнос сдвигает противоположную границу и нормальные числа не попадает
            iqr_range = iqr_coef * (np.quantile(temp_array, 0.75) - np.quantile(temp_array, 0.25))
            upper_limit = np.quantile(temp_array, 0.75) + iqr_range
            lower_limit = np.quantile(temp_array, 0.25) - iqr_range
            # проверить количество выбросов за границами
            if len(temp_array[(temp_array > upper_limit) | (temp_array < lower_limit)]) == 1:
                # есть ровно 1 выброс - убираем его
                temp_array = temp_array[(temp_array <= upper_limit) & (temp_array >= lower_limit)]
            return temp_array.mean()
        else:
            return None
        
    
    def transform(self, x, y=None, window=None, drop_outlier=False, iqr_coef=1.5):
        '''
        Передать данные в функцию и обработать их
        можно передавать только x - тогда возвращаем только обработанный x
        можно передавать x и y - тогда возвращаем обработанный x и обрезанный по таким же индексам y

        Parameters
        ----------
        x : list-like
            Данные для обработки.
        window : integer
            Окно скользящего среднего.
        y : list-like, optional
            Данные, связанные с данными для обработки. The default is None.
        drop_outlier : boolean, optional
            Использовать ли убирание одного выброса при расчёте среднего значения подвыборки. The default is False.
        iqr_coef : float, optional
            Коэффициент межквартильного размаха. IQR = Q_0.75 - Q_0.25. The default is 1.5.

        Returns
        -------
        x_res : list-like
            Обработанные данные.
        y_res : list-like
            В случае передачи y вернёт y, в которых элементы заменены на None соотетственно x_res.
        
        Examples
        -------
        data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        window: 5
        return: [None, None, None, None, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        '''
        
        # получение window из аттрубитов класса
        window = self.window if window is None else window
       
        if y is not None:
            # обработка каждой точки <y>
            if drop_outlier:
                y_res = list(map(lambda value: self._calculate_sma_outlier(value, y, window, iqr_coef=iqr_coef), range(len(y))))
            else:
                y_res = list(map(lambda value: self._calculate_sma(value, y, window), range(len(y))))
            x_res = copy.copy(x) # так как далее меняем x
            # для <x> сделать <window-1> первых элементов None, как в <y>
            for temp_index in range(window):
                x_res[temp_index] = None
            return x_res, y_res
        else:                
            # обработка каждой точки списка <x>
            if drop_outlier:
                x_res = list(map(lambda value: self._calculate_sma_outlier(value, x, window, iqr_coef=iqr_coef), range(len(x))))
            else:
                x_res = list(map(lambda value: self._calculate_sma(value, x, window), range(len(x))))
            return x_res
