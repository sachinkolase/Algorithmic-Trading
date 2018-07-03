
import pandas as pd
import numpy as np
from io import StringIO
import os
import matplotlib.pyplot as plt

data_lic=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\sample.csv",header=0)
data_mother=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\mothersumi.csv",header=0)
data_mrf=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\mrf.csv",header=0)
data_nmdc=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\nmdc.csv",header=0)
data_marico=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\marico.csv",header=0)
data_nhpc=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\nhpc.csv",header=0)
data_oil=pd.read_csv("F:\\MBA\\Case Study FA\\Case Study_algorithmic trading\\oil.csv",header=0)

#pd.concat([MA,data.UpperBB,data.LowerBB],axis=1).plot(figsize=(15,15),grid=True)
#data1=pd.concat([data_lic['Date'],data_mother['Close'],data_mrf['Close'],data_nmdc['Close'],data_marico['Close'],data_nhpc['Close'],data_oil['Close'],axis=1)
data=pd.concat([data_lic.Date,data_lic.Close,data_mother.Close,data_mrf.Close,data_nmdc.Close,data_marico.Close,data_nhpc.Close,data_oil.Close],axis=1)
#rsi
window_length = 14
for i in range(1,8):
    close = data.iloc[:,i]
    delta = close.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = pd.stats.moments.ewma(up, window_length)
    roll_down1 = pd.stats.moments.ewma(down.abs(), window_length)
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))
    data['RSI_'+str(i)]=RSI1
    
#bollinger
for i in range(1,8):
    MA = data.iloc[:,i].rolling(window=20).mean()
    SD = data.iloc[:,i].rolling(window=20).std()
    data['MA'+str(i)]=MA
    data['Upper_'+str(i)] = MA + (2 * SD) 
    data['Lower_'+str(i)] = MA - (2 * SD)

#bollinger graph
bolli_lic=pd.concat([data.iloc[:,1],data.MA1,data.Upper_1,data.Lower_1],axis=1).plot(figsize=(15,7))
bolli_mother=pd.concat([data.iloc[:,2],data.MA2,data.Upper_2,data.Lower_2],axis=1).plot(figsize=(15,7))
bolli_mrf=pd.concat([data.iloc[:,3],data.MA3,data.Upper_3,data.Lower_3],axis=1).plot(figsize=(15,7))
bolli_nmdc=pd.concat([data.iloc[:,4],data.MA4,data.Upper_4,data.Lower_4],axis=1).plot(figsize=(15,7))
bolli_marico=pd.concat([data.iloc[:,5],data.MA5,data.Upper_5,data.Lower_5],axis=1).plot(figsize=(15,7))
bolli_nhpc=pd.concat([data.iloc[:,6],data.MA6,data.Upper_6,data.Lower_6],axis=1).plot(figsize=(15,7))
bolli_oil=pd.concat([data.iloc[:,7],data.MA7,data.Upper_7,data.Lower_7],axis=1).plot(figsize=(15,7))

#rsi graph
rsi_lic=data.RSI_1.plot(figsize=(15,7))
rsi_mother=data.RSI_2.plot(figsize=(15,7))
rsi_mrf=data.RSI_3.plot(figsize=(15,7))
rsi_nmdc=data.RSI_4.plot(figsize=(15,7))
rsi_marico=data.RSI_5.plot(figsize=(15,7))
rsi_nhpc=data.RSI_6.plot(figsize=(15,7))
rsi_oil=data.RSI_7.plot(figsize=(15,7))


#buy-sell by bollinger
Upper_touch= pd.DataFrame(0, index=range(743), columns=range(7))
Upper_touch.columns = ['lic_sell','mother_sell','mrf_sell','nmdc_sell','marico_sell','nhpc_sell','oil_sell']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]>data['Upper_'+str(j)][i]):
            Upper_touch.iloc[i,j]=data.iloc[i,j]

lower_touch= pd.DataFrame(0, index=range(743), columns=range(7))
lower_touch.columns = ['lic_buy','mother_buy','mrf_buy','nmdc_buy','marico_buy','nhpc_buy','oil_buy']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]<data['Lower_'+str(j)][i]):
            lower_touch.iloc[i,j]=data.iloc[i,j]        

#buy-sell by bollinger+rsi
Upper_touch_b= pd.DataFrame(0, index=range(743), columns=range(8))
Upper_touch_b.iloc[:,0]=data['Date']
Upper_touch_b.columns = ['date_sell','lic_sell','mother_sell','mrf_sell','nmdc_sell','marico_sell','nhpc_sell','oil_sell']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]>data['Upper_'+str(j)][i] and data.iloc[i+1,j]<data['Upper_'+str(j)][i+1] and data['RSI_'+str(j)][i]>70):
            Upper_touch_b.iloc[i,j]=data.iloc[i,j]

