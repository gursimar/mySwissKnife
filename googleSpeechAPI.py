#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Google Cloud Speech API sample application using the REST API for batch
processing."""

# [START import_libraries]
import pandas as pd
import argparse
import base64
import json
import glob
import os

#-*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Code re-used from https://github.com/zszyellow/WER-in-python
'''

import sys
import numpy

from googleapiclient import discovery
import httplib2
from oauth2client.client import GoogleCredentials
# [END import_libraries]


# [START authenticating]
DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'
                 'version={apiVersion}')


# Application default credentials provided by env variable
# GOOGLE_APPLICATION_CREDENTIALS
def get_speech_service():
    credentials = GoogleCredentials.get_application_default().create_scoped(
        ['https://www.googleapis.com/auth/cloud-platform'])
    http = httplib2.Http()
    credentials.authorize(http)

    return discovery.build(
        'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)
# [END authenticating]


def main(speech_file):
    """Transcribe the given audio file.

    Args:
        speech_file: the name of the audio file.
    """
    # [START construct_request]
    with open(speech_file, 'rb') as speech:
        # Base64 encode the binary audio file for inclusion in the JSON
        # request.
        speech_content = base64.b64encode(speech.read())

    service = get_speech_service()
    service_request = service.speech().syncrecognize(
        body={
            'config': {
                # There are a bunch of config options you can specify. See
                # https://goo.gl/KPZn97 for the full list.
                #'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                'encoding': 'FLAC',  # raw 16-bit signed LE samples
                'sampleRate': 16000,  # 16 khz
                # See http://g.co/cloud/speech/docs/languages for a list of
                # supported languages.
                'languageCode': 'en-US',  # a BCP-47 language tag
                #'languageCode': 'en-IN',  # a BCP-47 language tag
            },
            'audio': {
                'content': speech_content.decode('UTF-8')
                }
            })
    # [END construct_request]
    # [START send_request]
    response = service_request.execute()
    print(json.dumps(response))
    return json.dumps(response)
    # [END send_request]

# [START run_application]
# SET GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Gursimar\repos\python-docs-samples\speech\api-client\simar-ae38c669c730.json
# echo %GOOGLE_APPLICATION_CREDENTIALS%
# sox file.abc --channels=1 --bits=16 --rate=16000 --endian=little audio.flac

if __name__ == '__main__':
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Gursimar\\repos\\python-docs-samples\\speech\\api-client\\simar-ae38c669c730.json"
    #folder = 'data/videos'
    folder = 'data/samplesall'
    os.chdir(folder)
    files = []
    results = []
    for file in glob.glob("*.flac"):
        print(file)
        try:
            result = main(file)
        except Exception as exception:
            result = repr(exception)
        print result
        files.append(file)
        results.append(result)
        print 'DONE'
    ds = pd.DataFrame(data = {'Files': files, 'Trans':results})
    ds.to_csv('results.csv')
    print'-----DONE ALL-----'