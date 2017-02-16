#!/usr/bin/python

from threading import Thread
import os
import vlc
import random
import urllib
class Music_Player:

    def __init__(self):
        
    
        self.random_state=False
        #
        # 0:   nothing playing
        # 1:   radio playing
        # 2:   playlist playing
        self.player_state=0
	# Create Instances for playing Media Files
	self.Instance=vlc.Instance()
	self.List_Player_Instance=self.Instance.media_list_player_new()
        self.File_Player_Instance=self.Instance.media_player_new()
        
        self.List_Player_Instance.set_media_player(self.File_Player_Instance)


	# Create Playlist
	self.playlist=vlc.MediaList()
        self.randomlist =vlc.MediaList()
        self.List_Player_Instance.set_media_list(self.playlist)


        

        
#--------------------- Methods -------------------------

    def play_next_song(self):

        self.List_Player_Instance.stop()
 
        if self.random_state:
            self.List_Player_Instance.set_media_list(self.randomlist)
            self.List_Player_Instance.play_item_at_index(self.randomlist.index_of_item(self.File_Player_Instance.get_media()))
 
        else:
            self.List_Player_Instance.set_media_list(self.playlist)
            self.List_Player_Instance.play_item_at_index(self.playlist.index_of_item(self.File_Player_Instance.get_media()))
           
 
        
        self.List_Player_Instance.next()




    def play_previous_song(self):


        self.List_Player_Instance.stop()
 
        
        if self.random_state:
            self.List_Player_Instance.set_media_list(self.randomlist)
            self.List_Player_Instance.play_item_at_index(self.randomlist.index_of_item(self.File_Player_Instance.get_media()))
 
        else:
            self.List_Player_Instance.set_media_list(self.playlist)
            self.List_Player_Instance.play_item_at_index(self.playlist.index_of_item(self.File_Player_Instance.get_media()))
        
        self.List_Player_Instance.previous()



    def play_music(self):

        self.player_state=2
        self.List_Player_Instance.stop()

        if self.random_state:
            self.create_random_playlist()
            self.List_Player_Instance.set_media_list(self.randomlist)
 

        else:
            self.List_Player_Instance.set_media_list(self.playlist)
        

        self.List_Player_Instance.play_item_at_index(0)
      

    def play_single_song(self,mrl):
        self.player_state=2
        self.List_Player_Instance.stop()
        self.File_Player_Instance.stop()

        single_song_playlist=vlc.MediaList([mrl])
        self.List_Player_Instance.set_media_list(single_song_playlist)
        self.List_Player_Instance.play_item_at_index(0)



    def play_list_song_index(self,index):
        self.player_state=2
        self.List_Player_Instance.stop()
        self.File_Player_Instance.stop()

        self.List_Player_Instance.set_media_list(self.playlist)
         
        
        self.List_Player_Instance.play_item_at_index(index)

        if self.random_state:
            self.List_Player_Instance.set_media_list(self.randomlist)
        else:
            self.List_Player_Instance.set_media_list(self.playlist) 
        



    def play_radio_channel(self,url):
        self.player_state=1
        Media_List = vlc.MediaList([url])
        self.List_Player_Instance.stop()
        self.File_Player_Instance.stop()
        self.List_Player_Instance.set_media_list(Media_List)
        self.List_Player_Instance.play()



    def stop_music(self):
        self.File_Player_Instance.stop()
        self.player_state=0 



    def pause(self):
	self.File_Player_Instance.pause()
        



    def stop_radio(self):
        self.List_Player_Instance.stop()
        self.player_state=0 



    def seek_forward(self):
        t=self.File_Player_Instance.get_position()+0.02
	if t<1:
            self.File_Player_Instance.set_position(t)
            



    def seek_backwards(self):
        t=self.File_Player_Instance.get_position()-0.02
	if t>0:
            self.File_Player_Instance.set_position(t)
            



    def append_file_to_playlist(self,mrl):
	self.playlist.add_media(mrl)
        



    def delete_playlist(self):
        
	self.playlist.lock()
        for i in range(self.playlist.count()):
            self.playlist.remove_index(0)

        self.playlist.unlock()

        self.create_random_playlist()
        



    def get_time(self):
 	time=self.File_Player_Instance.get_time()/1000
        mn,ss = divmod(time,60)
	return str(mn).zfill(2)+":"+str(ss).zfill(2)

    def get_duration(self):
        duration=self.File_Player_Instance.get_media().get_duration()/1000
        mnd,ssd=divmod(duration,60) 
	return str(mnd).zfill(2)+":"+str(ssd).zfill(2)

    def count(self):
	return self.playlist.count()


    def create_random_playlist(self):
        for i in range(self.randomlist.count()):
                self.randomlist.remove_index(0)

        if self.random_state and self.playlist.count()>1:
            rand_ind = range(self.playlist.count())
            random.shuffle(rand_ind)

            for i in rand_ind:
                self.randomlist.add_media(self.playlist.item_at_index(i))
                


             
    
    def set_random_mode(self,random_flag):
        self.random_state=random_flag
        

