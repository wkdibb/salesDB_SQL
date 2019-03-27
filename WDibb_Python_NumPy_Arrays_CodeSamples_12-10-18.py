#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### 12-10-18 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### Numpy arrays


# In[4]:


#1d array with 25 even-interval decimal numbers
#calculate min/max/mean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator

npseries = np.linspace(1,7,25)
print(npseries)

print(npseries.min())
print(npseries.max())
print(npseries.mean())


# In[5]:


#2d array 16x4, change shape to new 8x8 array
A = np.arange(64).reshape(16,4)
B = A.reshape(8,8)
B


# In[6]:


#elementwise addition using identity array
C = np.identity(8)
D = np.empty_like(B)
D = B + C
D


# In[7]:


#dot function of two arrays
np.dot(D,B)


# In[8]:


#create array from nested lists
#print shape and diagonal elements
numarray = np.array([[0,1,2],
                     [5,6,7],
                     [10,11,12]])

print('Numarray shape: ',numarray.shape)
#can manually identify individual elements in diagonal like this:
#print('Diagonal elements: ',numarray[0,0], numarray[1,1], numarray[2,2])
print('Diagonal elements: ',numarray.diagonal())


# In[9]:


#zeroes function
from numpy import *
array2 = zeros(15).reshape(3,5)
array2


# In[10]:


#ones function
#can also do explicit conversion to integer type
array3 = np.ones( (5,8), dtype=np.int ) 
#or by array3 = ones(40).reshape(5,8)
array3


# In[11]:


#identity matrix and eye function

#can use eye function and set k to 0 to populate as identity matrix:
#array4 = np.eye(7, 7, k = 0, dtype = int)

#or use basic identity function:
array4 = np.identity(7)

array4


# In[12]:


#An array with constant float values:
x = float(input('Enter value here: '))
array5 = np.full(21,x).reshape(3,7)
print(array5)
print('Data type: ',array5.dtype.name)


# In[ ]:




