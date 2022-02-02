import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from datetime import datetime
import sqlite3

# Note 
# For conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')
# Please change to the absolute path of the database file in your PC

# Define global variables here

# ----- student global variables -------
treeview = None
treeviewcancel = None
comboboxChannel = None
StudentWindow = None
# ----- student global variables end -------

# ----- staff global variables -----
entrychannelname = None
entrychannelstartdate = None
entrychannelenddate = None
entrychannelcapacity = None
entrysessionname = None
entrysessiondate = None
entrysessionstarttime = None
entrysessionendtime = None
entrysessioncapacity = None
comboboxchannel = None
StaffWindow = None
# ----- staff global variables end -----

# ----- admin global variables -----
AdminWindow = None
radiobuttonstudent = None
radiobuttonstaff = None
radiobuttonadmin = None
entryname = None
entryusername = None
entrypassword = None
selected = None
var = None
# ----- admin global variables end -----

# ----- login global variables ------
Dusername = None
OnlyDate = None
OnlyTime = None
# ----- login global variables end ------


# Declare the window
window = tk.Tk()

# set title of window
window.title("UOW Booking System")

# set size of window
window.geometry("600x400")

# ----------------------------------------------------- Student User ------------------------------------------------------------------------------------------

def comboclick(event):

       # clear all records from treeview first
       for record in treeview.get_children():
                     treeview.delete(record) 

       # connect to Sqlite Database
       conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

       # create a database cursor
       cursor = conn.cursor()

       # Define sql command
       cursor.execute("SELECT * FROM Session WHERE Channel_Name='"+comboboxChannel.get()+"'")

       # fetch data into variable
       rows = cursor.fetchall()

       # populate database data into treeview
       for row in rows:
          treeview.insert("", tk.END, values=row)

       # Commit our command
       conn.commit()

       # Close our connection
       conn.close()

def book():

    # Grab record number
    selected = treeview.focus()

    # Grab record values
    values = treeview.item(selected, 'values')

    # store treeview data into variables 
    SessionID = values[0]
    SessionName = values[1]
    ChannelID = values[6]
    ChannelName = values[7]

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursor = conn.cursor()

    # Define sql command
    cursor.execute("SELECT UserID FROM Users WHERE Username ='"+ Dusername +"' ")

    # Note: must get the student user who is booking the session
    UserID = cursor.fetchone()[0]
    # print(UserID)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    Username = Dusername

    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # https://www.w3schools.com/sql/sql_insert.asp

    # Insert Data into table
    cursor.execute("INSERT INTO Booking (SessionID, Session_Name, ChannelID, Channel_Name, UserID, Username) VALUES ("+str(SessionID)+",'" +SessionName+ "',"+str(ChannelID)+",'" +ChannelName+"'," +str(UserID)+ ",'" +Username+"')")

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # Show messagebox for successful completion
    messagebox.showinfo("Book a Session", "Booking Sucessful!!")

def cancel():
    
    # Grab record number
    selected = treeviewcancel.focus()

    # Grab record values
    values = treeviewcancel.item(selected, 'values')

    # store treeview data into variables 
    BookingID = values[0]

    # connect to database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # Insert into table
    cursor.execute("DELETE FROM Booking WHERE BookingID="+BookingID+"")

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # Delete from treeview
    deletionselection = treeviewcancel.selection()[0]
    treeviewcancel.delete(deletionselection)

    # Show messagebox for successful completion
    messagebox.showinfo("Cancel Booking", "Booking canceled sucessfully!!")

def studentLogout():
    
    # get logout date and time
    logoutdateandtime = datetime.now()

    studentlogouttime = logoutdateandtime.time()

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursor = conn.cursor()

    # Define sql command
    cursor.execute("SELECT UserID FROM Users WHERE Username ='"+ Dusername +"' ")

    # Note: must get the student user who is booking the session
    UserID = cursor.fetchone()[0]
    # print(UserID)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # connect to database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # Insert into table

    conn.execute("INSERT INTO ActivityHistory (Login_Date,Login_Time,Logout_Time,UserID,Username) VALUES (:logindate,:logintime,:logouttime,:userid,:username)",
               {
                   'logindate': OnlyDate,
                   'logintime': str(OnlyTime),
                   'logouttime' : str(studentlogouttime),
                   'userid' : UserID,
                   'username' : Dusername
               })

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    StudentWindow.destroy()

