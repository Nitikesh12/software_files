from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import time
tv=TvDatafeed()
df = tv.get_hist(symbol='BANKNIFTY',exchange='NSE',interval=Interval.in_daily,n_bars=602)

df.sort_index(inplace=True)

df['day'] = df.index.day_name()
a=df.loc[df['day'].isin(["Monday","Tuesday","Wednesday","Thursday","Friday"]),["high","low","day","close","open"] ]
# print(a)
# a.to_csv("full_data.csv",columns=["high","low","day","close","open"])
print(a)
i=0
b=5
l=[]
y=[]
z=[]
av=[]
op=[]

while i<len(a["day"]):
	j=0
	while j<1:

		m= a['high'].iloc[i:b].max()
		n= a['low'].iloc[i:b].min()
		ava=round(a["close"].iloc[i:b].sum()/4,2)
		p=a["open"].iloc[i]
		k=a.index
		
		# for t in k:
		l.append(m)
		y.append(n)
		z.append(k[i])
		av.append(ava)
		# print(t)
		op.append(p)
		
		
		break
	b+=5
	i+=5
# for demo in a.index:
# 	print(demo)
dict=pd.DataFrame({"date":z})
dict1=pd.DataFrame({"5high":l})
dict2=pd.DataFrame({"5low":y})
dict3=pd.DataFrame({"close_ava":av})
dict4=pd.DataFrame({"monday_open":op})
new_df=pd.concat([dict,dict1,dict2,dict3,dict4],axis=1)
new_df['range'] = round(new_df.apply(lambda x: x['5high'] - x['5low'], axis=1),2)
# new_df['4per']=round(new_df.apply(lambda x:x['range']/x['close_ava']*100,axis=1),2)

# # print(new_df)
# new_df['open-4high'] = round(new_df.apply(lambda x: x['4high'] - x['monday_open'], axis=1),2)
# new_df['open-4low'] = round(new_df.apply(lambda x: x['4low'] - x['monday_open'], axis=1),2)
# new_df['open-4high_p']=round(new_df.apply(lambda x:x['open-4high']/x['monday_open']*100,axis=1),2)
# new_df['open-4low_p']=round(new_df.apply(lambda x:x['open-4low']/x['monday_open']*100,axis=1),2)
# new_df['high_rolling4']=round(new_df['open-4high_p'].rolling(4).mean(),2)
# new_df['low_rolling4']=round(new_df['open-4low_p'].rolling(4).mean(),2)
new_df.to_csv("krishan1.csv",columns=["date","5high","5low","range"])
print(new_df)



