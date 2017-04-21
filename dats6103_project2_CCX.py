
# coding: utf-8

# # Project 2- Diamonds Analysis
#    Chunxu Chen

# ### Import Libraries

# In[1]:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from sklearn import datasets, linear_model
# from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import stats
import statsmodels.formula.api as smf


# In[2]:

diamonds=pd.read_csv('diamonds.csv')
diamonds=diamonds.drop('Unnamed: 0',1)


# In[4]:

diamonds.head(5)


# ### The dataset has 53940 rows and 10 columns

# In[3]:

diamonds.shape


# ### The three main features of diamond: cut, color and clarity affect the diamond price.
# Here is the level
#     
#     Cut     : Fair < Good < Very Good < Premium < Ideal
#     
#     Color   : D < E < F < G < H < I < J
#     
#     Clarity : I1 < SI2 < SI1 < VS2 < VS1 < VVS2 < VVS1 < IF

# ### Three boxplots shows the price distribution by cut, color and clarity features
# However a surprising relationship between the quality of diamonds and their price: low-quality diamonds (poor cuts, bad colors, and inferior clarity) have higher prices:

# In[5]:

for ele in ['cut','color','clarity']:
    diamonds.boxplot(column='price',by=ele,figsize=(8,5))
#     fig = axes.get_figure()
#     fig.suptitle('Boxplot of price by '+ele)
    plt.suptitle('Boxplot of price by '+ele)
    plt.title('')
    plt.show()


# ### Scatter plot shows the relationship between carat and price. 
# Check if carat affet the price

# In[6]:

diamonds.plot.scatter('carat', 'price',figsize=(10,6))
# plt.figure()
plt.show()


# ### Creat a variable indicates the fitted values from model.

# In[7]:

result = smf.ols('price~carat',diamonds).fit()
diamonds['yhat'] = result.fittedvalues


# In[8]:

plt.scatter(diamonds['carat'],diamonds['price'],color='black')
plt.plot(diamonds['carat'],diamonds['yhat'],color='blue',linewidth=2)
# plt.xticks(())
# plt.yticks(())
plt.ylim(0,20000)
plt.show()


# ### The statistic shows that the carat has significant effect on the price

# In[10]:

x2 = sm.add_constant(diamonds['carat'])
est = sm.OLS(diamonds['price'], x2)
est2 = est.fit()
print(est2.summary())


# ### We calcute the residuals of the model to remove the strong linear pattern between carat and price.

# In[ ]:

diamonds['resid'] = result.resid


# ### Define a function to sort the boxplot by median.

# In[62]:

def boxplot_sorted(df, by, column,col='', rot=0):
    # use dict comprehension to create new dataframe from the iterable groupby object
    # each group name becomes a column in the new dataframe
    df2 = pd.DataFrame({col:vals[column] for col, vals in df.groupby(by)})
    # find and sort the median values in this new dataframe
    # if there is ordered columns given use it
    if col!='':
        meds = [ind for ind,ele in enumerate(['D','E','F','J','H','I','G'])]
        # return axes so changes can be made outside the function
        return df2[meds].boxplot(rot=rot, return_type="axes")
    # else use the default
    else:
        # use the columns in the dataframe, ordered sorted by median value
        meds = df2.median().sort_values()
        return df2[meds.index].boxplot(rot=rot, return_type="axes")


# ### Redo the boxplots, show the distribution of residuals among each levels of three features
# Now we see the relationship we expect: as the quality of the diamond
# increases, so to does its relative price.

# In[67]:

for ele in ['cut','color','clarity']:
#     diamonds.boxplot(column='resid',by=ele,figsize=(8,5))
# #     fig = axes.get_figure()
# #     fig.suptitle('Boxplot of price by '+ele)
#     plt.suptitle('Boxplot of price by '+ele)
#     plt.title('')
    if ele=='color':
        axes=boxplot_sorted(diamonds,by=['color'],column='resid',col=['D','E','F','J','H','I','G'],rot=0)
        axes.set_title("Boxplot of "+ele)
        plt.show()
    else:
        axes = boxplot_sorted(diamonds, by=[ele], column="resid")
        axes.set_title("Boxplot of "+ele)
        plt.show()