def studentWindow():

    global StudentWindow
    window.destroy()
    StudentWindow = tk.Tk()
    StudentWindow.title("Student")
    StudentWindow.geometry("1100x700")
    
    # create Label
    LabelHeading = tk.Label(text="Session Booking for Students", bg="cyan", width="100", height="2", font=("Calibri", 16))
    LabelHeading.grid(column=0,row=0)

    # create a treeview
    global treeview
    treeview = ttk.Treeview(StudentWindow)
    treeview.bind("<ButtonRelease-1>") # single click  (selected)
    treeview.place(x=10,y=80)

    # define treeview columns
    treeview['columns'] = ("SessionID","Session Name","Session Date","Session Start Time","Session End Time","Session Capacity","Channel ID","Channel Name","UserID","Username")

    # format columns
    treeview.column("#0", width=0) # removes the phantom column
    treeview.column("SessionID", width=70) 
    treeview.column("Session Name", width=100)
    treeview.column("Session Date", width=100)
    treeview.column("Session Start Time", width=120)
    treeview.column("Session End Time", width=120)
    treeview.column("Session Capacity", width=100)
    treeview.column("Channel ID", width=70)
    treeview.column("Channel Name", width=100)
    treeview.column("UserID", width=70)
    treeview.column("Username", width=100)

    # Create headings
    treeview.heading("#0", text="")
    treeview.heading("SessionID", text="SessionID", )
    treeview.heading("Session Name", text="Session Name")
    treeview.heading("Session Date", text="Session Date")
    treeview.heading("Session Start Time", text="Session Start Time")
    treeview.heading("Session End Time", text="Session End Time")
    treeview.heading("Session Capacity", text="Session Capacity")
    treeview.heading("Channel ID", text="Channel ID")
    treeview.heading("Channel Name", text="Channel Name")
    treeview.heading("UserID", text="UserID")
    treeview.heading("Username", text="Username")

    # ------------------------------------- Treeview Operation ---------------------------------------

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursortreeview = conn.cursor()

    # Define sql command
    cursortreeview.execute("SELECT * FROM Session")

    # fetch data into variable
    rows = cursortreeview.fetchall()

    # populate database data into treeview
    for row in rows:
        treeview.insert("", tk.END, values=row)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # ------------------------------------- Treeview Operation End ---------------------------------------
   

    # ------------------------------------- ComboBox Operation ---------------------------------------

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    channelnamecursor = conn.cursor()

    # Define sql command
    channelnamecursor.execute("SELECT DISTINCT Channel_Name FROM Channel")

    # fetch data into variable
    rows = channelnamecursor.fetchall()
    # print(rows)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # ------------------------------------- ComboBox Operation End ---------------------------------------
    
    # create a Label
    label1 = tk.Label(StudentWindow,text="Browse channel")
    label1.place(x=10,y=330)

    # create a Button
    buttonbook = tk.Button(StudentWindow,text="Book", width=10, command=book)
    buttonbook.place(x=30,y=360)

    buttoncancelbooking = tk.Button(StudentWindow,text="Cancel Booking", width=13, command=CancelBookingWindow)
    buttoncancelbooking.place(x=30,y=390)

    buttonstudentlogout = tk.Button(StudentWindow,text="Logout", width=13, command=studentLogout)
    buttonstudentlogout.place(x=500,y=600)

    # create a combobox
    global comboboxChannel
    comboboxChannel = ttk.Combobox(StudentWindow, value=rows)
    comboboxChannel.current(0)
    comboboxChannel.bind("<<ComboboxSelected>>", comboclick) 
    comboboxChannel.place(x=100,y=330)

    StudentWindow.mainloop()

