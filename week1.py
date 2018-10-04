#
# week1
# COMP450Lab
#
# Created by Nehir Poyraz on 28.09.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.


import random


class Player:
    id = 0

    def __init__(self, randomness: bool = None):
        self.wincount = 0
        self.movecount = [0, 0, 0]
        self.action: str
        self.previous = None
        if randomness:
            self.israndom = randomness
        self.id = Player.id
        self.name = "Player"
        if self.id != 0:
            self.name += str(self.id)
        Player.id += 1

    def act(self):
        while True:
            try:
                if self.israndom:
                    action = random.choice(actions)
                else:
                    action = input("Make your move:\n[R]-[P]-[S]\n")

                self.movecount[actions.index(action)] += 1
                break
            except:
                print("Invalid move exception")
                continue
        self.action = action


class Computer(Player):
    id = 0

    def __init__(self):
        super().__init__()
        self.name = "Computer"
        self.previndex: int
        self.action: str
        self.id = Computer.id
        if self.id != 0:
            self.name += str(self.id)
        Computer.id += 1

    def act(self):
        if self.previous == 1:
            index = (self.previndex + 1) % 3
        elif self.previous == -1:
            index = (self.previndex - 1) % 3
        else:
            index = random.randint(0, 2)
        act = actions[index]
        self.movecount[index] += 1
        self.previndex = index
        self.action = act


counter = 0
actions = ['R', 'P', 'S']
winner: Player = None


def pushstat(opt: str, col1: str, col2: str, col3: str):
    with open('stats.txt', opt) as stats:
        line = "{0:^10}{1:^10}{2:^10}\n".format(col1, col2, col3)
        stats.write(line)


def getstat(player1: Player, player2: Player):
    moves = ["", "", ""]
    c = counter / 100
    for i in range(len(actions)):
        moves[i] = "{0:<3}{1:>5}{2:>2}{4:^10}{0:<3}{3:>5}{2:>2}".format(actions[i], (player1.movecount[i]/c), "%", (player2.movecount[i]/c), " ")
    status = "{0:<20}{1:<20}\n {2}\n {3}\n {4}".format(player1.name + "moves", player2.name + "moves", *moves)
    print("\n")
    print(status)
    print("\n")
    with open('stats.txt') as stats:
        stat = stats.read()
    print(stat)
    print(player1.name, "won", player1.wincount, "times")
    print(player2.name, "won", player2.wincount, "times")


def checkstatus(player1: Player, player2: Player):

    global winner, counter

    if player1.action == 'R':
        if player2.action == 'R':
            winner = None
            player1.previous = 0
            player2.previous = 0

        elif player2 == 'P':
            winner = player2
            player2.wincount += 1
            player1.previous = -1
            player2.previous = 1

        else:
            winner = player1
            player1.wincount += 1
            player1.previous = 1
            player2.previous = -1

    elif player1.action == 'P':
        if player2.action == 'R':
            winner = player1
            player1.wincount += 1
            player1.previous = 1
            player2.previous = -1

        elif player2.action == 'P':
            winner = None
            player1.previous = 0
            player2.previous = 0

        else:
            winner = player2
            player2.wincount += 1
            player1.previous = -1
            player2.previous = 1

    else:
        if player2.action == 'R':
            winner = player2
            player2.wincount += 1
            player1.previous = -1
            player2.previous = 1

        elif player2.action == 'P':
            winner = player1
            player1.wincount += 1
            player1.previous = 1
            player2.previous = -1

        else:
            winner = None
            player1.previous = 0
            player2.previous = 0
    counter += 1


def start(rand=False, loopcount=None, aimatch=False):
    if aimatch:
        player1 = Computer()
    else:
        player1 = Player(rand)
    player2 = Computer()
    pushstat('w', player1.name, player2.name, 'WINNER')
    for i in range(loopcount):
        loop(player1, player2)
    getstat(player1, player2)


def loop(player1: Player, player2: Player):
    player1.act()
    player2.act()
    checkstatus(player1, player2)
    print(player1.name, "move:", player1.action)
    print(player2.name, "move:", player2.action)
    if winner:
        pushstat('a', player1.action, player2.action, winner.name)
        print("The winner is", winner.name)
    else:
        pushstat('a', player1.action, player2.action, "-")
        print("It was a tie!")


if __name__ == '__main__':
    rand = False
    loopcount = 100

    start(rand, loopcount, aimatch=True)
