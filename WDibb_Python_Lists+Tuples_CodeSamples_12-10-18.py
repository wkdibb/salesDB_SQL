#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### 12-10-18 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### Lists, Sets, Tuples


# In[15]:


#Formatting list types

a = list()
type(a)

b = []
type(b)

c = list([1,2,3])
type(c)

d = [1,2,3]
type(d)


# In[16]:


#Shuffle list

list = [1,2,3,4,5,6,7]
import random
random.shuffle(list)
print(list)


# In[17]:


#Slice list

list = [4, 2, 2, 4, 5, 2, 1, 0]
print(list[0])
print(list[:2])
print(list[:-2])
print(list[4:6])


# In[18]:


#tuple elementwise values

t1 =  (1,2,4,3)
t2 = (1,2,3,4)
t1 < t2


# In[19]:


#function to remove largest and smallest elements of an input list

def maxmin_listnum(list1):  
    max = list1[0]  
    min = list1[0]
    for x in list1:  
        if x > max:  
            max = x 
        elif x < min:
            min = x
    list1.remove(min)
    list1.remove(max)
    return list1

list1 = [int(x) for x in input("List values with spaces between each value: ").split()]
print(maxmin_listnum(list1))


# In[20]:


#function to remove input list duplicates, then print reversed output

def remove_duplicates(list2):
    unique_list = []
    dup_list = set()
    for x in list2:
        if x not in dup_list:
            unique_list.append(x)
            dup_list.add(x)
    unique_list.sort()
    unique_list.reverse()
    return unique_list

inputlist = input("Introduce a list with numbers: ")
list2 = list(map(int, inputlist.split()))

print(remove_duplicates(list2))


# In[ ]:


#sort immutable tuple elements
tuple1 = input('Introduce a list with numbers: ')
tuple1 = tuple(map(int, tuple1.split()))

sorted(tuple1)


tuple2 = list(tuple1)
tuple2.sort()
tuple3 = tuple(tuple2)
print(tuple3)
type(tuple3)
    

