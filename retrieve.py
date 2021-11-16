# This script is for retriving the classifier after the data is trained
import requests
import json

params = {
    'version': '2021-02-15'
}

headers = {}

username = "apikey"
password = "ZbkyEnZCAk6_YTQPRoOdPzwcKj7DVUWggO3IFiKjk2T2"
url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f555922c-0fc4-428f-a4ec-71bd53f0cacd"
model_id = "d3a7e879-7331-4cfa-ae20-eb8c202507ce" # New model_id for a new set of trained data.

uri = url + '/v1/models/classifications/' + model_id

######### Make a call to NLU ######### 

response = requests.get(uri, auth=(username, password), params=params, verify=False, headers=headers)

######### Parse response from NLU ######### 

print('\033[1m'+ '\033[4m' + 'Response from NLU:' + '\033[4m' + '\033[0m')

print('\nStatus: ', response.status_code)

response_json = response.json()
print("Response body:", json.dumps(response_json, indent=4, sort_keys=True), )
