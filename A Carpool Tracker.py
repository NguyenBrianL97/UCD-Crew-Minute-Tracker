from tkinter import *
from tkinter import ttk

import mysql.connector

cnx = mysql.connector.connect(user='root', password=constant.password,
                              host='127.0.0.1',
                              database='carpool',
                              use_pure=False)
#cnx.close()
cursor = cnx.cursor()

root = Tk()
root.title("Carpool Minute Tracker")

# Initialize our country "databases":
#  - the list of country codes (a subset anyway)
#  - a parallel list of country names, in the same order as the country codes
#  - a hash table mapping country code to population<
countrycodes = ('sf', 'gr', 'ty')
countrynames = ('Stephen', 'Garret', 'Todd', 'Todd','Todd','Todd','Todd','Todd','Todd','Todd','Todd')
listnames=[]
cnames = StringVar(value=countrynames)
populations = {'sf':120, 'gr':60, 'ty':30}

#query database for table names
query = ("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='carpool'")
cursor.execute(query)
for TABLE_NAME in cursor:
  name=''.join(filter(str.isalpha, TABLE_NAME))
  listnames.append(name)
cnames = StringVar(value=listnames)


# Names of the gifts we can send
gifts = { 'card':'Greeting card', 'flowers':'Flowers', 'nastygram':'Nastygram'}

# State variables
gift = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

selectedmsg = StringVar()
new_driver_name = StringVar()
new_driver_name_i = StringVar()

duration = StringVar()
distance = StringVar()
date = StringVar()
description = StringVar()

#new driver entry
#new_driver_entry = ttk.Entry(c, width=7, textvariable=new_driver_name)
#new_driver_entry = ttk.Radiobutton(c, text=gifts['flowers'], variable=gift, value='flowers')
#new_driver_entry.grid(column=1, row=1, sticky=W, padx=20)

# Called when the selection in the listbox changes; figure out
# which country is currently selected, and then lookup its country
# code, and from that, its population.  Update the status message
# with the new population.  As well, clear the message about the
# gift being sent, so it doesn't stick around after we start doing
# other things.

def create_table():
    table_description=(
    "CREATE TABLE `{}` ("
    "  `Time` int(11),"
    "  `Distance` int(11) NOT NULL,"
    "  `Date` date NOT NULL,"
    "  `Description` varchar(255) NOT NULL"
    ") ENGINE=InnoDB".format(new_driver_name.get()))
    
    print("Trying to add a table to database...")
    cursor.execute(table_description)
    print("Added table to database (?)")

    lbox.insert("end", new_driver_name.get())
    listnames.append(new_driver_name.get())
    cnames = StringVar(value=listnames)
    
    #lbox = Listbox(c, listvariable=cnames, height=5)
    #lbox.grid(column=0, row=0, rowspan=5, sticky=(N,S,E,W))

def upload_data():
    idxs = lbox.curselection()
    idx = int(idxs[0])
    name = listnames[idx]
    add_driver_info = ("INSERT INTO {} "
               "(Time, Distance, Date, Description) "
               "VALUES (%s, %s, %s, %s)".format(name))
    print(add_driver_info)
    driving_data=(duration.get(),distance.get(),date.get(),description.get())
    print(driving_data)
    cursor.execute(add_driver_info, driving_data)
    print("Uploading data")
    cnx.commit()
    
    
