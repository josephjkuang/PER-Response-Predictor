# Script that will graph the classification data
import csv
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy
import pandas as pd
from scipy import stats

# Stopping Points in the Data
starting_point = 12
stopping_point1 = 267
stopping_point1half = 341
stopping_point2 = 500
stopping_point3 = 72
stopping_point4 = 136
unreachable = 999999
dot_size = 100

# Lists to store the classification scores
# Correct is the score given to the human-decided correct code
# Incorrect is the score given to the highest human-decided incorrect code
uncertainty_correct = []
uncertainty_incorrect = []
average_correct = []
average_incorrect = []
percenterror_correct = []
percenterror_incorrect = []
qualset_correct = []
qualset_incorrect = []

# CSV Row Assignments
student_id = 0
qual_set = 1
average = 2
percent_error = 3
uncertainty = 4
our_code = 5

def store_file_data(path):
    with open(path) as file:
        reader = csv.reader(file)
        r_list = [r for r in reader]  # convert csv file to a python list
        labels = r_list.pop(0)
    return r_list

 # Parsing Through the Data to Add the Correct and Incorrect Scores
 # @params r_list is the Data to parse through
 # @params start is the first student id we want to look at
 # @params stop is the last student id we want to look at
def parse_file(r_list, start, stop):
    startable = False
    for row in r_list:
        # Checking to see if we should start looking at the data yet
        if int(row[student_id]) == start:
            startable = True

        if startable:
            if row[our_code] == "uncertainty":
                uncertainty_correct.append(float(row[uncertainty]))
                uncertainty_incorrect.append(find_incorrect(row, uncertainty))
            elif row[our_code] == "average":
                average_correct.append(float(row[average]))
                average_incorrect.append(find_incorrect(row, average))
            elif row[our_code] == "percenterror":
                percenterror_correct.append(float(row[percent_error]))
                percenterror_incorrect.append(find_incorrect(row, percent_error))
            elif row[our_code] == "qualset":
                qualset_correct.append(float(row[qual_set]))
                qualset_incorrect.append(find_incorrect(row, qual_set))

            # Stopping at a certain ID
            if int(row[student_id]) == stop: 
                break

# Method that finds the highest incorrect classification percentaghe
def find_incorrect(row, number): 
    percentage = 0
    for i in range(1, 5):
        if i == number: # Don't want the correct code
            continue
        elif float(row[i]) > percentage:
            percentage = float(row[i])

    return percentage

# Method to draw scatter plots
# @params title is the name that we want to call the file.
def create_confidence_correlation(title): 
    # Plotting the dots for the graph
    plt.scatter(uncertainty_correct, uncertainty_incorrect, color = "red", marker = "x", label = "uncertainty", s = dot_size)
    plt.scatter(average_correct, average_incorrect, color = "blue", marker = "+", label = "average", s = dot_size)
    plt.scatter(percenterror_correct, percenterror_incorrect, color = "green", marker = "o", label = "percent error", s = dot_size)
    plt.scatter(qualset_correct, qualset_incorrect, color = "purple", marker= "*", label = "qual set", s = dot_size)

    # Labeling the Graph
    plt.legend(loc="upper right")
    plt.title(title)
    plt.xlabel("Score for Correctly Coded Term'")
    plt.ylabel("Highest Incorrect Confidence Score'")
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.savefig("Graphs/" + title + ".png")
    plt.show()
    print(len(uncertainty_correct))

# Graphing 44 Sample Model
# list44 = store_file_data("Classification/IBM_44_Sample_Trained_Data.csv")
# parse_file(list44, stopping_point1, stopping_point4)
# create_confidence_correlation("IBM Correlation of Untrained Confidence Scores for the 44 Sample Model")

# Graphing 67 Sample Model
# list67 = store_file_data("Classification/IBM_69_Sample_Trained_Data.csv")
# parse_file(list67, stopping_point1half, stopping_point4)
# create_confidence_correlation("IBM Correlation of Untrained Confidence Scores for the 67 Sample Model")

# Graphing 92 Sample Model
# list92 = store_file_data("Classification/IBM_92_Sample_Trained_Data.csv")
# parse_file(list92, stopping_point2, stopping_point4)
# create_confidence_correlation("IBM Correlation of Untrained Confidence Scores for the 92 Sample Model")

# Graphing 169 Sample Model
# list169 = store_file_data("Classification/IBM_Classification_Data.csv")
# parse_file(list169, start, stopping_point4)
# create_confidence_correlation("IBM Correlation of Confidence Scores for the 169 Sample Model")
