import math
import random

def get_number_of_collisions(arr):
    n = len(arr)
    collisions =0

    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j] or abs(arr[i]-arr[j])== abs(i-j):
                collisions += 1

    return collisions

def get_evaluation(arr):
    return -get_number_of_collisions(arr)

def gridFunction(arr):
    n =len(arr)

    for i in range(n):
        row = ['.'] *n
        row[arr[i]] = 'Q'
        print(" ".join(row))
    print()

def resultingFunction(startState,startTemp,maximumIterations,probability):
    runningState=startState.copy()
    runningTemp=startTemp

    while runningTemp > 0:
        for _ in range(maximumIterations):
            neighbors =[]

            for i in range(len(runningState)):
                for j in range(1, 4):
                    neighbor=runningState.copy()
                    neighbor[i]=(neighbor[i] +j)%4
                    neighbors.append(neighbor)

            best_neighbour = max(neighbors, key=get_evaluation)

            deltaE=get_evaluation(best_neighbour) - get_evaluation(runningState)

            if deltaE > 0 or random.randint(1, 100) <= math.floor(probability * 100):
                runningState =best_neighbour


        if get_number_of_collisions(runningState)==0:
            return runningState


        runningState=[random.randint(0, 3) for _ in range(4)]
        runningTemp -=1


    return runningState

def main():
    random.seed(42)
    startState=[random.randint(0, 3) for _ in range(4)]
    startTemp=1000
    maximumIterations=1000
    probability=0.5
    final = resultingFunction(startState,startTemp,maximumIterations,probability)
    print("The final state of the Queens without collisions is shown in the grid below:")
    gridFunction(final)
if __name__ == "__main__":
    main()
