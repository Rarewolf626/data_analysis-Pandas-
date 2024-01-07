#!/usr/bin/env python
# coding: utf-8

# In[11]:


# Importing python libraries
from urllib.request import urlretrieve
import os
import pandas as pd
import numpy as np


# In[3]:


pip install matplotlib


# In[5]:


pip install seaborn


# In[1]:


# Importing plotting and visualisation libraries
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)


# In[2]:


# URLs to fetch data
url_const_results = 'https://gist.githubusercontent.com/harikanth-m/f41f068dca8a309c81a04c6a45fecf58/raw/constructor_results.csv'
url_const_standings = 'https://gist.githubusercontent.com/harikanth-m/ccf0bd917f013d34928ae8c9b695059c/raw/constructor_standings.csv'
url_const = 'https://gist.githubusercontent.com/harikanth-m/f128413f4bff5c3c901b9a8c599a78b9/raw/constructors.csv'
url_driver_standings = 'https://gist.githubusercontent.com/harikanth-m/fcdb3e6650972ee6f0db07288074b0b7/raw/driver_standings.csv'
url_drivers = 'https://gist.githubusercontent.com/harikanth-m/d37be6c8c871300822bf8676e2206d9b/raw/drivers.csv'
url_lap_times = 'https://gist.githubusercontent.com/harikanth-m/61770032a57dd013651163142589b2bc/raw/lap_times.csv'
url_pit_stops = 'https://gist.githubusercontent.com/harikanth-m/45d94ae5a8b8e7f0cace662cc7942d04/raw/pit_stops.csv'
url_qualifying = 'https://gist.githubusercontent.com/harikanth-m/08f55f6687874c5a0bf01790c477e4bc/raw/qualifying.csv'
url_races = 'https://gist.githubusercontent.com/harikanth-m/9382cffceb1264e246fae76e4989cc31/raw/races.csv'
url_results = 'https://gist.githubusercontent.com/harikanth-m/6b1b6e36d3709abf3b97fc703303471b/raw/results.csv'
url_status = 'https://gist.githubusercontent.com/harikanth-m/c1bb17485523243929c57f4f13d4fcba/raw/status.csv'
url_schema = 'https://gist.githubusercontent.com/harikanth-m/71f7fd19c8afba09ad99664ece517268/raw/f1db_schema.txt'import os


# In[4]:


import os


# In[5]:


os.makedirs('./data', exist_ok=True)


# In[8]:


os.listdir('data')


# In[9]:


schema = open('./data/f1db_schema.txt', 'r')
print(schema.read())


# In[12]:


races_raw_df = pd.read_csv('data/races.csv')
races_raw_df


# In[13]:


races_raw_df = races_raw_df.sort_values('date')
races_raw_df


# In[19]:


Rces_df = races_raw_df[races_raw_df.date <= '2020-09-27']


# In[24]:


# Assuming you're working with pandas and have a DataFrame named races_df
import pandas as pd

# Code to create or load races_df
# For example:
races_df = races_df = pd.read_csv(r'S:\Projects\F1\races.csv')


# Now you can use races_df in the subsequent cells or code
idx = races_df.groupby(['year'])['date'].transform(max) == races_df['date']
season_finale = races_df[idx].rename(columns={'round': 'tot_races'})
season_finale = season_finale[season_finale.year != 2020]


# In[27]:


import pandas as pd

races_df = races_df = pd.read_csv(r'path to ur data set')

idx = races_df.groupby(['year'])['date'].transform('max') == races_df['date']
season_finale = races_df[idx].rename(columns={'round': 'tot_races'})
season_finale = season_finale[season_finale.year != 2020]


# In[28]:


plt.figure(figsize=(16, 6))

plt.plot(season_finale.year, season_finale.tot_races, 's-b')
plt.xlabel('Year')
plt.ylabel('Number of races')
plt.title("Championship races per seasons");


# In[29]:


circuits_raw_df = pd.read_csv('data/circuits.csv')
circuits_raw_df


# In[31]:


host_circuits = races_df.drop(['date', 'time', 'url', 'round'], axis=1).rename(columns={'name': 'gp_name'}).merge(
    circuits_raw_df.drop(['lat', 'lng', 'alt', 'url'], axis=1).rename(columns={'name': 'cir_name'}), how='left'
)


# In[44]:


host_countries = host_circuits[['raceId', 'year', 'country']].groupby(
    ['year','country']).size().reset_index().rename(columns = {0:'Races'})

plt.figure(figsize = (15,10))

