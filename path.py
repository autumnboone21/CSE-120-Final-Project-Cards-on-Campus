# used to read excel file
import pandas as pd
# used to access the numpy library
import numpy as np
# used to create a random path
import random


# creates random path from initial location to the destination
# initial_location and destination are inputs from the user
# landmark_tocoordinate and coordinate_tolandmark are dictionaries
def path(initial_location, destination, landmark_tocoordinate, coordinate_tolandmark):
    # creates a variable for the coordinate of the initial location
    initial_coor = landmark_tocoordinate[initial_location]
    # creates a variable for the coordinate of the destination
    dest_coor = landmark_tocoordinate[destination]
    # variable assigned as the variable for the initial coordinate
    next_step = initial_coor

    # creates the amount of steps (1 step each time) in which the the path will go in a certain direction
    north_south = -(initial_coor[1] - dest_coor[1]) / int(np.abs(initial_coor[1] - dest_coor[1]))
    east_west = -(initial_coor[0] - dest_coor[0]) / int(np.abs(initial_coor[0] - dest_coor[0]))

    # finds the amount of steps needed in order to reach the destination
    x = random.sample(range(np.abs(initial_coor[1] - dest_coor[1]) + np.abs(initial_coor[0] - dest_coor[0])), np.abs(initial_coor[0] - dest_coor[0]))
    for z in range(np.abs(initial_coor[1] - dest_coor[1]) + np.abs(initial_coor[0] - dest_coor[0])):
        # creates the coordinate for the next step based on the coordinate of the previous landmark
        if z in x:
            current = next_step
            next_step = (int(next_step[0] + north_south), int(next_step[1]))
        else:
            current = next_step
            next_step = (int(next_step[0]), int(next_step[1] + east_west))

        # allows the user to estimate how much distance they need to go
        # makes the code print "next block" instead of "nan" to help the user understand their path
        if coordinate_tolandmark[next_step] == "nan":
            coordinate_tolandmark[next_step] = "next block"
        elif coordinate_tolandmark[current] == "nan":
            coordinate_tolandmark[current] = "next block"

        # based on the coordinates of the excel file, this prints the direction in which the user needs to go
        if current[0] < next_step[0] and current[1] == next_step[1]:
            print("You will go south of", coordinate_tolandmark[current], "to the", coordinate_tolandmark[next_step])
        elif current[0] > next_step[0] and current[1] == next_step[1]:
            print("You will go north of the", coordinate_tolandmark[current], "to the", coordinate_tolandmark[next_step])
        elif current[1] < next_step[1] and current[0] == next_step[0]:
            print("You will go east of the", coordinate_tolandmark[current], "to the", coordinate_tolandmark[next_step])
        elif current[1] > next_step[1] and current[0] == next_step[0]:
            print("You will go west of the", coordinate_tolandmark[current], "to the", coordinate_tolandmark[next_step])


# main function
if __name__ == '__main__':
    # allows excel file (with map of campus) to be read as a dataframe
    df = pd.read_csv("uofl_landmarks_map.csv", header=None)

    # converts values in dataframe to a list
    landmarks = df.values.tolist()

    # creates matrix to find coordinates of landmarks
    matrix = np.array(landmarks)
    # creates the dictionaries
    landmark_tocoordinate = dict()
    coordinate_tolandmark = dict()
    # finds the coordinates for each landmark
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # only creates coordinates for the strings, not the nans(empty spaces from the excel file)
            if matrix[i][j] != np.nan:
                # assigns the dictionary key as the landmark and the value as the coordinate
                landmark_tocoordinate[matrix[i][j]] = (i, j)
                # assigns the dictionary key as the coordinate and the value as the landmark
                coordinate_tolandmark[(i, j)] = matrix[i][j]

    # asks the user where they are and where they want to go
    initial_location = input("Which building are you close to right now?")
    destination = input("Where do you want to go?")

    # verifies that the user is spelling the landmarks correctly
    if initial_location and destination is df:
        path(initial_location, destination, landmark_tocoordinate, coordinate_tolandmark)
    else:
        print("Please Answer The Questions Correctly")

    # if the landmark that the user is in is adjacent to the destination, this tells the user that the landmark is very close to them
    if path(initial_location, destination, landmark_tocoordinate, coordinate_tolandmark) is not None:
        print("You will pass", path(initial_location, destination, landmark_tocoordinate, coordinate_tolandmark),
              "into order to get to", destination)
    if path(initial_location, destination, landmark_tocoordinate, coordinate_tolandmark) is None:
        print(initial_location, "is next door to", destination)
