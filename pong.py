from tkinter import *
import random

width = 1280 # width of world
height = 720 # height of world

def bosskey(event):
    global bossflag
    pausegame()
    if bossflag is True:
        bossflag = False
        bosskeywindow.withdraw()
        window.deiconify()
    else:
        bossflag = True
        bosskeywindow.deiconify()
        window.withdraw()

def cheatcode1start(event):
    global cheatcodeone
    cheatcodeone = True

def cheatcode1stop(event):
    global cheatcodeone
    cheatcodeone = False

def cheatcode2(event):
    global score
    cheatcodetwo = True
    if cheatcodetwo is True:
        score += 10
        txt = 'Score: ' + str(score)
        canvas.itemconfigure(scoretext, text=txt)
    else:
        cheatcodetwo = False

def leftkey(event):
    global direction, pause
    if pause is False:
        direction = 'left'
        (x, y, a, b) = canvas.coords(platform)
        if a > 0:
            if cheatcodeone is False:
                edge = min(x, 20)
                canvas.move(platform, -edge, 0)
            else:
                edge = min(x, 60)
                canvas.move(platform, -edge, 0)

def rightkey(event):
    global direction, pause
    if pause is False:
        direction = 'right'
        (x, y, a, b) = canvas.coords(platform)
        if a < width:
            if cheatcodeone is False:
                edge = min(width - a, 20)
                canvas.move(platform, edge, 0)
            else:
                edge = min(width - a, 60)
                canvas.move(platform, edge, 0)

def pausegame():
    global pause
    if pause is True:
        pause = False
    else:
        pause = True

def overlapping(a, b):
	if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
		return True
	return False

def moveball():
	canvas.pack()
	global speedx, speedy, score, pause
	if pause is False:
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
				speedx = speedx + random.randint(0, 2)
				speedy = -speedy - random.randint(0, 2)
				score += 10
				txt = 'Score: ' + str(score)
				canvas.itemconfigure(scoretext, text = txt)
			elif overlapping(ballpos, badzone):
				canvas.create_image(640, 360, image = gameover)
				return
		canvas.move(ball, speedx, speedy)
	canvas.after(20, moveball)

def setbosskey(w, h):
    bosskeywindow = Toplevel()
    bosskeywindow.title("Document1")
    ws = window.winfo_screenwidth()  # computer's screen size
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)  # calculate center
    y = (hs/2) - (h/2)
    bosskeywindow.geometry('%dx%d+%d+%d' % (w, h, x, y))  # bosskey size
    return bosskeywindow

def createstars():
    for i in range(400):
        x = random.randint(1, 1279)
        y = random.randint(1, 350)
        size = random.randint(2, 5)
        f = random.randint(0, 2)
        xy = (x, y, x + size, y + size)
        tmp_star = canvas.create_oval(xy, fill=c[f])
        star.append(tmp_star)

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
canvas.pack()
platform = canvas.create_rectangle(550, 600, 730, 625, fill = 'blue', outline = 'white')
ball = canvas.create_oval(630, 360, 650, 380, fill = 'red', outline = 'white', width = 2)
nogozone = canvas.create_rectangle(0, 626, 1280, 720, fill = 'green')
speedx = 2
speedy = 2
score = 0
txt = 'Score: ' + str(score)
scoretext = canvas.create_text(width / 2, 650, fill = 'white', font = 'Arial 20 italic bold', text = txt)

star = []
c = ['white', '#fefefe', '#dfdfdf']
lead = 0

pause = False
pauseit = Button(window, text = 'Play/Pause', command = pausegame, anchor = 'n')
pauseit.configure(activebackground = 'white')
pausethis = canvas.create_window(1182, 23, anchor = 'nw', window = pauseit)

bosskeywindow = setbosskey(width, height)
boss = Canvas(bosskeywindow, bg = 'black', width = width, height = height)
boss.pack()
loremipsum = PhotoImage(file = "loremipsumtextscaled.png")
document = boss.create_image(640, 360, image = loremipsum)
bosskeywindow.withdraw()
bossflag = False

cheatcodeone = False

canvas.bind('<Left>', leftkey)
canvas.bind('<Right>', rightkey)
canvas.bind('<ButtonPress-1>', cheatcode1start)
canvas.bind('<ButtonRelease-1>', cheatcode1stop)
canvas.bind('<Return>', cheatcode2)
canvas.bind('<Tab>', bosskey)
bosskeywindow.bind('<Tab>', bosskey)

canvas.focus_set()

direction = 'right'

gameover = PhotoImage(file = "gameover.png")

createstars()
moveball()

window.mainloop()

