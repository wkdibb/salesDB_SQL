#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### 12-10-18 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### Dictionaries


# In[2]:
#create two dictionaries

PersonalInfo = {'First Name': 'Roberto', 
               'Last Name' : 'Ramsey',
               'Address' : '322 Mysharona Lane',
               'City' : 'London',
               'Country' : 'United Kingdom',
               'Cell Number' : 5415556972,
               'Patronus' : 'Red Panda'}

WorkInfo = {'Business Address' : '508 Snoopy Blvd',
            'Job Title' : 'Badger Tamer',
            'Employment' : 'FTE',
            'Compensation' : 'Not Applicable'}


# In[3]:

#update and delete functions for dictionaries

PersonalInfo.update({'Height' : '6\'20'})

del WorkInfo['Job Title']

print(PersonalInfo)
print(WorkInfo)


# In[4]:

#concatenate dictionaries, then iterate through to print key:value pairs on
#separate lines

TotalInfo = {}
for x in (PersonalInfo, WorkInfo):
    TotalInfo.update(x)
print(PersonalInfo)
print(WorkInfo)
print(TotalInfo)

for key in TotalInfo:
    print(TotalInfo.items())
    print()


# In[ ]:




