#import necessary modules
import os
import sys
import random
import tkinter as tk
from tkinter import ttk

#define directions and colors as numbers
up=1
right=2
down=3
left=4
white=0
black=1

# Create root window
root = tk.Tk()
root.title('Langton\'s ant')
root.geometry('660x660+0+0')

# Create canvas for images
can = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
can.pack(fill="both",expand="True")

# Load background image
bg = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\background_image.png")
can.create_image(0, 0, anchor="nw", image=bg)

# Ask for time duration between two moves
firstchoice= ["0.1","0.2","0.5","1", "2","5","10"] #the choices of the time between two moves
firstchoice_var = tk.StringVar() #the time between two moves

# Ask for num_of_obstacles
obschoice= ["0","1","2","3","4", "5","6","7","8"] #the choices of the number of obstacles
obschoice_var = tk.StringVar() #the number of obstacles

# Load ant images (1:up,2:right,3:down,4:left,w:whitebox,b:blackbox,r:redbox)
ant1w = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant1.png") #ant in white box looking up
ant2w = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant2.png") #ant in white box looking right
ant3w = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant3.png") #ant in white box looking down
ant4w = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant4.png") #ant in white box looking left
ant1b = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant1b.png") #ant in black box looking up
ant2b = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant2b.png") #ant in black box looking right
ant3b = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant3b.png") #ant in black box looking down
ant4b = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\ant4b.png") #ant in black box looking left
b = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\black_box.png") #empty black box
w = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\white_box.png") #empty white box
r = tk.PhotoImage(file=os.path.expanduser('~')+"\\Downloads\\Langton's_ant\\red_box.png") #empty red box (for the obstacles)
blacklist=[] #it contains all the (x,y) tuples that have black boxes (x:the number of the box the ant is on-at the x axis)
whitelist=[] #it contains all the (x,y) tuples that have white boxes (y:the number of the box the ant is on-at the y axis)
obstaclelist=[] #it contains all the (x,y) tuples that have obstacles

for x in range(0,11):
    for y in range(0,11):
        whitelist.append((x,y)) #insert all the boxes in the whitelist at first
   
def next_pos():
    global direction,color,xpos,ypos
    colorbefore=color #remember the color of the box where the ant is now
    if color==white: #change the color
        can.create_image(xpos*60, ypos*60+1, anchor="nw", image=b) #create empty black box here
        blacklist.append((xpos,ypos)) #insert the tuple to the blacklist
        if (xpos,ypos) in whitelist: whitelist.remove((xpos,ypos)) #remove the tuple from the whitelist
    else: #change the color
        can.create_image(xpos*60, ypos*60+1, anchor="nw", image=w)
        whitelist.append((xpos,ypos))
        if (xpos,ypos) in blacklist: blacklist.remove((xpos,ypos))
    if direction==up:
        ypos-=1 #one box up
        color=black_or_white(xpos,ypos) #define the next color for the new xpos,ypos
        if (xpos,ypos) in obstaclelist: #if there is an obstacle there move forward
            ypos+=1 #take back the one box up
            #according to what color it was the ant on and what color is going to be on create the image of the ant
            if colorbefore==white: 
                xpos-=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4b)
            else: 
                xpos+=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant2w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant2b)
        elif color==white: #if there were no obstacles then move the ant according to the rules
            direction+=1 #turn 90 degrees clockwise for the next move
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant1w) #create image
        elif color==black:
            direction=4 #turn 90 degrees counter-clockwise 
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant1b)
    elif direction==right:
        xpos+=1 #one box right
        color=black_or_white(xpos,ypos)
        if (xpos,ypos) in obstaclelist:
            xpos-=1
            if colorbefore==white: 
                ypos-=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant1w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant1b)
            else: 
                ypos+=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant3w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant3b)
        elif color==white:
            direction+=1
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant2w)
        elif color==black:
            direction=1
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant2b)
    elif direction==down:
        ypos+=1 #one box down
        color=black_or_white(xpos,ypos)
        if (xpos,ypos) in obstaclelist:
            ypos-=1
            if colorbefore==white: 
                xpos+=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant2w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant2b)
            else: 
                xpos-=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4b)
        elif color==white:
            direction+=1
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant3w)
        elif color==black:
            direction-=1
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant3b)
    elif direction==left:
        xpos-=1 #one box left
        color=black_or_white(xpos,ypos)
        if (xpos,ypos) in obstaclelist:
            xpos+=1
            if colorbefore==white: 
                ypos+=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant3w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant3b)
            else: 
                ypos-=1
                color=black_or_white(xpos,ypos)
                if color==white: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant1w)
                else: can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant1b)
        elif color==white:
            direction=1
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4w)
        elif color==black:
            direction-=1
            can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4b)