def CancelBookingWindow():

    CancelWindow = tk.Tk()
    CancelWindow.title("Cancel Booking")
    CancelWindow.geometry("600x500")
    
    # create Label
    LabelHeading = tk.Label(CancelWindow,text="Cancel Booking", bg="cyan", width="55", height="2", font=("Calibri", 16))
    LabelHeading.grid(column=0,row=0)

    # create a treeview
    global treeviewcancel
    treeviewcancel = ttk.Treeview(CancelWindow)
    treeviewcancel.bind("<ButtonRelease-1>") # single click  (selected)
    treeviewcancel.place(x=10,y=80)

    # define treeview columns
    treeviewcancel['columns'] = ("BookingID","SessionID","Session Name","Channel ID","Channel Name","UserID","Username")

    # format columns
    treeviewcancel.column("#0", width=0) # removes the phantom column
    treeviewcancel.column("BookingID", width=70) 
    treeviewcancel.column("SessionID", width=70) 
    treeviewcancel.column("Session Name", width=100)
    treeviewcancel.column("Channel ID", width=70)
    treeviewcancel.column("Channel Name", width=100)
    treeviewcancel.column("UserID", width=70)
    treeviewcancel.column("Username", width=100)

    # Create headings
    treeviewcancel.heading("#0", text="")
    treeviewcancel.heading("BookingID", text="BookingID", )
    treeviewcancel.heading("SessionID", text="SessionID", )
    treeviewcancel.heading("Session Name", text="Session Name")
    treeviewcancel.heading("Channel ID", text="Channel ID")
    treeviewcancel.heading("Channel Name", text="Channel Name")
    treeviewcancel.heading("UserID", text="UserID")
    treeviewcancel.heading("Username", text="Username")

    # ------------------------------------- Treeview Operation ---------------------------------------

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursortreeview = conn.cursor()

    # Define sql command
    cursortreeview.execute("SELECT * FROM Booking")

    # fetch data into variable
    rows = cursortreeview.fetchall()

    # populate database data into treeview
    for row in rows:
        treeviewcancel.insert("", tk.END, values=row)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # ------------------------------------- Treeview Operation End ---------------------------------------

    # create a Button
    buttoncancel = tk.Button(CancelWindow,text="Cancel Booking", width=13, command=cancel)
    buttoncancel.place(x=30,y=320)

# ----------------------------------------------------- Student User End ------------------------------------------------------------------------------------------

# ----------------------------------------------------- Staff User ------------------------------------------------------------------------------------------

def createChannel():
    
    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursor = conn.cursor()

    # Define sql command
    cursor.execute("SELECT UserID FROM Users WHERE Username ='"+ Dusername +"' ")

    # Note: must get the student user who is booking the session
    UserID = cursor.fetchone()[0]
    # print(UserID)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # connect to database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # Insert into table

    conn.execute("INSERT INTO Channel (Channel_Name, ChannelStartDate, ChannelEndDate, Channel_Capacity , UserID, Username) VALUES (:channelname,:channelstartdate,:channelenddate,:channelcapacity,:userid,:username)",
               {
                   'channelname':  entrychannelname.get(),
                   'channelstartdate': entrychannelstartdate.get(),
                   'channelenddate' : entrychannelenddate.get(),
                   'channelcapacity' : entrychannelcapacity.get(),
                   'userid' : UserID,
                   'username' : Dusername
               })

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()
 
    # Clear Textboxes
    entrychannelname.delete(0, END)
    entrychannelstartdate.delete(0, END)
    entrychannelenddate.delete(0, END)
    entrychannelcapacity.delete(0, END)

    # Show messagebox for successful completion
    messagebox.showinfo("Channel Creation", "Channel Created Successfully")

def createSession():

# ------ Get channel ID --------------------
    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursor = conn.cursor()

    # https://stackoverflow.com/questions/31264522/getting-the-selected-value-from-combobox-in-tkinter

    # Define sql command
    cursor.execute("SELECT ChannelID FROM Channel WHERE Channel_Name ='"+ comboboxchannel.get() +"' ")

    # Note: must get the student user who is booking the session
    ChannelID = cursor.fetchone()[0]
    # print(UserID)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# ------ Get channel ID  end --------------------

