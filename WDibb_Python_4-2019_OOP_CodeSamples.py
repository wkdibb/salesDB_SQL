#!/usr/bin/env python
# coding: utf-8

# In[25]:


#### 4-2019 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### OOP class/subclasses showing inheritance, polymorphism

#1. Briefly describe the design of a class which can be used to represent a concept that is relevant to 
#your work or research/clinical interest.

#In a clinical setting, patients are uniquely identified using a subset of personal identifiers. 
#In clinical research, there are additional data captured
#For oncology patients, certain disease-specific metrics are captured

#One way to use OOP to capture this information could be:
#Class Patient():
#Subclass Research(Patient):
#Subclass Cancer(Patient):

#Where the Research and Cancer classes inherit attributes from the parent Patient class, and a patient 
#who is on a research trial for leukemia study intervention would be polymorphic to Research and Oncology subclass methods
    
    


# In[95]:


#2. Write a simple implementation of this class, specifically:
        #. the __init__() “constructor” method with as many parameters as you may need
        #. getter and setters methods for modifying the values of the attributes
        #. other methods and attributes that describe the properties and behavior of your Class/concept

import os
import io

#name class
class Patient(object):
    #set any universal class attribute variables
    subjectType = 'Human'
    site = 'University of Chicago'
    #contructor method for any instantiation, setting self and any attribute inputs as parameters
    def __init__(self, MRN, age, sex, dz, pcp, inpatient):
        self.MRN = MRN
        self.age = age
        self.sex = sex
        self.dz = dz
        self.pcp = pcp
        self.inpatient = inpatient

    #Class method
    def adultPatient(cls, adultpt):
        cls.adultpt = adultpt
    
    #polymorphism method
    def ptCreated(self):
        raise NotImplementedError('Subclass must implement abstract method')
        
    #polymorphism for different types 
    def inpatient(self):
        self.inpatient.yes()
        
    def outpatient(self):
        self.inpatient.no()
        
    def is_inpatient(self):
        return self.inpatient.is_inpatient()
        
    #getter methods for demographic variables
    
    def getDemos(self):
        return self.MRN, self.age, self.sex
    
    def getMRN(self):
        return self.MRN
    
    def getAge(self):
        return self.age
    
    def getSex(self):
        return self.sex
    
    #getter method for primary disease
    
    def getDisease(self):
        return self.dz
    
    #getter method for primary care practitioner
    
    def getPCP(self):
        return self.pcp
    
    #setter methods for setting demographic variables
    def setDemos(self, MRN, age, sex):
        self.MRN = MRN
        self.age = age
        self.sex = sex

    def setMRN(self, MRN):
        self.MRN = MRN
    
    def setAge(self, age):
        self.age = age
    
    def setSex(self, sex):
        self.sex = sex
    
    #setter method for primary disease
    
    def setDisease(self, dz):
        self.dz = dz
    
    #setter method for primary care practitioner
    
    def setPCP(self, pcp):
        self.pcp = pcp
        
    #setter method for inpatient status
    
    def Inpatient(self):
        self.hosp.Inpatient()
        
    def Outpatient(self):
        self.hosp.Outpatient()

    #inpatient status
    def isInpatient(self):
        return self.hosp.isInpatient()


# In[96]:


#3. Instantiate several objects of your class

#instantiate object with input parameters
patient1 = Patient(11298761, 62, 'M', 'Irritable Bowel', 'Wilson', 'Inpatient')


#instantiate another object
patient2 = Patient(11914823, 28, 'F', 'Unfashionable', 'Ramsey', 'Outpatient')


#instantiate another object
patient3 = Patient(11381797, 44, 'F', 'Myelodysplastic Syndrome', 'Balthazar', 'Outpatient')


#instantiate another object
patient4 = Patient(11939969, 59, 'M', 'Rosacea', 'Merigold', 'Outpatient')

#instantiate another object
patient5 = Patient(117283677, 12, 'F', 'Rubella', 'Cooper', 'Inpatient')


# In[82]:


#4. Show how Inheritance works by creating at least 2 subclasses

#subclass Research inheriting Patient class
class Research(Patient):
    #all parameters for class and subclass
    subjectType = 'Human Research Subject'
    def __init__(self, study, phase, SID, MRN, age, sex, dz, pcp, inpatient):
        #Patient class attributes
        Patient.__init__(self, MRN, age, sex, dz, pcp, inpatient)
        #Research subclass attributes
        self.study = study
        self.phase = phase
        self.SID = SID
        self.inpatient = 'Outpatient'
    
    #getters and setters
    
    def getStudy(self):
        return self.study
        
    def getPhase(self):
        return self.phase
        
    def getSID(self):
        return self.SID
    
    def setClinTrial(self, study, phase, SID):
        self.study = study
        self.phase = phase
        self.SID = SID
    
    def setStudy(self, study):
        self.study = study
    
    def setPhase(self, phase):
        self.phase = phase
        
    def setSID(self, SID):
        self.SID = SID
        
    #polymorphism example
    def ptCreated(self):
        return 'Research Patient created.'
    
    #polymorphism for different types - string
    def inpatient(self):
        self.inpatient = 'Inpatient'
        print (self.inpatient)
        
    def outpatient(self):
        self.inpatient = 'Outpatient'
        
    def is_inpatient(self):
        return self.inpatient == 'Inpatient'
        
