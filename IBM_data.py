# Class that will take in a CSV of training data and convert it into a json.
# Each entry of the json will correspond to a single response
# They will generally have one label being its code (sometimes 2 if its a dual code)

import csv
import json

data = []

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

# Opens the CSV Data and Stores the CSV Data as a List
# @path is the relative path to the CSV file
# @return r_list is a nested list that contains the info of the csv
def store_file_data(path):
	with open(path) as file:
		reader = csv.reader(file)
		r_list = [r for r in reader]  # convert csv file to a python list
		labels = r_list.pop(0)
	return r_list

# Method that will parse through the r_list and 
def parse_file(stop):
	for row in r_list:
		word = "".join(row[code].split()).lower() # Removing whitespace and making lower case

		if word == "average" or word == "percenterror" or word == "qualset" or word == "uncertainty":
			append_data(row[statement], word, int(row[student_id])) # Making a call to add the entry to the data
		elif word == "dual":
			dual_word = "".join(row[comments].split()).lower() # Searching the comments for the code we want
			words = []

			if "average" in dual_word:
				words.append("average")
			if "percenterror" in dual_word:
				words.append("percenterror")
			if "qualset" in dual_word:
				words.append("qualset")
			if "uncertainty" in dual_word:
				words.append("uncertainty")

			# Adding the dual code to the data if we find the right two codes in the comments
			if len(words) == 2:
				data.append({
					"text" : row[statement],
					"labels" : words
					})
		elif word == "other" or word == "none":
			continue
		else:
			# We should never get here
			print(row[student_id] + " has a bad category")

		# Break statement to leave the loop early if we don't want to parse the whole file
		if int(row[student_id]) == stop:
			break

# Helper method that will add the student statment to the JSON
# @params content is a string with the student statement
# @params category is a list with the assigned code(s)
# @params id is no longer used
def append_data(content, category, id):
	data.append({
		"text" : content,
		"labels" : [category]
		})

# Method that saves the data into the json
# @params file the name of the file that we want to save our data to.
def save_json(file):
	with open("data/" + file, 'w', encoding='utf-8') as outfile:
		json.dump(data, outfile, indent=4)


# Method calls below that will create five different jsons based off the stopping points.
r_list = store_file_data('data/Data.csv')

parse_file(stopping_point1)
save_json(str(len(data)) + '_sample_data.json')
data.clear()

parse_file(stopping_point1half)
save_json(str(len(data)) + '_sample_data.json')
data.clear()

parse_file(stoppint_point2)
save_json(str(len(data)) + '_sample_data.json')
data.clear()

parse_file(stoppint_point3)
save_json(str(len(data)) + '_sample_data.json')
data.clear()

parse_file(stoppint_point4)
save_json(str(len(data)) + '_sample_data.json')
data.clear()