# ------ Get User ID  --------------------
    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursor = conn.cursor()

    # Define sql command
    cursor.execute("SELECT UserID FROM Users WHERE Username ='"+ Dusername +"' ")

    # Note: must get the student user who is booking the session
    UserID = cursor.fetchone()[0]
    # print(UserID)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

# ------ Get User ID end  --------------------

    # connect to database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # Insert into table

    conn.execute("INSERT INTO Session (Session_Name, Session_Date, SessionStartTime, SessionEndTime , SessionCapacity , ChannelID , Channel_Name , UserID, Username) VALUES (:sessionname, :sessiondate, :sessionstarttime,:sessionendtime ,:sessioncapacity ,:channelID ,:channelname ,:userid,:username)",
               {
                   'sessionname':  entrysessionname.get(),
                   'sessiondate': entrysessiondate.get(),
                   'sessionstarttime' : entrysessionstarttime.get(),
                   'sessionendtime' : entrysessionendtime.get(),
                   'sessioncapacity' : entrysessioncapacity.get(),
                   'channelID' : ChannelID,
                   'channelname' : comboboxchannel.get(),
                   'userid' : UserID,
                   'username' : Dusername
               })

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # Clear Textboxes
    entrysessionname.delete(0, END)
    entrysessiondate.delete(0, END)
    entrysessionstarttime.delete(0, END),
    entrysessionendtime.delete(0, END)
    entrysessioncapacity.delete(0, END)

    # Show messagebox for successful completion
    messagebox.showinfo("Session Creation", "Session Created Successfully")

def ChannelWindow():

    ChannelWindow = tk.Tk()
    ChannelWindow.title("Create Channel")
    ChannelWindow.geometry("350x500")

    # create Label
    LabelHeading = tk.Label(ChannelWindow,text="Create Channel", font=("Calibri", 16))
    LabelHeading.place(x=115,y=40)

    label1 = tk.Label(ChannelWindow,text="Channel Name")
    label1.place(x=5, y=105)
    label2 = tk.Label(ChannelWindow,text="Channel Start Date")
    label2.place(x=5, y=130)
    label3 = tk.Label(ChannelWindow,text="Channel End Date" )
    label3.place(x=5, y=155)
    label4 = tk.Label(ChannelWindow,text="Channel Capacity")
    label4.place(x=5, y=180)

    # create entry field
    global entrychannelname
    global entrychannelstartdate
    global entrychannelenddate
    global entrychannelcapacity 
    entrychannelname = tk.Entry(ChannelWindow,width="30")
    entrychannelname.place(x=125,y=108)
    entrychannelstartdate = tk.Entry(ChannelWindow,width="30")
    entrychannelstartdate.place(x=125,y=133)
    entrychannelenddate = tk.Entry(ChannelWindow,width="30")
    entrychannelenddate.place(x=125,y=158)
    entrychannelcapacity = tk.Entry(ChannelWindow,width="30")
    entrychannelcapacity.place(x=125,y=183)
    
    buttonCreate = tk.Button(ChannelWindow,text="Make Channel", font=("Calibri", 12), command=createChannel)
    buttonCreate.place(x=150,y=220)
     
    ChannelWindow.mainloop()

