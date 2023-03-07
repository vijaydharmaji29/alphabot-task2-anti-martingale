import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import numpy as np 
import pytz
from datetime import datetime, timedelta
import time



print("hi")


mt5.initialize()
timezone = pytz.timezone("Etc/UTC")




symbols = ["BTCUSD","ETHUSD"]
    
TIMEFRAME_CURRENT = mt5.TIMEFRAME_M5
VOLUME = 0.01
DEVIATION = 20
MAGIC = 600


def market_order(symbol, volume, order_type, deviation, magic, stoploss,takeprofit):
    tick = mt5.symbol_info_tick(symbol)
    
    price_dict = {'buy':tick.ask,'sell':tick.bid}
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if order_type == "buy" else mt5.ORDER_TYPE_SELL,
        "price": price_dict[order_type],
        "deviation": deviation,
        "magic": magic,
        "sl": stoploss,  
        "tp": takeprofit,
        "comment":"pyhton market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
        }
    
    order_result = mt5.order_send(request)
    print(order_result)
    
    return order_result

def changesl(ticket,symbol,SL,TP):
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol":symbol,
        "position":ticket,
        "sl": SL,
        "tp":TP,
        }
    result = mt5.order_send(request)
    return result
# close position and kill switch
def close_position(position):

    tick = mt5.symbol_info_tick(position.symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position.ticket,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
        "price": tick.ask if position.type == 1 else tick.bid,  
        "deviation": 20,
        "magic": 100,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result
#smooth range
def smoothrng(x,t,m):
    wper = (t*(2) -1 )
    avrng = ta.ema(abs(x-x.shift(1)),t)
    smoothrng = (ta.ema(avrng ,wper))*m
    return smoothrng
# Range Filter 
def rngfilt(x,r):
    rngfilt = x
    for i in range(1,len(x)):
        if(x[i]>rngfilt[i-1]):
            if((x[i]-r[i])<rngfilt[i-1]):
                rngfilt[i] = rngfilt[i-1]
            else:
                rngfilt[i] = x[i] - r[i]
        else:
            if((x[i]+r[i])>rngfilt[i-1]):
                rngfilt[i] = rngfilt[i-1]
            else:
                rngfilt[i] = x[i]+r[i]
    

    return rngfilt
import math
def checkhl(data_back, data_forward, hl):
    if hl == 'high' or hl == 'High':
        ref = data_back[len(data_back)-1]
        for i in range(len(data_back)-1):
            if ref < data_back[i]:
                return 0
        for i in range(len(data_forward)):
            if ref <= data_forward[i]:
                return 0
        return 1
    if hl == 'low' or hl == 'Low':
        ref = data_back[len(data_back)-1]
        for i in range(len(data_back)-1):
            if ref > data_back[i]:
                return 0
        for i in range(len(data_forward)):
            if ref >= data_forward[i]:
                return 0
        return 1


def pivot(osc, LBL, LBR, highlow):
    left = []
    right = []
    for i in range(len(osc)):
        pivots.append(0.0)
        if i < LBL + 1:
            left.append(osc[i])
        if i > LBL:
            right.append(osc[i])
        if i > LBL + LBR:
            left.append(right[0])
            left.pop(0)
            right.pop(0)
            if checkhl(left, right, highlow):
                pivots[i - LBR] = osc[i - LBR]
    return pivots

def nz(x,y=None):
	if isinstance(x,np.generic):
		return x.fillna(y or 0)
	if x!=x:
		if y is not None:
			return y 
		return 0 
	return x 
pl = pivot(data, lbl, lbr, 'low')
ph = pivot(data, lbl, lbr, 'high')

src = df["close"]
prd = input(int("Enter the period for selection:")) 
channelW = input(float("Enter the channel width:")) 
maxnumsr = int(5)
maxnumpp = input(int("Enter the max_pivot point:")) 
min_strenght = input(int("Enter the min_strenght:")) 
src1 = df["high"] 
src2 = df["low"] 
#ph = pivothigh(src1,prd,prd)
#pl = pivotlow(src1,prd,prd)
prdhighest = df["high"].max(300)
prdlowest = df["low"].min(300)
cwidth = (prdhighest - prdlowest)*ChannelW/100
pivotvals = [] 

if len(ph)!=0 or len(pl)!=0:
	if len(ph) !=0:
		pivotvals.insert(ph,0)
	else:
		if len(pl)!=0:
			pivotvals.insert(pl,0)
	
	if len(pivotvals)>maxnumpp:
		 
		pivotvals.pop(-1) 
def get_sr_vals(ind):
 
  lo = pivotvals[ind]
  hi = lo
  numpp = 0 
  for i in range(len(pivotvals)):
      
      cpp = pivotvals[i]
      if cpp <= lo:
            width = hi-cpp
	
      else:
            wdth = cpp-lo
      if wdth <= cwidth:
          if cpp<=lo:
              lo = cpp
          else:
              lo = lo
          if cpp > lo:
              hi = cpp
          else:
              hi = hi
              numpp +=1
              numpp
		      
  return hi,lo,numpp 
sr_up_level = []
sr_dn_level = []
sr_strength = []
def find_loc(strength):
	ret = len(sr_strength)
	for i in range(1,len(sr_up_level)):
		if strength <= sr_strength[i]:
			break
		ret = i 
	return ret 
def check_sr(hi,lo,strength):
	ret = True 
	for i in range(len(sr_up_level)):
		if ((sr_up_level[i] >=lo and sr_up_level[i] <= hi) or (sr_dn_level[i]>=lo and sr_dn_level[i]<=hi)):
			if strength >= strength[i]:
				sr_strength.pop[i]
				sr_strength.pop[i]
				sr_strength.pop[I]
				ret
			else:
				
				ret = false
				ret 
			break
	return ret

sr_lines = []
sr_labels = []
if len(ph)!=0 or len(pl)!=0:
	#because of new calculation , remove old S/R levels
	sr_up_level.clear()
	sr_dn_level.clear()
	sr_strenght.clear()
	#find S/R zones 
	for i in range(pivotvals):
		hi,lo,strenght = get_sr_values(x)
		if check_sr(hi,lo,strenght):
			loc = find_loc(strenght)
			#if strength is in first maxnumsr sr then insert it to the arrays 
			if loc < maxnumsr and strenght >= min_strenght:
				sr_strenght.insert(strenght,loc)
				sr_up_level.insert(hi, loc)
				sr_dn_level.insert(lo,loc)
			# keep size of the array = 5 
			if len(sr_strenght)>maxnumsr:
				sr_strenght.pop(-1)
				sr_strenght.pop(-1)
				sr_strenght.pop(-1)
	for i in range(1,10):
		sr_lines.pop(i)
		sr_labels.pop(i)
				
				
			
	for i in range(len(sr_up_level)):
		mid =  math.round((sr_up_level[i]+sr_dn_level[i]),2)
		rate = 100 * (mid-close)/close
		sr_lables.insert[mid,i]
		sr_lines.insert[mid,i]
				
def f_crossed_over():
	ret = False 
	for x in range(len(sr_levels)):
		mid = math.round(((sr_up_level[i] + sr_dn_level[I])/2),2)
		if close.iloc[i-1] <= mid and close.iloc[i] > mid :
			
			ret = True
			ret 
	return ret 
def f_crossed_under():
	ret = False
    
	for x in range(len(sr_levels)):
         mid = math.round(((sr_up_level[i] + sr_dn_level[i])/2),2)
         if close.iloc[i-1] >= mid and close.iloc[i] < mid:
             ret = True
             ret 
         return ret
    

length = input(int("Enter the length:")) 
MaxRiskPerReward = input(int("Enter the Value:"))
zigzagvalues = []
zigzagvaluesindex = []
zigzagdir = []

doubleTopBottomValues = []
doubleTopBottomValues = []
doubleTopBottomDir = []

max_array_size = int(10)
max_bars_back=df["high"].iloc[-1000:]
max_bars_back=df["low"].iloc[-1000:]

lineArray = []
labelArray = []

def pivot(df,lenght):

	for i in range(df[-lenght:]):
		if df["high"].iloc[i]<=df["high"].iloc[i-1]:
			ph = "NAN"
		else:
		    ph = df["high"].iloc[i]
		
			
	for i in range (df[-lenght:]):
         if df["low"].iloc[i]>=df["low"].iloc[i-1]:
             pl = "NAN"
         else:
             ph = df["low"].iloc[i]
		
		
	dir = 0 
	if pl!="NAN" and ph=="NAN":
		iff_1 == -1
	else:
		iff_1 = dir
	if ph!="NAN" and pl=="NAN":
		dir == 1 
	else:
		dir = iff_1 	
	

	return dir+ph+pl 
def add_to_array(value ,index, dir):
	if len(zigzagvalues)<2:
		mult = 1
	elif dir*value > dir * zigzagvalues[1]:
			mult = 2
	else:
		mult = 1
	zigzagindexes=zigzagindexes.insert(0,index)
	zigzagvalues=zigzagvalues.insert(0,value)
	zigzagdir=zigzagdir.insert(0,dir*mult)
	if len(zigzagindexes)>max_array_size:
		zigzagindexes = zigzagindexes.pop(-1)
		zigzagvalues = zigzagvalues.pop(-1)
		zigzagdir = zigzagdir.pop(-1)
def add_to_zigzag(dir,dirchanged,ph,pl,index):
	if dir == 1:
		value = ph
	else:
		value = pl 
	if len(zigzagvalues) == 0 or len(zigzagvalues) == dirchanged:
		add_to_array(value, index,dir)
	else:
		if (dir == 1 and value > zigzagvalues[0]) or ((dir==-1)and(value<zigzagvalue[0])):
			zigzagvalue = zigzagvalue.pop(0)
			zigzagindexes = zigzagindexes.pop(0)
			zigzagdir = zigzagdir.pop(0)
			add_to_array(value,index,dir)
def zigzag(df,length):
	dir,ph,pl = pivots(df,lenght)
	if dir ==1:
		dirchanged ==-1
	else:
		if dir ==-1:
			dirchanged == 1
	
	if len(ph)!=0 or len(pl)!=0 :
		
			add_to_zigzag(dir,dirchanged,ph,pl,df.iloc[-i])
def calculate_double_pattern(zigzagindexes):
	doubleTop = False 
	doubleTopConfirmation = 0 
	doubleBottom = False
	doubleBottomConfirmation = 0 
	if len(zigzagvalues)>=4:
		index = zigzagindexes[1]
		value = zigzagvalues[1]
		highLow = zigzagdir[1]
		
		lindex = zigzagindexes[2]
		lvalue = zigzagvalues[2]
		lhighLow = zigzagdir[2]
		
		llindex = zigzagindexes[3]
		llvalue = zigzagvalues[3]
		llhighLow = zigzagdir[3]

		risk = abs(value-llvalue)
		reward = abs(value-lvalue)
		riskPerReward = risk*100/(risk+reward)

		if highLow ==1 and llhighLow ==2 and lhighLow < 0 and (riskPerReward < MaxRiskPerReward):
			doubleTop = True
			doubleTop
		if highlow ==-1 and llhighLow ==-2 and lhighLow >0 and (riskPerReward < MaxRiskPerReward):
                     doubleBottom == True
                     doubleBottom 
		if doubleTop=="TRUE" or doubleBottom=="TRUE":
			doubleTopBottomValue[0] = value
			doubleTopBottomValue[1] = lvalue
			doubleTopBottomValue[2] = llvalue
			
			doubleTopBottomIndexes[0] = index
			doubleTopBottomIndexes[1] = lindex
			doubleTopBottomIndexes[2] = llindex
			
			doubleTopBottomDir[0] = highLow
			doubleTopBottomDir[1] = lhighLow
			doubleTopBottomDir[2] = llhighLow
		return doubleTop+doubleBottom

def get_crossover_info(df,doubleTop,doubleBottom):
		index = doubleTopBottomIndexes[0]
		value = doubleTopBottomValues[0]
		highLow = doubleTopBottomDir[0]
		
		lindex = doubleTopBottomIndexes[1]
		lvalue = doubleTopBottomValues[1]
		lhighLow = doubleTopBottomDir[1]
		
		llindex = doubleTopBottomIndexes[2]
		llvalue = doubleTopBottomValues[2]
		llhighLow = doubleTopBottomDir[2]

		latestDoubleTop = False
		lastestDoubleBottom = False
		if doubleTop == True and doubleBottom == False:
			latestDoubleTop = latestDoubleTop[1] 
		
			  
		if doubleBottom == True and doubleTop == False:
			latestDoubleBottom = latestDoubleBottom[1]
		
		doubleTopConfirmation = 0 
		doubleBottomConfirmation = 0
		if latestdoubleTop == True:
			if df["low"].iloc[-1] < lvalue.iloc[-1]:
				DoubleTopConfirmation = 1
			elif df["high"].iloc[-1] > llvalue.iloc[-1]:
					DoubleTopConfirmation = -1
			else:
					DoubleTopConfirmation = 0 

		else:
			DoubleTopConfirmation = 0 
		if latestdoubleBottom == True:
			if low.iloc[-1] < lvalue.iloc[-1]:
				DoubleBottomConfirmation = 1
			elif high.iloc[-1] > llvalue.iloc[-1]:
				DoubleBottomConfirmation = -1
			else:
                
				DoubleBottomConfirmation = 0 

		else:
			DoubleBottomConfirmation = 0 
			
 
		

		return doubleTopConfirmation+doubleBottomConfirmation
def draw_double_pattern(doubleTop, doubleBottom, doubleTopConfirmation, doubleBottomConfirmation):
    index = doubleTopBottomIndex[0]
    value = doubleTopBottomValues[0]
    highLow = doubleTopBottomDir[0]

    lindex = doubleTopBottomIndexesiloc[1]
    lvalue = doubleTopBottomValues.iloc[1]
    lhighLow = doubleTopBottomDir.iloc[1]

    llindex = doubleTopBottomIndexes[2]
    llvalue = doubleTopBottomValues[2]
    llhighLow = doubleTopBottomDir[2]
    isBullish = True
    if(doubleTop=="TRUE" or doubleBottom=="TRUE"):
        isBullish = doubleTop 
    else:
        isBullish = isBullish[1]

    risk = math.abs(value - llvalue)
    reward = math.abs(value - lvalue)
    riskPerReward = risk * 100 / (risk + reward)
    base = ll
    valuel1 = lvalue 
    l2 = llvalue
    baseLabel =  value
    if  doubleTop==  True or doubleBottom==True:
        base.clear()
        l1.clear()
        l2.clear()
        baseLabel.clear()
    doubleTopCount = 0 
    doubleBottomCount = 0 	
    if doubleTop == True:
       doubleTopCount = nz(doubleTopCount[1], 0) + 1
    else:
       doubleTopCount = nz(doubleTopCount[1], 0)
    if doubleBottom == True:
       doubleBottomCount = nz(doubleBottomCount[1], 0) + 1
    else:
        doubleBottomCount=nz(doubleBottomCount[1], 0)
    if base["date"] == base["date"].iloc[-1]:
        base[1].clear()
        l1.clear()
        l2.clear()
        baseLabel.clear()
        if doubleTop == True:
            doubleTopCount = doubleTopCount -1 
        else:
            doubleTopCount = doubleTopCount
        if doubleBottom ==True:
           doubleBottomCount == doubleBottomCount - 1
        else:
            doubleBottomCount = doubleBottomCount
            doubleBottomCount
    lres = lvalue 
    lsup = llvalue 
    lsup

    if doubletopConfirmation >0:
        doubleTopConfirmationCount = 1 
    else:
        doubleTopConfirmationCount = 0 
    if doubleBottomConfirmation >0:
       doubleBottomConfirmationCount = 1
    else:
       doubleBottomConfirmationCount = 0 
			 
    if doubleTopConfirmation < 0 :
       doubleTopInvalidationCount = 1 
    else:
       doubleTopInvalidationCount = 0 
    if doubleBottomConfirmation < 0:
       doubleBottomInvalidationCount = 1 
    else:
       doubleBottomInvalidationCount = 0 
	
    if doubleTopConfirmation != 0 or doubleBottomConfirmation != 0:
        if doubleTopConfirmation > 0 or doubleBottomConfirmation > 0:
            lresbreak = lvalue
            if lresbreak[1] == lresbreak:
                doubleTopConfirmationCount = 0
                doubleBottomConfirmationCount = 0
                doubleTopInvalidationCount = 0
                doubleBottomInvalidationCount = 0
                lresbreak.clear()
                lresbreak = lresbreak[1]
                lresbreak
        elif doubleTopConfirmation < 0 or doubleBottomConfirmation < 0:
             lsupbreak = llvalue 
        if lsupbreak[1] == lsupbreak:
                doubleTopInvalidationCount = 0
                doubleBottomInvalidationCount = 0
                doubleTopConfirmationCount = 0
                doubleBottomConfirmationCount = 0
                lsupbreak.clear()
                lsupbreak = lsupbreak[1]
                lsupbreak
	
    doubleTopConfirmationCount = nz(doubleTopConfirmationCount[1], 0) + doubleTopConfirmationCount
    doubleBottomConfirmationCount = nz(doubleBottomConfirmationCount[1], 0) + doubleBottomConfirmationCount
    doubleTopInvalidationCount = nz(doubleTopInvalidationCount[1], 0) + doubleTopInvalidationCount
    doubleBottomInvalidationCount = nz(doubleBottomInvalidationCount[1], 0) + doubleBottomInvalidationCount
    return doubleTopCount+doubleBottomCount+doubleTopConfirmationCount+doubleBottomConfirmationCount+doubleTopInvalidationCount+doubleBottomInvalidationCount

def get_signal(symbol):
    utc_from = (datetime.now() - timedelta(40))
    utc_to = datetime.today()
    bars=  pd.DataFrame(mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M5,utc_from ,utc_to ))
    bars['time']=pd.to_datetime(bars['time'], unit='s')
    bars = bars.set_index(bars['time'])
    smrng = smoothrng(bars["close"],16,3)
    filt = rngfilt(bars["close"],smrng) 
    bars["filt"] = filt
    bars["upward"] = (len(bars))*0
    bars["downward"]= 0*(len(bars))
    for i in range(1,len(bars["close"])):
        if (filt[i]>filt[i-1]):
            bars["upward"][i] = bars["upward"][i-1]+1
        else:
            if (filt[i]<filt[i-1]):
                bars["upward"][i] = 0
            else:
                bars["upward"][i] = bars["upward"][i-1]
    for i in range(1,len(bars["close"])):
        if (filt[i]<filt[i-1]):
            bars["downward"][i] = bars["downward"][i-1]+1
        else:
            if (filt[i]>filt[i-1]):
                bars["downward"][i] = 0
            else:
                bars["downward"][i] = bars["downward"][i-1]
    # Target Band 
    bars["hband"] = filt+smrng
    bars["lband"] = filt-smrng
    atr(bars)
    zigzag(df,lenght)

    #douleTop,doubleBottom  = calculate_double_pattern()
    #doubleTopConfirmation,doubleBottomConfirmation = get_crossover_info(doubleTop,doubleBottom)
    #doubleTopCount, doubleBottomCount, doubleTopConfirmationCount, doubleBottomConfirmationCount, doubleTopInvalidationCount, doubleBottomInvalidationCount = draw_double_pattern(doubleTop, doubleBottom, doubleTopConfirmation, doubleBottomConfirmation)
    if (len(zigzagindexes)>1):
        lastHigh = 0.0
        lastLow = 0.0
        for i in range(len(zigzagindexes)):
            i = len(zigzagindexes)-1-i
            index = zigzagindexes[i]
            value = zigzagvalues[i]
            highLow = zigzagdir[i]
            index_offset = df.last_valid_index()-index 
     
    

            if (highLow==2):
                labelText == "HH"
            elif (highLow==1):
                labelText == "LH"
            elif highLow ==-1:
                labelText = "HL"
            else:
                labelText = "LL"
    			  
            labelLocation = df["close"].iloc[-1]
            if showPivots==True:
                 l = df["close"].iloc[-1]
                 labelArray.insert(l,0)
            if (len(labelArray))>100:
                 labelarray.clear()
            if i < len(zigzagindexes)-1 and showzigzag==False:
                 indexLast = zigzagindexes[i+1]
                 valueLast = zigzagvalues[i+1]
                 l = valuelast
                            
                            
                            
                 lineArray.insert(l,0)
                 if len(lineArray)>100:
                       lineArray.clear()
    if (((bars["close"].iloc[-1]>filt.iloc[-1])and (bars["close"].iloc[-1]>bars["close"].iloc[-2])and( bars["upward"].iloc[-1]>0) and (bars["spread"].iloc[-1]<=bars["spread"].min()))and((labelText!="HH"))and(labelText!="LH")): #or ((bars["close"][i]>filt[i])and (bars["close"][i]<bars["close"][i-1])and (bars["upward"][i]>0) )):
        a =["BUY"]
        
       
        
            
    elif (((bars["close"].iloc[-1]<filt.iloc[-1])and (bars["close"].iloc[-1]<bars["close"][-2])and (bars["downward"].iloc[-1]>0)and (bars["spread"].iloc[-1]<=bars["spread"].min()))and((labelText!="LL"))and(labelText!="HL")):# or ((bars["close"][i]<filt[i])and (bars["close"]>bars["close"][i-1])and (bars["downward"][i]>0) )):
             a =["SELL"]
             
    else:
             a =[None]
    if ((bars["close"].iloc[-1]<filt.iloc[-1])or( bars["upward"].iloc[-1]<0)or(labelText=="HH")or(labelText=="LH")):
        b = ["SELL"]
    elif ((bars["close"].iloc[-1]>filt.iloc[-1])or( bars["downward"].iloc[-1]<0)or(labelText=="LL")or(labelTex=="HL")): 
        b = ["BUY"]
    else:
        b = [None]
    sl = [None]
    tp = [None]
    return a+b+sl+tp
