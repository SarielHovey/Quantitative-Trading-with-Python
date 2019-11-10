%load_ext Cython
import numpy as np
def gen_sn(M, I, anti_paths = False, mo_match = True):
        '''
        Generate Standard Normal random numbers for simulation, to standardize mean and volatility
        From "Python for Finance"
        '''
        if anti_paths == True and mo_match == False:
                sn = np.random.standard_normal((M+1, int(I/2)))
                sn = np.concatenate((sn, -sn), axis=1)
        elif anti_paths == False and mo_match == True:
                sn = np.random.standard_normal((M+1, I))
                sn = (sn - sn.mean()) / sn.std()
        else:
                print('Either anti_paths or mo_match should be True, not both!')


def op_eu_mcs(M, I, T, S0, K, r, sigma, option='C'):
        '''
        Monte Carlo Simulation for European Option based on standard BSM
        '''
        dt = T/M
        S = np.zeros((M+1, I))
        S[0] = S0
        sn = gen_sn(M, I)
        for t in range(1, M+1):
                S[t] = S[t-1] * np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*sn[t])
        if option == 'C':
                hT = np.maximum(S[-1]-K, 0)
                return np.exp(-r * T) * np.mean(hT)
        elif option == 'P':
                hT = np.maximum(K-S[-1], 0)
                return np.exp(-r * T) * np.mean(hT)
        else:
                print("Error: option should be 'C' or 'P'. ")
                return 'Error!'

        