#confirm class attributes are globally shared
print('Patient Site is Research Site: ', Patient.site is Research.site, '\n')

#confirm subclass can modify attributes for subclass only
print('Patient Subject Type is Research Subject Type: ', Patient.subjectType is Research.subjectType)
print('Patient class patientType: ',Patient.subjectType)
print('Research subclass patientType: ',Research.subjectType, '\n')

        

    
#subclass Cancer inheriting patient class
class Cancer(Patient):
    dztype = 'Cancer'
    def __init__(self, MRN, age, sex, dz, subtype, oncologist, pcp, inpatient):
        Patient.__init__(self, MRN, age, sex, dz, pcp, inpatient)
        self.subtype = subtype
        self.oncologist = oncologist
        self.dz = dz
        self.inpatient = False
   
    def getCanc(self):
        return self.dz + ' - Subtype: ' + self.subtype+ ' , ' + 'Oncologist: ' + self.oncologist
    
    def getSubtype(self):
        return self.subtype
    
    def getOncologist(self):
        return self.oncologist
    
    def setCanc(self, dz, subtype, oncologist):
        self.dz = dz
        self.subtype = subtype
        self.oncologist = oncologist
    
    def setSubtype(self, subtype):
        self.subtype = subtype
    
    def setOncologist(self, oncologist):
        self.oncologist = oncologist

    #polymorphism example
    def ptCreated(self):
        return 'Oncology Patient created.'
    
    #polymorphism for different types - boolean
    def inpatient(self):
        self.inpatient = True
        
    def outpatient(self):
        self.inpatient = False
        
    def is_inpatient(self):
        return self.inpatient

    

rpatient1 = Research('GutTex Probiotics Efficacy Trial', 2, 200012, 11292211, 47, 'M', 'Irritable Bowel', 'Scooby', 'Outpatient')

#confirm class method is shared
rpatient1.adultpt = True
print('Adult Research Patient: ', rpatient1.adultpt)


print(rpatient1.subjectType, '\n', 'MRN: ', rpatient1.MRN, ' has been enrolled on ', rpatient1.study, ', a Phase ', rpatient1.phase, 
     ' study as subject #', rpatient1.SID, ' at ', rpatient1.site, '\n', sep='')


lpatient1 = Cancer(114982772, 75, 'M', 'Leukemia','acute lymphoblastic', 'Bradley', 'Wilson', 'Inpatient')
print('MRN: ', lpatient1.MRN, '\n', 'Disease Type: ', lpatient1.dztype, '\n', lpatient1.getCanc(), '\n', 'Patient Status: ', lpatient1.inpatient, '\n', sep = '')
lpatient1.newpt = False
print('New Oncology Patient: ', lpatient1.newpt)

lpatient2 = Cancer(114982773, 59, 'M', 'Leukemia','acute myelogenous', 'Fahrenheit', 'Kelvin', 'Inpatient')
print('MRN: ', lpatient2.MRN, '\n', 'Disease Type: ', lpatient2.dztype, '\n', lpatient2.getCanc(), '\n', 'Patient Status: ',lpatient2.inpatient, sep = '')



# In[84]:


#5. Show how Polymorphism works by creating a method that could return different types based on the inputs

#Patients
patients = [Research('GutTex Probiotics Efficacy Trial', 2, 200012, 11292211, 47, 'M', 'Irritable Bowel', 'Scooby', 'Outpatient'),
           Cancer(114982772, 75, 'M', 'Leukemia','acute lymphoblastic', 'Bradley', 'Wilson', 'Inpatient'),
           Cancer(114982773, 59, 'M', 'Leukemia','acute myelogenous', 'Fahrenheit', 'Kelvin', 'Inpatient')]

for each in patients:
    print(each.ptCreated(),' MRN: ',each.MRN)


print('Research Patient 1 inpatient: ',rpatient1.is_inpatient())

print('Cancer Patient 1 inpatient: ', lpatient1.is_inpatient())


# In[115]:


#6. Write some example code to show how you would use your class, and eventually put it in a module/package format

#confirm patient 1 identity with PHI identifiers
print('Patient 1 ID: ', patient1.getDemos())

#confirm patient 1 primary disease
print('Patient 1 Primary Disease: ', patient1.getDisease(), '\n', sep = '')

#update patient 1 primary disease
patient1.setDisease('Gastroenteritis')   

#print updated patient 1 details:
print('Patient 1 Profile: ', '\n','Medical Record Number: ', patient1.getMRN(), '\n', 
      'Age: ', patient1.getAge(), '\n', 
      'Sex: ', patient1.getSex(), '\n', 
      'Primary Disease: ', patient1.getDisease(), '\n', 
      'Primary Care Physician: ', patient1.getPCP(), '\n', sep = '')

#see research patient 1 study:
print('Research Patient 1 Study: ', rpatient1.getStudy(), '\n')

