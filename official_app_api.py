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

auth_app_api = {
'device_id': 'android-e7c1756d44bc11ea',
'cookie': {
"__class__": "bytes",
 "__value__": 'gAN9cQBYDgAAAC5pbnN0YWdyYW0uY29tcQF9cQJYAQAAAC9xA31xBChYCgAAAGRzX3VzZXJfaWRx\nBWNodHRwLmNvb2tpZWphcgpDb29raWUKcQYpgXEHfXEIKFgOAAAAcGF0aF9zcGVjaWZpZWRxCYhY\nBwAAAHZlcnNpb25xCksAWAQAAABuYW1lcQtoBVgLAAAAY29tbWVudF91cmxxDE5YBAAAAHBhdGhx\nDWgDWBAAAABkb21haW5fc3BlY2lmaWVkcQ6IWAYAAABzZWN1cmVxD4hYDgAAAHBvcnRfc3BlY2lm\naWVkcRCJWAUAAAB2YWx1ZXERWAsAAAAyNDg2MjI1MDg2OXESWAUAAABfcmVzdHETfXEUWBIAAABk\nb21haW5faW5pdGlhbF9kb3RxFYhYBgAAAGRvbWFpbnEWWA4AAAAuaW5zdGFncmFtLmNvbXEXWAcA\nAABleHBpcmVzcRhK+cKrXlgHAAAAZGlzY2FyZHEZiVgHAAAAcmZjMjEwOXEaiVgEAAAAcG9ydHEb\nTlgHAAAAY29tbWVudHEcTnViWAkAAABjc3JmdG9rZW5xHWgGKYFxHn1xHyhoCYhoCksAaAtYCQAA\nAGNzcmZ0b2tlbnEgaAxOaA1oA2gOiGgPiGgQiWgRWCAAAABxSUs1VUNqYTA0NU5QbGRHR21QclQ5\nRWRpeHo2MmljQ3EhaBN9cSJoFYhoFlgOAAAALmluc3RhZ3JhbS5jb21xI2gYSvn9FGBoGYloGolo\nG05oHE51YlgDAAAAcnVycSRoBimBcSV9cSYoaAmIaApLAGgLWAMAAABydXJxJ2gMTmgNaANoDoho\nD4hoEIloEVgDAAAAQVROcShoE31xKVgIAAAASHR0cE9ubHlxKk5zaBWIaBZYDgAAAC5pbnN0YWdy\nYW0uY29tcStoGE5oGYhoGoloG05oHE51YlgJAAAAc2Vzc2lvbmlkcSxoBimBcS19cS4oaAmIaApL\nAGgLaCxoDE5oDWgDaA6IaA+IaBCJaBFYIQAAADI0ODYyMjUwODY5JTNBRzVPZlBacERSN3FhZnIl\nM0ExOHEvaBN9cTBYCAAAAEh0dHBPbmx5cTFOc2gViGgWWA4AAAAuaW5zdGFncmFtLmNvbXEyaBhK\neU8WYGgZiWgaiWgbTmgcTnViWAUAAABzaGJ0c3EzaAYpgXE0fXE1KGgJiGgKSwBoC2gzaAxOaA1o\nA2gOiGgPiGgQiWgRWBIAAAAxNTgwNTM4ODczLjI1MzQyMTVxNmgTfXE3WAgAAABIdHRwT25seXE4\nTnNoFYhoFlgOAAAALmluc3RhZ3JhbS5jb21xOWgYSnlWPl5oGYloGoloG05oHE51YlgDAAAAbWlk\ncTpoBimBcTt9cTwoaAmIaApLAGgLaDpoDE5oDWgDaA6IaA+IaBCJaBFYHAAAAFhqVWItQUFCQUFI\nekN3WEo1M2FSYmR3dGJIRl9xPWgTfXE+aBWIaBZYDgAAAC5pbnN0YWdyYW0uY29tcT9oGEr4HgFx\naBmJaBqJaBtOaBxOdWJYBwAAAGRzX3VzZXJxQGgGKYFxQX1xQihoCYhoCksAaAtoQGgMTmgNaANo\nDohoD4hoEIloEVgUAAAAY29sbGVjdGl2ZWx5cmF0aW9uYWxxQ2gTfXFEWAgAAABIdHRwT25seXFF\nTnNoFYhoFlgOAAAALmluc3RhZ3JhbS5jb21xRmgYSvnCq15oGYloGoloG05oHE51YlgFAAAAc2hi\naWRxR2gGKYFxSH1xSShoCYhoCksAaAtoR2gMTmgNaANoDohoD4hoEIloEVgFAAAAMTc0MjRxSmgT\nfXFLWAgAAABIdHRwT25seXFMTnNoFYhoFlgOAAAALmluc3RhZ3JhbS5jb21xTWgYSnlWPl5oGYlo\nGoloG05oHE51YnVzcy4=\n"}, "ad_id": "09a7748d-2f17-a19c-fc14-2a453bd76198'
},
'created_ts':1580538873,
'uuid': 'e7c1756c-44bc-11ea-a427-2016d8b686de',
'session_id': 'e7c1756e-44bc-11ea-a427-2016d8b686de'
}


settings_file_path = "./test_credentials.json"





        settings_file = args.settings_file_path

user_name = 'collectivelyrational'
password = 'Leeko#1521'

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
