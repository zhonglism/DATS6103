import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

military=pd.read_excel('military.xlsx',sheetname='Data')

print(military.head())
print(military.tail())

def long(df,value_name):
    return pd.melt(df, 
           id_vars=['Country Name'], 
           value_vars=[2011, 2012,2013,2014,2015], 
           var_name='year', 
           value_name=value_name)

military_expenditure_percentage=military[0:19]
gdp=military[19:38]
population=military[38:57]

military_expenditure_percentage_long=long(military_expenditure_percentage,
                                         'Military expenditure (% of GDP)')
#military_expenditure_percentage_long

gdp_long=long(gdp,value_name='GDP')
#gdp_long

population_long=long(population,'population')
#population_long

print(population.tail(5))
print(population_long.tail(5))

left=pd.merge(military_expenditure_percentage_long,
         gdp_long,
         on=['Country Name','year'])

result=pd.merge(left,population_long,
               on=['Country Name','year'])


result.tail(5)

result['Military expenditure']=result['Military expenditure (% of GDP)']/100*result['GDP']

result['Military expenditure per person']=result['Military expenditure']/result['population']

result['GDP per person']=result['GDP']/result['population']

result = result.sort(['Military expenditure', 'GDP'], ascending=[0, 0])

map1={511:2011,512:2012,513:2013,514:2014,515:2015}
fig=plt.figure(figsize=(10,20))
for key,value in map1.items():
    ax=fig.add_subplot(key)
    ax1 = ax.twinx() # Create another axes that shares the same x-axis as ax.
    width = 0.4

    results=result[result['year']==value]
    results['GDP'].plot(kind='bar', color='blue', ax=ax1, width=width, position=0)
    results['Military expenditure'].plot(kind='bar', color='red', ax=ax, width=width, position=1)
    
    ax.set_ylabel('Military expenditure',color='red')
    ax1.set_ylabel('GDP',color='blue')
    
    x=results['Country Name']
    y_pos = np.arange(len(x))
    plt.xticks(y_pos, x)
    plt.title('year '+str(value))
plt.show()


sum(result[result['year']==2011]['Military expenditure'])

for i in range(2011,2016):
    print(sum(result[result['year']==i]['Military expenditure']))

result_copy=result

for i in range(2011,2016):
    result_copy.loc[result_copy['year']==i,'total']=sum(result_copy[result_copy['year']==i]['Military expenditure'])

result_copy['percentage']=result_copy['Military expenditure']/result_copy['total']*100


result_copy.tail(5)

fig=plt.figure(figsize=(10,20))
for key,value in map1.items():
    ax=fig.add_subplot(key)
    
    width=.6
    
    results1=result_copy[result_copy['year']==value]
    results1['percentage'].plot(kind='bar', color='yellow', ax=ax, width=width, position=.5)
    
    ax.set_ylabel('percentage %')
    
    x=results1['Country Name']
    y_pos = np.arange(len(x))
    if value==2015:
        plt.xticks(y_pos, x)
    else:
        ax.set_xticklabels([])
    plt.title('year '+str(value))
plt.show()

fig=plt.figure(figsize=(10,20))
for key,value in map1.items():
    ax=fig.add_subplot(key)
    ax1 = ax.twinx() # Create another axes that shares the same x-axis as ax.
    width = 0.4

    results2=result_copy[result_copy['year']==value]
    results2['GDP per person'].plot(kind='bar', color='blue', ax=ax1, width=width, position=0)
    results2['Military expenditure per person'].plot(kind='bar', color='red', ax=ax, width=width, position=1)
    
    ax.set_ylabel('Military expenditure per person',color='red')
    ax1.set_ylabel('GDP per person',color='blue')
    
    x=results2['Country Name']
    y_pos = np.arange(len(x))
    plt.xticks(y_pos, x)
    plt.title('year '+str(value))
plt.show()


military_expenditure=result_copy[['Country Name','year','Military expenditure']]
wide=military_expenditure.pivot(index='Country Name', columns='year', values='Military expenditure')

print(wide.iloc[:,0:6].diff(axis=1).head(5))

wide=wide.iloc[:,0:6].diff(axis=1)
increament_long=pd.melt(wide, 
       id_vars=['Country Name'], 
       value_vars=[2012,2013,2014,2015], 
       var_name='year', 
       value_name='increament')
increament_long['Country Name']=military_expenditure['Country Name']


increament_long_groupby_country=increament_long.groupby(increament_long['Country Name'])
increament_long_groupby_country.mean().sort('increament',ascending=0).head(5)

plt.figure(figsize=(12,8))
for coun in increament_long[increament_long['year']==2015]['Country Name']:
    plt.plot([2012,2013,2014,2015],
         increament_long[increament_long['Country Name']==coun]['increament'],
         '-o',label=coun)
    plt.xticks(np.arange(2012,2016, 1.0))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
plt.show()

wide_percentage=military_expenditure.pivot(index='Country Name', columns='year', values='Military expenditure')
# print(wide_percentage)
wide_percentage_2011_2014=wide_percentage.iloc[:,0:4]
wide_percentage_2012_2015=wide_percentage.iloc[:,1:5]
wide_percentage_2011_2014.columns=[2012,2013,2014,2015]
# print(wide_percentage_2011_2014)
# print(wide_percentage_2012_2015)
wide_increase_ratio=(wide_percentage_2012_2015-wide_percentage_2011_2014)/wide_percentage_2011_2014*100
wide_increase_ratio

increase_ratio_long=pd.melt(wide_increase_ratio, 
       id_vars=['Country Name'], 
       value_vars=[2012,2013,2014,2015], 
       var_name='year', 
       value_name='increase_ratio')
increase_ratio_long['Country Name']=military_expenditure['Country Name']
#increase_ratio_long


increase_ratio_long_groupby_ratio=increase_ratio_long.groupby(increase_ratio_long['Country Name'])
increase_ratio_long_groupby_ratio.mean().sort('increase_ratio',ascending=0).head(5)

plt.figure(figsize=(12,8))
for coun in increase_ratio_long[increase_ratio_long['year']==2015]['Country Name']:
    plt.plot([2012,2013,2014,2015],
         increase_ratio_long[increase_ratio_long['Country Name']==coun]['increase_ratio'],
         '-o',label=coun)
    plt.xticks(np.arange(2012,2016, 1.0))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
plt.show()