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
moves = [False, False, False]
previous = None
previndex = None
winner = None


def pushstat(opt, col1, col2, col3):
    with open('stats.txt', opt) as stats:
        line = "{0:^10}{1:^10}{2:^10}\n".format(col1, col2, col3)
        stats.write(line)


pushstat('w', 'PLAYER', 'COMPUTER', 'WINNER')


def getstat():
    global counter, playermoves, computermoves
    pmoves, cmoves = [0, 0, 0], [0, 0, 0]
    for i in range(len(actions)):
        pmoves[i] = str(playermoves[i] / counter * 100) + "%"
        cmoves[i] = str(computermoves[i] / counter * 100) + "%"
    status = "{0:^20}{1:^20}\n{2:^20}{5:^20}\n{3:^20}{6:^20}\n{4:^20}{7:^20}".format("Player moves", "Computer moves",
                                                                                     *pmoves, *cmoves)
    print(status)
    print("\n\n")
    with open('stats.txt') as stats:
        stat = stats.read()
    print(stat)



def checkstatus(playeract, computeract):

    global winner, previous, counter

    if playeract == 'R':
        if computeract == 'R':
            previous = 't'
            winner = '-'
        elif computeract == 'P':
            previous = 'w'
            winner = 'computer'
        else:
            previous = 'l'
            winner = 'player'

    elif playeract == 'P':
        if computeract == 'R':
            previous = 'l'
            winner = 'player'
        elif computeract == 'P':
            previous = 't'
            winner = '-'
        else:
            previous = 'w'
            winner = 'computer'

    else:
        if computeract == 'R':
            previous = 'w'
            winner = 'computer'
        elif computeract == 'P':
            previous = 'l'
            winner = 'player'
        else:
            previous = 't'
            winner = '-'
    counter += 1
    pushstat('a', playeract, computeract, winner)

#def start():
    # loop()


def loop():
    playeract = playeraction()
    computeract = computeraction()
    checkstatus(playeract, computeract)

# victory condition check
    # increment match counter


#def test():
    # initialize the counter
    # set list of actions
    # loop(10000)
    # stats



def playeraction():
    while True:
        try:
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



for i in range(5):
    loop()
getstat()