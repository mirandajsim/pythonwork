from tkinter import *
import random
import time
import pickle

width = 1280 # width of world
height = 720 # height of world

# Changes platform colour
def changeplatformcolour():
    global colours
    randomcolournumber = random.randint(0, len(colours) - 1)
    randomcolour = colours[randomcolournumber]
    canvas.itemconfig(platform, fill=randomcolour)

# Changes colour of the ball
def changeballcolour():
    global colours
    randomcolournumber = random.randint(0, len(colours) - 1)
    randomcolour = colours[randomcolournumber]
    canvas.itemconfig(ball, fill=randomcolour)

# Boss key (click tab to activate/deactivate)
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

# Starts cheat code one (hold mouse down to increase platform movement)
def cheatcode1start(event):
    global cheatcodeone
    cheatcodeone = True

# Stops cheat code one (release mouse to resume usual movement)
def cheatcode1stop(event):
    global cheatcodeone
    cheatcodeone = False

# Cheat code two (add 10 points every time return is hit)
def cheatcode2(event):
    global score
    cheatcodetwo = True
    if cheatcodetwo is True:
        score += 10
        txt = 'Score: ' + str(score)
        canvas.itemconfigure(scoretext, text=txt)
    else:
        cheatcodetwo = False

# Move platform left
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

# Move platform right
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

# Pauses game
def pausegame():
    global pause
    if pause is True:
        pause = False
    else:
        pause = True

# Save progress
def savegame():
	global score
	pausegame()
	file = open('savegame.txt', 'wt')
	file.write(str(score))
	file.close()
	time.sleep(1)
	pausegame()
	print('Save game loaded.')

# Retrieve saved game
def retrievegame():
	global score
	try:
		pausegame()
		file = open('savegame.txt', 'r')
		score = file.read()
		score = int(score)
		txt = 'Score: ' + str(score)
		canvas.itemconfigure(scoretext, text = txt)
		file.close()
		time.sleep(1)
		pausegame()
	except FileNotFoundError:
		print('Error')

# Destroys entry page
def submitleaderboard(initials):
    global leaderboardprompt
    submitinitials(initials)
    leaderboardprompt.destroy()

# Gets information for leaderboard
def leaderboardentry():
    global score, lead, leaderboardprompt
    while (lead == 0):
        lead += 1
        leaderboardprompt = Toplevel(window)
        leaderboardprompt.geometry('423x238+536+342')
        leaderboardprompt.title('Game Leaderboard Entry')
        label = Label(leaderboardprompt, text='Enter your initials:', font=('Arial Bold', 23))
        label.pack()
        note = Label(leaderboardprompt, text='NOTE: if you enter more than two characters,\nonly the first two will be used.\n', font=('Arial', 14))
        note.pack()
        initialsentry = Entry(leaderboardprompt, width=2, bd=3)
        initialsentry.pack()
        submitscore = Button(leaderboardprompt, text='Submit Score', command=lambda: submitleaderboard(initialsentry.get()))
        submitscore.pack(pady=21)

# Ensures only two characters are submitted to leaderboard
def twoinitials(x=''):
    return x[:2]

# Checks user enters initials correctly
def submitinitials(x=''):
    global leaderboard
    if x != '':
        x = twoinitials(x)
        x = x.upper()
        newscore = [x, score]
        leaderboard.append(newscore)
        leaderboardhistory()
    else:
        print('Please enter a valid set of initials.')

# Gets leaderboard history from data file
def leaderboardhistory():
    global leaderboard, highscores
    try:
        with open('leaderboard.data', 'rb') as filehandle:
            highscores = (pickle.load(filehandle))
            for i in range(0, len(leaderboard)):
                highscores.append(leaderboard[i])
    except FileNotFoundError:
        highscores = leaderboard
    finalleaderboard()

# Sort leaderboard by score function
def sort(board):
    l = len(board)
    for x in range(0, l):
        for y in range(0, l-x-1):
            if (board[y][1] < board[y+1][1]):
                ldb = board[y]
                board[y] = board[y + 1]
                board[y + 1] = ldb
    return board[:5]

# Sort top 5 scores only
def sortboard():
    global highscores
    sort(highscores)
    return highscores[:5]

# Generate final leaderboard
def finalleaderboard():
    global highscores, finalscores, end
    end.config(image='')
    finalscores = sortboard()
    canvas.create_rectangle(0, 626, 1280, 720, fill='green')
    canvas.create_rectangle(0, 0, 1280, 626, fill='black')
    canvas.create_rectangle(550, 600, 730, 625, fill='blue', outline='white')
    canvas.create_oval(630, 580, 650, 600, fill='red', outline='white', width=2)
    canvas.create_text(640, 75, fill='white', font='Arial 48 bold', text='LEADERBOARD')
    canvas.create_text(550, 150, fill='white', font='Arial 32 bold', text='Player')
    canvas.create_text(730, 150, fill='white', font='Arial 32 bold', text='Score')
    canvas.create_text(width / 2, 675, fill='white', font='Arial 20 italic', text='If submitting a current score, wait a few seconds after the entry window closes for the board to refresh.')
    for i in range(0, len(finalscores)):
        playerentry = finalscores[i][0]
        scoreentry = str(finalscores[i][1])
        canvas.create_text(550, 150 + (75 * (i + 1)), fill='white', font='Arial 20', text=playerentry)
        canvas.create_text(730, 150 + (75 * (i + 1)), fill='white', font='Arial 20', text=scoreentry)
    saveleaderboard()

