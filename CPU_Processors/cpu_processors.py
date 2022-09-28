#!/usr/bin/env python
# coding: utf-8

# In[39]:


#importing the libraries
import pandas as pd
from collections import defaultdict
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


# In[40]:


#input from user 
CPU_GEN = input()
if CPU_GEN not in ['4','5','6','7','8','9','10','11']:
    print("Enter valid values between 4 and 11")
    while CPU_GEN not in ['4','5','6','7','8','9','10','11']:
        print("Enter valid values between 4 and 11")
        CPU_GEN = input()
    
intel_dict = defaultdict(list)
#Reading the text file
with open('a2_cpu_amd_intel.txt') as txtfile:
    data = txtfile.readlines()
for i in data:
    if all(x in i for x in ['@','Intel Core']) and any(x in i for x in ['i3','i5','i7','i9']) and not any(x in i for x in ['#','NA']):
        l = i.split()
        processor  = l[2].split('-')
        intel_dict['model'].append(l[2])
        intel_dict['processor'].append(processor[0])
        #else condition is for the entry in data where the intel core processor is 
        #not in format ix-processornumber/name instead it is ix processornumber/name
        if len(processor) > 1:
            gen_extrt = processor[1]
            clock = l[4]
            cpu_mark = l[6]
            money = l[7]
        else:
            gen_extrt = l[3]
            clock = l[5]
            cpu_mark = l[7]
            money = l[8]
        cpu_mark_number = float(cpu_mark.replace(',',''))
        number_money = [float(i.replace(",", "")) for i in re.findall(r'([\d.,]+)[^\d.,]*', money)]
        intel_dict['money'].append(number_money[0])
        intel_dict['cpu_mark'].append(cpu_mark_number)
        number_gen_extrt = ''.join(re.findall(r'\d+', gen_extrt))
        number_clock = [float(i) for i in re.findall(r'\d+\.\d', clock)]
        intel_dict['clock_speed'].append(number_clock[0])
        if len(number_gen_extrt) >= 5:
            intel_dict['generation'].append(number_gen_extrt[0:2])
        elif len(number_gen_extrt) == 4 or len(number_gen_extrt) == 3:
            intel_dict['generation'].append(number_gen_extrt[0])

df_intel = pd.DataFrame.from_dict(intel_dict)
#filtering data based on the generation entered by user  
df_intel_gen  = df_intel[df_intel['generation'] == CPU_GEN]
#finding top 3 best processor for each processor and generation mentioned by use
df_intel_gen.groupby(['processor']).apply(lambda x: x.sort_values(["cpu_mark"], ascending = False)).reset_index(drop=True)
top_df = df_intel_gen.groupby(['processor']).head(1).reset_index(drop=True)


# In[41]:


#basic layout for subplots
fig, axes = plt.subplots(1, 2,figsize=(11, 4.5))

#scatter plot cpu mark vs clock speed 
sns.scatterplot(ax = axes[0] , data=df_intel, x="clock_speed", y="cpu_mark",
               hue="processor",style="processor", palette=["red","green","orange","royalblue"],
               markers={'i3':'^','i5':'X','i7':'*','i9':"o"},s=60)

axes[0].set_title("Intel single Core performance vs Clock speed",fontsize=10)
axes[0].set_xlabel("Clock speed in GHz")
axes[0].set_ylabel("cpuMark")
axes[0].set_ylim(500,4800)
axes[0].set_xlim(1,4.5)
axes[0].set_yticks(np.arange(500, 4800, 500))
#text for the heading of best gen intel processors
axes[0].text(1.1, 4600, 'Best {0}th Gen Intel Processors'.format(CPU_GEN))
#Arrows and text highlighting the best processor
axes[0].annotate(''.join(top_df.iloc[0:1,0:1].values[0]), xy =(top_df.iloc[0:1,4:5].values[0],top_df.iloc[0:1,3:4].values[0]),
                xytext =(1.1, 4300), 
                arrowprops = dict(arrowstyle="->",linestyle = '-.'))
axes[0].annotate(''.join(top_df.iloc[1:2,0:1].values[0]), xy =(top_df.iloc[1:2,4:5].values[0],top_df.iloc[1:2,3:4].values[0]),
                xytext =(1.1, 4050), 
                arrowprops = dict(arrowstyle="->",linestyle = '-.'))
axes[0].annotate(''.join(top_df.iloc[2:3,0:1].values[0]), xy =(top_df.iloc[2:3,4:5].values[0],top_df.iloc[2:3,3:4].values[0]),
                xytext =(1.1, 3800), 
                arrowprops = dict(arrowstyle="->",linestyle = '-.'))
handles, labels = axes[0].get_legend_handles_labels()
axes[0].legend(handles[::-1], labels[::-1],  loc='lower left')


#scatter plot cpu mark vs Cost
sns.scatterplot(ax = axes[1] , data=df_intel, x="money", y="cpu_mark", 
                hue="processor", style="processor", palette=["red","green","orange","royalblue"],
               markers={'i3':'^','i5':'X','i7':'*','i9':"o"},s=60)
axes[1].set_title("Intel single Core performance vs Cost",fontsize=10)
axes[1].set_xlabel("Price in USD")
axes[1].set_ylabel("cpuMark")
axes[1].set_ylim(500,4800)
axes[1].ticklabel_format(style='plain', axis='both')
axes[1].set_yticks(np.arange(500, 4800, 500))
#Hiding the legend on 2nd graph in subplot as mentioned in assignment
axes[1].legend().set_visible(False)
#Making the price scale as log scale as mentioned
axes[1].set_xscale('log',base=10)
axes[1].xaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
axes[1].set_xticks([25,50,100,250,500,1000,2500])

#text for the heading of best gen intel processors
axes[1].text(25, 4600, 'Best {0}th Gen Intel Processors'.format(CPU_GEN))

#Arrows and text highlighting the best processor
axes[1].annotate(''.join(top_df.iloc[0:1,0:1].values[0]), xy =(top_df.iloc[0:1,2:3].values[0],top_df.iloc[0:1,3:4].values[0]),
                xytext =(25, 4300), 
                arrowprops = dict(arrowstyle="->",linestyle = '-.'))
axes[1].annotate(''.join(top_df.iloc[1:2,0:1].values[0]), xy =(top_df.iloc[1:2,2:3].values[0],top_df.iloc[1:2,3:4].values[0]),
                xytext =(25, 4050), 
                arrowprops = dict(arrowstyle="->",linestyle = '-.'))
axes[1].annotate(''.join(top_df.iloc[2:3,0:1].values[0]), xy =(top_df.iloc[2:3,2:3].values[0],top_df.iloc[2:3,3:4].values[0]),
                xytext =(25, 3800), 
                arrowprops = dict(arrowstyle="->",linestyle = '-.'))
plt.show()

