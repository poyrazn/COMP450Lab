#
# week2
# COMP450Lab
#
# Created by Nehir Poyraz on 5.10.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.

class State(object):
    def __init__(self, cannibals, missionaries, boatpos):
        """
        Class constructor
        :param cannibals: int, number of cannibals on the left side  of the river
        :param missionaries: int, number of missionaries on left side of the river
        :param boatpos: str, boat's position on the river(side)
        """
        self.state = cannibals, missionaries, boatpos    # State name i.e initial state name is (3, 3, 'L')
        self.cannibals = cannibals
        self.missionaries = missionaries
        self.boatpos = boatpos
        self.parent: State = None                       # State object that is parent to this state intance(self)
        self.children = []                              # list of children states of self


    def action(self, boat: list):
        """ method of the State class returns the next state (State object)
            parameters
            self: State object
            boat: list of integers  -- usage = [c,m]  c: #of cannibals, m: #of missionaries on the boat
            """
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
        # a new state is returned
        return state

    def isGoal(self):
        """
        goal state = (0, 0, 'R')
        all the cannibals and the missionaries is on the right side (0 on the left), the boat is also on the right (R)
        :return: True if self is the goal state
        """
        if self.state == (0, 0, 'R'):
            return True
        return False

    def isValid(self):
        """
        method of the State class returns bool value
        restrictions:
        (number of cannibals can't be more than number of missionaries in either side of the river)

        :return: True if the state is valid
        """
        if 0 <= self.cannibals <= 3 and 0 <= self.missionaries <= 3:
            cright = 3 - self.cannibals
            mright = 3 - self.missionaries
            if (self.cannibals <= self.missionaries or self.missionaries == 0) and (cright <= mright or mright == 0):

                return True
        return False


def loop(current_state: State, visited_states: list):
    """

    :param current_state:
    :param visited_states:
    :return: next state choosen from the visited states
    """
    print("Current State:", current_state.state)
    for c in range(3):
        for m in range(3):
            boat = [c, m]
            # c: int, number of cannibals on the boat
            # m: int, number of missionaries on the boat
            if 0 < c + m <= 2:  # at least one, at most two person(s) should be on the boat
                next_state = current_state.action(boat) # creates a new state with
                if next_state.isValid():    # check if the next state is valid (both sides of the river should follow the rules)
                    if next_state.state not in visited:         # if next state has never been visited
                        visited_states.append(next_state.state)     # add state to the visited states list
                        current_state.children.append(next_state)   # add state to the current state's children list
                        next_state.parent = current_state           # add current state as parent to next state
                        print("New state visited:", next_state.state)
                        if next_state.isGoal():                 # check if the next state is final state
                            global final
                            final = True
                            break
                    else:
                        print("No new discovery")
    global index
    index += 1
    # choose the next state to go (from the visited states)
    return_state = State(visited_states[index][0], visited_states[index][1], visited_states[index][2])
    return return_state




if __name__ == '__main__':
    start = State(3, 3, "L")
    visited = [start.state]
    global index
    global final
    index = 0
    final = False
    while not final:    # The loop will stop when we reached the final state
        start = loop(start, visited)
    print("It took", index, "moves to figure it out.")