def showPopulation(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        code = countrycodes[idx]
        name = listnames[idx]
        popn = populations[code]
        statusmsg.set("%s has driven %d minutes" % (name, popn))
        selectedmsg.set("%s selected" % (name))
    sentmsg.set('')

# Called when the user double clicks an item in the listbox, presses
# the "Send Gift" button, or presses the Return key.  In case the selected
# item is scrolled out of view, make sure it is visible.
#
# Figure out which country is selected, which gift is selected with the 
# radiobuttons, "send the gift", and provide feedback that it was sent.
def sendGift(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = countrynames[idx]
        # Gift sending left as an exercise to the reader
        sentmsg.set("Sent %s to leader of %s" % (gifts[gift.get()], name))

# Create and grid the outer content frame
c = ttk.Frame(root, padding=(6, 6, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

# Create the different widgets; note the variables that many
# of them are bound to, as well as the button callback.
# Note we're using the StringVar() 'cnames', constructed from 'countrynames'
#SHOW <b>lbox</b> = Listbox(c, <b>listvariable=cnames</b>, height=5)
#HIDE
lbox = Listbox(c, listvariable=cnames, height=5)
#/HIDE
lbl = ttk.Label(c, text="Send to country's leader:")
lbl1 = ttk.Label(c, text="Driver's First Name (lowercase)")
#lbl2 = ttk.Label(c, text="First and Last initials")

lbl3 = ttk.Label(c, text="Time (minutes)")
lbl4 = ttk.Label(c, text="Distance (miles)")
lbl5 = ttk.Label(c, text="Date (YYYY-MM-DD)")
lbl6 = ttk.Label(c, text="Description")

btn = ttk.Button(c, text='Add driver', command=create_table, default='active')
btn2 = ttk.Button(c, text='Upload Data', command=upload_data, default='active')
#SHOW g1 = ttk.Radiobutton(c, text=gifts['card'], <b>variable=gift</b>, value='card')
#SHOW g2 = ttk.Radiobutton(c, text=gifts['flowers'], <b>variable=gift</b>, value='flowers')
#SHOW g3 = ttk.Radiobutton(c, text=gifts['nastygram'], <b>variable=gift</b>, value='nastygram')
#SHOW send = ttk.Button(c, text='Send Gift', <b>command=sendGift</b>, default='active')
#SHOW sentlbl = ttk.Label(c, <b>textvariable=sentmsg</b>, anchor='center')
#SHOW status = ttk.Label(c, <b>textvariable=statusmsg</b>, anchor=W)
#HIDE

#g1 = ttk.Radiobutton(c, text=gifts['card'], variable=gift, value='card')
#g2 = ttk.Radiobutton(c, text=gifts['flowers'], variable=gift, value='flowers')
#g3 = ttk.Radiobutton(c, text=gifts['nastygram'], variable=gift, value='nastygram')

g4 = ttk.Entry(c, width=10, textvariable=new_driver_name)
#g5 = ttk.Entry(c, width=3, textvariable=new_driver_name_i)
#inputdata
send = ttk.Entry(c, width=10, textvariable=duration)
send2 = ttk.Entry(c, width=10, textvariable=distance)
send3 = ttk.Entry(c, width=10, textvariable=date)
send4 = ttk.Entry(c, width=10, textvariable=description)

sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)
status2 = ttk.Label(c, textvariable=selectedmsg, anchor=CENTER)
#/HIDE

# Grid all the widgets
lbox.grid(column=0, row=0, rowspan=5, sticky=(N,S,E,W))
#lbl.grid(column=1, row=0, padx=10, pady=5)

#labels above add driver information
lbl1.grid(column=2, row=0, padx=10, pady=5)
#lbl2.grid(column=2, row=0, padx=10, pady=5)

#input data labels
lbl3.grid(column=1, row=3, padx=10, pady=5)
lbl4.grid(column=2, row=3, padx=10, pady=5)
lbl5.grid(column=1, row=5, padx=10, pady=5)
lbl6.grid(column=2, row=5, padx=10, pady=5)

#radio button gridding
#g1.grid(column=1, row=1, sticky=W, padx=20)
#g2.grid(column=1, row=2, sticky=W, padx=20)
#g3.grid(column=1, row=3, sticky=W, padx=20)

g4.grid(column=2, row=1, sticky=W, padx=40) #First name field
#g5.grid(column=2, row=1, sticky=W, padx=40) #Intials field
btn.grid(column=3, row=1, padx=10, pady=5) #add driver button
btn2.grid(column=2, row=7, padx=10, pady=5) #add driver button

#input data fields
send.grid(column=1, row=4, sticky=E) 
send2.grid(column=2, row=4, sticky=E)
send3.grid(column=1, row=6, sticky=E)
send4.grid(column=2, row=6, sticky=E)

sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5) #sent gift
status.grid(column=0, row=7, columnspan=2, sticky=(W,E)) #has driven 120 miles

status2.grid(column=1, row=2, columnspan=2, sticky=(W,E))

c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

# Set event bindings for when the selection in the listbox changes,
# when the user double clicks the list, and when they hit the Return key
lbox.bind('<<ListboxSelect>>', showPopulation)
lbox.bind('<Double-1>', sendGift)
root.bind('<Return>', sendGift)

# Colorize alternating lines of the listbox
for i in range(0,len(listnames),2):
    lbox.itemconfigure(i, background='#f0f0ff')

# Set the starting state of the interface, including selecting the
# default gift to send, and clearing the messages.  Select the first
# country in the list; because the &lt;&lt;ListboxSelect&gt;&gt; event is only
# generated when the user makes a change, we explicitly call showPopulation.
gift.set('card')
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)
showPopulation()

root.mainloop()
#HIDE
#update idletasks; update
#$::lbox selection clear 0
#$::lbox selection set 4
#$::lbox yview scroll 2 units
#wm geometry . [expr [winfo width .]+15]x[expr [winfo height .]+20]
#showPopulation
#set gift nastygram
#sendGift
#/HIDE
