# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:01:54 2024

@author: 123
"""

import numpy as np

class MovingAverage():
    def __init__(self, window, direction='both'):
        self.window = window
        self.direction = direction
    
    def transform(self, x, y=None):
        '''
        Передать данные в функцию и обработать их
        можно передавать только x - тогда возвращаем только обработанный x
        можно передавать x и y - тогда возвращаем обработанный x и обрезанный по таким же индексам y

        Parameters
        ----------
        x : list-like
            Данные для обработки.
        y : list-like, optional
            Данные, связанные с данными для обработки. The default is None.

        Returns
        -------
        None.

        '''
        
        # обработка x
        # привод типа данных к numpy
        if type(x) != np.ndarray:
            x = np.array(x)
        # обработка каждой точки np.array(list(map(lambda x: func(x), date)))
        
        
        if not y:
            # обработка y
            pass
        
        return x, y