lower_touch_b= pd.DataFrame(0, index=range(743), columns=range(8))
lower_touch_b.iloc[:,0]=data['Date']
lower_touch_b.columns = ['date_buy','lic_buy','mother_buy','mrf_buy','nmdc_buy','marico_buy','nhpc_buy','oil_buy']
for j in range(1,8):
    for i in range (0,743):
        if(data.iloc[i,j]<data['Lower_'+str(j)][i] and data['RSI_'+str(j)][i]<40):
            lower_touch_b.iloc[i,j]=data.iloc[i,j]



lic=pd.concat([lower_touch_b.date_buy,lower_touch_b.lic_buy,Upper_touch_b.lic_sell],axis=1)
mother=pd.concat([lower_touch_b.date_buy,lower_touch_b.mother_buy,Upper_touch_b.mother_sell],axis=1)
mrf=pd.concat([lower_touch_b.date_buy,lower_touch_b.mrf_buy,Upper_touch_b.mrf_sell],axis=1)
nmdc=pd.concat([lower_touch_b.date_buy,lower_touch_b.nmdc_buy,Upper_touch_b.nmdc_sell],axis=1)
marico=pd.concat([lower_touch_b.date_buy,lower_touch_b.marico_buy,Upper_touch_b.marico_sell],axis=1)
nhpc=pd.concat([lower_touch_b.date_buy,lower_touch_b.nhpc_buy,Upper_touch_b.nhpc_sell],axis=1)
oil=pd.concat([lower_touch_b.date_buy,lower_touch_b.oil_buy,Upper_touch_b.oil_sell],axis=1)

#final datafrae of buy sell
lic=lic[(lic.lic_buy+lic.lic_sell)!=0]
mother=mother[(mother.mother_buy+mother.mother_sell)!=0]
mrf=mrf[(mrf.mrf_buy+mrf.mrf_sell)!=0]
nmdc=nmdc[(nmdc.nmdc_buy+nmdc.nmdc_sell)!=0]
marico=marico[(marico.marico_buy+marico.marico_sell)!=0]
nhpc=nhpc[(nhpc.nhpc_buy+nhpc.nhpc_sell)!=0]
oil=oil[(oil.oil_buy+oil.oil_sell)!=0]
















#trail and error
lic=lic[]
data['RSI'+str(1)]
data.head()
data.iloc[2,1]        
data['Upper_1'][2]        
        
data['Upper_5'][65]
df=pd.DataFrame(1:50,index=range(10),columns=range(5)) 
height = 10
width = 20

df=

#return by only bollinger
boll_udate=[1,2]
boll_ldate=[1,2]
for i in range (1,len(data)):
    if(data['Close'][i]>data['UpperBB'][i]):
        boll_udate.append(data['Date'][i])
for i in range (1,len(data)):
    if(data['Close'][i]<data['LowerBB'][i]):
        boll_ldate.append(data['Date'][i])
del boll_udate[0:2]
del boll_ldate[0:2]

#return by combining both
comb_udate=[1,2]
comb_ldate=[1,2]
for i in range (1,len(data)):
    if(data['rsi'][i]>60 and data['Close'][i]>data['UpperBB'][i]):
        comb_udate.append(i)
for i in range (1,len(data)):
    if(data['rsi'][i]<40 and data['Close'][i]<data['LowerBB'][i]):
        comb_ldate.append(i)
del comb_udate[0:4]
del comb_ldate[0:2]

empty_dict = dict.fromkeys(comb_udate)
for i in range (0,len(comb_udate)):
    for j in range (0,len(comb_ldate)):
        if(comb_ldate[j]<comb_udate[i]):
            empty_dict[comb_udate[i]]=empty_dict[comb_udate[i]],comb_ldate[j]
    for k in range (0,len(comb_ldate)):
        if(comb_ldate[k]<comb_udate[i]):
            comb_ldate[k]=0
    
#lower_rsi=[1,2]
#lower_rdate=[1,2]
#for i in range(1,len(data)):
#    if(data['rsi'][i]<40 and data['rsi'][i+1]>40):
#       lower_rsi.append(data['rsi'][i])
#      lower_rdate.append(data['Date'][i])
    
#upper_rsi=[1,2]
#upper_rdate=[1,2]
#for i in range(1,len(data)):
#    if(data['rsi'][i]>60 and data['rsi'][i+1]<60):
#        upper_rsi.append(data['rsi'][i])
#        upper_rdate.append(data['Date'][i])

#combining rsi and bollinger


                

# Compare graphically
plt.figure()
RSI1.plot()
RSI2.plot()
plt.legend(['RSI via EWMA', 'RSI via SMA'])
plt.show()



#pd.concat([MA,data.UpperBB,data.LowerBB],axis=1).plot(figsize=(15,15),grid=True)
#pd.concat([MA,data.Close,data.UpperBB,data.LowerBB],axis=1).plot(figsize=(15,15),grid=True)
#RSI1.plot()
#data.plot()
#plt.show()
