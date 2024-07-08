import time

from tkinter import * #all classes of lib are imported
#more preferred than import tkinter or import tkinter as tk because
# in the former, we can directly call the functions as func() rather than tk.func() or tkinter.func()  
# tkinter - lib used to build basic GUIs
#time - lib used to conntect the GUI with time 

from tkinter import filedialog #filedialog module imported
#filedialog module-used where you need to ask the user to browse a file or a directory from the system here music files

from pygame import mixer #used for make the buttons functional
#PyGame library is used to create video games.
#This library includes several modules for playing sound, drawing graphics, handling mouse inputs, etc.
#mixer module-for loading and playing sounds is available and initialized before using it.

from PIL import Image, ImageTk, ImageSequence

import os
#The OS module in Python provides functions for creating and removing a directory (folder),
# fetching its contents, changing and identifying the current directory, etc.
#to build a video playing pannel

#import ttkbootstrap as tb
import tkinter.ttk as ttk
#In Python and Tkinter, ttk stands for "themed Tkinter," and it is part of the Tkinter library. The ttk module provides access to the Tk themed widget set, which includes a set of enhanced and modern-looking widgets compared to the standard Tkinter widgets.
#for song slider
import sys
from mutagen.mp3 import MP3

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



root= Tk()
'''"Tk()": Tk is short for Tkinter, which is the name of the library. The Tk() part is like telling Python to create a blank window where you can put buttons, text, and other things. It's like starting with an empty canvas for your graphical interface.

"root = ": This is like giving a name to the blank window you just created. Here, we're calling it "root," but you could choose a different name if you wanted to.

So, in simple terms, root = Tk() is like telling Python to create a new empty window for a graphical program, and we're calling that window "root" so we can refer to it later in our code.'''

root.geometry("595x700+290+10")
'''root.geometry():

This is a command in Tkinter that sets the size and position of the main window.
"485x700":The first part, "485x700," specifies the dimensions of the window. In this case, it's saying the window should be 485 pixels wide and 700 pixels tall.
"+290+10":The second part, "+290+10," specifies the position of the window on the screen. The first number (290) is the distance from the left edge of the screen, and the second number (10) is the distance from the top edge of the screen.'''

root.title("Symphony")
'''gives title to the window'''

root.configure(background="#DAC9F8")
'''configure() command in Tkinter is a versatile method that allows you to configure various properties of the main window.'''
#if we want to restict resizing of our window by user- root.resizable(False(for width), False(for height))

root.resizable(False,False)

#gif frame

gif_lb=Label(root)
gif_lb.pack(fill=BOTH)
gif_lb.config(width=400,height=260)
gif_lb.place(x=50,y=40)
gif_file=Image.open(resource_path('images\\background.gif'))
def play_gif():
    global i,gif_file
    for i in ImageSequence.Iterator(gif_file):
        i=ImageTk.PhotoImage(i)
        gif_lb.config(image=i)
        root.update()
    root.after(0,play_gif)

play_gif()

#making the browse function
def browse():
    path=filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs=os.listdir(path)

    for song in songs:
        if song.endswith(".mp3"):
            Playlist.insert(END, song)
    play_gif()
             
#line 54: end krdo loop ko or return krdo song, song yaha playlist me insert ho rha

#MAKING FUNCTIONS FOR BUTTONS
#the ispause variable checks the state of player: 0=no song started,1=playing,2=paused
ispause=0
#making the play function
def Play():
    get_time()
    global give_v
    mixer.music.set_volume(slider_v.get())
    give_v=mixer.music.get_volume()*100
    slider_label.config(text=f'{give_v}')
    global ispause
    #to get and print music name from playlist
    name=Playlist.get(ACTIVE)
    print(name)
    if ispause==0:
        #mixer initialized
        mixer.init()
        #to play the music
        mixer.music.load(Playlist.get(ACTIVE))
        mixer.music.play()
        ispause=1
        #slider_pos=int(song_length)
        #slider.config(to=slider_pos, value=0)
    elif ispause==2:
        mixer.init()
        mixer.music.unpause()
        ispause=1 
    elif ispause==1:
        mixer.music.stop()
        # Load and play the newly selected song
        mixer.init()
        mixer.music.load(Playlist.get(ACTIVE))
        mixer.music.play()
        ispause = 1

