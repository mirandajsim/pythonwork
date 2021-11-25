from tkinter import Tk, Canvas

width = 1280 # width of world
height = 720 # height of world

def leftkey(event):
	global direction
	direction = 'left'
	(x, y, a, b) = canvas.coords(platform)
	if a > 0:
		edge = min(x, 10)
		canvas.move(platform, -edge, 0)

def rightkey(event):
	global direction
	direction = 'right'
	(x, y, a, b) = canvas.coords(platform)
	if a < width:
		edge = min(width - a, 10)
		canvas.move(platform, edge, 0)

def moveplatform():
	canvas.pack()

def setwindowdimensions(w, h):
    window = Tk()
    window.title("Game")
    ws = window.winfo_screenwidth()  # computer's screen size
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)  # calculate center
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))  # window size
    return window

window = setwindowdimensions(width, height)
canvas = Canvas(window, bg = 'black', width = width, height = height)

platform = canvas.create_rectangle(550, 600, 730, 625, fill = 'blue', outline = 'white')
direction = 'right'

canvas.bind('<Left>', leftkey)
canvas.bind('<Right>', rightkey)
canvas.focus_set()

moveplatform()

window.mainloop()
