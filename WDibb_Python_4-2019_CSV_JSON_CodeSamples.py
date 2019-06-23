#!/usr/bin/env python
# coding: utf-8

# In[2]:


#### 4-2019 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### CSV, JSON, Shelve, Pickle

import csv
import io
import sys
import pickle
import shelve
import json

#1. Create a csv data file containing 10-20 rows and 6-8 columns containing built-in Py data types, 
#i.e. integers, floats, strings, bytes.
        #.Use the csv module to load this data into the memory of a Py program by assigning each record field to a specific data container (list) that one could access later.
        #.Use both the reader () / writer () and DictReader () / DictWriter () methods.


# In[3]:


#Write CSV file with writer()

with open('patient_cbc_lists.csv', mode = 'w', newline = '') as cbc_lists_csv:

    writer = csv.writer(cbc_lists_csv, delimiter = ',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
    
    writer.writerow([114982772, 75, 'M', True, 3.72, 12.5, 210])
    writer.writerow([114982376, 42, 'F', True, .03, 10.1, 88])
    writer.writerow([114982028, 19, 'F', True, 10.22, 15.0, 59])
    writer.writerow([117984362, 66, 'F', True, 1.1, 9.1, 116])
    writer.writerow([113624889, 34, 'M', True, 3.87, 12.1, 412])
    writer.writerow([117892345, 28, 'F', True, 1.98, 13.9, 186])
    writer.writerow([118998222, 68, 'M', True, 7.80, 11.9, 114])
    writer.writerow([118776925, 60, 'F', True, 3.65, 14.1, 97])
    writer.writerow([118793478, 55, 'F', True, 0.93, 12.5, 145])
    writer.writerow([117923611, 117, 'M', True, 2.53, 6.66, 205])
    


# In[4]:


#Read CSV file with reader()

with open('patient_cbc_lists.csv', mode = 'r') as cbc_lists_csv:
    
    csv_reader = csv.reader(cbc_lists_csv, delimiter = ',')
    list_series = []
    for row in csv_reader:
        #create list for each row
        list_series.append(row)
        print('  '.join(row))


# In[5]:


#Write CSV file with DictWriter()
with open('patient_cbc_dicts.csv', mode = 'w', newline = '') as cbc_dicts_csv:

    fieldnames = ['MRN', 'Age', 'Sex', 'CBC', 'WBC', 'HGB', 'PLT']
    dict_writer = csv.DictWriter(cbc_dicts_csv, delimiter = ',', fieldnames = fieldnames)
    
    dict_writer.writeheader()
    dict_writer.writerow({'MRN': 114982772, 'Age': 75, 'Sex': 'M', 'CBC' : True, 'WBC' : 3.72, 'HGB' : 12.5, 'PLT' : 301})
    dict_writer.writerow({'MRN': 114982376, 'Age': 42, 'Sex': 'F', 'CBC' : False, 'WBC' : None, 'HGB' : None, 'PLT' : None})
    dict_writer.writerow({'MRN': 114982028, 'Age': 19, 'Sex': 'F', 'CBC' : True, 'WBC' : 1.11, 'HGB' : 14.4, 'PLT' : 77})
    dict_writer.writerow({'MRN': 114982736, 'Age': 66, 'Sex': 'F', 'CBC' : True, 'WBC' : 0.02, 'HGB' : 4.0, 'PLT' : 115})
    dict_writer.writerow({'MRN': 114679465, 'Age': 70, 'Sex': 'M', 'CBC' : True, 'WBC' : 1.62, 'HGB' : 12.8, 'PLT' : 261})
    dict_writer.writerow({'MRN': 114258978, 'Age': 32, 'Sex': 'M', 'CBC' : True, 'WBC' : 1.27, 'HGB' : 12.6, 'PLT' : 98})
    dict_writer.writerow({'MRN': 117582891, 'Age': 63, 'Sex': 'F', 'CBC' : True, 'WBC' : 3.2, 'HGB' : 11.1, 'PLT' : 108})
    dict_writer.writerow({'MRN': 118943784, 'Age': 34, 'Sex': 'M', 'CBC' : True, 'WBC' : 1.30, 'HGB' : 10.5, 'PLT' : 192})
    dict_writer.writerow({'MRN': 118374122, 'Age': 72, 'Sex': 'M', 'CBC' : True, 'WBC' : 2.74, 'HGB' : 12.8, 'PLT' : 134})
    dict_writer.writerow({'MRN': 114679469, 'Age': 55, 'Sex': 'F', 'CBC' : True, 'WBC' : 1.0, 'HGB' : 9.5, 'PLT' : 115})


# In[7]:


#Read CSV file with DictReader()

with open('patient_cbc_dicts.csv', mode = 'r') as patient_cbc_csv:
    #DictReader()
    dict_series = []
    csv_reader = csv.DictReader(patient_cbc_csv, delimiter = ',')
    for row in csv_reader:
        dict_series.append(row)
        print(row)

print('')
print('Patient 1: ', dict_series[0])


# In[8]:


#2. Serialize the data from the data containers into a pickle file using the pickle module.
        #.Do it for both the basic types data as well as for the dictionaries obtained from using the DictReader () method.
        #.Unpickle the recorded files to retrieve the initial data.

#pickle lists serialization
with open('pt_cbc_lists.pickle', 'wb') as pkl_output:
    pickle.dump(list_series, pkl_output, pickle.HIGHEST_PROTOCOL)
    
#retrieve lists from serialized pickle file
with open('pt_cbc_lists.pickle', 'rb') as pkl_input:
    pt_list_input = pickle.load(pkl_input)
    for row in pt_list_input:
        print(row)


# In[9]:


#pickle dicts serialization
with open('pt_cbc_dicts.pickle', 'wb') as pkl_output:
    pickle.dump(dict_series, pkl_output, pickle.HIGHEST_PROTOCOL)
    
#retrieve dicts from serialized pickle file
with open('pt_cbc_dicts.pickle', 'rb') as pkl_input:
    pt_dict_input = pickle.load(pkl_input)
    for row in pt_dict_input:
        print('\nPatient Entry: \n')
        print(row)
        


# In[10]:


#Can also assign patient Keys to each dictionary (or list) using shelve:

with shelve.open('shelf_cbc.db', 'c') as shelf:
    shelf['Pt1'] = dict_series[0]
    shelf['Pt2'] = dict_series[1]
    shelf['Pt3'] = dict_series[2]
    shelf['Pt4'] = dict_series[3]
    shelf['Pt5'] = dict_series[4]
    shelf['Pt6'] = dict_series[5]
    shelf['Pt7'] = dict_series[6]
    shelf['Pt8'] = dict_series[7]
    shelf['Pt9'] = dict_series[8]
    shelf['Pt10'] = dict_series[9]

with shelve.open('shelf_cbc.db', 'r') as shelf:
    for key in shelf.keys():
        print(repr(key), 'Data: ', repr(shelf[key]), '\n')


# In[26]:


#3. Serialize the data from the data containers using the json module.
        #.Persist the JSON encoded data to a file on disk.
        #.Do it for both the basic types data as well as for the dictionaries obtained from using the DictReader () method.
        #.Save the same data using sorting.

#Persisted list data dump to disk

#Unsorted:
with open('cbc_lists_unsort.json', 'w') as cbc_json_lists:
    json.dump(list_series, cbc_json_lists)
    
#Load lists
with open('cbc_lists_unsort.json', 'r') as cbc_json_lists:
    json_lists = json.load(cbc_json_lists)
    print('JSON Unsorted Lists: ', json_lists, '\n') 
    
#Sorted:
with open('cbc_lists_sort.json', 'w') as cbc_json_lists:
    json.dump(list_series, cbc_json_lists, sort_keys = True)

#Load lists 
with open('cbc_lists_sort.json', 'r') as cbc_json_lists:
    json_lists = json.load(cbc_json_lists)
    print('JSON Sorted Lists: ', json_lists) 
    


# In[25]:


#Persisted dict data dump to disk

#Unsorted:
with open('cbc_dicts_unsort.json', 'w') as cbc_json_dicts:
    json.dump(dict_series, cbc_json_dicts)

    
with open('cbc_dicts_unsort.json', 'r') as cbc_json_dicts:
    json_dicts_sort = json.load(cbc_json_dicts)
    print('JSON Unsorted Dicts:\n')
    for row in json_dicts_sort:
        print(row)   

print('\n')

#Sorted:
with open('cbc_dicts_sort.json', 'w') as cbc_json_dicts:
    json.dump(dict_series, cbc_json_dicts, sort_keys=True)

    
with open('cbc_dicts_sort.json', 'r') as cbc_json_dicts:
    json_dicts_sort = json.load(cbc_json_dicts)
    print('JSON Sorted Dicts:\n')
    for row in json_dicts_sort:
        print(row)    


# In[ ]:




