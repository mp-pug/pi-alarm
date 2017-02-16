#!/usr/bin/python


from Tkinter import *
from threading import Thread
from threading import Lock
import vlc
import os
import time
import pandas as pd
import eyed3
import urllib
import urllib2 
import random




class Music_Player_Frames:

    def __init__(self,master,Music_Player,media_root_directory,ch_df):

        self.Music_Player=Music_Player
        eyed3.log.setLevel("ERROR")
        # set current path 
        self.current_path=media_root_directory
        self.playlist_index=[0]*2
        self.button_view_flag=False
        self.channel_frames_max=0
        self.channel_frame_index=0
        self.repeat_state=0
        self.random_state=0
        self.time_val=0
        self.playlist_lock=Lock()
        self.listbox_lock=Lock()

       # Create Music Player Frame
        self.music_player_frame=Frame(master)
        self.music_player_frame.grid(row=1,column=0,sticky="nsew")

        # Create Title Frame on the left hand side
        self.music_player_title_frame=Frame(self.music_player_frame)
        self.music_player_title_frame.grid(row=0,column=0,sticky="nsew")
        self.music_player_frame.grid_rowconfigure(0,weight=1)
        self.music_player_frame.grid_columnconfigure(0,weight=1)

        self.title_label=Label(self.music_player_title_frame,text="Pi Alarm Music Player",width=30)
        self.music_player_title_frame.grid_rowconfigure(0,weight=1)
        self.music_player_title_frame.grid_columnconfigure(0,weight=1)
        self.title_label.grid(row=0,column=0,sticky="nsew")

        self.time_label=Label(self.music_player_title_frame,text="00:00/00:00",justify=CENTER)
        self.time_label.grid(row=1,column=0,sticky="se")


        self.music_player_play_mode_frame=Frame(self.music_player_title_frame)
        self.music_player_play_mode_frame.grid(row=2,column=0,sticky="nsew")

        self.repeat_btn=Button(self.music_player_play_mode_frame,text="Repeat None",command=self.change_repeat_mode)
        self.repeat_btn.pack(side=LEFT)

        self.random_btn=Button(self.music_player_play_mode_frame,text="Random Off",command=self.change_random_mode)
        self.random_btn.pack(side=LEFT)

        # Create Folder content box to scroll through the mediathek
        # Init the current path 

        self.folder_scrollbar = Scrollbar(self.music_player_title_frame)
        self.folder_content_box=Listbox(self.music_player_title_frame,yscrollcommand=self.folder_scrollbar.set)
        self.folder_scrollbar.grid(row=3,column=1,sticky="ns") 
        self.folder_content_box.grid(row=3,column=0,sticky="nsew")
        self.folder_scrollbar.config(command=self.folder_content_box.yview)
        self.folder_content_box.bind('<Double-1>',lambda x: self.seek_folder_content_foward())
        self.folder_content_box.bind('<Button-3>', self.show_folder_content_popup)

        self.folder_control_frame=Frame(self.music_player_title_frame)
        self.folder_control_frame.grid(row=4,column=0)

        self.folder_backwards_btn=Button(self.folder_control_frame,text="back",command=self.seek_folder_content_backwards)
        self.folder_backwards_btn.pack(side=LEFT)

        self.file_folder_scrollbar=Scrollbar(self.music_player_title_frame)
        self.file_folder_content_box=Listbox(self.music_player_title_frame,yscrollcommand=self.file_folder_scrollbar.set)
        self.file_folder_scrollbar.grid(row=5,column=1,sticky="ns")
        self.file_folder_content_box.grid(row=5,column=0,sticky="nsew")
        self.file_folder_scrollbar.config(command=self.file_folder_content_box.yview)
        self.file_folder_content_box.bind('<Double-1>',lambda x:self.append_file_to_playlist())




        # Create Playlist Frame on the rhs
        self.music_player_playlist_frame=Frame(self.music_player_frame)
        self.music_player_playlist_frame.grid(row=0,column=1,sticky="nsew")
        self.music_player_frame.grid_columnconfigure(1,weight=1)

        self.playlist_scrollbar=Scrollbar(self.music_player_playlist_frame)

        self.music_player_playlist=Listbox(self.music_player_playlist_frame,yscrollcommand=self.playlist_scrollbar.set)
        self.music_player_playlist.grid(row=0,column=0,sticky="nsew")
        self.playlist_scrollbar.grid(row=0,column=1,sticky="ns")
        self.music_player_playlist_frame.grid_rowconfigure(0,weight=1)
        self.music_player_playlist_frame.grid_columnconfigure(0,weight=1)
        self.playlist_scrollbar.config(command=self.music_player_playlist.yview)
        self.music_player_playlist.bind('<Double-1>', lambda x:self.play_list_song())
        self.music_player_playlist.bind('<Button-3>', self.show_playlist_popup)
        self.music_player_playlist.bind('<B1-Motion>', self.shift_entry)       

        # Create Music player control frame
        self.music_player_control_frame=Frame(master)
        self.music_player_control_frame.grid(row=2,column=0,sticky="nsew")

        self.music_player_play_btn=Button(self.music_player_control_frame,text="Play",command=self.Music_Player.play_music)
        self.music_player_play_btn.pack(side=LEFT)

        self.music_player_pause_btn=Button(self.music_player_control_frame,text="Pause",command=self.Music_Player.pause)
        self.music_player_pause_btn.pack(side=LEFT)

        self.music_player_stop_btn=Button(self.music_player_control_frame,text="Stop",command=self.stop_music)
        self.music_player_stop_btn.pack(side=LEFT)

        self.music_player_prev_btn=Button(self.music_player_control_frame,text="<<",command=self.Music_Player.play_previous_song)
        self.music_player_prev_btn.pack(side=LEFT)

        self.music_player_prev_seek_btn=Button(self.music_player_control_frame,text="<",command=self.Music_Player.seek_backwards)
        self.music_player_prev_seek_btn.pack(side=LEFT)

        self.music_player_next_seek_btn=Button(self.music_player_control_frame,text=">",command=self.Music_Player.seek_forward)
        self.music_player_next_seek_btn.pack(side=LEFT)

        self.music_player_next_btn=Button(self.music_player_control_frame,text=">>",command=self.Music_Player.play_next_song)
        self.music_player_next_btn.pack(side=LEFT)


        self.music_player_change_view=Button(self.music_player_control_frame,text="View",command=lambda:Thread(target=self.switch_view,args=(master,)).start() )
        self.music_player_change_view.pack(side=RIGHT)

        self.music_player_clear_playlist=Button(self.music_player_control_frame,text="-",command=self.delete_playlist)
        self.music_player_clear_playlist.pack(side=RIGHT)

        self.music_player_save_playlist=Button(self.music_player_control_frame,text="Save As",command=self.export_media_list)
        self.music_player_save_playlist.pack(side=RIGHT)

        self.music_player_previous_channel_frame=Button(self.music_player_control_frame,text="<<",command=self.raise_previous_channel_frame)
        self.music_player_previous_channel_frame.pack(side=RIGHT)
        self.music_player_previous_channel_frame.pack_forget()

        self.music_player_next_channel_frame=Button(self.music_player_control_frame,text=">>",command=self.raise_next_channel_frame)
        self.music_player_next_channel_frame.pack(side=RIGHT)
        self.music_player_next_channel_frame.pack_forget()

        #create popup menu for folder content


        self.folder_popup=Menu(self.folder_content_box,tearoff=0)
