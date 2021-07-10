import random

import pygame

clock = pygame.time.Clock()


def in_ratio(ratio):
    l = []
    [l.append(True) for m2 in range(1)]
    [l.append(False) for m in range(100 - ratio[1])]
    random.shuffle(l)

    return random.choice(l)


class Virus:
    def __init__(self, params):
        self.pL = []
        self.day = 0
        self.total_num_infected = 0
        self.num_currently_infected = 0
        self.num_recovered = 0
        self.num_deaths = 0
        self.num_protected = 0

        self.recovery_rate = params["recovery_rate"]
        self.spread_rate = params["spreading_rate"]
        self.death_rate = params["death_rate"]
        self.severe_infection = int(params["severe_infection"] * 100)
        self.inform_rate = params["inform_rate"]
        self.protection_immunity = params["protection_immunity"]

    def infect(self):
        while True:
            ids = [m.id for m in self.pL]

            for p1 in self.pL:
                if p1.is_infected:

                    for i in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
                        if [p1.id[0] + i[0], p1.id[1] + i[1]] in ids and in_ratio(
                                [1, self.spread_rate]):
                            p2 = self.pL[ids.index([p1.id[0] + i[0], p1.id[1] + i[1]])]
                            if not p2.is_dead and not p2.is_protected:
                                p2.is_infected = True
                                self.num_currently_infected += 1
                                self.total_num_infected += 1

                            if p2.is_protected and in_ratio([1, self.protection_immunity]):
                                p2.is_infected = True
                                p2.is_protected = False
                                self.num_currently_infected += 1
                                self.total_num_infected += 1

                            elif p2.was_infected and in_ratio([1, self.protection_immunity]):
                                p2.is_infected = True
                                self.num_currently_infected += 1
                                self.total_num_infected += 1

                    if in_ratio([1, self.death_rate]):
                        p1.life -= 100
                    elif in_ratio([1, self.severe_infection]):
                        p1.life -= 40

                    if p1.life <= 0:
                        self.num_deaths += 1

            clock.tick(60)

    def recover(self):
        while True:
            for p in self.pL:
                if p.is_infected:
                    if in_ratio([1, self.recovery_rate]):
                        p.is_infected = False
                        p.was_infected = True
                        p.is_recovered = True
                        p.life = 100
                        self.num_recovered += 1
                        self.num_currently_infected -= 1
            clock.tick(60)

    def inform_others(self):
        while True:
            ids = [m.id for m in self.pL]

            for p1 in self.pL:
                if p1.was_infected and not p1.is_infected and p1.is_recovered:

                    for i in [[-2, 0], [2, 0], [0, -2], [0, 2]]:
                        if [p1.id[0] + i[0], p1.id[1] + i[1]] in ids and in_ratio([1, self.inform_rate]):
                            p2 = self.pL[ids.index([p1.id[0] + i[0], p1.id[1] + i[1]])]
                            if not p2.is_dead and not p2.was_infected and not p2.is_protected and not p2.is_recovered and not p2.is_infected:
                                p2.is_protected = True
                                self.num_protected += 1

            clock.tick(60)

    def update(self, pL):
        self.pL = pL
