"""
This is a Virus Simulator
Created on: 07-07-2021
Time: 07-38-15
By PrathameshBhatkar
"""

import math
from threading import *
from tkinter import *
import sys
import random

from PIL import Image, ImageTk
import pygame

from VirusStats import VirusToSimulate
from Colors import *
from Virus import Virus
from Person import Person

pygame.init()

FPS = 60
cellSize = 10
cellNumber = 80


class Gui:
    def run(self):
        ms_delay = 200
        root = Tk()
        root.geometry('700x650')
        root.title('Simulator GUI')

        l1 = Label(root, text=f"Total number of people infected :{v.num_currently_infected}", font=("Courier", 15))
        l2 = Label(root, text=f"Total number of people currently infected by Virus :{v.total_num_infected}",
                   font=("Courier", 15))
        l3 = Label(root, text=f"Total number of people cured/recovered from diseases :{v.num_recovered}",
                   font=("Courier", 15))
        l4 = Label(root, text=f"Total number of people died :{v.num_deaths}",
                   font=("Courier", 15))
        l5 = Label(root, text=f"Total number of people informed :{v.num_deaths}",
                   font=("Courier", 15))

        image = Image.open("index.png")
        photo = ImageTk.PhotoImage(image)
        label = Label(image=photo)

        l1.pack()
        l2.pack()
        l3.pack()
        l4.pack()
        l5.pack()
        label.pack()
        Label().pack()
        Label().pack()
        Button(root, text='Add Infection', command=self.add_infection, padx=15, pady=10).pack()

        def check_condition():
            l1['text'] = f"Total num of people currently infected by Sars :{v.total_num_infected}"
            l2["text"] = f"Total num of people infected :{v.num_currently_infected}"
            l3['text'] = f"Total num of people cured/recovered from diseases :{v.num_recovered}"
            l4['text'] = f"Total number of people died :{v.num_deaths}"
            l5['text'] = f"Total number of people informed :{v.num_protected}"

            root.after(ms_delay, check_condition)

        root.after(ms_delay, check_condition)
        root.mainloop()

    def add_infection(self):
        global peopleL
        random.choice(peopleL).is_infected = True


screen = pygame.display.set_mode((cellNumber * cellSize, cellNumber * cellSize))
pygame.display.set_caption('Virus Simulation')
clock = pygame.time.Clock()

peopleL = [Person([m, s + 10], cellSize) for m in range(cellNumber) for s in range(cellNumber - 10)]

v = Virus(VirusToSimulate)
gui = Gui()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

Thread(target=gui.run).start()
Thread(target=v.infect).start()
Thread(target=v.inform_others).start()
Thread(target=v.recover).start()

Day = 1


def draw_window(pL, day):
    screen.fill(COLOR_DARK_GRAY)
    for p in pL:
        p.draw(screen)
    t = STAT_FONT.render(f"Day: {int(day)}", False, COLOR_WHITE)
    screen.blit(t, (10, 10))

    pygame.display.update()


def roundup(x):
    return int(math.ceil(x / 10.0)) * 10


while True:
    Day += 0.416666667
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            random.choice(peopleL).is_infected = True
        if event.type == pygame.MOUSEBUTTONDOWN:

            try:
                coor = pygame.mouse.get_pos()
                ids = [m.id for m in peopleL]
                peopleL[
                    ids.index([int(roundup(coor[0]) / cellSize), int(roundup(coor[1]) / cellSize)])].is_infected = True
            except:
                pass

    v.update(peopleL)
    draw_window(peopleL, Day)
    clock.tick(FPS)
