import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# In[21]:


df = pd.read_csv('gs://stockcsv/oneminstock.csv')
df.head()


# In[22]:


Ticker = list(set(df.Ticker))
len(Ticker)


# In[23]:


Ticker[:30]


# In[24]:


# selecting YHOO stocks
df = df[df['Ticker']=='ICICIBANK.NSE']

# preparing input features
df = df.drop(['Ticker'], axis=1)


# In[25]:


df


# In[26]:


X = df[['Open', 'High', 'Low', 'Volume']].values
y = df['Close'].values


# In[27]:


import xgboost

# XGboost algorithm
xgb = xgboost.XGBRegressor(objective ='reg:squarederror')


# In[28]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y)
xgb.fit(X_train,y_train)


# In[29]:


from sklearn.metrics import explained_variance_score

predictions = xgb.predict(X_test)
print(explained_variance_score(predictions,y_test))


# In[30]:


# from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer

# Preprocessing data
my_imputer = SimpleImputer()
X_train = my_imputer.fit_transform(X_train)
X_test = my_imputer.transform(X_test)


# In[31]:


from xgboost import XGBRegressor

model = XGBRegressor(objective ='reg:squarederror')
# Add silent=True to avoid printing out updates with each cycle
model.fit(X_train, y_train, verbose=True)


# In[32]:


# make predictions
predictions = model.predict(X_test)

from sklearn.metrics import mean_absolute_error
print("Mean Absolute Error : " + str(mean_absolute_error(predictions, y_test)))


# In[33]:


plt.plot(predictions,color = 'blue', label='Predicted')
plt.plot(y_test,color = 'red', label='Ground Truth')
plt.legend()
plt.show()
