from tkinter import Tk, Canvas, PhotoImage

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

def overlapping(a, b):
	if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
		return True
	return False

def moveball():
	canvas.pack()
	global speedx, speedy
	(x, y, a, b) = canvas.coords(ball)
	if x <= 0 or a >= width:
		speedx = -speedx
	if y <= 0:
		speedy = -speedy
	elif b >= 600:
		c = (x + a) / 2
		(p, q, r, s) = canvas.coords(platform)
		ballpos = canvas.coords(ball)
		badzone = canvas.coords(nogozone)
		if (p <= c <= r):
			speedy = -speedy - 1
		elif overlapping(ballpos, badzone):
			canvas.create_image(640, 360, image = gameover)
			return
	canvas.move(ball, speedx, speedy)
	canvas.after(20, moveball)

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
ball = canvas.create_oval(630, 360, 650, 380, fill = 'red', outline = 'white', width = 2)
nogozone = canvas.create_rectangle(0, 626, 1280, 720, fill = 'green')
speedx = 2
speedy = 2

canvas.bind('<Left>', leftkey)
canvas.bind('<Right>', rightkey)
canvas.focus_set()

direction = 'right'

gameover = PhotoImage(file = "gameover.png")

moveplatform()
moveball()
window.mainloop()
