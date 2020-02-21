#MyPortafolio
#Because I wanted to test several traiding strategis, using different triggers and comparisons,
#and I did not found a simple library that help my do it, I created my own.
#It not suppous to be as complex as Quantopian or Backtrader.
#I just thought it would be fun to create it from scratch.

import pandas as pd 

MyPortafolio = pd.DataFrame(columns=["Stock", 'buy_price','buy_quantity','buy_total','sell_price','sell_quantity','sell_total'])
Current_Position = ""

def Buy_Portafolio ( stock_function, date_function, price_function, quantity_function ):
    global MyPortafolio
    global Current_Position
    MyBuy = {"Stock" : stock_function, "DatePurchase" : date_function, "Price_Purchase" : price_function, "Quantity" : quantity_function , "Total_Amount" : price_function * -1 * quantity_function}
    
    if Current_Position != "Long":
        MyPortafolio = MyPortafolio.append(MyBuy, ignore_index = True)
        Current_Position = "Long"
    
def Sell_Portafolio ( stock_function, date_function, price_function, quantity_function ):
    global MyPortafolio
    global Current_Position
    MyBuy = {"Stock" : stock_function, "DatePurchase" : date_function, "Price_Purchase" : price_function, "Quantity" : (quantity_function) , "Total_Amount" : price_function * quantity_function}
    
    if Current_Position != "Short":
        MyPortafolio = MyPortafolio.append(MyBuy, ignore_index = True)
        Current_Position = "Short"
    
def Status_Portafolio (Stock_Name, Date_From, Date_Until):
    if Stock_Name == "":
        Status_Portafolio = MyPortafolio[MyPortafolio["DatePurchase"] >= Date_From][MyPortafolio["DatePurchase"] <= Date_Until]["Total_Amount"].sum()
    else:
        Status_Portafolio = MyPortafolio[MyPortafolio["Stock"] == Stock_Name][MyPortafolio["DatePurchase"] >= Date_From][MyPortafolio["DatePurchase"] <= Date_Until]["Total_Amount"].sum()
    return Status_Portafolio

def Clean_Portafolio ():
    MyPortafolio = pd.DataFrame(columns=["Stock", "DatePurchase", "Price_Purchase", "Quantity", "Total_Amount"])

def First_Day_Month (MyDates):
    FDM = []
    for i in list(range(len(MyDates))):
        if MyDates[i].month != MyDates[i-1].month:
            FDM.append(MyDates[i])
        else:
            FDM.append("")
    return FDM

def Compare_Portafolio():
    MyPortafolio
