#
# week2
# COMP450Lab
#
# Created by Nehir Poyraz on 5.10.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.

class State(object):
    def __init__(self, cannibals, missionaries, boatpos):
        self.state = cannibals, missionaries, boatpos    # State name i.e initial state name is (3, 3, 'L')
        self.cannibals = cannibals                      # Number of cannibals on left side of the river
        self.missionaries = missionaries                # Number of missionaries on left side of the river
        self.boatpos = boatpos                          # Boat's position on the river(side)
        self.parent: State = None                       # State object that is parent to this state instance
        self.children = []                              # list of children states
#        self.parenthood = False                         # True if this state is parent to another state
#        self.childhood = False                          # True if this state is child of another state

    def action(self, boat):
        if self.boatpos == 'L':
            # if boat is on the left side in this state, passengers will go from left to right
            # then for the new state the passengers on the boat should be subtracted from the existing state values
            # (state attributes always indicates the left side)
            cannibals = self.cannibals - boat[0]    # arg to next state
            missionaries = self.missionaries - boat[1]  # arg to next state
            boatpos = 'R'           # arg to next state
        if self.boatpos == 'R':
            # if boat is on the right side in this state, passengers will go from right to left
            # then the passengers on the boat should be added to the state values
            cannibals = self.cannibals + boat[0]    # arg to next state
            missionaries = self.missionaries + boat[1]  # arg to next state
            boatpos = 'L'   # arg to next state
        state = State(cannibals, missionaries, boatpos)
        return state

    def isGoal(self):
        if self.state == (0, 0, 'R'):
            return True
        return False

    def isValid(self):
        if 0 <= self.cannibals <= 3 and 0 <= self.missionaries <= 3:
            cright = 3 - self.cannibals
            mright = 3 - self.missionaries
            if (self.cannibals <= self.missionaries or self.missionaries == 0) and (cright <= mright or mright == 0):
                # restrictions for number of cannibals and missionaries
                return True
        return False


def loop(current: State, visited: list):
    print("Current State:", current.state)

    for c in range(3):
        for m in range(3):
            boat = [c, m]
            if 0 < c + m <= 2:
                next_state = current.action(boat)
                if next_state.isValid():
                    if next_state.state not in visited:
                        visited.append(next_state.state)
                        current.children.append(next_state)
                        next_state.parent = current
                        print("New State:", next_state.state)
                        if next_state.isGoal():
                            global found
                            found = True
                            break
    global index
    index += 1
    return State(visited[index][0], visited[index][1], visited[index][2])




if __name__ == '__main__':
    start = State(3, 3, "L")
    visited = [start.state]
    global index
    global found
    index = 0
    found = False
    while not found:
        start = loop(start, visited)
    print("It took", index, "moves to figure it out.")





