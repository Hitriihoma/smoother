# -*- coding: utf-8 -*-
"""
Engineering Statistics Handbook
Double Exponential Smoothing
https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc433.htm

Single Smoothing does not excel in following the data when there is a trend. 
This situation can be improved by the introduction of a second equation with a second constant, gamma, which must be chosen in conjunction with alpha.
S[t] = alpha * y[t] + (1 - alpha) * (S[t-1] + b[t-1]) # 0 <= alpha <= 1
b[t] = gamma * (S[t] - S[t-1]) + (1 - gamma) * b[t-1] # 0 <= gamma <= 1
# Note that the current value of the series is used to calculate its smoothed value replacement in double exponential smoothing

# Meaning of the smoothing equations
The first smoothing equation adjusts S_t directly for the trend of the previous period, b_(t-1), by adding it to the last smoothed value, S_(t-1). 
This helps to eliminate the lag and brings S_t to the appropriate base of the current value.
The second smoothing equation then updates the trend, which is expressed as the difference between the last two values. 
The equation is similar to the basic form of single smoothing, but here applied to the updating of the trend.

# Non-linear optimization techniques can be used
The values for alpha and gamma can be obtained via non-linear optimization techniques, such as the Marquardt Algorithm.

# Test from https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc434.htm
# Input
y = [6.4,  5.6,  7.8,  8.8,  11,  11.6,  16.7,  15.3,  21.6,  22.4]
alpha = 0.3623
gamma = 1.0
S[0] = y[0] = 6.5
b[0] = 1/3 * ((y[1]-y[0]) + (y[2]-y[1]) + (y[3]-y[2]))
# Test output
S = [6.4, 6.6, 7.2, 8.1, 9.8, 11.5, 14.5, 16.7, 19.9, 22.8]
# My output
S= [6.4, 6.6203199999999995, 7.188216127999999, 8.134312785651199, 9.77587710199394, 
    11.4835823924733, 14.462494155418913, 16.665574554141056, 19.85822126344086, 22.815058506216722]
"""

class DES():
    def __init__(self, alpha, gamma):
        self.alpha = alpha
        self.gamma = gamma
        
    def _calculate_des(self, y, alpha, gamma, type_b=2):
        # Set initial values for S[t] and b[t] in double smoothing
        # S_1 is in general set to y_1. Here are three suggestions for b_1
        S = [y[0]]
        b = [None]
        match type_b:
            case 1:
                # Difference between second and first elements of y
                b[0] = y[1] - y[0]
            case 2:
                # Pair difference 2 & 1, 3 & 2, 4 & 3 elements of y
                b[0] = 1/3 * ((y[1]-y[0]) + (y[2]-y[1]) + (y[3]-y[2]))
            case 3:
                # Difference between n-th and first elements of y
                n = 10 # some number
                b[0] = (y[n] - y[0]) / (n-1)
            case _:
                # If no template coincided
                raise ValueError("type_b not correct. Must be one of 1, 2, 3")

        for t in range(1,len(y)): # form 2nd element (index 0 1)
            S_t = alpha * y[t] + (1 - alpha) * (S[t-1] + b[t-1]) # 0 <= alpha <= 1
            S.append(S_t)
            b_t = gamma * (S[t] - S[t-1]) + (1 - gamma) * b[t-1] # 0 <= gamma <= 1
            b.append(b_t)
            
        return S
        
    def transform(self, x, y=None, alpha=None, gamma=None):
        # Get alpha and gamme from class attrinute
        alpha = self.alpha if alpha is None else alpha
        if alpha is None or alpha < 0 or alpha > 1:
            raise ValueError("For parameter alpha must be 0 <= alpha <= 1")
        gamma = self.gamma if gamma is None else gamma
        if gamma is None or gamma < 0 or gamma > 1:
            raise ValueError("For parameter gamma must be 0 <= gamma <= 1")
        
        if y is not None:
            # Process every point of list <y>
            S = self._calculate_des(y, alpha, gamma)
            return x, S
        else:                
            # Process every point of list <x>
            S = self._calculate_des(x, alpha, gamma)
            return S