def SessionWindow():

    SessionWindow = tk.Tk()
    SessionWindow.title("Create Session")
    SessionWindow.geometry("410x500")

    # create Label
    LabelHeading = tk.Label(SessionWindow,text="Create Session", font=("Calibri", 16))
    LabelHeading.place(x=115,y=40)

    label1 = tk.Label(SessionWindow,text="Session Name")
    label1.place(x=5, y=105)
    label2 = tk.Label(SessionWindow,text="Session Date")
    label2.place(x=5, y=130)
    label3 = tk.Label(SessionWindow,text="Session Start Time" )
    label3.place(x=5, y=155)
    label4 = tk.Label(SessionWindow,text="Session End Time")
    label4.place(x=5, y=180)
    label5 = tk.Label(SessionWindow,text="Session Capacity")
    label5.place(x=5, y=205)

    # create entry field
    global entrysessionname
    global entrysessiondate
    global entrysessionstarttime
    global entrysessionendtime
    global entrysessioncapacity
    entrysessionname = tk.Entry(SessionWindow,width="30")
    entrysessionname.place(x=125,y=108)
    entrysessiondate = tk.Entry(SessionWindow,width="30")
    entrysessiondate.place(x=125,y=133)
    entrysessionstarttime = tk.Entry(SessionWindow,width="30")
    entrysessionstarttime.place(x=125,y=158)
    entrysessionendtime = tk.Entry(SessionWindow,width="30")
    entrysessionendtime.place(x=125,y=183)
    entrysessioncapacity = tk.Entry(SessionWindow,width="30")
    entrysessioncapacity.place(x=125,y=208)
    
    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    channelnamecursor = conn.cursor()

    # Define sql command
    channelnamecursor.execute("SELECT DISTINCT Channel_Name FROM Channel")

    # fetch data into variable
    rows = channelnamecursor.fetchall()
    # print(rows)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    label6 = tk.Label(SessionWindow,text="Select Channel")
    label6.place(x=10, y=250)
    
    global comboboxchannel
    comboboxchannel = ttk.Combobox(SessionWindow, value=rows)
    comboboxchannel.current(0)
    comboboxchannel.bind("<<ComboboxSelected>>") # comboclick
    comboboxchannel.place(x=100,y=250)

    buttonCreate = tk.Button(SessionWindow,text="Make Session", font=("Calibri", 12), command=createSession)
    buttonCreate.place(x=280,y=250)
     
    SessionWindow.mainloop()

def staffLogout():
    
    # get logout date and time
    logoutdateandtime = datetime.now()

    stafflogouttime = logoutdateandtime.time()

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursor = conn.cursor()

    # Define sql command
    cursor.execute("SELECT UserID FROM Users WHERE Username ='"+ Dusername +"' ")

    # Note: must get the student user who is booking the session
    UserID = cursor.fetchone()[0]
    # print(UserID)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    # connect to database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # Insert into table

    conn.execute("INSERT INTO ActivityHistory (Login_Date,Login_Time,Logout_Time,UserID,Username) VALUES (:logindate,:logintime,:logouttime,:userid,:username)",
               {
                   'logindate': OnlyDate,
                   'logintime': str(OnlyTime),
                   'logouttime' : str(stafflogouttime),
                   'userid' : UserID,
                   'username' : Dusername
               })

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    StaffWindow.destroy()

def staffWindow():

    window.destroy()
    global StaffWindow
    StaffWindow = tk.Tk()
    StaffWindow.title("Staff")
    StaffWindow.geometry("400x300")

    # create Label
    LabelHeading = tk.Label(StaffWindow,text="Create Channels and Sessions", bg="cyan", width="37", height="2", font=("Calibri", 16))
    LabelHeading.grid(column=0,row=0)

    # create button
    buttonchannel = tk.Button(StaffWindow, text="Create Channel", font=("Calibri", 12), width=15, command=ChannelWindow)
    buttonchannel.place(x=120,y=100)

    buttonchannel = tk.Button(StaffWindow, text="Create Session", font=("Calibri", 12), width=15, command=SessionWindow)
    buttonchannel.place(x=120,y=150)

    buttonstafflogout = tk.Button(StaffWindow, text="Logout", font=("Calibri", 12), width=15, command=staffLogout)
    buttonstafflogout.place(x=120,y=250)

    StaffWindow.mainloop()

# ----------------------------------------------------- Staff User End ------------------------------------------------------------------------------------------


# ----------------------------------------------------- Administrator User ------------------------------------------------------------------------------------------

def createUser():

    # connect to database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # Create a cursor --> tells the database what the user wants to do
    cursor = conn.cursor() # cursor instance

    # Insert into table

    conn.execute("INSERT INTO Users (Name,Username,Password,UserType) VALUES (:name,:username,:password,:usertype)",
               {
                   'name' : entryname.get(),
                   'username' : entryusername.get(),
                   'password' : entrypassword.get(),
                   'usertype' : selected,
               })

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    entryname.delete(0, END)
    entryusername.delete(0, END)
    entrypassword.delete(0, END)
    
    radiobuttonstudent.deselect()
    radiobuttonstaff.deselect()
    radiobuttonadmin.deselect()

    # Show messagebox for successful completion
    messagebox.showinfo("User Creation", "User created Successfully")

