Quantitative Trading With R
=============================

Quantitative Trading with R. For personal reference purpose.

I have a bad memory for codes, thus this one serves as some kind of dictionary.

The contents are made to be as clearly as possible. Basic knowledge with finance as well as R programming is required for usage, otherwize you will get a headache easily. :-)

\textbf(Under Construction, plz neglect below)

A typical order for Quantitative Trading:

1. Data Preparation
-------------------
    This stage involves getting data from sources like Yahoo! Finance(yahoo API & YQL are no longer 
    available), Google and etc.. For building a trading platform, API is a must. Luckily there are 
    dozens of cheap serice to be achieve on the Internet. 

https://github.com/SarielHovey/Quantitative_Trading_With_R/blob/master/Data%20Preparation.r


2. Data Cleaning
-------------------
    After importing data from Step 1, it needs to be modified for the following steps. Issues like Holiday, 
    Merger & Acquisition may cause 'NA' value; Stock Splits and Dividents may require Open, Close, High, Low 
    and Volume to be adjusted; Unadjusted Open and Unadjusted Close must be saved for Order Execution, Account 
    Management, Performance Assessment. 

https://github.com/SarielHovey/Quantitative_Trading_With_R/blob/master/Data%20Cleaning.r

3. Get Portfolio Adjustment via Indicators & Rule Sets
------------------
    Data from Step 2 should be transferred by Indicators into a form that could then be process by Rule Sets, 
    adjusted by Account Parameters. 
    The Ultimate Goal is to get the final Portfolio Adjustment -- which guides you to trade.

    For Indicators, an example:
https://github.com/SarielHovey/Quantitative_Trading_With_R/blob/master/Indicators.r

    For Simulating, an example:
https://github.com/SarielHovey/Quantitative_Trading_With_R/blob/master/Simulating%20Peformance.r

    For process from date to simulating, an example:
https://github.com/SarielHovey/Quantitative_Trading_With_R/blob/master/Example_1%20Data%20to%20Simulating.r


