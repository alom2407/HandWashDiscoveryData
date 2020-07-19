#!/usr/bin/env python
# coding: utf-8

# ## 1. Meet Dr. Ignaz Semmelweis
# <p><img style="float: left;margin:5px 20px 5px 1px" src="https://assets.datacamp.com/production/project_20/img/ignaz_semmelweis_1860.jpeg"></p>
# <!--
# <img style="float: left;margin:5px 20px 5px 1px" src="https://assets.datacamp.com/production/project_20/datasets/ignaz_semmelweis_1860.jpeg">
# -->
# <p>This is Dr. Ignaz Semmelweis, a Hungarian physician born in 1818 and active at the Vienna General Hospital. If Dr. Semmelweis looks troubled it's probably because he's thinking about <em>childbed fever</em>: A deadly disease affecting women that just have given birth. He is thinking about it because in the early 1840s at the Vienna General Hospital as many as 10% of the women giving birth die from it. He is thinking about it because he knows the cause of childbed fever: It's the contaminated hands of the doctors delivering the babies. And they won't listen to him and <em>wash their hands</em>!</p>
# <p>In this notebook, we're going to reanalyze the data that made Semmelweis discover the importance of <em>handwashing</em>. Let's start by looking at the data that made Semmelweis realize that something was wrong with the procedures at Vienna General Hospital.</p>

# In[152]:


# importing modules

import pandas as pd
# Read datasets/yearly_deaths_by_clinic.csv into yearly
yearly = pd.read_csv("datasets/yearly_deaths_by_clinic.csv")

# Print out yearly

print(yearly)


# ## 2. The alarming number of deaths
# <p>The table above shows the number of women giving birth at the two clinics at the Vienna General Hospital for the years 1841 to 1846. You'll notice that giving birth was very dangerous; an <em>alarming</em> number of women died as the result of childbirth, most of them from childbed fever.</p>
# <p>We see this more clearly if we look at the <em>proportion of deaths</em> out of the number of women giving birth. Let's zoom in on the proportion of deaths at Clinic 1.</p>

# In[154]:


# Calculate proportion of deaths per no. births

yearly["proportion_deaths"]=yearly["deaths"]/yearly["births"]
# Extract clinic 1 data into yearly1 and clinic 2 data into yearly2
yearly1 = yearly.loc[yearly["clinic"]=="clinic 1"]
yearly2 = yearly.loc[yearly["clinic"]=="clinic 2"]

# Print out yearly1

print(yearly1)


# ## 3. Death at the clinics
# <p>If we now plot the proportion of deaths at both clinic 1 and clinic 2  we'll see a curious pattern...</p>

# In[156]:


# This makes plots appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
# Plot yearly proportion of deaths at the two clinics


ax=yearly1.plot(x="year",y="proportion_deaths",label="yearly1")
yearly2.plot(x="year",y="proportion_deaths",label="yearly2",ax=ax)
ax.set_ylabel("Proportion_deaths")


# ## 4. The handwashing begins
# <p>Why is the proportion of deaths constantly so much higher in Clinic 1? Semmelweis saw the same pattern and was puzzled and distressed. The only difference between the clinics was that many medical students served at Clinic 1, while mostly midwife students served at Clinic 2. While the midwives only tended to the women giving birth, the medical students also spent time in the autopsy rooms examining corpses. </p>
# <p>Semmelweis started to suspect that something on the corpses, spread from the hands of the medical students, caused childbed fever. So in a desperate attempt to stop the high mortality rates, he decreed: <em>Wash your hands!</em> This was an unorthodox and controversial request, nobody in Vienna knew about bacteria at this point in time. </p>
# <p>Let's load in monthly data from Clinic 1 to see if the handwashing had any effect.</p>

# In[158]:


# Read datasets/monthly_deaths.csv into monthly
monthly = pd.read_csv("datasets/monthly_deaths.csv",parse_dates=["date"])

# Calculate proportion of deaths per no. births

monthly["proportion_deaths"]=(monthly["deaths"]/monthly["births"])
# Print out the first rows in monthly

print(monthly.head(1))


# ## 5. The effect of handwashing
# <p>With the data loaded we can now look at the proportion of deaths over time. In the plot below we haven't marked where obligatory handwashing started, but it reduced the proportion of deaths to such a degree that you should be able to spot it!</p>

# In[160]:


# Plot monthly proportion of deaths

ax=monthly.plot(x="date",y="proportion_deaths",label="monthly")
ax.set_ylabel("Proportion deaths")


# ## 6. The effect of handwashing highlighted
# <p>Starting from the summer of 1847 the proportion of deaths is drastically reduced and, yes, this was when Semmelweis made handwashing obligatory. </p>
# <p>The effect of handwashing is made even more clear if we highlight this in the graph.</p>

# In[162]:


# Date when handwashing was made mandatory
import pandas as pd
handwashing_start = pd.to_datetime('1847-06-01')

# Split monthly into before and after handwashing_start
before_washing = monthly[monthly["date"] < handwashing_start]
after_washing =  monthly[monthly["date"] >= handwashing_start]

# Plot monthly proportion of deaths before and after handwashing

ax=before_washing.plot(x="date",y="proportion_deaths",label="before washing")
after_washing.plot(x="date",y="proportion_deaths",label="after washing", ax=ax)
ax.set_ylabel("Proportion deaths")


# ## 7. More handwashing, fewer deaths?
# <p>Again, the graph shows that handwashing had a huge effect. How much did it reduce the monthly proportion of deaths on average?</p>

# In[173]:


# Difference in mean monthly proportion of deaths due to handwashing
before_proportion = before_washing["proportion_deaths"]
after_proportion = after_washing["proportion_deaths"]
mean_diff = after_proportion.mean() - before_proportu.mean()
mean_diff


# ## 8. A Bootstrap analysis of Semmelweis handwashing data
# <p>It reduced the proportion of deaths by around 8 percentage points! From 10% on average to just 2% (which is still a high number by modern standards). </p>
# <p>To get a feeling for the uncertainty around how much handwashing reduces mortalities we could look at a confidence interval (here calculated using the bootstrap method).</p>

# In[166]:


# A bootstrap analysis of the reduction of deaths due to handwashing
boot_mean_diff = []
for i in range(3000):
    boot_before = before_proportion.sample(frac=1,replace=True)
    boot_after =  after_proportion.sample(frac=1,replace=True)
    boot_mean_diff.append( boot_before.mean()-boot_after.mean() )

# Calculating a 95% confidence interval from boot_mean_diff 
confidence_interval = pd.Series(boot_mean_diff).quantile([0.025,0.975])
confidence_interval


# ## 9. The fate of Dr. Semmelweis
# <p>So handwashing reduced the proportion of deaths by between 6.7 and 10 percentage points, according to a 95% confidence interval. All in all, it would seem that Semmelweis had solid evidence that handwashing was a simple but highly effective procedure that could save many lives.</p>
# <p>The tragedy is that, despite the evidence, Semmelweis' theory — that childbed fever was caused by some "substance" (what we today know as <em>bacteria</em>) from autopsy room corpses — was ridiculed by contemporary scientists. The medical community largely rejected his discovery and in 1849 he was forced to leave the Vienna General Hospital for good.</p>
# <p>One reason for this was that statistics and statistical arguments were uncommon in medical science in the 1800s. Semmelweis only published his data as long tables of raw data, but he didn't show any graphs nor confidence intervals. If he would have had access to the analysis we've just put together he might have been more successful in getting the Viennese doctors to wash their hands.</p>

# In[168]:


# The data Semmelweis collected points to that:
doctors_should_wash_their_hands = False

