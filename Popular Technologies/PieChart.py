#!/usr/bin/env python
# coding: utf-8

# In[269]:


#Loading the libraries
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt


# In[270]:


#reading the file
df = pd.read_csv("a3_2021f_coop_tech-1.csv")


# In[278]:


#Replace column with similiar names 
df.replace(to_replace = 'NodeJS', value = 'Nodejs',inplace=True)
df.replace(to_replace = 'AngularJS', value = 'AngularJs',inplace=True)
df.replace(to_replace = 'Javascript', value = 'JavaScript',inplace=True)
df.replace(to_replace = 'TypeScript', value = 'Typescript',inplace=True)
df.replace(to_replace = 'VSCode', value = 'Visual Studio',inplace=True)


# In[283]:


#DataFrame conversion from series
x = pd.DataFrame(df.value_counts())
#Renaming the column
x.rename(columns = {0:'frequency'} , inplace='True')
#New data frame for values which are repeated more than once
newdf = x[x['frequency'] != 1]
newdf = newdf.sort_values(by='frequency')
#Cobining frequency with value 1 into one var
y = ("Other",)
row = pd.Series({'frequency':sum(x['frequency'] == 1)},name=y)
newdf = newdf.append(row)


# In[303]:


#plot figure according to requirements 800 * 600
plt.figure(figsize=(800/96, 600/96), dpi=96)
new_list = newdf.index.tolist()
#labels
res = [item[0] for item in new_list]
#Colors to be used in pie chart
colors = ['tab:blue', 'tab:orange', 'yellow','tab:green', 'teal', 'gold','tab:cyan', 'tab:pink' ,'tab:gray' , 'tab:olive',  ]
k = []
#custom pct function
def my_autopct(pct):
    if pct > 2.5:
        return '{0:1.0f}%'.format(pct) 
for i in range(len(res)-1):
    k.append(0)
k.append(0.05)
#for top slice to come out of the main chart
explode =  tuple(k)
patches, texts, autotexts = plt.pie(newdf['frequency'], labels = res , startangle=150 ,colors=colors,autopct=my_autopct,explode=explode,rotatelabels=True,labeldistance=1.02)
for t in autotexts:
    t.set_fontsize(8)
#Setting alignment and positioning according to the requirements
texts[-1].set_rotation("horizontal")
texts[-1].set_horizontalalignment ("center")
texts[-1].set_verticalalignment("bottom")
autotexts[-1].set_verticalalignment("bottom")
x,y = autotexts[-1].get_position()
#Labels in between a slice
plt.text(x-0.6, y-0.2, "Many Specialized Technologies \n Were Reported Only Once.")
autotexts[-1].set_fontsize(10)
#Plot title
plt.title("Technologies used by COOP in 2021",font='Comic Sans MS',fontsize=27,fontweight=20)
plt.show()