#Trading loop
i = 0 

while i <=10 :
    
    
        #Strategy Logic
        #if((datetime.now().second == 1)&((datetime.now().minute % 1 == 0))):
            
            for symbol in symbols:
                b = 10
                print(symbol)
                signal,exit1,sl,tp = get_signal(symbol)
                print(symbol,signal,exit1)
              
                point=mt5.symbol_info(symbol).point
                
                a = len(mt5.positions_get(symbol = symbol))
                if(a!=0):
                    for i in range(a):
                        b = mt5.positions_get(symbol =symbol)[i].magic
                        if(b==600):
                            break
                if(b!=600):
                    tick = mt5.symbol_info(symbol)
                    if (signal == "BUY"):
                        market_order(symbol, VOLUME,'buy',DEVIATION,MAGIC,sl,tp)
                       
                        
                    if (signal == "SELL"):
                        market_order(symbol, VOLUME,'sell',DEVIATION,MAGIC,sl,tp)
                try:
                    
                    for i in range(a):
                        if(mt5.positions_get(symbol =symbol)[i].magic==600):
                            pos = mt5.postions_get(symbol =symbol)[i].type
                            if((pos==0)&(exit1 =="SELL")):
                                mt5.Close(symbol)
                                
                                
                            elif((pos==1)&(exit1 == "BUY")):
                                mt5.Close(symbol)
                                
                except:
                    pass
                       
                