#making the pause function
def Pause():
    global ispause
    if ispause==0 or ispause==2:
        print("nothing to pause")
    elif ispause==1:
        mixer.init()
        mixer.music.pause()
        ispause=2
    else:
        ispause=0

#making the next song function
def Next():
    slider.config(value=0)
    global ispause
    #here next is tuple for the curr. song(songs in playlist are numbered in tuples)
    next=Playlist.curselection()
    #here next is incremented by 1, so actually this is the tuple for the next song
    next=next[0]+1
    #next song loaded and played
    mixer.music.load(Playlist.get(next))
    mixer.music.play()
    ispause=1
    #Updating the selection bar in the Playlist
    #1st we clear the selection bar from the whole playlist(from 0th to end song)
    Playlist.selection_clear(0, END) 
    #now we will activate the the selection bar for the next song
    Playlist.activate(next)
    #setting selection bar on next song
    Playlist.selection_set(next, last=None)

    
#making the prev song function
def Prev():
    slider.config(value=0)
    global ispause
    #here prev is tuple for the curr. song(songs in playlist are numbered in tuples)
    prev=Playlist.curselection()
    #here prev is decremented by 1, so actually this is the tuple for the prev song
    prev=prev[0]-1
    #prev song loaded and played
    mixer.music.load(Playlist.get(prev))
    mixer.music.play()
    ispause=1
    Playlist.selection_clear(0, END)
    Playlist.activate(prev)
    Playlist.selection_set(prev, last=None)

#making the 5 sec before button
def back5():
    converted_song_time=song_time()
    global slider_update, cur_time, converted_cur_time
    mixer.music.load(Playlist.get(ACTIVE))
    slider_update-=5
    cur_time=slider_update
    mixer.music.play(loops=0, start=slider_update)
    converted_cur_time=time.strftime('%M:%S',time.gmtime(slider_update))
    time_bar.config(text=f'time elapsed : {converted_cur_time} of {converted_song_time}')
    slider_pos=int(song_length)
    slider.config(to=slider_pos, value=slider_update)

#making the 5 sec after button
def forward5():
    converted_song_time=song_time()
    global slider_update, cur_time, converted_cur_time
    mixer.music.load(Playlist.get(ACTIVE))
    slider_update+=5
    cur_time=slider_update
    mixer.music.play(loops=0, start=slider_update)
    converted_cur_time=time.strftime('%M:%S',time.gmtime(slider_update))
    time_bar.config(text=f'time elapsed : {converted_cur_time} of {converted_song_time}')
    slider_pos=int(song_length)
    slider.config(to=slider_pos, value=slider_update)

lower_frame=Frame(root, bg="#B095DE", width=595, height=160)
'''This part is creating a new frame widget. A frame is like a container that you can use to organize and hold other widgets (like buttons, labels, etc.).

root is the parent widget, which usually refers to the main window in Tkinter. It means the new frame will be placed inside the main window.

bg sets the background color, width and height specify dimensions'''

lower_frame.place(x=0,y=350)
'''this is to tell that in the root where the frame will be placed, where to start from x and y axis'''

#making the time record bar(for total time length of song and time duration covered)
time_bar=Label(root, text="",bd=1, relief=RIDGE, bg="#7B23B4",font=("Tahoma",10,"normal"),fg="#FCFAE3",anchor="center",height=1,width=100)
time_bar.pack(side=BOTTOM,fill=X)
time_bar.place(x=0,y=490)