# Save leaderboard data for next time
def saveleaderboard():
    global finalscores
    with open('leaderboard.data', 'wb') as filehandle:
        pickle.dump(finalscores, filehandle)
        print('Leaderboard saved.')

# Collision detection
def overlapping(a, b):
	if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
		return True
	return False

# Ball movement (main gameplay)
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
				end.place(x=0, y=0)
				time.sleep(1)
				leaderboardentry()
		canvas.move(ball, speedx, speedy)
	canvas.after(20, moveball)

# Boss key set up
def setbosskey(w, h):
    bosskeywindow = Toplevel()
    bosskeywindow.title("Document1")
    ws = window.winfo_screenwidth()  # computer's screen size
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)  # calculate center
    y = (hs/2) - (h/2)
    bosskeywindow.geometry('%dx%d+%d+%d' % (w, h, x, y))  # bosskey size
    return bosskeywindow

# Star design
def createstars():
    for i in range(400):
        x = random.randint(1, 1279)
        y = random.randint(1, 350)
        size = random.randint(2, 5)
        f = random.randint(0, 2)
        xy = (x, y, x + size, y + size)
        tmp_star = canvas.create_oval(xy, fill=c[f])
        star.append(tmp_star)

# Main window set up
def setwindowdimensions(w, h):
    window = Tk()
    window.title("Game")
    ws = window.winfo_screenwidth()  # computer's screen size
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)  # calculate center
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))  # window size
    return window

# Misc. variables for basic gameplay
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
direction = 'right'

# Images
gameover = PhotoImage(file = "gameover.png")
end = Label(window, image=gameover)
end.pack()

# Star variables
star = []
c = ['white', '#fefefe', '#dfdfdf']
lead = 0

# Pause variables
pause = False
pauseit = Button(window, text = 'Play/Pause', command = pausegame, anchor = 'n')
pauseit.configure(activebackground = 'white')
pausethis = canvas.create_window(1182, 23, anchor = 'nw', window = pauseit)

# Save/retrieve game buttons
save = Button(window, text = 'Save Progress', command = savegame)
save.place(x = 1161, y = 48)
retrieve = Button(window, text = 'Retrieve Game', command = retrievegame)
retrieve.place(x = 1160, y = 73)

# Leaderboard variables
lead = 0
leaderboard = []
highscores = []
finalscores = []
viewleaderboard = Button(window, text='Forfeit Game / Submit Current\nScore / View Leaderboard', command=leaderboardhistory)
viewleaderboard.place(x=1067, y=148)

# Boss key variables
bosskeywindow = setbosskey(width, height)
boss = Canvas(bosskeywindow, bg = 'black', width = width, height = height)
boss.pack()
loremipsum = PhotoImage(file = "loremipsumtextscaled.png")
document = boss.create_image(640, 360, image = loremipsum)
bosskeywindow.withdraw()
bossflag = False

# Cheat code variables
cheatcodeone = False

# Change colour variables
colours = ['red', 'yellow', 'green', 'blue', 'orange', 'white', 'gray', 'gold',
           'magenta', 'pink', 'purple', 'plum', 'sea green', 'tomato',
           'violet', 'blanched almond', 'brown', 'cadet blue', 'chartreuse',
           'coral', 'cornflower blue', 'cornsilk', 'cyan', 'dark goldenrod',
           'dark olive green', 'deep sky blue', 'firebrick', 'honeydew',
           'hot pink', 'indian red', 'ivory', 'khaki', 'lavender blush',
           'lawn green', 'lemon chiffon', 'light steel blue', 'linen',
           'maroon', 'medium violet red', 'midnight blue', 'mint cream',
           'misty rose', 'moccasin', 'navajo white', 'old lace', 'olive drab',
           'orchid', 'papaya whip', 'peach puff', 'rosy brown', 'seashell',
           'sienna', 'slate gray', 'thistle', 'wheat']
alterball = Button(window, text='Change Ball Colour', command=changeballcolour)
alterball.place(x=1133, y=98)
alterplatform = Button(window, text='Change Platform Colour', command=changeplatformcolour)
alterplatform.place(x=1103, y=123)

# Key binds
canvas.bind('<Left>', leftkey)
canvas.bind('<Right>', rightkey)
canvas.bind('<ButtonPress-1>', cheatcode1start)
canvas.bind('<ButtonRelease-1>', cheatcode1stop)
canvas.bind('<Return>', cheatcode2)
canvas.bind('<Tab>', bosskey)
bosskeywindow.bind('<Tab>', bosskey)
canvas.focus_set()

createstars()
moveball()

window.mainloop()
