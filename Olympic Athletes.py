#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Importing the dataset

athletes = pd.read_csv('C:/Users/Minh Doan/Desktop/Olympic Athlete Analysis/athlete_events.csv')
regions = pd.read_csv('C:/Users/Minh Doan/Desktop/Olympic Athlete Analysis/noc_regions.csv')


# In[3]:


athletes.head()


# In[4]:


regions.head()


# In[5]:


#Combine both of the datasets

athletes_df = athletes.merge(regions, how = 'left', on = 'NOC')
athletes_df.head()


# In[6]:


athletes_df.shape


# In[7]:


#Change column names to consistent

athletes_df.rename(columns={'region':'Region','notes':'Notes'}, inplace= True)


# In[8]:


athletes_df.head()


# In[9]:


athletes_df.info()


# In[10]:


#Checking statistical analysis of Olympics

athletes_df.describe()


# In[11]:


#Checking for null values

nan_values = athletes_df.isna()
nan_columns = nan_values.any()
print(nan_columns)


# In[12]:


athletes_df.isnull().sum()


# In[13]:


#United States details

athletes_df.query('Team == "United States"').head()


# In[14]:


#Japan details

athletes_df.query('Team == "Japan"').head()


# In[15]:


#Top countries with countries participating

top_10_countries = athletes_df.Team.value_counts().sort_values(ascending=False).head(10)
print(top_10_countries)


# In[16]:


#Plotting the top 10 countries

plt.figure(figsize =(16,8))
plt.title('Top 10 Participation by Country')
sns.barplot(x=top_10_countries.index, y=top_10_countries, palette = 'Set3')


# In[17]:


#Age Distibution of participants

plt.figure(figsize=(12,6))
plt.title('Age Distribution of Participants')
plt.xlabel('Age')
plt.ylabel('Number of Participants')
plt.hist(athletes_df.Age, bins = np.arange(10,70,2), color = 'blue', edgecolor = 'white')


# In[18]:


#Unique values of winter Olympic sports

winter_sports = athletes_df[athletes_df.Season == 'Winter'].Sport.unique()
print(winter_sports)


# In[19]:


#Unique values of summer Olympic sports

sinter_sports = athletes_df[athletes_df.Season == 'Summer'].Sport.unique()
print(sinter_sports)


# In[20]:


#Total of male and female participants

gender_counts = athletes_df.Sex.value_counts()
print(gender_counts)


# In[21]:


#Pie plot for male and female participants

plt.figure(figsize=(12,6))
plt.title('Gender Distribution')
plt.pie(gender_counts,labels = gender_counts.index, autopct = '%1.1f%%', startangle = 180, shadow = 'True',)


# In[22]:


#Total amount of medals

athletes_df.Medal.value_counts()


# In[23]:


#Total amount of female participants in each summer Olypmics

female_participants = athletes_df[(athletes_df.Sex == 'F') & (athletes_df.Season == 'Summer')][['Sex', 'Year']]
female_participants = female_participants.groupby('Year').count().reset_index()
female_participants.tail()


# In[24]:


womenOlympics = athletes_df[(athletes_df.Sex == 'F') & (athletes_df.Season == 'Summer')]


# In[25]:


sns.set(style = 'darkgrid')
plt.figure(figsize = (20,10))
sns.countplot(x='Year', data = womenOlympics, palette = 'light:b')
plt.title('Women Participation')


# In[26]:


part = womenOlympics.groupby('Year')['Sex'].value_counts()
plt.figure(figsize = (20,10))
part.loc[:,'F'].plot()
plt.title('Female Participants Over Time')


# In[27]:


#Gold medal athletes

goldmedals = athletes_df[(athletes_df.Medal == 'Gold')]
goldmedals.head()


# In[28]:


#Take the only values that are different from NaN

goldmedals = goldmedals[np.isfinite(goldmedals['Age'])]


# In[29]:


goldmedals['ID'][goldmedals['Age'] > 60].count()


# In[30]:


#Check which sport has the gold medalist above 60 years old

sporting_event = goldmedals['Sport'][goldmedals['Age']>60]
print(sporting_event)


# In[31]:


#Plot for sporting_event

plt.figure(figsize=(12,6))
plt.tight_layout()
sns.countplot(sporting_event)
plt.title('Gold Medals for Participants Over 60 Years')


# In[32]:


#Gold medals from each country

goldmedals.Region.value_counts().reset_index(name = 'Medal').head()


# In[35]:


totalgoldmedals = goldmedals.Region.value_counts().reset_index(name = 'Medal').head(5)
g = sns.catplot(x='index', y= 'Medal', data = totalgoldmedals,
               height = 5, kind = 'bar', palette = 'mako')
g.despine(left = True)
g.set_xlabels('Top 5 Countries')
g.set_ylabels('Number of Medals')
plt.title('Gold Medals per Country')


# In[38]:


#Rio Olympics gold medalist totals

max_year = athletes_df.Year.max()
print(max_year)

team_names = athletes_df[(athletes_df.Year == max_year) & (athletes_df.Medal == 'Gold')].Team

team_names.value_counts().head(10)


# In[39]:


sns.barplot(x= team_names.value_counts().head(20), y = team_names.value_counts().head(20).index)

plt.ylabel('Countries')
plt.xlabel('Medals for Rio Olympics')


# In[42]:


not_null_medals = athletes_df[(athletes_df['Height'].notnull()) & (athletes_df['Weight'].notnull())]


# In[44]:


#Plot weight and height of medalists per male and female

plt.figure(figsize= (20,10))
axis = sns.scatterplot(x = 'Height', y = 'Weight', data = not_null_medals, hue = 'Sex')
plt.title('Height vs Weight of Olypmic Medalist')

