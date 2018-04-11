# -*- coding: utf-8 -*-
"""
For this project, you’ll act as a data analyst for the National Park Service. You’ll be helping them 
analyze data on endangered species from several different parks.

The National Parks Service would like you to perform some data analysis on the conservation 
statuses of these species and to investigate if there are any patterns or themes to the types of 
species that become endangered. During this project, you will analyze, clean up, and plot data, 
pose questions and seek to answer them in a meaning way.

@author: jcal1
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

species = pd.read_csv('C:\\Users\\jcal1\\Google Drive\\Coding\\Python\\species_info.csv')
#print(species.head())

#Counts the total number of species in the scientific_names column
species_count = species.scientific_name.count()
#print(species_count)

#Counts total number of entries in the scientific_names column.
species_unique = species.scientific_name.nunique()
#print(species_unique)

#Lists the unique values in the category column.
categories = species.category.unique()
#print(categories)

#Lists the unique values in the conservation_status column.
c_status = species.conservation_status.unique()
#print(c_status)

#Performs a count of species in each conservation status item. #
status_count = species.groupby('conservation_status').scientific_name.nunique().reset_index()
#print(status_count)

#Runs the same code as before, but will add a line to replace null values with "No Intervention"
species.fillna('No Intervention', inplace=True)
status_count = species.groupby('conservation_status').scientific_name.nunique().reset_index()
#print(status_count)

#Creates a new DataFrame called protection_counts, which is sorted by scientific_name.
protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')
#print(protection_counts)

#Renames columns from protection_counts table and keeps the format.    
protection_table = protection_counts.rename(columns={'conservation_status': 'Conservation Status', 'scientific_name': 'Species Count'})
#print(protection_table)

'''
#Creates a bar chart for the new frame.
plt.figure(figsize=(10, 4))
ax = plt.subplot()
ax.set_xticks(range(len(protection_counts)))
#NOTE - adding .values to the end of a column turns the column values into an array.
ax.set_xticklabels(protection_counts.conservation_status.values)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
#Sets the x-values equal to the number of values we have in protection counts - the number of bars our chart will have.
#Sets the y-values/heights of the bars as an array of the different entries in the protection_counts scientific_name column.
plt.bar(range(len(protection_counts)), protection_counts.scientific_name.values)
plt.plot()'''

#Creates a new column in species called is_protected, which is True if conservation_status is not equal to 
#No Intervention, and False otherwise.
species['is_protected'] = species.conservation_status.apply(lambda x: True if x != 'No Intervention' else False)
#print(species)

#Groups by both category and is_protected to count entries in the scientific_name column.
category_counts = species.groupby(['category', 'is_protected'])\
.scientific_name.nunique().reset_index()
#print(category_counts)

#Creates a pivot table from category_counts
category_pivot = category_counts.pivot(
        columns='is_protected',
        index='category',
        values='scientific_name').reset_index()
#print(category_pivot)

#Changes the names of the columns from category, True and false to the names below:
category_pivot.columns = ['category', 'not_protected', 'protected']
#print(category_pivot)

#Creates a new column of category_pivot called percent_protected, which is equal to protected (the number of species that are protected)
#divided by protected plus not_protected (the total number of species) - rounds to two decimals.
category_pivot['percent_protected'] = round(((category_pivot.protected / \
(category_pivot.protected + category_pivot.not_protected)) * 100), 2)
#print(category_pivot)

#Reproduces the category_pivot with new column names.
category_pivot2 = category_pivot.rename(columns={'category': 'Category', 'not_protected': 'Not Protected', 'protected': 'Protected', 'percent_protected': 'Percent Protected'})
#print(category_pivot2)

#Performs a significance test between Mammal and Bird percentage_protected. Begins with a contingency table.

# Contingency table
#       protected  |  not protected
# Mammal     30    |    146
# Bird       75    |    413

from scipy.stats import chi2_contingency

x = [[30, 146], [75, 413]] 

chi2, pvalx, dof, expected = chi2_contingency(x)
#print(pvalx)

#Performs the same, but with Reptile and Mammal:

# Contingency table
#       protected  |  not protected
# Mammal     30    |    146
# Reptile     5    |     73

y = [[30, 146], [5, 73]] 

chi2, pvaly, dof, expected = chi2_contingency(y)
#print(pvaly)

#****************************

observations = pd.read_csv('C:\\Users\\jcal1\\Google Drive\\Coding\\Python\\observations.csv')
#print(observations.head())

#Creates a new column called is_sheep that is True if the string 'Sheep' exists in the row.
species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
#print(species.head())

#Selects the rows of species where is_sheep is True. 
species_sheep = species[species.is_sheep]
#print(species_sheep)

#Selects the rows of species where is_sheep is true and the category is Mammal
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
#print(species_sheep_filtered)

#Finds a common column between species_sheep DataFrame and observations DataFrame and merges
sheep_observations = observations.merge(sheep_species)
#print(sheep_observations)

#Groups the data by sum of observations in each park (park_name)
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()

#Creates a bar chart for obs_by_park.
plt.figure(figsize=(16, 4))
ax = plt.subplot()
ax.set_xticks(range(len(obs_by_park)))
#NOTE - adding .values to the end of a column turns the column values into an array.
ax.set_xticklabels(obs_by_park.park_name.values)
plt.ylabel('Number of Observations')
plt.title('Observations of Sheep per Week')
#Sets the x-values equal to the number of values we have in obs_by_park - the number of bars our chart will have.
#Sets the y-values/heights of the bars as an array of the different entries in the obs_by_park observation column.
plt.bar(range(len(obs_by_park)), obs_by_park.observations.values)
plt.plot()

"""Calculates how many observations are needed for an A/B test that compares the mean instances of foot and mouth disease (15%) against
#a program target reduction of 5%. We need our Baseline, the minimum detectable effect and we have chosen a significance of 90%"""
#Our baseline is 15%
#Our desired significance is 90%
#The minimum detectable effect is 33% of the baseline, as illustrated in the code below.
minimum_detectable_effect = 100 * (5/15)
#print(minimum_detectable_effect)
"""#An online calculator used these values to determine we need a sample of 520 observations."""
sample_size = 520

#Below measures how many weeks, based on the rate of observation, it would take to get enough observations - 520 at each park.
bryce_observation_time = 520/250
yellowstone_observation_time = 520/507
#print(bryce_observation_time, yellowstone_observation_time)

#2.08 weeks at Bryce National Park and 1.03 weeks at Yellowstone National Park
