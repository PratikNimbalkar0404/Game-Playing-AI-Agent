import random
import time
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        p = self.player_number
        n = state[1][1].get_int()
        start_time = time.clock()
        time_difference = 0.05
        def nextplayer(n):
            if(n==2):
                return 1
            else:
                return 2
        def evalutionFunction(state):
            return get_pts(p,state[0]) - 2*get_pts(nextplayer(p),state[0])
        def Action(state,a,v):
            tempboard = state[0]
            board2 = []
            for i in range(len(tempboard)):
                board2.append(tempboard[i][0:])
            board = np.array(board2)
            if(a[-1] != 'p'):
                for i in range(len(board)-1,-1,-1):
                    if(board[i][int(a)] == 0):
                        board[i][int(a)] = v
                        break
            else:
                l = 0
                for i in range(len(board)-2,0,-1):
                    if(i == 0):
                        board[i][int(a[:-1])] = 0
                    else:
                        board[i][int(a[:-1])] = board[i-1][int(a[:-1])]
                        if board[i-1][int(a[:-1])] == 0 : break
            return board, state[1]
        # Against an Adversarial Agent
        def max(state,a,b,pop,d):
            if(time.clock() - start_time > self.time - time_difference):
                return [evalutionFunction(state),'-1']
            if(d==0 or len(get_valid_actions(p,state)) == 0):
                return [evalutionFunction(state),'-1']
            current = [-np.inf,'-1']
            for i in get_valid_actions(p,state):
                succesor  = []
                if(i[1] == False):
                    succesor = min(Action(state,str(i[0]),p),a,b,pop,d-1)
                    succesor[1] = i
                else:
                    if(pop == 0):
                        break
                    succesor = min(Action(state,str(i[0])+'p',p),a,b,pop-1,d-1)
                    succesor[1] = i
                if(succesor[0] > current[0]):
                    current = succesor
                if(current[0]>=b):
                    return current
                if(current[0]>a):
                    a = current[0]
            return current
        # Against an Adversarial Agent
        def min(state,a,b,pop,d):
            if(time.clock() - start_time > self.time - time_difference):
                    return [evalutionFunction(state),'-1']
            if(d==0 or len(get_valid_actions(p,state)) == 0):
                return [evalutionFunction(state),'-1']
            current = [np.inf,'-1']
            for i in get_valid_actions(p,state):
                succesor  = []
                if(i[1] == False):
                    succesor = max(Action(state,str(i[0]),nextplayer(p)),a,b,pop,d-1)
                    succesor[1] = i
                else:
                    if(pop == 0):
                        break
                    succesor = max(Action(state,str(i[0])+'p',nextplayer(p)),a,b,pop-1,d-1)
                    succesor[1] = i
                if(succesor[0] < current[0]):
                    current = succesor
                if(current[0]<=a):

                    return current
                if(current[0]<b):
                    b = current[0]
            return current
        # Iterative Deepening
        t = 1
        while(True):
            next_action = max(state,-np.inf,np.inf,n,t)
            t = t + 1
            if(time.clock() - start_time > self.time - time_difference):
                if(current_action[1] == '-1'):
                    for i in get_valid_actions(p,state):
                        return i
                return current_action[1]
            current_action =  next_action

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        p = self.player_number
        n = state[1][1].get_int()
        start_time = time.clock()
        time_difference = 0.05
        def nextplayer(n):
            if(n==2):
                return 1
            else:
                return 2
        def evalutionFunction(state):
            return get_pts(p,state[0]) - 2*get_pts(nextplayer(p),state[0])
        def Action(state,a,v):
            tempboard = state[0]
            board2 = []
            for i in range(len(tempboard)):
                board2.append(tempboard[i][0:])
            board = np.array(board2)
            if(a[-1] != 'p'):
                for i in range(len(board)-1,-1,-1):
                    if(board[i][int(a)] == 0):
                        board[i][int(a)] = v
                        break
            else:
                l = 0
                for i in range(len(board)-2,0,-1):
                    if(i == 0):
                        board[i][int(a[:-1])] = 0
                    else:
                        board[i][int(a[:-1])] = board[i-1][int(a[:-1])]
                        if board[i-1][int(a[:-1])] == 0 : break
            return board, state[1]
        # Against an Random Agent
        def expectimax(state,pop,d):
            if(time.clock() - start_time > self.time - time_difference):
                return [evalutionFunction(state),'-1']
            if(d==0 or len(get_valid_actions(p,state)) == 0):
                return [evalutionFunction(state),'-1']
            current = [-np.inf,'-1']
            for i in get_valid_actions(p,state):
                succesor  = []
                if(i[1] == False):
                    succesor = expectimin(Action(state,str(i[0]),p),pop,d-1)
                    succesor[1] = i
                else:
                    if(pop == 0):
                        break
                    succesor = expectimin(Action(state,str(i[0])+'p',p),pop-1,d-1)
                    succesor[1] = i
                if(succesor[0] > current[0]):
                    current = succesor
            return current
        # Against an Random Agent
        def expectimin(state,pop,d):
            if(time.clock() - start_time > self.time - time_difference):
                return [evalutionFunction(state),'-1']
            if(d==0 or len(get_valid_actions(p,state)) == 0):
                return [evalutionFunction(state),'-1']
            current = [0,'-1']
            s = 0
            for i in get_valid_actions(p,state):
                s = s + 1
                succesor  = []
                if(i[1] == False):
                    succesor = expectimax(Action(state,str(i[0]),nextplayer(p)),pop,d-1)
                    succesor[1] = i
                else:
                    if(pop == 0):
                        break
                    succesor = expectimax(Action(state,str(i[0])+'p',nextplayer(p)),pop-1,d-1)
                    succesor[1] = i
                current[0] = current[0] + succesor[0]
            current[0] = current[0] / s
            return current
        # Iterative Deepening
        t = 1
        while(True):
            next_action = expectimax(state,n,t)
            t = t + 1
            if(time.clock() - start_time > self.time - time_difference):
                if(current_action[1] == '-1'):
                    for i in get_valid_actions(p,state):
                        return i
                return current_action[1]
            current_action =  next_action
        # Do the rest of your implementation here
