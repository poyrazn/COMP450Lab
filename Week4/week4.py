#
# week4
# COMP450Lab
#
# Created by Nehir Poyraz on 19.10.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.


import random as r

iterations = 10000
wins = 0.0
losses = 0.0

#Task1 user plays
def game():
    global wins
    global losses
    for i in range(iterations):
        numberofdoors = 3
        doors = [i for i in range(numberofdoors)]
        carindex = r.randint(0, numberofdoors-1)
        print(doors)
        choice = int(input("Choose a door from the list "))
        dooropen = r.choice(doors)
        while (dooropen == choice) or (dooropen == carindex):
            dooropen = r.randint(0, numberofdoors-1)
        doors.remove(dooropen)
        doors.insert(dooropen, "Goat")
        print("There is a goat behind the door", dooropen)
        print(doors)
        select = input("Do you want to stay with the choice you want or do you want to change? [C/S] ")
        if select == 'S':
            if choice == carindex:
                print("You win")
                wins += 1
            else:
                print("You lose")
                losses += 1
        else:
            if choice == "Car":
                print("You lose")
                losses += 1
            else:
                print("You win")
                wins += 1

#Task2 random game & user stays with the choice s/he made
def testStay():
    global wins
    global losses
    for i in range(iterations):
        numberofdoors = 3
        doors = [i for i in range(numberofdoors)]
        carindex = r.randint(0, numberofdoors-1)
        choice = r.choice(doors)
        dooropen = r.choice(doors)
        while (dooropen == choice) or (dooropen == carindex):
            dooropen = r.choice(doors)
        doors.remove(dooropen)
        select = 'S'
        if select == 'S':
            if choice == carindex:
                wins += 1
            else:
                losses += 1
        else:
            if choice == carindex:
                losses += 1
            else:
                wins += 1

#Task3 random game & user changes the choice
def testChange():
    global wins
    global losses
    for i in range(iterations):
        numberofdoors = 3
        doors = [i for i in range(numberofdoors)]
        carindex = r.randint(0, numberofdoors-1)
        choice = r.choice(doors)
        dooropen = r.choice(doors)
        while (dooropen == choice) or (dooropen == carindex):
            dooropen = r.choice(doors)
        doors.remove(dooropen)
        select = 'C'
        if select == 'S':
            if choice == carindex:
                wins += 1
            else:
                losses += 1
        else:
            if choice == carindex:
                losses += 1
            else:
                wins += 1



if __name__ == '__main__':
    testChange()
    percentage = (wins / iterations) * 100
    print("Wins: " + str(wins))
    print("Losses: " + str(losses))
    print("You won " + str(percentage) + "% of the time")