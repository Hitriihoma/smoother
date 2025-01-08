# -*- coding: utf-8 -*-
"""
Engineering Statistics Handbook
Single Exponential Smoothing
https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc431.htm

Exponential smoothing weights past observations with exponentially decreasing weights to forecast future values
S_i : smoothed observation
y : original observation

This smoothing scheme begins by setting S_2 to y_1, where S_i stands for smoothed observation or EWMA, and y stands for the original observation. 
The subscripts refer to the time periods 1,2...n. For the third period, S_3 = alpha*y_2+(1-alpha)*S_2; and so on. 
There is no S_1; the smoothed series starts with the smoothed version of the second observation.

For any time period t, the smoothed value  S_t is found by computing
S_t = alpha*y_(t-1) + (1-alpha)*S(t-1) # 0 < aplha <= 1 t >= 3
This is the basic equation of exponential smoothing and the constant or parameter alpha is called the smoothing constant.

By substituting for S_(t-2), then for S_(t-3), and so forth, until we reach S_2 (which is just y1), 
it can be shown that the expanding equation can be written as:
S_t = \alpha \sum_{i=1}^{t-2} (1-\alpha)^{i-1} y_{t-i} + (1-\alpha)^{t-2} S_2 \, t \ge 2 \

S = [None, y[0]] # There is no S_1; the smoothed series starts with the smoothed version of the second observation. S_2 = y_1 
for t in range(3,len(y)+2):
    S_t = alpha * sum([(1 - alpha)**(i-1) * y[t-i] for i in range(1,t-2+1)]) + (1 - alpha)**(t-2) * S[1]
    S.append(S_t)
    
# Test from https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc434.htm
# Input
y = [6.4,  5.6,  7.8,  8.8,  11,  11.6,  16.7,  15.3,  21.6,  22.4]
alpha = 0.977
# Test output
S = [None, 6.4, 5.6, 7.8, 8.8, 10.9, 11.6, 16.6, 15.3, 21.5]
# My output because of len(y)+2 and S.pop(0)
[6.4, 5.618399999999999, 7.749823199999999, 8.7758459336, 10.9488444564728, 
 11.585023422498875, 16.582355538717472, 15.329494177390503, 21.45577836607999, 22.378282902419834]
"""

class SES():
    def __init__(self, alpha):
        self.alpha = alpha
        
    def _calculate_ses(self, y, alpha):
        S = [None, y[0]] # There is no S_1; the smoothed series starts with the smoothed version of the second observation. S_2 = y_1    
        for t in range(3,len(y)+2): # add extra element controvedrsal to Engineering Statistics Handbook
            S_t = alpha * sum([(1 - alpha)**(i-1) * y[t-i-1] for i in range(1,t-2+1)]) + (1 - alpha)**(t-2) * S[1]
            S.append(S_t)
        S.pop(0) # Delete S_1 (None)
        
        return S
        
    def transform(self, x, y=None, alpha=None):
        # Get alpha from class attrinute
        alpha = self.alpha if alpha is None else alpha
        if alpha is None or alpha <= 0 or alpha > 1:
            raise ValueError("For parameter alpha must be 0 < alpha <= 1")
        
        if y is not None:
            # Process every point of list <y>
            S = self._calculate_ses(y, alpha)
            return x, S
        else:                
            # Process every point of list <x>
            S = self._calculate_ses(x, alpha)
            return S
