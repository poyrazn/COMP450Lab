#
# week8
# COMP450Lab
#
# Created by Nehir Poyraz on 16.11.2018
# Copyright © 2018 Nehir Poyraz. All rights reserved.



import itertools
from utils import Expr, expr, first
from logic import FolKB
import numpy as np
import random

class PDLL:
    """
    PDLL used to define a search problem.
    It stores states in a knowledge base consisting of first order logic statements.
    The conjunction of these logical statements completely defines a state.
    """

    def __init__(self, initial_state, actions, goal_test):
        self.kb = FolKB(initial_state)
        self.actions = actions
        self.goal_test_func = goal_test

    def goal_test(self):
        return self.goal_test_func(self.kb)

    def act(self, action):
        """
        Performs the action given as argument.
        Note that action is an Expr like expr('Remove(Glass, Table)') or expr('Eat(Sandwich)')
        """
        action_name = action.op
        args = action.args
        list_action = first(a for a in self.actions if a.name == action_name)
        if list_action is None:
            raise Exception("Action '{}' not found".format(action_name))
        if not list_action.check_precond(self.kb, args):
            raise Exception("Action '{}' pre-conditions not satisfied".format(action))
        list_action(self.kb, args)


class Action:
    """
    Defines an action schema using preconditions and effects.
    Use this to describe actions in PDDL.
    action is an Expr where variables are given as arguments(args).
    Precondition and effect are both lists with positive and negated literals.
    Example:
    precond_pos = [expr("Human(person)"), expr("Hungry(Person)")]
    precond_neg = [expr("Eaten(food)")]
    effect_add = [expr("Eaten(food)")]
    effect_rem = [expr("Hungry(person)")]
    eat = Action(expr("Eat(person, food)"), [precond_pos, precond_neg], [effect_add, effect_rem])
    """

    def __init__(self, action, precond, effect):
        self.name = action.op
        self.args = action.args
        self.precond_pos = precond[0]
        self.precond_neg = precond[1]
        self.effect_add = effect[0]
        self.effect_rem = effect[1]

    def __call__(self, kb, args):
        return self.act(kb, args)

    def substitute(self, e, args):
        """Replaces variables in expression with their respective Propositional symbol"""
        new_args = list(e.args)
        for num, x in enumerate(e.args):
            for i in range(len(self.args)):
                if self.args[i] == x:
                    new_args[num] = args[i]
        return Expr(e.op, *new_args)

    def check_precond(self, kb, args):
        """Checks if the precondition is satisfied in the current state"""
        # check for positive clauses
        for clause in self.precond_pos:
            if self.substitute(clause, args) not in kb.clauses:
                return False
        # check for negative clauses
        for clause in self.precond_neg:
            if self.substitute(clause, args) in kb.clauses:
                return False
        return True

    def act(self, kb, args):
        """Executes the action on the state's kb"""
        # check if the preconditions are satisfied
        if not self.check_precond(kb, args):
            raise Exception("Action pre-conditions not satisfied")
        # remove negative literals
        for clause in self.effect_rem:
            kb.retract(self.substitute(clause, args))
        # add positive literals
        for clause in self.effect_add:
            kb.tell(self.substitute(clause, args))


