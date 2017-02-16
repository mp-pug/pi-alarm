#!/usr/bin/python

from Tkinter import *

class Alarm_Clock_Frames:

    def __init__(self,master,alarm_clock):

        self.alarm_clock=alarm_clock
        self.toplevel_raised=False
        self.alarm_clock_frame=Frame(master)
        self.alarm_clock_frame.grid(row=1,column=0,sticky="nsew")

        # Create Date and Time labels
        self.time_label=Label(self.alarm_clock_frame,text="",font=("Courier",74),justify=CENTER,pady=25)
        self.time_label.pack(fill=X)

        self.date_label=Label(self.alarm_clock_frame,text="",font=("Courier",36),justify=CENTER)
        self.date_label.pack(fill=X)

        # Create Canvas containing alarm list
        self.alarm_clock_view=Frame(self.alarm_clock_frame)
        self.alarm_clock_view.pack(fill=BOTH,expand=True)
        
        self.alarm_scrollbar=Scrollbar(self.alarm_clock_view)
        self.alarm_clock_canvas=Canvas(self.alarm_clock_view,yscrollcommand=self.alarm_scrollbar.set)
        self.alarm_clock_canvas.pack(fill=BOTH,side=LEFT)
        
        self.alarm_scrollbar.pack(side=RIGHT,fill=Y)

        self.alarm_scrollbar.config(command=self.alarm_clock_canvas.yview)
         

        #Create Alarm Clock control Frame
        self.alarm_clock_control_frame=Frame(master)
        self.alarm_clock_control_frame.grid(row=2,column=0,sticky="nsew")

        self.add_alarm_btn=Button(self.alarm_clock_control_frame,text="+",command=self.add_alarm)
        self.add_alarm_btn.pack(side=RIGHT)


        self.add_alarm_frames()
        
    def raise_frames(self):
        self.alarm_clock_frame.tkraise()
        self.alarm_clock_control_frame.tkraise()
        


    def add_alarm_frames(self):
        pady=5
        days = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
        self.alarm_frames=[None]*self.alarm_clock.alarms.shape[0]
        self.time_labels=[None]*self.alarm_clock.alarms.shape[0]
        self.description_labels=[None]*self.alarm_clock.alarms.shape[0]
        self.day_btn_frames=[None]*self.alarm_clock.alarms.shape[0]
        self.day_btns=[ [None]*7 for i in range(self.alarm_clock.alarms.shape[0])]
        self.edit_btns=[None]*self.alarm_clock.alarms.shape[0]
        for i in range(self.alarm_clock.alarms.shape[0]):
            self.alarm_frames[i]=Frame(self.alarm_clock_canvas)
            self.alarm_frames[i].grid(row=i,column=0,sticky="ew")
            self.time_labels[i]=Label(self.alarm_frames[i],text=str(self.alarm_clock.alarms.iloc[i]['time_h']).zfill(2)+":"+str(self.alarm_clock.alarms.iloc[i]['time_min']).zfill(2))
            self.time_labels[i].grid(row=0,column=0,ipady=pady)
            self.description_labels[i]=Label(self.alarm_frames[i],text=self.alarm_clock.alarms.iloc[i]['description'])
            self.description_labels[i].grid(row=0,column=1,ipady=pady)
            self.day_btn_frames[i]=Frame(self.alarm_frames[i])
            self.day_btn_frames[i].grid(row=0,column=2,ipady=pady)
            for j in range(7):
                self.day_btns[i][j]=Button(self.day_btn_frames[i],text=days[j],command=lambda l=i,k=j:self.change_day_state(l,k))
                self.day_btns[i][j].pack(side=LEFT)
                self.update_button_state(i,j)
            self.edit_btns[i]=Button(self.alarm_frames[i],text="Edit",command=lambda l=i:self.edit_alarm(l))
            self.edit_btns[i].grid(row=0,column=3,ipady=pady)
            for j in range(4):
                self.alarm_frames[i].columnconfigure(j,weight=1)
   

    def change_day_state(self,i,j):
        if j==0:
            if self.alarm_clock.alarms.iloc[i]['sun']==1:
                self.alarm_clock.alarms.set_value(i,'sun',0)
            else:
                self.alarm_clock.alarms.set_value(i,'sun',1)
        if j==1:
            if self.alarm_clock.alarms.iloc[i]['mon']==1:
                self.alarm_clock.alarms.set_value(i,'mon',0)
            else:
                self.alarm_clock.alarms.set_value(i,'mon',1)
        if j==2:
            if self.alarm_clock.alarms.iloc[i]['tue']==1:
                self.alarm_clock.alarms.set_value(i,'tue',0)
            else:
                self.alarm_clock.alarms.set_value(i,'tue',1)
        if j==3:
            if self.alarm_clock.alarms.iloc[i]['wed']==1:
                self.alarm_clock.alarms.set_value(i,'wed',0)
            else:
                self.alarm_clock.alarms.set_value(i,'wed',1)
        if j==4:
            if self.alarm_clock.alarms.iloc[i]['thu']==1:
                self.alarm_clock.alarms.set_value(i,'thu',0)
            else:
                self.alarm_clock.alarms.set_value(i,'thu',1)
        if j==5:
            if self.alarm_clock.alarms.iloc[i]['fri']==1:
                self.alarm_clock.alarms.set_value(i,'fri',0)
            else:
                self.alarm_clock.alarms.set_value(i,'fri',1)
        if j==6:
            if self.alarm_clock.alarms.iloc[i]['sat']==1:
                self.alarm_clock.alarms.set_value(i,'sat',0)
            else:
                self.alarm_clock.alarms.set_value(i,'sat',1)
       
        self.update_button_state(i,j)


    def update_button_state(self,i,j):    
        if j==0:
            if self.alarm_clock.alarms.iloc[i]['sun']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
                
        if j==1:
            if self.alarm_clock.alarms.iloc[i]['mon']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
        if j==2:
            if self.alarm_clock.alarms.iloc[i]['tue']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
        if j==3:
            if self.alarm_clock.alarms.iloc[i]['wed']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
        if j==4:
            if self.alarm_clock.alarms.iloc[i]['thu']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
        if j==5:
            if self.alarm_clock.alarms.iloc[i]['fri']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
        if j==6:
            if self.alarm_clock.alarms.iloc[i]['sat']==1:
                self.day_btns[i][j].configure(fg="White",bg="Black")
            else:
                self.day_btns[i][j].configure(fg="Black",bg="White")
       


    def set_time_label(self,label_text):
        self.time_label.config(text=label_text)
 
    def set_date_label(self,label_text):
        self.date_label.config(text=label_text)

    def edit_alarm(self,index):
        print "edit_alarm"



    def add_alarm(self):
        if  not self.toplevel_raised:
            self.toplevel_raised=True
            toplevel=Toplevel()
            toplevel.protocol("WM_DELETE_WINDOW",lambda: self.toplevel_closed(toplevel))
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

            time_select_frame=Frame(toplevel)
            time_select_frame.grid(row=0,column=0,sticky="nsew")

            hours_scrollbar=Scrollbar(time_select_frame)
            hours=Listbox(time_select_frame,height=1,yscrollcommand=hours_scrollbar.set)
            for i in range(24):
                hours.insert(END,str(i).zfill(2))
            hours.grid(row=0,column=0,sticky="nsew")
            hours_scrollbar.grid(row=0,column=1,sticky="ns")
            hours_scrollbar.config(command=hours.yview)
            time_sep_label=Label(time_select_frame,text=":")
            time_sep_label.grid(row=0,column=2,sticky="nsew")

            minutes=Listbox(time_select_frame,height=1)
            for i in range(60):
                minutes.insert(END,str(i).zfill(2))
            minutes.grid(row=0,column=3,sticky="nsew")

            alarm_select_frame=Frame(toplevel)
            alarm_select_frame.grid(row=1,column=0,sticky="nsew")


            control_frame=Frame(toplevel)
            control_frame.grid(row=2,column=0,sticky="nsew")
        
    def toplevel_closed(self,window):
        self.toplevel_raised=False
        self.add_alarm_frames()
        window.destroy()
