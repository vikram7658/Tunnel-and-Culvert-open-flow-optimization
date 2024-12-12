# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:25:05 2024

@author: vikra
"""

from scipy.optimize import minimize
import numpy as np
import pandas as pd

class ManningOptimisation:
    def __init__(self, n, s, Q_target, w, h):
        
        self.n = n
        self.s = s
        
        self.Qmin, self.Qmax = Q_target
        self.w = w
        self.h = h
    
    
    def discharge(self, w, h):
        A = w*h
        p = w+2*h
        R = A/p
        
        v = 1/self.n*(R**(2/3))*self.s**0.5
            
        Q = A*v
        return Q
    
    def objective (self, params):
        w, h = params
        Q = self.discharge(w, h)
        return abs(Q-(self.Qmax+self.Qmin)/2)
    
    def optimise (self):
        initial_guess = [(self.w[0]+self.w[1])/2,(self.h[0]+self.h[1])/2]
        bound = [self.w, self.h]
        
        result = minimize(self.objective, initial_guess, bounds=bound)
        
        
        w_opt, h_opt = result.x
        Q_opt = self.discharge(w_opt, h_opt)
        return {'w': w_opt, 'h': h_opt, 'Q': Q_opt}
        
            
#Test the Value 
optimiser = ManningOptimisation(0.015, 1/600, (49,52), (4,6), (2,3))  
optimal_result = optimiser.optimise()  
df = pd.DataFrame([optimal_result])
df['v'] = df.Q/(df.w*df.h)

print (f"The optimum width is {df.w[0]:.3f} m ")
print (f"The optimum height is {df.h[0]:.3f} m ")
print (f"The optimum Discharge is {df.Q[0]:.3f} m3/s ")
print (f"The optimum velocity is {df.v[0]:.3f} m/s ")
    