def three_block_tower(initial_state=False):
    # Defines a PDLL object (class definition is above) for the three block tower and returns it.

    # I have also defined a positional argument as initial_state
    # If it is predefined and passed as an argument, it will be the initial state.
    # Else, the initial state would be defined as follows
    if not initial_state:

        # Blocks A and B are on table, block C is on block A
        init = [expr('On(A, Table)'),
                expr('On(B, Table)'),
                expr('On(C, A)'),
                expr('Block(A)'),
                expr('Block(B)'),
                expr('Block(C)'),
                expr('Clear(B)'),
                expr('Clear(C)')]
    else:
        init = initial_state

    def goal_test(kb):
        # goal state: blocks are stacked on top of each other with C at the bottom and C at the very top. (C, B, A)
        required = [expr('On(A, B)'), expr('On(B, C)')]
        for q in required:
            if kb.ask(q) is False:
                return False
        return True

    # Actions

    # Actions have been defined below. Parameters are the same as given in Action Class parametes.

    #  Move
    precond_pos = [expr('On(b, x)'), expr('Clear(b)'), expr('Clear(y)'), expr('Block(b)'),
                   expr('Block(y)')]
    precond_neg = []
    effect_add = [expr('On(b, y)'), expr('Clear(x)')]
    effect_rem = [expr('On(b, x)'), expr('Clear(y)')]
    move = Action(expr('Move(b, x, y)'), [precond_pos, precond_neg], [effect_add, effect_rem])

    #  MoveToTable
    precond_pos = [expr('On(b, x)'), expr('Clear(b)'), expr('Block(b)')]
    precond_neg = []
    effect_add = [expr('On(b, Table)'), expr('Clear(x)')]
    effect_rem = [expr('On(b, x)')]
    moveToTable = Action(expr('MoveToTable(b, x)'), [precond_pos, precond_neg],
                         [effect_add, effect_rem])

    return PDLL(init, [move, moveToTable], goal_test)

# init = [expr('On(C, Table)'),
#                 expr('On(B, C)'),
#                 expr('On(A, B)')]
# myPDLL = three_block_tower(init)
# print(myPDLL.kb.clauses)
# print(myPDLL.goal_test())

#Task 2A



class WUMBUS:

    """ environment is a room of n x n blocks (ndarray w/ shape=(n,n) and datatype is tuple)
        n-1 blocks (randomly assigned) have dirt, that will be cleaned by the agent
        n-2 blocks (randomly assigned) have stuff (that agent cannot clean) (agent cannot go these blocks)

        If the first element of the tuple is -1 (presence) or 1 (absence), annotating the presence of the agent.
        The numbers are arbitrary and chosen for visual easiness.
        Else (0), means that there is a block.
        Second element of the tuple represents the dirt in binary. 0 is clean, 1 is dirty.
        (If the block is obstructed, it can't be dirty.)
        (1, 0) --> Agent is not here, floor is clean (available cell, agent can come here)
        (1, 1) --> Agent is not here, floor is dirty (available cell, agent can come here)
        (-1, 1) --> Agent is here, floor is dirty
        (-1, 0) --> Agent is here, floor is clean
        (0, 0) --> There is a block. Agent cannot be here.

        goal: clean the board completely
        actions: move to the neighbors unless there is a stuff,
                clean if there is dirt."""

    def __init__(self, n, start):
        self.environ = np.ndarray(shape=(n, n), dtype=tuple)
        self.environ.fill((1, 0))
        self.dirt = []
        self.stuff = []
        self.pos = start
        self.environ[start] = (-1, 0)
        self.actions = {'left': [0, -1], 'right': [0, 1], 'up': [-1, 0], 'down': [1, 0], 'clean': [0, 0]}
        self.neighbors = self.neighbors_func({})
        self.visited = [self.pos]
        self.directionalcost = []
        self.realcost = []

        for i in range(n - 1):
            if i < n - 2:
                s = (random.randint(0, n - 1), random.randint(0, n - 1))
                while s == start:
                    s = (random.randint(0, n - 1), random.randint(0, n - 1))
                self.stuff.append(s)
                self.environ[s] = (0, self.environ[s][1])

            d = (random.randint(0, n - 1), random.randint(0, n - 1))
            while d in self.stuff:
                d = (random.randint(0, n - 1), random.randint(0, n - 1))
            self.dirt.append(d)
            self.environ[d] = (self.environ[d][0], 1)

    def neighbors_func(self, neighbors):
        neighbors.update(left=(self.pos[0] + self.actions['left'][0], self.pos[1] + self.actions['left'][1]))
        neighbors.update(right=(self.pos[0] + self.actions['right'][0], self.pos[1] + self.actions['right'][1]))
        neighbors.update(up=(self.pos[0] + self.actions['up'][0], self.pos[1] + self.actions['up'][1]))
        neighbors.update(down=(self.pos[0] + self.actions['down'][0], self.pos[1] + self.actions['down'][1]))
        return neighbors


    def isgoal(self):
        if self.dirt:
            return False
        else:
            return True


    def move(self, action):
        if action == 'clean':
            print("\nCLEANING...\n")
            self.dirt.remove(self.pos)
            self.environ[self.pos] = (self.environ[self.pos][0], 0)
        else:
            nextpos = self.neighbors[action]
            # if self.environ[nextpos][0]:
            print("\nMOVING", action, '\n')
            self.environ[self.pos] = (1, self.environ[self.pos][1])
            self.pos = nextpos
            self.neighbors_func(self.neighbors)
            if self.pos not in self.visited:
                self.visited.append(self.pos)
            self.environ[self.pos] = (-1, self.environ[self.pos][1])

    def sense(self):
        directionalcost, realcost = [], []
        for i in range(len(self.dirt)):
            directionalcost.append((self.dirt[i][0] - self.pos[0], self.dirt[i][1] - self.pos[1]))
            realcost.append((abs(directionalcost[i][0]) + abs(directionalcost[i][1])))
        i = realcost.index(min(realcost))
        target = self.dirt[i]
        targetcost = directionalcost[i]
        self.directionalcost = directionalcost
        self.realcost = realcost
        return target, targetcost