def black_or_white(xpos,ypos):  #define the next color
    try:
        if (xpos, ypos) in blacklist: color = black
        elif (xpos, ypos) in whitelist: color = white
        return color
    except UnboundLocalError: #if the ant has reached the boundaries then stop it and destroy the root
        print("The ant has reached the boundaries") #without obstacles it goes until the 224th step
        root.destroy()
        sys.exit()
        

def play_function():
    window.geometry("+600+900")  # Move the window elsewhere
    schedule_function() #the ant begins 

def schedule_function():
    global c
    if c==0:
        for fores in range(num_of_obstacles): #create as many obstacles as they were asked
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            # Check if the difference between x and y coordinates is more than 2 or if the x,y is the center so that no problems will occur at the process
            while (any(abs(x - pl[0]) <= 2 and abs(y - pl[1]) <= 2 for pl in obstaclelist) and (x!=5 or y!=5)):
                x = random.randint(2, 10)
                y = random.randint(2, 10)
            obstaclelist.append((x, y))
        for x,y in obstaclelist:
            can.create_image(x*60, y*60+1, anchor="nw", image=r)
    root.after(int(first*1000), schedule_function) #after as many seconds as they were given move the ant
    print(c) #print how many steps the ant has done
    if c!=0: next_pos() #the first time it the ant should not move
    c+=1 

def callback(event):
    global first
    first=float(firstchoice_var.get()) #the time beteen two seconds in sec 

def callback2(event):
    global num_of_obstacles
    num_of_obstacles=int(obschoice_var.get()) #the number of obstacles

def choose_time_and_num_of_obstacles():
    playbutton=tk.Button(window,text="Play",font="Arial 20",command=play_function) #button to press so that the ant will start moving
    playbutton.place(x=10,y=10)
    timelabel=tk.Label(window,text="duration between two moves (in sec):",font="Arial 12")
    timelabel.place(x=10,y=70)
    obslabel=tk.Label(window,text="number of obstacles:",font="Arial 14") 
    obslabel.place(x=10,y=100)
    firstchoice_combobox = ttk.Combobox(window, textvariable= firstchoice_var, values= firstchoice) #choosing the time between two moves
    firstchoice_combobox.place(x=280, y=72)
    firstchoice_combobox.bind("<<ComboboxSelected>>", callback)
    obschoice_combobox = ttk.Combobox(window, textvariable= obschoice_var, values= obschoice) #choosing the number of obstacles
    obschoice_combobox.place(x=210, y=102)
    obschoice_combobox.bind("<<ComboboxSelected>>", callback2)


##MAIN
c=0 
direction=up #the ant is going to turn up at first
color=white #the ant is on a white box at first
xpos=5 #the ant is in the middle at first (xpos is the number of the box the ant is on-at the x axis)
ypos=5 #the ant is in the middle at first (xpos is the number of the box the ant is on-at the y axis)
first=1 #the time between two moves if the user presses the playbutton without choosing from the combobox
num_of_obstacles=0 #the number of obstacles if the user presses the playbutton without choosing from the combobox
can.create_image(xpos*60, ypos*60+1, anchor="nw", image=ant4w)

# Create new window to ask for time between two moves and the number of obstacles
window=tk.Toplevel()
window.geometry('500x140+900+400')
window.configure(bg="#A7D9D7")# Set the background color
choose_time_and_num_of_obstacles() #choose time and number of obstacles

root.mainloop()
