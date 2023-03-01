#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('mamba install bs4==4.10.0 -y')
get_ipython().system('mamba install html5lib==1.1 -y')
get_ipython().system('pip install lxml==4.6.4')
get_ipython().system('pip install yfinance==0.1.67')
get_ipython().system('pip install nbformat==4.2.0')


# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[3]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[4]:


tsla = yf.Ticker("TSLA")


# In[5]:


tsla_data = tsla.history(period="max")


# In[6]:


tsla_data.reset_index(inplace=True)
tsla_data.head()


# In[33]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

html_data = requests.get(url).text


# In[34]:


soup = BeautifulSoup(html_data, 'html5lib')


# In[39]:


tesla_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[41]:


tesla_revenue.dropna(axis=0, how='all', subset=['Revenue']) #drop NaN values
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[42]:


tesla_revenue.tail(5)


# In[43]:


gme = yf.Ticker('GME')


# In[44]:


gme_data = gme.history(period='max')


# In[45]:


gme_data.reset_index(inplace=True)
gme_data.head(5)


# In[46]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text


# In[47]:


soup = BeautifulSoup(html_data, "html5lib")


# In[48]:


gme_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("GameStop Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[49]:


gme_revenue.tail(5)


# In[51]:


tesla = yf.Ticker('TSLA')


# In[52]:


tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)


# In[53]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[54]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