#set cancer patient 1 cancer details
lpatient1.setCanc('Lymphoma', 'diffuse B-cell', 'Nelly')
#print updated cancer patient 1 details
print('Cancer Patient 1 Profile: ')
print('Medical Record Number: ', lpatient1.getMRN())
print('Age: ', lpatient1.getAge())
print('Sex: ', lpatient1.getSex())
print('Primary Disease: ', lpatient1.getDisease())
print('Disease Subtype: ', lpatient1.getSubtype())
print('Oncologist: ', lpatient1.getOncologist())
print('Primary Care Physician: ', patient1.getPCP(), '\n')



#update individual attributes of cancer patient 2
lpatient2.subtype = 'chronic myelogenous'
lpatient2.oncologist = 'Mariposa'
#print updated cancer patient 2 details
print('Cancer Patient 2 Profile: ')
print('Medical Record Number: ', lpatient2.getMRN())
print('Age: ', lpatient2.getAge())
print('Sex: ', lpatient2.getSex())
print('Primary Disease: ', lpatient2.getDisease())
print('Disease Subtype: ', lpatient2.getSubtype())
print('Oncologist: ', lpatient2.getOncologist())
print('Primary Care Physician: ', patient2.getPCP(), '\n')




# In[113]:


import os

#save class and each subclass in separate .py files
#save empty __init__.py in same directory

from firstpkg.Patient import Patient
x = Patient(11298761, 62, 'M', 'Irritable Bowel', 'Wilson', 'Inpatient')
x.subjectType

from firstpkg.Patient import *
y = Research('GutTex Probiotics Efficacy Trial', 2, 200012, 11292211, 47, 'M', 'Irritable Bowel', 'Scooby', 'Outpatient')
print(y.getStudy())


# In[114]:


#Modules for writing, reading, packing/unpacking file data

import csv
import io
import sys
import pickle
import shelve
import json

#write CSV file from a dictionary
with open('testdata.csv', mode = 'w') as onc_patient_csv:
    fieldnames = ['MRN', 'Age', 'Sex', 'Primary Disease', 'Subtype', 'Oncologist', 'PCP']
    writer = csv.DictWriter(onc_patient_csv, fieldnames = fieldnames)
    
    writer.writeheader()
    writer.writerow({'MRN': 114982772, 'Age': 75, 'Sex': 'M', 'Primary Disease' : 'Lymphoma', 'Subtype' : 'diffuse B-cell', 'Oncologist' : 'Nelly', 'PCP' : 'Wilson'})
    writer.writerow({'MRN': 114982773, 'Age': 59, 'Sex': 'M', 'Primary Disease': 'Leukemia', 'Subtype' : 'chronic myelogenous', 'Oncologist': 'Mariposa', 'PCP' : 'Ramsey'})
    writer.writerow({'MRN': 114982774, 'Age': 33, 'Sex': 'F', 'Primary Disease': 'Myeloma', 'Subtype': 'kappa light-chain', 'Oncologist': 'Ferdinand', 'PCP': 'Wilson'})

#read CSV file in as dict
with open('testdata.csv', mode = 'r') as onc_patient_csv:
    csv_reader = csv.DictReader(onc_patient_csv)


#dump and load pickle file into drive with dictionaries
oncpt1 = {'MRN': 114982772, 'Age': 75, 'Sex': 'M', 'Primary Disease' : 'Lymphoma', 'Subtype' : 'diffuse B-cell', 'Oncologist' : 'Nelly', 'PCP' : 'Wilson'}
oncpt2 = {'MRN': 114982773, 'Age': 59, 'Sex': 'M', 'Primary Disease': 'Leukemia', 'Subtype' : 'chronic myelogenous', 'Oncologist': 'Mariposa', 'PCP' : 'Ramsey'}
oncpt3 = {'MRN': 114982774, 'Age': 33, 'Sex': 'F', 'Primary Disease': 'Myeloma', 'Subtype': 'kappa light-chain', 'Oncologist': 'Ferdinand', 'PCP': 'Wilson'}


with open('oncpt2.pk1', 'wb') as file:
    pickle.dump(oncpt2, file)
    
with open('oncpt2.pk1', 'rb') as file:
    pickle.load(file)
print('Pickle File Onc Patient 2: ', oncpt2, '\n')

#serializing data using memory
oncpttest1 = pickle.dumps(oncpt1)

oncpt1_orig = pickle.loads(oncpttest1)
print('Pickle Memory Onc Patient 1: ',oncpt1_orig, '\n')
    
#save/open using shelve dict-style format
with shelve.open('test_shelf.db') as shelf_file:
    shelf_file['pkey'] = {'MRN': 11298761, 'Age': 62, 'Sex': 'M', 'Primary Disease': 'Irritable Bowel', 'PCP': 'Wilson', 'Status': 'Inpatient'}
    
with shelve.open('test_shelf.db') as shelf_file:
    shelfpt1 = shelf_file['pkey']

print('Shelf Patient 1: ',shelfpt1, '\n')

#json using io
k = io.StringIO()
json.dump(oncpt3, k)

print('JSON Dump Onc Patient 3: ',k.getvalue(), '\n')


# In[ ]:




