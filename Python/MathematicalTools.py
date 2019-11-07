%load_ext Cython
#     Monte Carlo for BSM Motion (Static Simulation)
%%cython 
import numpy as np 
cdef double MC_eu(double S0, double r, double sigma, double T, int I):
      return S0 * np.mean(np.random.lognormal((r - 0.5 * sigma ** 2) * T, sigma*np.sqrt(T), size=I)) 

result = MC_eu(50, 0.04, 0.3, 1, 500000000)
print(result)
#>52.03952248242908



#     MC for BSM Motion (Dynamic Simualtion)
import numpy as np
I = 10000; M = 50
r = 0.04; sigma = 0.3
dt = I / M
S = np.zeros((M + 1, I))
S[0] = 50
for t in range(1, M + 1):
      S[t] = S[t - 1] * np.exp((r - 0.5* sigma ** 2)*dt + sigma * np.sqrt(dt) * np.random.standard_normal(I))
S[-1]