import datetime
import numpy as np
import pandas as pd
import quandl

AUTH_TOKEN = 'Your_AUTH_Here'

def futures_rollover_weights(start_date, expiry_dates, contracts, rollover_days=5): 
    """
    This constructs a pandas DataFrame that contains weights (between 0.0 and 1.0) of contract positions to hold in order to carry out a rollover of rollover_days prior to the expiration of the earliest contract. The matrix can then be 'multiplied' with another DataFrame containing the settle prices of each contract in order to produce a continuous time series futures contract."""
    # Construct a sequence of dates beginning from the earliest contract start
    # date to the end date of the final contract
    dates = pd.date_range(start_date, expiry_dates[-1], freq='B')
    # Create the ’roll weights’ DataFrame that will store the multipliers for
    # each contract (between 0.0 and 1.0)
    roll_weights = pd.DataFrame(np.zeros((len(dates), len(contracts))), index=dates, columns=contracts)
    prev_date = roll_weights.index[0]
    # Loop through each contract and create the specific weightings for
    # each contract depending upon the settlement date and rollover_days
    for i, (item, ex_date) in enumerate(expiry_dates.iteritems()): 
        if i < len(expiry_dates) - 1: 
            roll_weights.loc[prev_date:ex_date - pd.offsets.BDay(), item] = 1 
            roll_rng = pd.date_range(end=ex_date - pd.offsets.BDay(), periods=rollover_days + 1, freq='B')
            # Create a sequence of roll weights (i.e. [0.0,0.2,...,0.8,1.0]
            # and use these to adjust the weightings of each future
            decay_weights = np.linspace(0, 1, rollover_days + 1)
            roll_weights.loc[roll_rng, item] = 1 - decay_weights
            roll_weights.loc[roll_rng, expiry_dates.index[i+1]] = decay_weights
        else: 
            roll_weights.loc[prev_date:, item] = 1
        prev_date = ex_date
    return roll_weights

if __name__ == "__main__":
    # Download the current Front and Back (near and far) futures contracts
    # for WTI Crude, traded on NYMEX, from Quandl.com. You will need to
    # adjust the contracts to reflect your current near/far contracts
    # depending upon the point at which you read this!
    cme_near = quandl.get("CHRIS/CME_CL1", authtoken=AUTH_TOKEN)
    cme_far = quandl.get("CHRIS/CME_CL2", authtoken=AUTH_TOKEN)
    cme = pd.DataFrame({'CL1': cme_near['Settle'], 'CL2': cme_far['Settle']}, index=cme_far.index)
    # Create the dictionary of expiry dates for each contract
    expiry_dates = pd.Series({'CL1': datetime.datetime(2020, 1, 21), 'CL2': datetime.datetime(2020, 2, 11)}).sort_values()
    # Obtain the rollover weighting matrix/DataFrame
    weights = futures_rollover_weights(cme_near.index[0], expiry_dates, cme.columns)
    """
    Typical weights before and after
        Date,CL1,CL2
        2020-01-10,1,0
        2020-01-13,1,0
        2020-01-14,0.8,0.2
        2020-01-15,0.6,0.4
        2020-01-16,0.4,0.6
        2020-01-17,0.2,0.8
        2020-01-20,0,1
        2020-01-21,0,1
    """
    # Construct the continuous future of the WTI CL contracts
    cme_cts = (cme * weights).sum(axis=1).dropna()
    # Output the merged series of contract settle prices
    print(cme_cts.tail(60))

    