def Task2A():
    dim = 7
    start = (0, 0)
    agent = WUMBUS(dim, start)

    directions = ['left', 'right', 'up', 'down']
    print(agent.environ)
    print()

    counter = 0
    previous = None
    while not agent.isgoal():
        if agent.environ[agent.pos][1]:     # if dirty
            agent.move('clean')
            print("\nCLEANING...\n")
        a = random.choice(directions)
        if (agent.neighbors[a][0] >= 0 and agent.neighbors[a][0] < dim) and (agent.neighbors[a][1] >= 0 and agent.neighbors[a][1] < dim):
            if agent.environ[agent.neighbors[a]][0]:
                if previous != agent.neighbors[a]:
                    previous = agent.pos
                    agent.move(a)
                print(agent.environ, '\n')
        counter += 1

    print(agent.isgoal())
    print('The room is cleaned in', counter, 'moves')



def Task3A():
    dim = 7
    start = (2, 3)
    agent = WUMBUS(dim, start)

    directions = ['left', 'right', 'up', 'down']
    print("WUMBUS environment")
    print(agent.environ)
    print()

    counter = 0
    while not agent.isgoal():
    # for i in range(3):
        target, cost = agent.sense()
        print('I am on block', agent.pos)
        print('Dirt on locations:', agent.dirt)
        print('Nearest dirt location:', target, 'Required moves:', cost)
        print()

        if cost[0] > 0:     # down
            action = 'down'
        if cost[0] < 0:
            action = 'up'

        while agent.pos[0] - target[0]:
            if agent.environ[agent.neighbors[action]]:
                agent.move(action)
                print('I am on block', agent.pos)
                print(agent.environ)
                counter += 1
            else:
                print('Cannot go anymore.')
                break

        if cost[1] > 0:
            action = 'right'
        if cost[1] < 0:
            action = 'left'
        while agent.pos[1] - target[1]:
            if agent.environ[agent.neighbors[action]]:
                agent.move(action)
                print('I am on block', agent.pos)
                print(agent.environ)
                counter += 1
            else:
                print('Cannot go anymore.')
                break

        if cost == (0, 0) and agent.environ[agent.pos][1]:
            agent.move('clean')
            counter += 1


        print()
        print(agent.environ)
    print(agent.isgoal())
    print('The room is cleaned in', counter, 'moves')



# Task2A()

Task3A()