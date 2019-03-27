#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### 12-10-18 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### Strings


# In[2]:


#String slicing
print("abcd"[2:])


# In[8]:


#Reverse string functions

def reverse_string1(str1):
    str1 = str1[::-1]
    return str1

str1 = input('Enter first string: ')
print(reverse_string1(str1))


#the way that defines the length of the string and specifies all positions of the string
#including separate concatenation of 0th index

def reverse_string2(str2):
    n = len(str2)+1
    str2 = str2[n:0:-1] + str2[0] 
    return str2

str2 = input('Enter second string: ')
print(reverse_string2(str2))

#the way that creates a list of the string, then iterates backwards from the end of the list

def reverse_string3(str3):
    str3 = list(str3)
    n = len(str3)-1
    for i in str3:
        output = (str3[n])
        n = n-1
        print(output, end="")
    return ""

str3 = input('Enter third string: ')
print(reverse_string3(str3))

#The way that uses the join and reverse functions

str4 = input('Enter fourth string: ')
def reverse_string4(str4):
    str4 = list(str4)
    str4.reverse()
    outputstr4 = "".join(str4)
    return(outputstr4)
print(reverse_string4(str4))

#can also do in a single line as print("".join(reversed(str4)))


# In[4]:


#Hexadecimal format
print(0xA + 0xB + 0xC)


# In[6]:


#modify input string to replace middle 1-2 characters with initial 1-2 characters
x = input('Enter string here: ')
result = ""
oddmid = int((len(x)/2))
evenmid_upper = int((len(x)/2))
evenmid_lower = int((len(x)/2)-1)
for i in x:
    if len(x) % 2 != 0:
        result = x[:oddmid] + x[0] + x[oddmid+1:]
    else:
        result = x[:evenmid_lower] + x[0:2] + x[evenmid_upper+1:]
print(result)


# In[7]:


#modify input string to replace even index characters with 'i'
str = input('Enter string here: ')
def even_ichange(str):  
  result = ""   
  for i in range(len(str)):  
    if i % 2 != 0:  
      result = result + str[i]  
    elif i % 2 == 0:
      result = result + 'i'
  return result  
print(even_ichange(str))


# In[ ]:




