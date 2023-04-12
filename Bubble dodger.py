'''
Bubble Dodger
v1.0
'''


import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from random import randint
from math import sqrt
from time import sleep, time


HEIGHT = 500
WIDTH = 800
MID_X = WIDTH / 2
MID_Y = HEIGHT / 2
SHIP_R = 15
MIN_BUB_R = 10
MAX_BUB_R = 30
MAX_BUB_SPEED = 10
GAP = 100
BUB_CHANCE = 25
SPEED = 10
SCOREBOARD = "highscores.txt"


# Create a game window
window = tk.Tk()
window.title('Bubble Dodge')
c = tk.Canvas(master=window, width=WIDTH, height=HEIGHT, bg='darkblue')
c.pack()


# Create event listeners to control the ship with the arrow keys
def move_ship(event):
    if event.keysym == 'Up':
        c.move(ship_id, 0, -SPEED)
        c.move(ship_id2, 0, -SPEED)
    elif event.keysym == 'Down':
        c.move(ship_id, 0, SPEED)
        c.move(ship_id2, 0, SPEED)
    elif event.keysym == 'Left':
        c.move(ship_id, -SPEED, 0)
        c.move(ship_id2, -SPEED, 0)
    elif event.keysym == 'Right':
        c.move(ship_id, SPEED, 0)
        c.move(ship_id2, SPEED, 0)


# Generate an enemy (bubble)
def make_bubbles():
    x = WIDTH + GAP
    y = randint(0, HEIGHT)
    r = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = c.create_oval(x-r, y-r, x+r, y+r, outline='white')
    bub_id.append(id1)
    bub_r.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPEED))


# Move enemy to the left
def move_bubbles():
    for i in range(len(bub_id)):
        c.move(bub_id[i], -bub_speed[i], 0)


# Get X and Y position of an item
def get_coord(id_num):
    pos = c.coords(id_num)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y


# Destroy an item
def delete_bubble(i):
    c.delete(bub_id[i])
    del bub_id[i]
    del bub_r[i]
    del bub_speed[i]


# Destroy all items
def clear_bubbles():
    for i in range(len(bub_id)-1, -1, -1):
        x, y = get_coord(bub_id[i])
        if x < -GAP:
            delete_bubble(i)


# Measure the distance between 2 items
def distance(id1, id2):
    x1, y1 = get_coord(id1)
    x2, y2 = get_coord(id2)
    return sqrt((x2-x1)**2+(y2-y1)**2)


# Detect when 2 items hit each other
def collision():
    for bub in range(len(bub_id)-1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < (SHIP_R + bub_r[bub]):
            return True
        else:
            continue
    return False


# Update the timer display
def view_time(timer):
    c.itemconfig(time_text, text=str(timer))


# Sort a list from the highest to the lowest score
def scoresort(lst):
    if len(lst) < 1:
        return lst

    # Clean list from invalid lines
    for l in range(len(lst)):
        try:
            if not (':' in lst[l]):
                del lst[l]
        except:
            pass

    for j in range(len(lst)):
        for k in range(len(lst)):
            item1 = lst[k]
            item1t = float((item1.split(':')[1]))
            if k != len(lst)-1:
                item2 = lst[k+1]
                item2t = float((item2.split(':')[1]))
                if item1t < item2t:
                    # Swap items
                    lst[k] = str(item2)
                    lst[k+1] = str(item1)
    return lst


# Provide high score table
def high_scores():
    global end_time

    try:
        file = open(SCOREBOARD, 'r')
    except:
        file = open(SCOREBOARD, 'x')
        scores = []
    else:
        scores = file.readlines()
    finally:
        # Get the player's name
        n = sd.askstring("Save your score", "What's your name?")
        s = end_time
        scores.append(f"{n}:{s}")
        scores = scoresort(scores)
        file = open(SCOREBOARD, 'w')
        for i in scores:
            file.write(str(i) + '\n')
        file.flush()
        file.close()

    c.create_text(MID_X, MID_Y+60, text='High scores:', fill='white', font=('Helvetica', 20))
    for i in range(len(scores)):
        c.create_text(MID_X, MID_Y+90+i*20, text=scores[i], fill='white')


while True:
    bub_id = []
    bub_r = []
    bub_speed = []
    end_time = 0
    c.delete("all")

    ship_id = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
    ship_id2 = c.create_oval(0, 0, 30, 30, outline='red')

    c.move(ship_id, MID_X, MID_Y)
    c.move(ship_id2, MID_X, MID_Y)

    c.create_text(50, 30, text='TIME', fill='white')
    time_text = c.create_text(50, 50, fill='white')
    c.bind_all('<Key>', move_ship)

    sleep(1.0)
    start = time()

    # Main loop
    while True:
        # Spawn a new bubble by chance
        if randint(1, BUB_CHANCE) == 1:
            make_bubbles()

        move_bubbles()
        clear_bubbles()
        view_time(int(time()-start))
        window.update()

        # Game finishes if the player hits a bubble or the edge
        if collision() or get_coord(ship_id)[0] > WIDTH or get_coord(ship_id)[0] < 0 or get_coord(ship_id)[1] > HEIGHT or get_coord(ship_id)[1] < 0:
            break

        sleep(0.01)

    # Difference between the time at the beginning and the time at the end = duration of the game
    end_time = time()-start

    c.create_text(MID_X, MID_Y, text='GAME OVER', fill='white', font=('Helvetica', 30))
    c.create_text(MID_X, MID_Y+30, text='Score: ' + str(int(end_time)), fill='white')

    high_scores()

    if not mb.askyesno(title="Play again", message="Do you want to play another round?"):
        break