def selection():
    
    global selected

    if var.get() == 1:
          selected = "student"
    elif var.get() == 2:
          selected = "staff"
    elif var.get() == 3:
          selected = "administrator"

def AdminLogout():

    AdminWindow.destroy()

def ActivityHistoryWindow():

    ActivityHistoryWindow = tk.Tk()
    ActivityHistoryWindow.title("Activity History")
    ActivityHistoryWindow.geometry("700x500")

    treeviewactivity = ttk.Treeview(ActivityHistoryWindow,height=20)
    treeviewactivity.bind("<ButtonRelease-1>") # single click  (selected)
    treeviewactivity.place(x=10,y=10)

    # define treeview columns
    treeviewactivity['columns'] = ("Activity ID","Login Date","Login Time","Logout Time","User ID","Username")

    # format columns
    treeviewactivity.column("#0", width=0) # removes the phantom column
    treeviewactivity.column("Activity ID", width=70) 
    treeviewactivity.column("Login Date", width=70) 
    treeviewactivity.column("Login Time", width=130)
    treeviewactivity.column("Logout Time", width=130)
    treeviewactivity.column("User ID", width=70)
    treeviewactivity.column("Username", width=100)

    # Create headings
    treeviewactivity.heading("#0", text="")
    treeviewactivity.heading("Activity ID", text="Activity ID", )
    treeviewactivity.heading("Login Date", text="Login Date", )
    treeviewactivity.heading("Login Time", text="Login Time")
    treeviewactivity.heading("Logout Time", text="Logout Time")
    treeviewactivity.heading("User ID", text="User ID")
    treeviewactivity.heading("Username", text="Username")

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursortreeview = conn.cursor()

    # Define sql command
    cursortreeview.execute("SELECT * FROM ActivityHistory")

    # fetch data into variable
    rows = cursortreeview.fetchall()

    # populate database data into treeview
    for row in rows:
        treeviewactivity.insert("", tk.END, values=row)

    # Commit our command
    conn.commit()

    # Close our connection
    conn.close()

    ActivityHistoryWindow.mainloop()


def adminWindow():

    window.destroy()
    global AdminWindow
    AdminWindow = tk.Tk()
    AdminWindow.title("Administrator")
    AdminWindow.geometry("350x500")

    # create Label
    LabelHeading = tk.Label(AdminWindow,text="Manage Accounts", bg="cyan", width="33", height="2", font=("Calibri", 16))
    LabelHeading.grid(column=0,row=0)

    label1 = tk.Label(AdminWindow,text="Name")
    label1.place(x=35, y=105)
    label2 = tk.Label(AdminWindow,text="Username")
    label2.place(x=35, y=130)
    label3 = tk.Label(AdminWindow,text="Password")
    label3.place(x=35, y=155)

    # create entry field
    global entryname
    global entryusername
    global entrypassword
    entryname = tk.Entry(AdminWindow,width="30")
    entryname.place(x=105,y=108)
    entryusername = tk.Entry(AdminWindow,width="30")
    entryusername.place(x=105,y=133)
    entrypassword = tk.Entry(AdminWindow,width="30")
    entrypassword.config(show="*")
    entrypassword.place(x=105,y=158)

    global var
    var = IntVar()
     
    # create a radioButton 
    global radiobuttonstudent 
    global radiobuttonstaff
    global radiobuttonadmin
    radiobuttonstudent = tk.Radiobutton(AdminWindow,text="Student", variable=var, value=1, command=selection)
    radiobuttonstudent.place(x=35,y=190)

    radiobuttonstaff = tk.Radiobutton(AdminWindow,text="Staff", variable=var, value=2, command=selection )
    radiobuttonstaff.place(x=35,y=220)

    radiobuttonadmin = tk.Radiobutton(AdminWindow,text="Administrator", variable=var, value=3, command=selection )
    radiobuttonadmin.place(x=35,y=250)
    
    buttoncreateuser = tk.Button(AdminWindow,text="Create User", font=("Calibri", 12), command=createUser)
    buttoncreateuser.place(x=35,y=280)

    buttonviewactivityhistory = tk.Button(AdminWindow,text="View Activity History", font=("Calibri", 12), command=ActivityHistoryWindow)
    buttonviewactivityhistory.place(x=35,y=320)

    buttonadminlogout = tk.Button(AdminWindow, text="Logout", font=("Calibri", 12), width=15, command=AdminLogout)
    buttonadminlogout.place(x=120,y=400)

    AdminWindow.mainloop()

