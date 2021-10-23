### THIS FILE CREATED THE CONTROL MAPS WITH THE ACTUAL DIMENSIONS OF THE BOXES ON THE WEBOT SIMULATOR 
# maps created are used in compare_images.py 

# CAN CHANGE VALUES FOR DIFFERENT MAPS

from tkinter import *
# in meters * 100
box_width = 60

master = Tk()
canvas_width=600
canvas_height=600
canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()

def make_box(left, top, canvas):
    canvas.create_rectangle(left, top, left + box_width, top + box_width)

def make_arena(width,length,canvas):
    canvas.create_rectangle(50, 50, 50 + width, 50 + length)
make_box (canvas_width-(150+box_width), 150, canvas)
make_box (150, canvas_height-(150+box_width), canvas)
make_arena (500, 500, canvas)
master.mainloop()