def get_time():
    converted_song_time=song_time()
    global ispause
    #getting elapsed time with time
    mixer.init()
    global cur_time
    cur_time=(mixer.music.get_pos()/1000)+1
    global slider_update
    slider_update=int(slider.get())
    if int(slider.get())==int(song_length):
        pass
    elif ispause==2:
        pass
    elif int(slider.get())==int(cur_time):
        #slider has not been moved
        converted_cur_time=time.strftime('%M:%S',time.gmtime(int(cur_time)))
        time_bar.config(text=f'time elapsed : {converted_cur_time} of {converted_song_time}')
        slider_pos=int(song_length)
        slider.config(to=slider_pos, value=int(cur_time))
    else:
        #slider HAS been moved
        converted_cur_time=time.strftime('%M:%S',time.gmtime(int(slider.get())))
        time_bar.config(text=f'time elapsed : {converted_cur_time} of {converted_song_time}')
        slider_pos=int(song_length)
        slider.config(to=slider_pos, value=int(slider.get()))
        global next_time
        next_time=(int(slider.get())+1)
        slider.config(value=next_time)
        cur_time=next_time
  
    #update slider_label as pseudo to check slider.get and cur_time sync
    #slider_label.config(text=f'slider: {int(slider.get())} and song position: {int(cur_time)}')
    #converting into time format
    converted_cur_time=time.strftime('%M:%S',time.gmtime(cur_time))
    time_bar.config(text=f'time elapsed : {converted_cur_time} of {converted_song_time}')
    #slider.config(value=int(cur_time))
    #slider_label.config(text=f'{int(slider.get())} of {int(song_length)}')
    time_bar.after(1000, get_time)

def song_time():
    #getting song time
    song=Playlist.get(ACTIVE)
    song_mut=MP3(song)
    global song_length
    song_length=song_mut.info.length
    converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))
    return converted_song_length

def high_v():
    mixer.init()
    new_high_V=(slider_v.get())+0.01
    mixer.music.set_volume(new_high_V)
    slider_v.config(value=new_high_V)
    global give_v
    give_v=mixer.music.get_volume()*100
    slider_label.config(text=f'{give_v}')

def low_v():
    mixer.init()
    new_low_V=(slider_v.get())-0.01
    mixer.music.set_volume(new_low_V)
    slider_v.config(value=new_low_V)
    global give_v
    give_v=mixer.music.get_volume()*100
    slider_label.config(text=f'{give_v}')

#MAKING SLIDERS

#Slider for SONG POSITION :

#making the slider function
def slide(X):
    #slider_label.config(text=f'{int(slider.get())} of {int(song_length)}')
    mixer.init()
    #to play the music
    mixer.music.load(Playlist.get(ACTIVE))
    mixer.music.play(loops=0,start=int(slider.get()))

#create a temporary slider label
slider_label=Label(root, text="0",bg="#DAC9F8",font=("Helvetica",12),fg="#4A0D5E")
slider_label.pack()
slider_label.place(x=520,y=277.5)

#making song slider using ttk
style = ttk.Style()
style.theme_use('alt')
style.configure("Primary.Horizontal.TScale", background="#B095DE",troughcolor='#342B42', troughrelief='groove')
slider=ttk.Scale(root, from_=0, to=100,orient=HORIZONTAL,value=0, command=slide, length=360, style="Primary.Horizontal.TScale")
slider.pack(pady=20)
slider.place(x=117.5,y=450)

#making volume slider function
def slide_v(X):
    mixer.init()
    mixer.music.set_volume(slider_v.get())
    global give_v
    give_v=mixer.music.get_volume()*100
    slider_label.config(text=f'{give_v}')

#Slider for VOLUME :
volume_frame=LabelFrame(root, width=70,height=200, bg="#B095DE", text="Volume",font=("Tahoma",12),relief=FLAT)
volume_frame.place(x=495,y=75)

style_v= ttk.Style()
style_v.theme_use('alt')
style_v.configure("Primary.Vertical.TScale", background="#B095DE",troughcolor='#342B42', troughrelief='groove')
slider_v=ttk.Scale(root, from_=1, to=0,orient=VERTICAL,value=1, command=slide_v, length=150, style="Primary.Vertical.TScale")
slider_v.pack()
slider_v.place(x=520,y=100)

#MAKING BUTTONS

#making play button
play_image = Image.open(resource_path("images\\play button-modified.png"))
resized_play_image = play_image.resize((50, 50), Image.LANCZOS)
playbutton=ImageTk.PhotoImage(resized_play_image)
#from PIL import Image, ImageTk is an import statement in Python. It imports the Image and ImageTk classes from the PIL module (which is actually a sub-module of the Pillow library). These classes are used to manipulate images in Python.
#ImageTk is used as an intermediate to convert image to PhotoImage object
#The Image class is used to open, manipulate, and save images. The ImageTk class is used to create and manipulate Tkinter-compatible photo images, which can be displayed by Tkinter widgets like buttons.
Button(root, image=playbutton, bg="#B095DE", bd=0, height=50, width=50, command=Play).place(x=230,y=380)

