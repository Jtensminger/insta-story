from instagram_private_api import Client, ClientCompatPatch
import json
import codecs
import os.path
import argparse
import datetime

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object




settings_file_path = "./test_credentials.json"





        settings_file = args.settings_file_path


#api = Client(user_name, password, auth_app_api['cookie'], auth_app_api['device_id'])
api = Client(user_name, password, settings=auth_app_api_json)
#results = api.reals_media()

user_id = api.authenticated_user_id()
user_name_api = api.authenticated_user_name()


print("user_id")
print(user_id)
print("user_name")
print(user_name_api)
items = [item for item in results.get('feed_items', [])
         if item.get('media_or_ad')]
for item in items:
    # Manually patch the entity to match the public api as closely as possible, optional
    # To automatically patch entities, initialise the Client with auto_patch=True
    ClientCompatPatch.media(item['media_or_ad'])
    print(item['media_or_ad']['code'])