#        self.folder_popup.add_command(label="Add Selection to Playlist",command=self.start_append_thread)
        self.folder_popup.add_command(label="Add Selection to Playlist",command=lambda:Thread(target=self.append_folder_to_playlist,args=()).start())
        self.playlist_popup=Menu(self.music_player_playlist,tearoff=0)
        self.playlist_popup.add_command(label="Delete Selection",command=self.delete_track)


        # Create Radio Frames
        self.ch_df=ch_df
        self.radio_frame_max=0
        self.btn_frame_count=0
        self.channel_index=[0]*2
        self.current_radio_channel=""
        self.master=master
    
        # radio control frame
        # add the control buttons
        self.radio_control_frame = Frame(master)
        self.radio_control_frame.grid(row=2,column=0,sticky="nsew")

        self.stream_stop_btn=Button(self.radio_control_frame,text='Stop',command=self.stop_radio_channel)
        self.stream_stop_btn.pack(side=LEFT)


        self.next_btn=Button(self.radio_control_frame,text='>>',command=self.next_radio_channel_frame)
        self.next_btn.pack(side=RIGHT)
        self.prev_btn=Button(self.radio_control_frame,text='<<',command=self.prev_radio_channel_frame)
        self.prev_btn.pack(side=RIGHT)





        # Create Event manager and attach events 
	list_player_event_manager=self.Music_Player.List_Player_Instance.event_manager()
        list_player_event_manager.event_attach(vlc.EventType.MediaListPlayerNextItemSet,lambda x: self.refresh_title_label())
        file_player_event_manager=self.Music_Player.File_Player_Instance.event_manager()
        file_player_event_manager.event_attach(vlc.EventType.MediaPlayerTimeChanged,lambda x: self.update_display_values())


        # Call init methods 
        self.show_folder_content()
        self.refresh_playlist()
        self.load_media_list("current_playlist.m3u")
        self.create_radio_channel_buttons()
