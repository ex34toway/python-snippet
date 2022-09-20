# -*- coding: utf-8 -*-

# This simple app uses the '/translate' resource to translate text from
# one language to another.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

import os, requests, uuid, json


subscription_key = '2aac9c6a5a06453a850be1d8a0a47852'

endpoint = 'https://api.cognitive.microsofttranslator.com'

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
path = '/translate?api-version=3.0'
params = '&from=en&to=zh-CN&to=it'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.
body = [{
    'text' : 'PostgreSQL can devise query plans which can leverage multiple CPUs in order to answer queries faster. '
}]
request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

print(response[0]['translations'][0]['text'])