sns.scatterplot(data = host_countries, x = 'year', y = 'country', s = 100, hue = 'Races', palette="deep")
plt.title('F1 host countries')
plt.xlabel('Year')
plt.ylabel('');


# In[45]:


constructors_raw = pd.read_csv('data/constructors.csv')
constructors_raw


# In[46]:


results_raw = pd.read_csv('data/results.csv')
results_raw


# In[47]:


const_inter_df1 = results_raw.groupby(['constructorId', 'raceId']).size()

const_inter_df2 = const_inter_df1.groupby('constructorId').count().reset_index().rename(columns = {0:'races_ent'}) 

const_races_entered = const_inter_df2.merge(constructors_raw, on = 'constructorId')
const_races_entered


# In[49]:


const_races_entered_top = const_races_entered.sort_values('races_ent', ascending=False).head(10)

plt.figure(figsize=(14, 6))

sns.barplot(x='races_ent', y='name', data=const_races_entered_top)
plt.title('Top 10 F1 constructor entries')
plt.xlabel('Number of races entered')
plt.ylabel('')
plt.show()


# In[50]:


const_country = const_races_entered[['constructorId', 'nationality']].groupby(
    'nationality').count().rename(columns = {'constructorId' : 'counts'}) 

const_country = const_country[const_country.counts >= 10].sort_values('counts', ascending = False)
const_country.loc['Others'] = [(len(const_races_entered) - const_country.counts.sum())] 

plt.figure(figsize=(12,6))
explode = np.append(np.zeros(5),0.1)  
plt.axis('equal')

plt.title('Constructor Countries')
plt.pie(const_country.counts, explode=explode, labels=const_country.index, autopct='%1.1f%%',
        shadow=True, startangle=270);


# In[51]:


const_country_num = const_races_entered.nationality.nunique()
print('F1 teams have registered with licenses in {} different countries.'.format(const_country_num))


# In[52]:


results_wins = results_raw[results_raw['position'] == '1']
results_wins


# In[53]:


results_wins[results_wins.duplicated(subset=['raceId'])]


# In[55]:


plt.figure(figsize=(16, 6))

sns.barplot(x='wins', y='name', data=const_win_counts.head(5))
plt.title('Top 5 F1 constructors with most wins')
plt.xlabel('Number of wins')
plt.ylabel('')
plt.show()


# In[57]:


plt.figure(figsize=(16, 5))
sns.barplot(x='name', y='win_percent', data=const_win_percent)
plt.xticks(rotation=90)
plt.title('Constructors with high win percentage')
plt.xlabel('')
plt.ylabel('%')
plt.show()


# In[59]:


plt.figure(figsize=(14, 9))

sns.barplot(x='titles', y='name', data=const_champ_tot)
plt.title('Constructors with World Championship Titles')
plt.xlabel('Number of times crowned')
plt.ylabel('')
plt.show()


# In[60]:


drivers_raw = pd.read_csv('data/drivers.csv')
drivers_raw


# In[61]:


drivers_country = drivers_raw[['driverId', 'nationality']].groupby('nationality').count().rename(
    columns = {'driverId' : 'counts'})

drivers_country = drivers_country[drivers_country.counts > 30].sort_values('counts', ascending = False)
drivers_country.loc['Others'] = [(len(drivers_raw) - drivers_country.counts.sum())]

plt.figure(figsize=(12,6))
explode = np.append(np.zeros(6),0.1) 
plt.axis('equal')

plt.title('Driver Nationalities')
plt.pie(drivers_country.counts, explode=explode, labels=drivers_country.index, autopct='%1.1f%%',
        shadow=True, startangle=270);


# In[62]:


def podium_counter(pos):
    if pos in ['1', '2', '3']:
        return True
    else:
        return False

def win_counter(pos):
    if pos == '1':
        return True
    else:
        return False
    
def pole_counter(grid):
    if grid == 1:
        return True
    else:
        return False


# In[63]:


results_copy = results_raw[['raceId', 'driverId', 'grid', 'position', 'points', 'laps', 'rank']].copy().rename(
    columns = {'rank':'fastlap'})


results_copy['podium'] = results_copy.position.apply(podium_counter)
results_copy['win'] = results_copy.position.apply(win_counter)
results_copy['pole'] = results_copy.grid.apply(pole_counter)
results_copy['fastestLap'] = results_copy.fastlap.apply(win_counter)

driver_stats_1 = results_copy.drop(columns = ['position', 'grid', 'fastlap']).groupby('driverId')
func_dic = {'raceId':'count', 'points':'sum', 'laps':'sum', 'podium':'sum', 'win':'sum', 'pole':'sum', 'fastestLap':'sum'}
driver_stats_1 = driver_stats_1.aggregate(func_dic).reset_index().rename(columns = {'raceId':'races'})


