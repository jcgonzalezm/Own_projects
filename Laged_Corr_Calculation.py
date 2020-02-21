#The idea of this is to test a simple, but almost certainly wrong, hypothesis that_
#if we could find a high corr between the movement in t of a stock and the movement in another stock at t-i
#This were we could find a lagged relationship between two stocks.


import pandas as pd
import numpy as np
import pickle
from os import listdir
from os.path import isfile, join


mypath = 'C:/Users/josecg1/.spyder-py3/My scripts/Moving_Average/with pickle/pickles'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

compare_against = 'Pickle_AMZN'

onlyfiles.pop(onlyfiles.index(compare_against))

Stocks_List = onlyfiles
days_lag = 1

corr_l = []
max_corr = []
day_higest_corr = []

for Ticker in Stocks_List:
    
    main_df = pd.DataFrame()
    
    for x in [compare_against,Ticker]:
        pickle_in = open(str(mypath + '/' + str(x)),'rb')
        Prices_df = pickle.load(pickle_in) 

#       TO CALCULATE THE VAR_CHANGE FROM BEGGINING
        main_df[x] = (Prices_df['Adj_Close'] - Prices_df['Adj_Close'][0])/Prices_df['Adj_Close'][0] * 100

#       TO CALCULATE VAR FROM DAY-TO-DAY
        Prices_df['MA_22d'] = np.round(Prices_df['Adj_Close'].rolling(window = 22).mean(),2)
        main_df[x] = Prices_df['MA_22d'].pct_change()

#   Start finding the corr
    corr_l = []
    for i in list(range(30)):
        main_df[main_df.columns[1]] = main_df[main_df.columns[1]].shift(-i)
        Corr_df = main_df.corr() #this is a dataframe
        
        corr_l.append(abs(Corr_df[x][0]))
    
    Result_df = pd.DataFrame({'Corr' : corr_l})
    
    max_corr.append(Result_df['Corr'].max())
    day_higest_corr.append(Result_df[Result_df['Corr'] == Result_df['Corr'].max()].index[0])

# DF to store it
My_df = pd.DataFrame({'Stock' : Stocks_List,
                      'Max_Corr' : max_corr,
                      'Higest_day' : day_higest_corr})

My_df.to_excel('Corr_Matrix.xlsx')