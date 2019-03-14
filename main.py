from sokoban_search import Search
from sokoban import SokobanState
from read_problems import problems_in
from astar import HEUR
# from trivial_test_problems import TEST_PROBLEMS

import time
import os
import csv

PROBLEMS = problems_in() # problems are from Microban by David W. Skinnner
DEMO = False # whether to demonstrate the path

problem_index = range(len(PROBLEMS))
#problem_index = range(20)
solved = [0] * len(problem_index)
unsolved = []
os.system('cls')

tic_total = os.times()[0]

for i in problem_index:
    se = Search(PROBLEMS[i]) # initalize searching

    print("\n-->\nSystem: searching problem #" + str(i + 1))
    # start searching
    tic = os.times()[0]
    a, b = se.search() # a: true or false, whether searching is successful; b: last sokoban state searched
    toc = os.times()[0]
    # end searching
    searching_time = toc - tic
    print("System: searching time: " + str(searching_time) + 's')

    if a == True:
        solved[i] = searching_time
    else:
        unsolved.append(i + 1)
        solved[i] = -1

    if DEMO:
        if a == True:
            state_count = 0

            time.sleep(2) # wait for some time and print the board

            lst = []
            p = b
            while p:
                lst.append(p)
                p = p.predecessor
                state_count += 1
            
            while lst:
                b = lst.pop()
                os.system('cls')
                b.print_board()

                time.sleep(0.35)

            print("System: total steps: " + str(state_count - 1)) # the "start" state does not count as a step

toc_total = os.times()[0]
# show summary of the searching
print("From {} of questions, {} are solved, {} are unsolved".format(len(problem_index), len(solved) - len(unsolved), len(unsolved)))
if unsolved:
    print("The indexs of unsolved quesions are:")
    print(unsolved)

print("System: using " + str(HEUR))
print('\nTotal searching time for {} questions is {} seconds'.format(len(PROBLEMS), toc_total - tic_total))

with open(str(HEUR) + '.csv', 'w') as csvfile:
    fieldname = ['index', 'search time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldname)

    writer.writeheader()
    for i in range(len(solved)):
        writer.writerow({'index': i + 1, 'search time': solved[i]})