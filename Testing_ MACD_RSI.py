#The pourpuse of this code is to meaasure the return of a very popular conmbined traiding strategy_
#that invovles using the MACD and the RSI
#the idea was to test them and compare them with a our SPY benchamrk under different buy/sell triggers
#comparing against buying periodically under a calendar schedual and buying on certain conditions.

#One of the most important factors, is that this traiding idea was idealy thought to "being automaticly executed"
#for this, in my personal consideration, was to mantain a low risk prospect, so I was loocking for not quantity of executions_
#but consistency of results.
#So its very important to measure how often the triggers were shoot. 

#Portafolio_Backtester is my own backtester.
import Portafolio_Backtester as MyP
import pandas as pd
import pickle
from os import listdir
from os.path import isfile, join
import numpy as np

Stock_Name_List = []
Profit_List = []
Quantity_of_Movments = []

#------------------------------------------------------------------------------------------------------

MyP.Clean_Portafolio()

#Reach to prices data
mypath = 'C:/Users/josecg1/.spyder-py3/My scripts/Moving_Average/with pickle/SP500_Pickles'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
window_lenght = 7

good_PL = []
total_PL = []
n = 0
for x in onlyfiles:
    n += 1
    
    if n == 50:
        print ('done')
        break
    
    pickle_in = open(str(mypath + '/' + str(x)),'rb')
    Prices_df = pickle.load(pickle_in)
    
#    Calculate MACD_Diff for each period-------------------
    Prices_df['MA_Volume_5'] = np.round(Prices_df['Volume'].rolling(window = 5).mean(),2)                
    exp12 = Prices_df['Adj_Close'].ewm(span = 12, adjust=False).mean()
    exp26 = Prices_df['Adj_Close'].ewm(span = 26, adjust=False).mean()
    MACD = exp12 - exp26
    MACD_Signal = MACD.ewm(span=9, adjust=False).mean()
    
    Higher = []
    for i in list(range(len(MACD))):
        if MACD_Signal[i] > MACD[i]:
            Higher.append("Signal")
        else:
            Higher.append("MACD")

    MACD_Cross = []
    for i in list(range(len(Higher))):
        if Higher[i] != Higher[i -1]:
            if Higher[i-1] == "MACD":
                MACD_Cross.append ("Down")
            else:
                MACD_Cross.append ("Up")
        else:
            MACD_Cross.append ("")
    
    MACD_Diff = MACD - MACD_Signal   
    
#    Calculate RSI for each period----------------------------
    ADL_Diff = Prices_df['Adj_Close'].diff()
    ADL_Diff = ADL_Diff[1:]
    up, down = ADL_Diff.copy(), ADL_Diff.copy()
    
    up[up<0] = 0
    down[down>0] = 0
    
    Prices_df['Change'] = ADL_Diff
    Prices_df['up'] = up
    Prices_df['down'] = abs(down)
    
    roll_up = Prices_df['up'].ewm(span = window_lenght, adjust = False).mean()
    roll_down = Prices_df['down'].ewm(span = window_lenght, adjust = False).mean()
   
    RS = roll_up/roll_down
    RSI = 100 - (100/(1.0 + RS))
    
#   Now I will define my triggers, I preffer to past them as a list, for leater being capable of looking individually
    MySignal = []
    for i in list(range(len(Higher))):
    
        if MACD_Diff[i] < -1 and RSI[i] < 20 and MACD_Signal[i] < 0 :
            MySignal.append("Long")
        else:
            MySignal.append("")            
    
    for i in list(range(len(MySignal))):
        if MySignal[i] == "Long":
            MyP.Buy_Portafolio(x,Prices_df.index[i],Prices_df['Adj_Close'][i],1)
        elif MySignal[i] == "Short":
            MyP.Sell_Portafolio(x,Prices_df.index[i],Prices_df['Adj_Close'][i],1)         

#   Start creating my data base to being analyzed.
    FDM = []
    for i in list(range(len(pd.to_datetime( Prices_df.index.values)))):
        if (pd.to_datetime( Prices_df.index.values).month[i] != pd.to_datetime( Prices_df.index.values).month[i-1]):
            FDM.append ('First')
        else:
            FDM.append ("")
#   for knowing where each parts of my triggers will happend. 
    Prices_df['FDM'] = FDM
    Prices_df['MACD_diff'] = MACD_Diff
    Prices_df['RSI'] = RSI
    Prices_df['Signal'] = MySignal
    
    Buy_Price = []
    Buy_Date = []
    for i in list(range(len(MySignal))):
        if MySignal[i] == "Long" :
            Buy_Price.append (Prices_df['Adj_Close'][i])
            Buy_Date.append(Prices_df.index[i])
    
    Sell_Price = [0] * len(Buy_Price)
    Sell_Date = [0] * len(Buy_Price)
    
#   crate my triggers for selling 
    for buy in list(range(len(Buy_Price))):
        for date in list(range(len(Prices_df.index))):
            if Prices_df.index[date] > Buy_Date[buy]:
                if (Prices_df['Adj_Close'][date] < 0.95 * Buy_Price[buy]) or (Prices_df['Adj_Close'][date] > 1.1 * Buy_Price[buy]):
                    Sell_Price[buy] =  (Prices_df['Adj_Close'][date])
                    Sell_Date[buy]  = (Prices_df.index[date])
                    break
        else:
            continue
        
    for sell in list(range(len(Sell_Price))):
        if Sell_Price[sell] == 0:
            Buy_Price[sell] = 0
    
    Buy_df = pd.DataFrame({'Buy_Price': Buy_Price, 'Buy_Date' : Buy_Date,'Sell_Price': Sell_Price,'Sell_Date': Sell_Date})       

#   Calculate the full profit for this stock.
    Buy_df['Profit'] = Buy_df['Sell_Price'] - Buy_df['Buy_Price']
    
    Stock_Name_List.append(x)
    Profit_List.append(sum(Buy_df['Profit']))
    Quantity_of_Movments.append(Buy_df['Profit'].count())
    
Data_df = pd.DataFrame({'Stock':Stock_Name_List,'Profit':Profit_List,'Quantity':Quantity_of_Movments})
Data_df.to_excel('TEST_4.xlsx')