# In[64]:


driver_st_raw = pd.read_csv('data/driver_standings.csv')
driver_st_season_end = season_finale[['raceId', 'year', 'tot_races']].merge(driver_st_raw, on = 'raceId')
driver_champ = driver_st_season_end[driver_st_season_end['position'] == 1]
driver_champ_tot = driver_champ[['driverId', 'position']].groupby('driverId').sum().reset_index().merge(
    drivers_raw[['forename', 'surname', 'driverId']]).rename(
    columns={'position':'titles'}).sort_values('titles', ascending = False)


driver_stats = driver_stats_1.merge(driver_champ_tot[['driverId', 'titles']], how = 'left').fillna(0)
driver_stats = drivers_raw[['driverId', 'forename', 'surname', 'nationality']].merge(driver_stats, on = 'driverId')
driver_stats


# In[65]:


def get_driver_stats():
    try:
        f_n, s_n = input("Enter driver name (as Forename Surname): ").split()
        df = driver_stats.loc[(driver_stats['forename'] == f_n) & (driver_stats['surname'] == s_n)].squeeze()
        return print('''Name: {} {}
Nationality: {}
Stats
Races Entered:\t \t{}
Drivers' Titles:\t{:.0f}
Race Wins:\t \t{}
Pole Positions:\t \t{}
Podiums:\t \t{}
Total Points:\t \t{}
Fastest Laps:\t \t{}
Laps Raced:\t \t{}'''.format(df.forename, df.surname, df.nationality, df.races, df.titles,
          df.win, df.pole, df.podium, df.points, df.fastestLap, df.laps))
    
    except TypeError:
        print('No driver found! Make sure the first letters are capital.')
        
    except ValueError:
        print('Please enter both forename and surname.')


# In[67]:


get_driver_stats()


# In[69]:


get_driver_stats()


# In[72]:


print('The most experienced driver in terms of races entered is {} {} with {} race entries.'.format(
    driver_stats.sort_values('races').tail(1).squeeze().forename, 
    driver_stats.sort_values('races').tail(1).squeeze().surname, 
    driver_stats.sort_values('races').tail(1).squeeze().races))


# In[73]:


print('In terms of laps raced, the most experienced driver is {} {} with {} laps.'.format(
    driver_stats.sort_values('laps').tail(1).squeeze().forename, 
    driver_stats.sort_values('laps').tail(1).squeeze().surname, 
    driver_stats.sort_values('laps').tail(1).squeeze().laps))


# In[74]:


top_drivers = driver_stats[(driver_stats['surname'].isin(['Schumacher', 'Hamilton', 'Prost', 'Senna', 'Fangio']))
            & (driver_stats['forename'].isin(['Michael', 'Lewis', 'Alain', 'Ayrton', 'Juan']))]

top_drivers = top_drivers.drop(['driverId', 'forename', 'nationality', 'points', 'laps', 'fastestLap']
                        , axis = 1).set_index('surname')
top_drivers = top_drivers.rename(columns = 
                                 {'races':'Races', "podium":'Podiums', 'win':'Wins', 'pole':'Poles', 'titles':'Titles'})

# Plotting
sns.set_style('dark')

top_drivers.plot(secondary_y = 'Titles', kind = 'bar', figsize=(14,7), title = 'Comparing driver stats', 
                 xlabel = '', rot = 0, grid = True);


# In[75]:


dri_year_end_st = season_finale[['raceId', 'year']].merge(driver_st_raw)
lewis_year_end_st = dri_year_end_st[dri_year_end_st['driverId'] == 1]

# Plotting
sns.set_style('darkgrid')
plt.figure(figsize=(14, 6))

plt.bar(lewis_year_end_st.year, lewis_year_end_st.wins)
plt.xlabel('Year')
plt.ylabel('Wins')
plt.title("Lewis' year-round wins");


# In[80]:


dri_year_end_st = season_finale[['raceId', 'year']].merge(driver_st_raw)
Schumacher_year_end_st = dri_year_end_st[dri_year_end_st['driverId'] == 1]

# Plotting
sns.set_style('darkgrid')
plt.figure(figsize=(14, 6))

plt.bar(Schumacher_year_end_st.year, Schumacher_year_end_st.wins)
plt.xlabel('Year')
plt.ylabel('Wins')
plt.title("Schumacher' year-round wins");


# In[ ]:




