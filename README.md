# PER-Response-Predictor
UIUC PER Machine Learning Code that will predict the type of response given by a student

## Purpose
The purpose of this project was to see if we could use IBM's Machine Learning API Label Classifer (https://cloud.ibm.com/apidocs/machine-learning-cp) to categorize student responses into different categories, dependent on their solving methodology. This way in the future, we may be able to see what techniques students prefer in a whole myriad of ways.

## Results
The classifier begins to become accurate when only about 100 responses were loaded in. Of course, the results would become more accurate as we provided more training data, but a reasonable stopping point would be around 100 responses. 

## Details 
- IBM_data.py : Class that will take in a CSV of training data and convert it into a json.
- trainer.py : Script for training the data with IBM's API
- retrieve.py : Script for retriving the classifier after the data is trained
- using_model.py :  Script for after you retrieve the classifier and you want to send in data to be classified.
- scatter.py : Script that will graph the classification data
- Data : Folder that contains the sample data
- Classification : Folder that contains the results of the classification
- Graphs : Folder that contains the different scatter plots representing the results