#--------------------- Methods -------------------------


    def raise_player_frames(self):

        if self.button_view_flag:
            self.music_player_pause_btn.pack_forget()
            self.music_player_change_view.pack_forget()
            self.music_player_previous_channel_frame.pack_forget()
            self.music_player_next_channel_frame.pack_forget()

            self.music_player_play_btn.pack(side=LEFT)
            self.music_player_pause_btn.pack(side=LEFT)
            self.music_player_stop_btn.pack(side=LEFT)
            self.music_player_prev_btn.pack(side=LEFT)
            self.music_player_prev_seek_btn.pack(side=LEFT)
            self.music_player_next_seek_btn.pack(side=LEFT)
            self.music_player_next_btn.pack(side=LEFT) 
            self.music_player_change_view.pack(side=RIGHT)
            self.music_player_clear_playlist.pack(side=RIGHT)
            self.button_view_flag=False

        self.music_player_frame.tkraise()
        self.music_player_control_frame.tkraise()


    def stop_music(self):
        self.Music_Player.stop_music()
        if hasattr(self,'ch_btns') and len(self.ch_btns)>self.playlist_index[1]:
            self.ch_btns[self.playlist_index[0]].configure(fg='Black')
            self.ch_btns[self.playlist_index[1]].configure(fg='Black')
        self.music_player_playlist.itemconfig(self.playlist_index[0],{'fg':'black'})
        self.music_player_playlist.itemconfig(self.playlist_index[1],{'fg':'black'})
        self.title_label.config(text="Pi Alarm Music Player")
        self.time_label.config(text="00:00/00:00")

    def raise_next_channel_frame(self):
        if self.channel_frame_index<self.channel_frames_max-1:
            self.channel_frame_index+=1
        self.raise_channel_frame_index(self.channel_frame_index)

    def raise_previous_channel_frame(self):
        if self.channel_frame_index>0:
            self.channel_frame_index-=1
        self.raise_channel_frame_index(self.channel_frame_index)

    def raise_channel_frame_index(self,index):
        self.channel_frames[index].tkraise()


    def seek_folder_content_foward(self):
        self.current_path+=os.sep+self.folder_content_box.get(self.folder_content_box.curselection()[0])+os.sep
        self.show_folder_content() 

    def seek_folder_content_backwards(self):
        split_path=self.current_path.split(os.sep)

        self.current_path=os.sep
        for p in split_path[:-2]:
            if not p=="":
                self.current_path+=p+os.sep

        self.show_folder_content()


    def show_folder_content(self):
        self.folder_content_box.delete(0,END)
        self.file_folder_content_box.delete(0,END)
        folder_content=next(os.walk(self.current_path)) 
        for fd in folder_content[1]:
            self.folder_content_box.insert(END,fd)

        for fl in folder_content[2]:
            self.file_folder_content_box.insert(END,fl)

    def append_file_to_playlist(self):
        title=self.file_folder_content_box.get(self.file_folder_content_box.curselection())
        mrl=self.current_path+os.sep+title

        self.Music_Player.append_file_to_playlist(mrl)
        self.refresh_playlist()
        
        if self.random_state:
            self.Music_Player.create_random_playlist()



    def append_folder_to_playlist(self): 
        try:
            subdir=self.current_path+os.sep+self.folder_content_box.get(self.folder_content_box.curselection()[0])

            for r,d,f in os.walk(subdir):
                for ff in f:
                    title=ff
                    tt_split=title.split(".")
                    if tt_split[-1]=="mp3" or tt_split[-1]=="wma":
                        mrl=os.path.join(r,ff)
                        self.playlist_lock.acquire()
                        self.Music_Player.append_file_to_playlist(mrl)
                        self.playlist_lock.release()
            self.refresh_playlist()

            if self.random_state:
                self.Music_Player.create_random_playlist()
        except:
            pass

    def refresh_playlist(self):
        self.music_player_playlist.delete(0,END)
        for i in range(self.Music_Player.count()):
            path= urllib.unquote(self.Music_Player.playlist.item_at_index(i).get_mrl())
            tag=path.split(os.sep)
            try:
                track= eyed3.load(path[7:])
                self.music_player_playlist.insert(END,track.tag.artist+" - "+track.tag.title)
            except:
                self.music_player_playlist.insert(END,tag[-1])

        self.refresh_title_label()

    def create_button_labels(self):
        labels=[None]*self.Music_Player.count()
        for i in range(self.Music_Player.count()):
            path= urllib.unquote(self.Music_Player.playlist.item_at_index(i).get_mrl())
            tag=path.split(os.sep)

            try:
                track= eyed3.load(path[7:])
                labels[i]=track.tag.artist+"\n"+track.tag.title
            except:
                labels[i]=tag[-1]

        return labels

    def show_folder_content_popup(self,event):
        try:
            self.folder_popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.folder_popup.grab_release()

    def show_playlist_popup(self,event):
        try:
            self.playlist_popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.playlist_popup.grab_release()



    def delete_track(self):
        try:
            self.Music_Player.playlist.lock()
            if self.music_player_playlist.curselection()[0]==self.playlist_index[0]:
               self.playlist_index[0]=0;
            self.playlist_lock.acquire()
            self.Music_Player.playlist.remove_index(self.music_player_playlist.curselection()[0])
            self.playlist_lock.release()
            self.Music_Player.playlist.unlock()

            self.listbox_lock.acquire()
            self.refresh_playlist()
            self-listbox_lock.release()

            if self.random_state:
                self.Music_Player.create_random_playlist()
        except :
            self.Music_Player.playlist.unlock()
            pass


    def delete_playlist(self):
        self.playlist_lock.acquire()
        self.Music_Player.delete_playlist()
        self.playlist_lock.release()
        self.playlist_index[0]=0
        self.channel_frame_index=0 
        self.refresh_playlist()
    
    def update_display_values(self):
        self.refresh_time_label()
        t=self.Music_Player.File_Player_Instance.get_time()/1000    
         
        if t%5==0 and self.time_val%5!=0:
            self.refresh_title_label()
        self.time_val=t       

    def refresh_time_label(self):
        self.time_label.config(text=self.Music_Player.get_time()+"/"+self.Music_Player.get_duration(),justify=CENTER  )

    def refresh_title_label(self):
        if self.Music_Player.player_state==2:
            if self.Music_Player.playlist.index_of_item(self.Music_Player.File_Player_Instance.get_media())!= -1:
                path= urllib.unquote(self.Music_Player.File_Player_Instance.get_media().get_mrl())
                tag=path.split(os.sep)
                self.playlist_index[1]=self.Music_Player.playlist.index_of_item(self.Music_Player.File_Player_Instance.get_media())
                
                if hasattr(self,'ch_btns') and len(self.ch_btns)>self.playlist_index[1]:
                    self.ch_btns[self.playlist_index[0]].configure(fg='Black')
                    self.ch_btns[self.playlist_index[1]].configure(fg='Blue')
                self.music_player_playlist.itemconfig(self.playlist_index[0],{'fg':'black'})
                self.music_player_playlist.itemconfig(self.playlist_index[1],{'fg':'blue'})
                self.radio_ch_btns[self.channel_index[0]].configure(fg='Black')
                self.radio_ch_btns[self.channel_index[1]].configure(fg='Black')

                self.playlist_index[0]=self.playlist_index[1]
                try:
                    track= eyed3.load(path[7:])
                    self.title_label.config(text=track.tag.artist+" - "+track.tag.title)
                except:
                    self.title_label.config(text=tag[-1])

            else:
                if self.Music_Player.File_Player_Instance.get_media()!=None:
                    path= urllib.unquote(self.Music_Player.File_Player_Instance.get_media().get_mrl())
                    tag=path.split(os.sep) 
                    try:
                        track= eyed3.load(path[7:])
                        self.title_label.config(text=track.tag.artist+" - "+track.tag.title)
                    except:
                        self.title_label.config(text=tag[-1])


        if self.Music_Player.player_state==1:
            request = urllib2.Request(self.Music_Player.File_Player_Instance.get_media().get_mrl())
            try:
                request.add_header('Icy-MetaData', 1)
                response = urllib2.urlopen(request)
                icy_metaint_header = response.headers.get('icy-metaint')
                if icy_metaint_header is not None:
                    metaint = int(icy_metaint_header)
                    read_buffer = metaint+255
                    content = response.read(read_buffer)
                    title = content[metaint:].split("'")[1]
                    self.title_label.config(text=title) 
            except:
                self.title_label.config(text=self.current_radio_channel)

            
    def raise_button_playlist_view(self,master):
        # Create panels for control and channel buttons
        row_n= 4
        column_n = 4
        frame_n= row_n*column_n
        btn_height=10;
        btn_width=15;

        frame_max=((self.Music_Player.count()-self.Music_Player.count()%(frame_n))/(frame_n))+1
        self.channel_frames_max=frame_max
        self.channel_frames = frame_max*[None]

        labels=self.create_button_labels()
        # add the channel buttons
        self.ch_btns=self.Music_Player.count()*[None]

        for i in range(0,frame_max):
            self.channel_frames[i]=Frame(master)
            self.channel_frames[i].grid(row=1,column=0,sticky="nsew")
            if i==frame_max-1:
                r_max=(((self.Music_Player.count()%frame_n)-((self.Music_Player.count()%frame_n)%column_n))/column_n)+1 
                for j in range(0,r_max):
                    if j==r_max-1:
                        for k in range(0,(self.Music_Player.count()%frame_n)%column_n):
                            self.ch_btns[i*frame_n+j*row_n+k]=Button(self.channel_frames[i],text=labels[i*frame_n+j*row_n+k],command=lambda l=(i*frame_n+j*row_n+k):self.play_button_song(l),height=btn_height,width=btn_width )
                            self.ch_btns[i*frame_n+j*row_n+k].grid(row=j,column=k,sticky="nsew")
                    else:
                        for k in range(0,column_n):
                            self.ch_btns[i*frame_n+j*row_n+k]=Button(self.channel_frames[i],text=labels[i*frame_n+j*row_n+k],command=lambda l=(i*frame_n+j*row_n+k):self.play_button_song(l),height=btn_height,width=btn_width )
                            self.ch_btns[i*frame_n+j*row_n+k].grid(row=j,column=k,sticky="nsew")

            else:
                for j in range(0,row_n):    
                    for k in range(0,column_n):
                        self.ch_btns[i*frame_n+j*row_n+k]=Button(self.channel_frames[i],text=labels[i*frame_n+j*row_n+k],command=lambda l=(i*frame_n+j*row_n+k):self.play_button_song(l),height=btn_height,width=btn_width )
                        self.ch_btns[i*frame_n+j*row_n+k].grid(row=j,column=k,sticky="nsew")

        self.channel_frames[0].tkraise()
        self.refresh_title_label()

    def play_button_song(self,index):
        self.Music_Player.play_list_song_index(index)
        
    def switch_view(self,master):
        if self.button_view_flag:
            self.music_player_frame.tkraise()
            self.music_player_pause_btn.pack_forget()
            self.music_player_change_view.pack_forget()
            self.music_player_previous_channel_frame.pack_forget()
            self.music_player_next_channel_frame.pack_forget()

            self.music_player_play_btn.pack(side=LEFT)
            self.music_player_pause_btn.pack(side=LEFT)
            self.music_player_stop_btn.pack(side=LEFT)
            self.music_player_prev_btn.pack(side=LEFT)
            self.music_player_prev_seek_btn.pack(side=LEFT)
            self.music_player_next_seek_btn.pack(side=LEFT)
            self.music_player_next_btn.pack(side=LEFT) 
            self.music_player_change_view.pack(side=RIGHT)
            self.music_player_clear_playlist.pack(side=RIGHT)
            self.button_view_flag=False
        else:
            self.raise_button_playlist_view(master)
            self.raise_channel_frame_index(self.channel_frame_index) 
            self.music_player_play_btn.pack_forget()      
            self.music_player_pause_btn.pack_forget()  
            self.music_player_stop_btn.pack_forget()  
            self.music_player_prev_btn.pack_forget()   
            self.music_player_prev_seek_btn.pack_forget()  
            self.music_player_next_seek_btn.pack_forget()  
            self.music_player_next_btn.pack_forget()   
            self.music_player_change_view.pack_forget()   
            self.music_player_clear_playlist.pack_forget()

            self.music_player_pause_btn.pack(side=LEFT)
            self.music_player_change_view.pack(side=RIGHT)
            self.music_player_next_channel_frame.pack(side=RIGHT)
            self.music_player_previous_channel_frame.pack(side=RIGHT)
            self.button_view_flag=True

    def play_list_song(self):
        self.Music_Player.play_list_song_index(self.music_player_playlist.curselection()[0])
        #self.refresh_title_label()

    def shift_entry(self,event):
        self.Music_Player.playlist.lock()
        i = self.music_player_playlist.nearest(event.y)

        if i < self.music_player_playlist.curselection()[0]:
            x = self.music_player_playlist.get(i)
            self.music_player_playlist.delete(i)
            media = self.Music_Player.playlist.item_at_index(i)
            self.Music_Player.playlist.remove_index(i)
            self.music_player_playlist.insert(i+1,x)
            self.Music_Player.playlist.insert_media(media,i+1)

        elif i > self.music_player_playlist.curselection()[0]:
            x = self.music_player_playlist.get(i)
            self.music_player_playlist.delete(i)
            media = self.Music_Player.playlist.item_at_index(i)
            self.Music_Player.playlist.remove_index(i)
            self.music_player_playlist.insert(i-1,x)
            self.Music_Player.playlist.insert_media(media,i-1)

        self.Music_Player.playlist.unlock()  

        #for i in range(self.playlist.count()):
        #    print self.playlist.item_at_index(i).get_mrl()

        self.refresh_title_label()

    def change_repeat_mode(self):
        self.repeat_state+=1
        self.repeat_state=self.repeat_state%3
        

        if self.repeat_state==0:
            self.repeat_btn.config(text="Repeat None")
            self.Music_Player.List_Player_Instance.set_playback_mode(0)

        if self.repeat_state==1:
            self.repeat_btn.config(text="Repeat One")
            self.Music_Player.List_Player_Instance.set_playback_mode(2)

        if self.repeat_state==2:
            self.repeat_btn.config(text="Repeat All")
            self.Music_Player.List_Player_Instance.set_playback_mode(1)
        
    def change_random_mode(self):
        self.random_state= not self.random_state
        self.Music_Player.set_random_mode(self.random_state)
        if self.random_state:
            self.random_btn.config(text="Random On")
            self.Music_Player.create_random_playlist()
        else:
            self.random_btn.config(text="Random Off")
   
    def load_media_list(self,path):
        if os.path.isfile(path):
            f=open(path,'r')
            for line in f:
                if list(line)[0]!='#' and list(line)[0]!=" ":
                    self.Music_Player.playlist.add_media(line.rstrip(os.linesep))
            self.refresh_playlist()
            f.close()

    def export_media_list(self,path):
        if self.random_state:
            medialist=self.Music_Player.randomlist
        else:
            medialist=self.Music_Player.playlist

        f=open(path,'w')
        f.write("#EXTM3U \n")
        for i in range(medialist.count()):
            path= urllib.unquote(medialist.item_at_index(i).get_mrl())
            tag=path.split(os.sep)
               
            try:
                track= eyed3.load(path[7:])
                title_artist=track.tag.artist+" - "+track.tag.title
            except:
                title_artist=tag[-1]

            f.write("#EXTINF:"+str(vlc.libvlc_media_get_duration(medialist.item_at_index(i))/1000.0)+" "+title_artist)
            f.write(os.linesep)
            f.write(path[7:])
            f.write(os.linesep)

        f.close()


        
    def create_radio_channel_buttons(self):
        # Create panels for control and channel buttons
        row_n= 4
        column_n = 4
        frame_n= row_n*column_n
        btn_height=10;
        btn_width=15;

        self.radio_frame_max=((self.ch_df.shape[0]-self.ch_df.shape[0]%(frame_n))/(frame_n))+1
        self.radio_channel_frames = self.radio_frame_max*[None]

        
        # add the channel buttons
        self.radio_ch_btns=self.ch_df.shape[0]*[None]
        for i in range(0,self.radio_frame_max):
            self.radio_channel_frames[i]=Frame(self.master)
            self.radio_channel_frames[i].grid(row=1,column=0,sticky="nsew")
            if i==self.radio_frame_max-1:
                r_max=(((self.ch_df.shape[0]%frame_n)-((self.ch_df.shape[0]%frame_n)%column_n))/column_n)+1 
                for j in range(0,r_max):
                    if j==r_max-1:
                        for k in range(0,(self.ch_df.shape[0]%frame_n)%column_n):
                            self.radio_ch_btns[i*frame_n+j*row_n+k]=Button(self.radio_channel_frames[i],text=self.create_radio_button_label(self.ch_df.Channel[i*frame_n+j*row_n+k]),command=lambda l=(i*frame_n+j*row_n+k):self.play_radio_channel(l),height=btn_height,width=btn_width )
                            self.ch_btns[i*frame_n+j*row_n+k].grid(row=j,column=k,sticky="nsew")
                    else:
                        for k in range(0,column_n):
                            self.radio_ch_btns[i*frame_n+j*row_n+k]=Button(self.radio_channel_frames[i],text=self.create_radio_button_label(self.ch_df.Channel[i*frame_n+j*row_n+k]),command=lambda l=(i*frame_n+j*row_n+k):self.play_radio_channel(l),height=btn_height,width=btn_width )
                            self.radio_ch_btns[i*frame_n+j*row_n+k].grid(row=j,column=k,sticky="nsew")
            else:
                for j in range(0,row_n):    
                    for k in range(0,column_n):
                        self.radio_ch_btns[i*frame_n+j*row_n+k]=Button(self.radio_channel_frames[i],text=self.create_radio_button_label(self.ch_df.Channel[i*frame_n+j*row_n+k]),command=lambda l=(i*frame_n+j*row_n+k):self.play_radio_channel(l),height=btn_height,width=btn_width )
                        self.radio_ch_btns[i*frame_n+j*row_n+k].grid(row=j,column=k,sticky="nsew")
        
        # raise the first channel frame 
        self.radio_channel_frames[0].tkraise()




    def create_radio_button_label(self,text):
        indices=list()
        for i in range(len(text)):
            if text[i]==" " or text[i]=="#" or text[i]=="!" or text[i]=="?" or text[i]=="-":
                indices.append(i)
        indices.append(len(text))
        text=list(text)
        line_sum=0
        for i in range(0,len(indices)):
            if i==0:
                diff=indices[0]
            else:
                diff=indices[i]-indices[i-1]
            if (line_sum+diff)>6:
                if indices[i]!=len(text):
                    text[indices[i]]="\n"
                line_sum=0
            else:
                line_sum+=diff
        return "".join(text) 

    
    def next_radio_channel_frame(self):
        if self.btn_frame_count<self.radio_frame_max-2:
            self.btn_frame_count+=1
            self.radio_channel_frames[self.btn_frame_count].tkraise()

    def prev_radio_channel_frame(self):
        if self.btn_frame_count>0:
            self.btn_frame_count-=1
            self.radio_channel_frames[self.btn_frame_count].tkraise()

    def raise_radio_frames(self):
        self.radio_channel_frames[self.btn_frame_count].tkraise()
        self.radio_control_frame.tkraise()

    def play_radio_channel(self,index):
        self.Music_Player.play_radio_channel(self.ch_df.Stream[index])
        self.current_radio_channel=self.ch_df.Channel[index]
        self.time_val=0
        self.channel_index[0]=self.channel_index[1]
        self.channel_index[1]=index
        self.radio_ch_btns[self.channel_index[0]].configure(fg='Black')
        self.radio_ch_btns[self.channel_index[1]].configure(fg='Blue')
        
        if hasattr(self,'ch_btns') and len(self.ch_btns)>self.playlist_index[1]:
            self.ch_btns[self.playlist_index[0]].configure(fg='Black')
            self.ch_btns[self.playlist_index[1]].configure(fg='Black')
        self.music_player_playlist.itemconfig(self.playlist_index[0],{'fg':'black'})
        self.music_player_playlist.itemconfig(self.playlist_index[1],{'fg':'black'})

           

    def stop_radio_channel(self):
        self.Music_Player.stop_radio()
        self.radio_ch_btns[self.channel_index[0]].configure(fg='Black')
        self.radio_btns[self.channel_index[1]].configure(fg='Black')
        self.title_label.config(text="Pi Alarm Music Player")
        self.time_label.config(text="00:00/00:00")
