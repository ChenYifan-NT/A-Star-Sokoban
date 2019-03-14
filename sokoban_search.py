import heapq
import os
# from sokoban import *

class Unexpanded:

    def __init__(self):
        self.unexpanded = []
    
    def push(self, state):
        heapq.heappush(self.unexpanded, state)

    def pop(self):
        return heapq.heappop(self.unexpanded)

    def is_empty(self):
        return not self.unexpanded

class Search:

    def __init__(self, init_state, time_limit=10):
        self.time_limit = time_limit
        # print("System: time limit is " + str(time_limit) + " seconds\n")

        self.unexpanded = Unexpanded()
        self.unexpanded.push(init_state)

        self.loop_dict = dict()
        self.loop_dict[init_state.state_hash()] = init_state.gval

    def search(self):

        self.search_start_time = os.times()[0]
        self.search_stop_time = self.search_start_time + self.time_limit

        while not self.unexpanded.is_empty():
            current_state = self.unexpanded.pop()

            if current_state.is_goal():
                print("System: solution found, returning")
                return True, current_state

            if os.times()[0] > self.search_stop_time:
                print("System: time exceeded")
                return False, current_state

            successors = current_state.successors()

            for st in successors: # st: state
                st_hash = st.state_hash()

                if st_hash in self.loop_dict: # if we have achieved the same state before
                    fm_gval = self.loop_dict[st_hash] # former gval
                    if fm_gval < st.gval: # if former is better than current, then change the current to former
                        st.gval = fm_gval
                    else: # current is better
                        self.loop_dict[st_hash] = st.gval
                    continue

                else:
                    self.unexpanded.push(st)

                    self.loop_dict[st_hash] = st.gval


        print("System: did not find solutions")
        return False, current_state