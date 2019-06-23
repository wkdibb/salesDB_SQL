#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### 5-2019 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### tkinter GUI

#Fahrenheit to Celsius, Celsius to Fahrenheit
#T(F) = T(C) * 1.8 + 32
#T(C) = (T(F) - 32)/1.8

#Code a simple GUI 
#using tkinter that takes an input the weight in kilograms and converts it 
#into pounds (the example below shows lb to kg)

#Note: 1 lb. = 0.453 Kg
#1 Kg = 2.205 lb

from tkinter import *
from tkinter import ttk 

#includes ttk class with below methods

def calculate(*args):
    try:
        value = float(kilograms.get())
        pounds.set(value * 2.20462)
    except ValueError:
        pass
    
root = Tk()
root.title('Kilograms to Pounds Conversion:')

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column = 1, row = 1, sticky = (N, W, E, S))
mainframe.columnconfigure(1, weight = 1)
mainframe.rowconfigure(1, weight = 1)

kilograms = StringVar()
pounds = StringVar()

kg_entry = ttk.Entry(mainframe, width = 10, textvariable=kilograms)
kg_entry.grid(column = 2, row = 1, sticky = (W, E))

ttk.Label(mainframe, textvariable=pounds).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text='Calculate', command=calculate).grid(column=2, row=3, sticky=W)

ttk.Label(mainframe, text='kilograms (kg)').grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text='converts to').grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text='pounds (lb)').grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=7, pady=7)

kg_entry.focus()
root.bind('<Return>', calculate)
root.geometry('350x120')

root.mainloop()


# In[ ]:


12