# ----------------------------------------------------- Administrator User  End ------------------------------------------------------------------------------------------

# -------------------------------------------------------------------- LOGIN --------------------------------------------------------------------------------------

def login():
    
    # https://www.youtube.com/watch?v=ngynJQ0iVwM&list=LL&index=7&t=796s

    # Get user input from textbox
    Username = str(entryUsername.get())
    Password = str(entryPassword.get())

    # connect to Sqlite Database
    conn = sqlite3.connect(r'C:\Coding Workspaces\Python\Database\Database Connection\Database Connection\pythonDatabase.db')

    # create a database cursor
    cursorUsername = conn.cursor()
    cursorPassword = conn.cursor()
    cursorUserType = conn.cursor()

    # construct database query
    usernamequery = ("SELECT Username FROM Users WHERE Username = ?")
    passwordquery = ("SELECT Password FROM Users WHERE Password = ?")
    usertypequery = ("SELECT UserType FROM Users WHERE Username = ?")

    # execute query
    cursorUsername.execute(usernamequery,[(Username)])
    cursorPassword.execute(passwordquery,[(Password)])
    cursorUserType.execute(usertypequery,[(Username)])

    try:
        # Fetch data 
        global Dusername
        Dusername = str(cursorUsername.fetchone()[0]) # get element in the 0 index of tuple
        Dpassword = str(cursorPassword.fetchone()[0]) # get element in the 0 index of tuple
        Dusertype = str(cursorUserType.fetchone()[0]) # get element in the 0 index of tuple

        # check user input against database and go to correct window
        if Username == Dusername and Password == Dpassword and Dusertype == "student":
                
                # Save current date and time
                currentdateandtime = datetime.now()
                 
                global OnlyDate
                global OnlyTime
                OnlyDate = currentdateandtime.date()
                OnlyTime = currentdateandtime.time()
                #print(OnlyDate)
                #print(OnlyTime)

                studentWindow()

            

        elif Username == Dusername and Password == Dpassword and Dusertype == "staff":

                # Save current date and time
                currentdateandtime = datetime.now()
                 
                OnlyDate = currentdateandtime.date()
                OnlyTime = currentdateandtime.time()

                staffWindow()

        elif Username == Dusername and Password == Dpassword and Dusertype == "administrator":

                adminWindow()
    
    except TypeError: # Handles the typeerror exception as input does not match database
           
                messagebox.showerror("Error", "Username or Password is wrong")
                entryUsername.delete(0, "end")
                entryPassword.delete(0, "end")

 

# create Label
LabelHeading = tk.Label(text="Welcome to UOW Booking System", bg="cyan", width="55", height="2", font=("Calibri", 16))
LabelHeading.grid(column=0,row=0)

label1 = tk.Label(text="Login" , font=("Calibri", 16))
label1.place(x=280, y=70)
label2 = tk.Label(text="Username" ,font=("Calibri", 12))
label2.place(x=135, y=130)
label3 = tk.Label(text="Password" ,font=("Calibri", 12))
label3.place(x=135, y=155)

 # create entry field
entryUsername = tk.Entry(width="30")
entryUsername.place(x=215,y=133)
entryPassword = tk.Entry(width="30")
entryPassword.config(show="*")
entryPassword.place(x=215,y=158)

# create button
buttonlogin = tk.Button(text="Login", command=login)
buttonlogin.place(x=285,y=190)

# display the window
window.mainloop()

# -------------------------------------------------------------------- LOGIN END ------------------------------------------------------------------------