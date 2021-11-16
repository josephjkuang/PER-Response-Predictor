# This script is for after you retrieve the classifier and you want to send in data to be classified.
# This script will pass in some student statements to be classifed and save it to a csv.
import requests
import json
import csv

# ID's for IBM training
username = "apikey"
password = "ZbkyEnZCAk6_YTQPRoOdPzwcKj7DVUWggO3IFiKjk2T2"
url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f555922c-0fc4-428f-a4ec-71bd53f0cacd"
model_id = "d3a7e879-7331-4cfa-ae20-eb8c202507ce" # New model_id for a new set of trained data.

# Constants for the rows of certain fields in the csv file
student_id = 0
code = 12
comments = 13
statement = 14

# Stopping points for the sample data
stopping_point1 = 267 # End of our first 50 codes (44 entries in json when excluding none/other)
stopping_point1half = 341 # 85 codes (69 entries in json)
stoppint_point2 = 500 # 116 codes (92)
stoppint_point3 = 72 # 166 codes (130)
stoppint_point4 = 136 # 216 codes (169) 
unreachable = 999999

# Lists that will populate each column of the csv
student_ids = []
statements = []

# The percent value determined by the classifier that the code is this:
qual_set = []
average = []
percent_error = []
uncertainty = []

our_code = [] # The human-decided code
machine_code = [] # The machine-decided code

headers = ["ID", "Qual Set", "Average", "Percent Error", "Uncertainty", "Our Code", "Machine Code", "Statement"]

# Method that will accept a statement and make a call to the api to classify it. 
def create_request(text):
    # Format of the api request
    analyze_request_data = {
        "text": text,
        "language": "en",
        "features": {
            "classifications": {
                "model": model_id
            }
        }
    }

    # Source address for the request
    uri = url + '/v1/analyze'
    params = { 'version': '2021-02-15' }
    headers = {'Content-Type' : 'application/json'}

    ######### Make a call to NLU #########

    response = requests.post(uri,
                             params=params,
                             json=analyze_request_data,
                             headers=headers,
                             auth=(username, password),
                             verify=False,
                            )

    # This happens generally if data is not done classifying or something else very bad
    if response.status_code != 200:
        print('Failed to make request to model. Reason:')
        print(response.text)

        # Adding all 0's in case, it was just one code that failed.
        qual_set.append(0)
        average.append(0)
        percent_error.append(0)
        uncertainty.append(0)
        machine_code.append("none")
    else:
        print("Successfully analyzed request. Response from NLU:\n")

        # This is the percent values spitted back by IBM's api 
        response_json = response.json()
        output = json.dumps(response_json, indent=4, sort_keys=True)
        # print(output)

        # Using split to find the percent value classifications.
        cleaned_output = output.split("\"classifications\": [\n")
        cleaner_output = cleaned_output[1].split("]")
        seperate_output = cleaner_output[0].split("\"class_name\": \"")

        for i in range(1, 5): # Looping 4 times to get the results of each category (qual, average, error, uncertainty)
            word = seperate_output[i].split("\"")

            # Only adding to the machine code if it's the greatest percent value
            # IBM's API outputs the data with highest percent value in the first index. 
            if i == 1:
                if word[0] == our_code[-1]:
                    machine_code.append("")
                else:
                    machine_code.append(word[0])

            # Appending the scores of each category
            if word[0] == "qualset":
                score = word[3].split(":")
                cleaned_score = score[1].split("\n")
                float_score = round(float(cleaned_score[0]), 3)
                qual_set.append(float_score)
            elif word[0] == "average":
                score = word[3].split(":")
                cleaned_score = score[1].split("\n")
                float_score = round(float(cleaned_score[0]), 3)
                average.append(float_score)
            elif word[0] == "percenterror":
                score = word[3].split(":")
                cleaned_score = score[1].split("\n")
                float_score = round(float(cleaned_score[0]), 3)
                percent_error.append(float_score)
            else:
                score = word[3].split(":")
                cleaned_score = score[1].split("\n")
                float_score = round(float(cleaned_score[0]), 3)
                uncertainty.append(float_score)

# Opens the CSV Data and Stores the CSV Data as a List
# @path is the relative path to the CSV file
# @return r_list is a nested list that contains the info of the csv
def store_file_data(path):
    with open(path) as file:
        reader = csv.reader(file)
        r_list = [r for r in reader]  # convert csv file to a python list
        labels = r_list.pop(0)
    return r_list

# Method that will look through both the CSV of Data and the info returned by the Classifier
# to create the lists that will populate the columns of the saved csv file.
# @params stop is the last point in the CSV of Data that we want to examine.
def parse_file(stop):
    for row in r_list:
        student_ids.append(row[student_id])
        statements.append(row[statement])

        # This is for untrained_data so there will be no human_code already in place
        if stop == unreachable:
            our_code.append("")
            create_request(row[statement])
        else:
            word = "".join(row[code].split()).lower() # Removing whitespace and to lower case

            if word == "average" or word == "percenterror" or word == "qualset" or word == "uncertainty":
                our_code.append(word)
                create_request(row[statement]) # Making a call to get the classifier's data
            elif word == "dual":
                dual_word = "".join(row[comments].split()).lower() # Searching the comments for the code we want
                word = "Dual"

                if "average" in dual_word:
                    word += "Average"
                if "percenterror" in dual_word:
                    word += "PercentError"
                if "qualset" in dual_word:
                    word += "QualSet"
                if "uncertainty" in dual_word:
                    word += "Uncertainty"

                our_code.append(word)
                create_request(row[statement])
            elif word == "other" or word == "none":
                our_code.append(word)
                create_request(row[statement])
            else:
                print(row[student_id] + " has a bad category")
                student_ids.pop()
                statements.pop()

            # Break statement to leave the loop early if we don't want to parse the whole file
            if int(row[student_id]) == stop:
                break

# Saving the data to a csv
# @params file is the name of the file that we want to save the data to.
def save_data(file): 
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(len(student_ids)):
            # Saving each list to be a column in the csv
            writer.writerow([student_ids[i], qual_set[i], average[i], percent_error[i], uncertainty[i], our_code[i], machine_code[i], statements[i]])

# Run this to see the results of the data that were used to train the model
r_list = store_file_data('data/Data.csv')
parse_file(stopping_point2)
save_data('Classification/IBM_92_Sample_Trained_Data.csv')

# Run this to see the results of the data that wasn't used to train the model originally
# r_list = store_file_data('data/UncodedData.csv')
# parse_file(unreachable)
# save_data('IBM_Uncoded_Data.csv')
