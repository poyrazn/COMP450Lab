#
# week1
# COMP450Lab
#
# Created by Nehir Poyraz on 28.09.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.


import random


counter = 0
actions = ['R', 'P', 'S']
playermoves = [0, 0, 0]
computermoves = [0, 0, 0]
previous = None
previndex = None
winner = None
playerwin = 0
computerwin = 0


def pushstat(opt, col1, col2, col3):
    with open('stats.txt', opt) as stats:
        line = "{0:^10}{1:^10}{2:^10}\n".format(col1, col2, col3)
        stats.write(line)


pushstat('w', 'PLAYER', 'COMPUTER', 'WINNER')


def getstat():
    global counter, playermoves, computermoves, playerwin, computerwin
    moves = ["", "", ""]
    c = counter / 100
    for i in range(len(actions)):
        moves[i] = "{0:<3}{1:>5}{2:>2}{4:^10}{0:<3}{3:>5}{2:>2}".format(actions[i], (playermoves[i]/c), "%", (computermoves[i]/c), " ")
    status = "{0:<20}{1:<20}\n {2}\n {3}\n {4}".format("Player moves", "Computer moves", *moves)
    print("\n")
    print(status)
    print("\n")
    with open('stats.txt') as stats:
        stat = stats.read()
    print(stat)
    print("Player won", playerwin, "times")
    print("Computer won", computerwin, "times")

def checkstatus(playeract, computeract):

    global winner, previous, counter, computerwin, playerwin

    if playeract == 'R':
        if computeract == 'R':
            previous = 't'
            winner = '-'
        elif computeract == 'P':
            previous = 'w'
            winner = 'computer'
            computerwin += 1
        else:
            previous = 'l'
            winner = 'player'
            playerwin += 1

    elif playeract == 'P':
        if computeract == 'R':
            previous = 'l'
            winner = 'player'
            playerwin += 1
        elif computeract == 'P':
            previous = 't'
            winner = '-'
        else:
            previous = 'w'
            winner = 'computer'
            computerwin += 1

    else:
        if computeract == 'R':
            previous = 'w'
            winner = 'computer'
            computerwin += 1
        elif computeract == 'P':
            previous = 'l'
            winner = 'player'
        else:
            previous = 't'
            winner = '-'
    counter += 1
    pushstat('a', playeract, computeract, winner)


def start(test=False, n=None):
    for i in range(n):
        loop(test)


def loop(test):

    playeract = playeraction(test)
    computeract = computeraction()
    checkstatus(playeract, computeract)


def playeraction(test=False):

    while True:
        try:
            if test:
                playeract = random.choice(actions)
            else:
                playeract = input("Make your move:\n[R]-[P]-[S]\n")
            global playermoves
            playermoves[actions.index(playeract)] += 1
            break
        except:
            print("Invalid move exception")
            continue
    return playeract


def computeraction():
    global previndex
    if previous == 'w':
        index = (previndex + 1) % 3
    elif previous == 'l':
        index = (previndex - 1) % 3
    else:
        index = random.randint(0, 2)
    compact = actions[index]
    global computermoves
    computermoves[index] += 1
    previndex = index
    return compact


if __name__ == '__main__':

    start(False, 5)
    getstat()