#making pause button
play_image2 = Image.open(resource_path("images\\pause button-modified.png"))
resized_play_image2 = play_image2.resize((50, 50), Image.LANCZOS)
pausebutton=ImageTk.PhotoImage(resized_play_image2)
Button(root, image=pausebutton, bg="#B095DE", bd=0, height=50, width=50, command=Pause).place(x=315,y=380)

#making next button
play_image3 = Image.open(resource_path("images\\next song-modified.png"))
resized_play_image3 = play_image3.resize((40, 40), Image.LANCZOS)
nextbutton=ImageTk.PhotoImage(resized_play_image3)
Button(root, image=nextbutton, bg="#B095DE", bd=0, height=40, width=40, command=Next).place(x=490,y=385)

#making prev button
play_image4 = Image.open(resource_path("images\\prev song-modified.png"))
resized_play_image4 = play_image4.resize((40, 40), Image.LANCZOS)
prevbutton=ImageTk.PhotoImage(resized_play_image4)
Button(root, image=prevbutton, bg="#B095DE", bd=0, height=40, width=40, command=Prev).place(x=65,y=385)

#making back5 button
play_image5 = Image.open(resource_path("images\\5 sec before button-modified.png"))
resized_play_image5 = play_image5.resize((40, 40), Image.LANCZOS)
back5button=ImageTk.PhotoImage(resized_play_image5)
Button(root, image=back5button, bg="#B095DE", bd=0, height=40, width=40, command=back5).place(x=150,y=385)

#making back5 button
play_image6 = Image.open(resource_path("images\\5 sec after button-modified.png"))
resized_play_image6 = play_image6.resize((40, 40), Image.LANCZOS)
forward5button=ImageTk.PhotoImage(resized_play_image6)
Button(root, image=forward5button, bg="#B095DE", bd=0, height=40, width=40, command=forward5).place(x=405,y=385)

#vol up image:
vol_up= Image.open(resource_path("images\\vol up-modified.png"))
resized_vol_up= vol_up.resize((30, 30), Image.LANCZOS)
vol_up_button=ImageTk.PhotoImage(resized_vol_up)
Button(root, image=vol_up_button, bg="#DAC9F8", bd=0, height=30, width=30, command=high_v).place(x=512,y=22.5)

#vol down image:
vol_down= Image.open(resource_path("images\\vol low-modified.png"))
resized_vol_down= vol_down.resize((30, 30), Image.LANCZOS)
vol_down_button=ImageTk.PhotoImage(resized_vol_down)
Button(root, image=vol_down_button, bg="#DAC9F8", bd=0, height=30, width=30, command=low_v).place(x=512,y=305)


#FOR LOGO
image_icon=PhotoImage(file=resource_path("images\\logo Symphony.png"))
root.iconphoto(False, image_icon)

menu= PhotoImage(file=resource_path("images\\menu.png"))
Label(root, image=menu).place(x=0,y=510, width= 595, height=190)

frame=Frame(root, bd=2, relief = GROOVE) #bd means border
frame.place(x=0,y=550, width=595,height=190)

Button(root, text="Browse Music",width=60,height=1,font=("Comic Sans MS",13,"bold"), fg="#342B42",bg="#F9EAA8",command=browse).place(x=0,y=510)
#fg means forground(color of font)
Scroll=Scrollbar(frame)
Playlist=Listbox(frame,width=100, font=("Times New Roman",10), bg="#CACCFC", fg="black", selectbackground="#6F1FA9", cursor="hand2", bd=0,yscrollcommand=Scroll.set)
Scroll.config(command = Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT,fill=BOTH)

root.mainloop()
'''"root.mainloop()":

mainloop() is a special function provided by Tkinter. When you call root.mainloop(), you are telling Python to start running the program and keep it running until the user decides to close the window.
It's like saying, "Hey Python, start showing the window, and keep running the program as long as the window is open."'''

