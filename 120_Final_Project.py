# used to access the code in our path file
import os
# used to randomize the order of the questions and answers in the multiple_choice() function
import random
# used to read excel file
import pandas as pd


# function that prints multiple choice answers and keeps score
def multiple_choice():
    # drops the "Difficulty", "Category", and "Fun Fact" columns so that we are only taking strings from the "Landmarks" and "Locations" columns
    d = dict(df.drop(["Difficulty", "Category", "Fun Fact"], axis=1).to_dict("split")["data"])
    # helps remove nans from the code and assigns the location to the landmark
    d = {k: v for k, v in d.items() if pd.notna(k)}
    # assigns the keys from the dictionary as the landmarks
    locations = list(d.values())
    # assigns the values from the dictionary as the locations
    landmarks = list(d.keys())
    # randomizes the order of the landmarks so that the order of questions will be random
    random.shuffle(landmarks)
    # at the beginning of the quiz, the user's score will be 0
    score = 0
    # allows the quiz to ask a question for every landmark in the list
    # loop stops when all the landmarks have been in a question once
    for k in landmarks:
        print("Where is " + k + "?")
        # chooses 4 random locations from the list
        random_answers = random.sample(list(locations), 4)
        # ensures that random_answers will include the correct answer (that correlates with the landmark the quiz asks about)
        if d[k] not in random_answers:
            random_answers[3] = d[k]
        # ensures that the correct answer will be in a random spot within the random_answers
        random.shuffle(random_answers)
        # prints the index of the random_answers list to label the location and prints random_answer elements
        for i in range(4):
            print(i+1, ": ", random_answers[i])
        quiz = input("Please enter 1, 2, 3, 4, or 0: ")
        # prints if the user selected the correct or the incorrect answer
        if random_answers[int(quiz) - 1] == d[k]:
            score = score + 1
            print("Correct")
            # prints the fun fact
            funfact(k)
        else:
            score = score + 0
            print("Incorrect!")
        # prints current and final score, separating each question with asterisks
        print("Current score is: ", score)
        print("*************************")
    print("Final score: ", score)


# allows the code to print the fun fact
def funfact(k):
    with open('uofl_landmarks_locations.csv', 'r') as f:
        for (i, line) in enumerate(f):
            sline = line.split(',')
            if k in sline:
                print(sline[-1])


# main function
if __name__ == "__main__":
    # allows excel file (with columns: landmarks, locations, difficultly, categories, and fun facts) to be read as a dataframe
    df = pd.read_csv("uofl_landmarks_locations.csv")

    # prints out the main menu choices and allows user to choose which quiz to play
    # calls the multiple_choice() function for each choice
    while input != 0:
        print('Welcome to "Cards on Campus"!')
        print("1 All Landmarks", "\n2 Residence Halls", "\n3 Restaurants", "\n4 Paths", "\n0 Exit")
        choice_1 = input("Select 1, 2, 3, 4, or 0: ")
        # allows the user to choose "Easy" or "Hard" mode for the "All Landmarks" choice
        if choice_1 == "1":
            print("1 Easy", "\n2 Hard")
            choice_1a = input("Select 1 or 2")
            if choice_1a == "1":
                print("Welcome to General Easy Mode!")
                # filters the dataframe items only for the rows that include "Easy" from the "Difficulty" column
                df = df.where(df["Difficulty"] == "Easy")
                multiple_choice()
            if choice_1a == "2":
                print("Welcome to General Hard Mode!")
                # filters the dataframe items only for the rows that include "Hard" from the "Difficulty" column
                df = df.where(df["Difficulty"] == "Hard")
                multiple_choice()
        if choice_1 == "2":
            print("Welcome to Residence Halls Quiz!")
            # filters the dataframe items only for the rows that include "Residence Hall" from the "Category" column
            df = df.where(df["Category"] == "Residence Hall")
            multiple_choice()
        if choice_1 == "3":
            print("Welcome to Restaurants Quiz!")
            # filters the dataframe items only for the rows that include "Restaurant" from the "Category" column
            df = df.where(df["Category"] == "Restaurant")
            multiple_choice()
        if choice_1 == "4":
            # allows code to access another file that runs the code for the path quiz
            os.system("python path.py")
        # allows user to exit and return to the main menu
        if choice_1 == "0":
            break
        else:
            print("Play again!")
            continue
