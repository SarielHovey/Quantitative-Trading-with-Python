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



#     Square-root diffusion (Cox, Ingersoll, Ross)
def Srd(T, M, I, x0, theta, kappa, sigma):
      '''
      Stochastic differential equation for square-root diffusion
      params: x0: initial value
            kappa: mean reversion factor, [0, 1]
            theta: long-term mean value
            sigma: volatility factor
      '''
      x = np.zeros((M+1, I))
      dt = T/M
      x[0] = x0
      for t in range(1, M+1):
            df = 4 * theta * kappa / sigma ** 2
            c = (sigma ** 2 * (1 - np.exp(-kappa * dt))) / (4 * kappa)
            nc = np.exp(-kappa * dt) / c * x[t - 1]
            x[t] = c * np.random.noncentral_chisquare(df, nc, size=I)
      return x



#     Stochastic Volatility Model (Heston(1993))
def Heston(T, M, I, S0, v0, theta, kappa, sigma, rho):
            '''
      Heston's Stochastic volatility model. BSM for price, Srd for volatility
      params: S0: initial value
            v0: initial volatility value
            kappa: mean reversion factor for volatility, [0, 1]
            theta: long-term mean value for volatility
            sigma: volatility factor for volatility
            rho: correlation between Brownian Motions for BSM and Srd
      '''
      corr_mat = np.zeros((2,2))
      corr_mat[0, :] = [1, rho]
      corr_mat[1, :] = [rho, 1]
      cho_mat = np.linalg.cholesky(corr_mat)
      dt = T/M
      ran_num = np.random.standard_normal((2, M+1, I))
      v = np.zeros_like(ran_num[0])
      vh = np.zeros_like(v)
      v[0] = vh[0] = v0
      S = np.zeros_like(ran_num[0])
      S[0] = S0
      for t in range(1, M+1):
            ran = np.dot(cho_mat, ran_num[:, t, :])
            vh[t] = (vh[t-1] + kappa * (theta - np.maximum(vh[t-1], 0)) * dt + sigma * np.sqrt(np.maximum(vh[t-1], 0)) * np.sqrt(dt) * ran[1])
            S[t] = S[t-1] * np.exp(r - 0.5*np.maximum(vh[t], 0) * dt + np.sqrt(np.maximum(vh[t], 0)) * ran[0] * np.sqrt(dt))
      v = np.maximum(vh, 0)
      return {'Price': S, 'Volatility': v}



#     Jump Diffusion (Merton Jump Diffusion Model)



