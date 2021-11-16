# This script is for training the data with IBM's API
import json
import ntpath
import requests
import sys
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


######### Create parameters required for making a call to NLU ######### 
feature_to_train = 'classifications'

headers = {}

data = {
    'name':'Classifications model #1',
    'language':'en',
    'version':'1.0.1'
}

params = {
    'version': '2021-03-25'
}

username = "apikey"
password = "ZbkyEnZCAk6_YTQPRoOdPzwcKj7DVUWggO3IFiKjk2T2"
url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f555922c-0fc4-428f-a4ec-71bd53f0cacd"
uri = url + '/v1/models/{}'.format(feature_to_train)


print('\nCreating custom model...')

training_data_filename = 'data/92_sample_data.json' # CHANGE_ME for different iterations

######### Make a call to NLU to train the model ######### 
with open(training_data_filename, 'rb') as f:
    response = requests.post(uri,
                         params=params,
                         data=data,
                         headers=headers,
                         files={'training_data': (ntpath.basename(training_data_filename), f, 'application/json')},
                         auth=(username, password),
                         verify=False,
                        )

######### Parse response from NLU ######### 
    
print('Model creation returned: ', response.status_code)

if response.status_code != 201:
    print('Failed to create model')
    print(response.text)
else:
    print('\nCustom model training started...')
    response_json = response.json()
    model_id = response_json['model_id']
    print('Custom Model ID: ', model_id)
