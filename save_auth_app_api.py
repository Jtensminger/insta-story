import json
import codecs
import datetime
import os.path
import logging
import argparse
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError, ClientCompatPatch,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='login callback and save settings demo')
    parser.add_argument('-settings', '--settings', dest='settings_file_path', type=str, required=True)
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(client_version))

    device_id = None
    try:

        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print('Unable to find file: {0!s}'.format(settings_file))

            # login new
            api = Client(
                args.username, args.password,
                on_login=lambda x: onlogin_callback(x, args.settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print('Reusing settings: {0!s}'.format(settings_file))

            device_id = cached_settings.get('device_id')
            # reuse auth settings
            api = Client(
                args.username, args.password,
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            args.username, args.password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(9)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(99)

    # Show when login expires
    cookie_expiry = api.cookie_jar.auth_expires
    print('Cookie Expiry: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%dT%H:%M:%SZ')))

    airtable_id = 'appBbhGoVwwockVVP'
    account_que = ['1697296', '6867616399', '359090248', '10206720', '268071795', '4136433602', '434820235', '1911166915', '182528637', '26490008', '8663171404']
    for account in account_que:
        # Call the api
        results = api.user_reel_media(account)

        if str(results['latest_reel_media']) == 'None':
            print('No stories')
            continue

        items = results['items']
        stories = []
        for item in items:
            story_raw = ClientCompatPatch.media(item)
            story = {
                'story_feed_media': story_raw.get('story_feed_media'),
                'story_questions': story_raw.get('story_questions'),
                'story_countdowns': story_raw.get('story_countdowns'),
                'story_hashtags': story_raw.get('story_hashtags'),
                'story_voter_registration_stickers': story_raw.get('story_voter_registration_stickers'),
                'story_polls': story_raw.get('story_polls'),
                'is_dash_eligible': story_raw.get('is_dash_eligible'),
                'ad_action': story_raw.get('ad_action'),
                'story_cta': story_raw.get('story_cta'),
                'link_text': story_raw.get('link_text'),
                'imported_taken_at': story_raw.get('imported_taken_at'),
                'user': story_raw.get('user'),
                'number_of_qualities': story_raw.get('number_of_qualities'),
                'has_audio': story_raw.get('has_audio'),
                'video_dash_manifest': story_raw.get('video_dash_manifest'),
                'video_codec': story_raw.get('video_codec'),
                'video_versions': story_raw.get('video_versions'),
                'video_duration': story_raw.get('video_d,uration'),
                'videos': story_raw.get('videos'),
                'is_reel_media': story_raw.get('is_reel_media'),
                'expiring_at': story_raw.get('expiring_at'),
                'original_width': story_raw.get('original_width'),
                'original_height': story_raw.get('original_height'),
                'code': story_raw.get('code'),
                'reel_mentions': story_raw.get('reel_mentions'),
                'story_sliders': story_raw.get('story_sliders'),
                'device_timestamp': story_raw.get('device_timestamp'),
                'type': story_raw.get('type'),
                'creative_config': story_raw.get('creative_config'),
                'original_height': story_raw.get('original_height'),
                'can_reshare': story_raw.get('can_reshare'),
                'created_time': story_raw.get('created_time'),
                'organic_tracking_token': story_raw.get('organic_tracking_token'),
                'tags': story_raw.get('tags'),
                'filter_type': story_raw.get('filter_type'),
                'can_viewer_save': story_raw.get('can_viewer_save'),
                'caption_position': story_raw.get('caption_position'),
                'client_cache_key': story_raw.get('client_cache_key'),
                'show_one_tap_fb_share_tooltip': story_raw.get('show_one_tap_fb_share_tooltip'),
                'can_send_custom_emojis': story_raw.get('can_send_custom_emojis'),
                'filter': story_raw.get('filter'),
                'supports_reel_reactions': story_raw.get('supports_reel_reactions'),
                'users_in_photo': story_raw.get('users_in_photo'),
                'location': story_raw.get('location'),
                'story_app_attribution': story_raw.get('story_app_attribution'),
                'image_versions2': story_raw.get('image_versions2'),
                'likes': story_raw.get('likes'),
                'can_reply': story_raw.get('can_reply'),
                'id': story_raw.get('id'),
                'comments': story_raw.get('comments'),
                'images': story_raw.get('images'),
                'low_resolution': story_raw.get('low_resolution'),
                'standard_resolution': story_raw.get('standard_resolution'),
                'caption_is_edited': story_raw.get('caption_is_edited'),
                'link': story_raw.get('link'),
                'taken_at': story_raw.get('taken_at'),
                'user': story_raw.get('user'),
            }

            story_sliders = story['story_sliders']
            story_owner_id = story['user']['id']
            story_owner_full_name = story['user']['full_name']
            story_owner_username = story['user']['username']
            story_owner_is_verified = story['user']['is_verified']
            ad_action = story['ad_action']
            story_cta = story['story_cta']
            link_text = story['link_text']
            story_feed_media = story['story_feed_media']
            story_questions = story['story_questions']
            story_polls = story['story_polls']
            story_countdowns = story['story_countdowns']
            story_hashtags = story['story_hashtags']
            imported_taken_at = story['imported_taken_at']
            has_audio = story['has_audio']

            video_duration = story['video_duration']
            if story['video_versions']:
                original_video_url = story['video_versions'][0]['url']
            else:
                original_video_url = ''
            story_voter_registration_stickers = story['story_voter_registration_stickers']
            original_image_url = story['image_versions2']['candidates'][0]['url']
            creative_config = story['creative_config']
            type = story['type']
            original_width = story['original_width']
            original_height = story['original_height']
            story_tags = story['tags']
            story_filter_type_code = story['filter_type']
            filter = story['filter']
            caption_position = story['caption_position']
            created_time = story['created_time']
            users_in_photo = story['users_in_photo']
            location = story['location']

            if story['story_app_attribution'] == True:
                story_app_attribution = {
                    'id': story['story_app_attribution']['id'],
                    'name': story['story_app_attribution']['name'],
                    'app_action_text': story['story_app_attribution']['app_action_text'],
                    'app_icon_url': story['story_app_attribution']['app_icon_url'],
                    'link': story['story_app_attribution']['link'],
                    'content_url': story['story_app_attribution']['content_url'],
                }

            reel_mentions = []
            if story['reel_mentions'] == True:
                for mention in story['reel_mentions']:
                    reel_mentions.push({
                        'display_type': mention['display_type'],
                        'height': mention['height'],
                        'is_fb_sticker': mention['is_fb_sticker'],
                        'is_hidden': mention['is_hidden'],
                        'is_pinned': mention['is_pinned'],
                        'is_sticker': mention['is_sticker'],
                        'rotation': mention['rotation'],
                        'user': mention['user'],
                        'width': mention['width'],
                        'x': mention['x'],
                        'y': mention['y'],
                        'z': mention['y']
                    })

            id = story['id']
            taken_at = story['taken_at']


            #for item in items:
                # Manually patch the entity to match the public api as closely as possible, optional
                # To automatically patch entities, initialise the Client with auto_patch=True
                #ClientCompatPatch.media(item['media_or_ad'])
                #print(item['media_or_ad']['code'])
                #print(ClientCompatPatch.media(item))
            #assert len(results.get('items', [])) > 0
            stories.append(story)
            #print('All ok')
        records = []
        for story in stories:
            story['created_time']

            image_asset = {
                'url': story['image_versions2']['candidates'][0]['url'],
                'width': story['image_versions2']['candidates'][0]['width'],
                'height': story['image_versions2']['candidates'][0]['height']
            }

            if story['video_versions']:
                original_video_url = story['video_versions'][0]['url']
            else:
                original_video_url = ''

            video_asset = {
                'url': original_video_url
            }

            story_cta_blob = story['story_cta']

            if str(story['story_cta']) != 'None':
                story_cta_uri = story['story_cta'][0]['links'][0]['webUri']
            else:
                story_cta_uri = ''


            question_blob = story['story_questions']
            if str(story['story_questions']) != 'None':
                question_text = story['story_questions'][0]['question_sticker']['question']

            else:
                question_text = ''

            creative_config_blob = story['creative_config']

            polls_blob = story['story_polls']

            if str(story['story_polls']) != 'None':
                polls_is_shared_result = story['story_polls'][0]['poll_sticker']['is_shared_result']
                polls_finished = story['story_polls'][0]['poll_sticker']['finished']
                polls_question = story['story_polls'][0]['poll_sticker']['question']
                polls_tallies = story['story_polls'][0]['poll_sticker']['tallies']

            else:
                poll_is_shared_result = ''
                polls_finished = ''
                polls_question = ''
                polls_tallies = ''

            countdowns_blob = story['story_countdowns']
            if str(story['story_countdowns']) != 'None':
                countdown_end_time = story['story_countdowns'][0]['countdown_sticker']['end_ts']
                countdown_text = story['story_countdowns'][0]['countdown_sticker']['text']
            else:
                countdown_end_time = ''
                countdown_text = ''
            hashtags_blob = story['story_hashtags']
            if str(story['story_hashtags']) != 'None':
                hashtag_name = story['story_hashtags'][0]['hashtag']['name']
            else:
                hashtag_name = ''

            voter_registration_blob = story['story_voter_registration_stickers']



            location_blob = story['location']
            if str(story['location']) != 'None':
                location_name = story['location']['name']
                location_coordinates = [story['location']['lat'], story['location']['lng']]
            else:

                location_name = ''
                location_coordinates = ''


            reel_mentions_blob = story['reel_mentions']
            records.append({
                'fields': {
                    'story_id': story['id'],
                    'owner_id': story['user']['id'],
                    'image_asset': [image_asset['url']],
                    'created_time': story['created_time'],
                    'story_cta_blob': story_cta_blob,
                    'has_audio': story['has_audio'],
                    'username':  story['user']['username'],
                    'fullname': story['user']['full_name'],
                    'slider_sticker': story['story_sliders'],
                    'story_feed_media': story['story_feed_media'],
                    'video_duration': story['video_duration'],
                    'story_type': story['type'],
                    'video_asset': [video_asset['url']],
                    'taked_at': story['taken_at'],
                    'ad_action': story['ad_action'],
                    'story_cta_uri': story_cta_uri,
                    'link_text': story['link_text'],
                    'question_blob': question_blob,
                    'question_text': question_text,
                    'creative_config_blob': creative_config_blob,
                    'poll_blob': polls_blob,
                    'polls_is_shared_result': poll_is_shared_result,
                    'polls_finished': polls_finished,
                    'polls_question': polls_question,
                    'polls_tallies': polls_tallies,
                    'countdown_blob': countdowns_blob,
                    'countdown_end_time': countdown_end_time,
                    'countdown_text': countdown_text,
                    'hashtags_blob': hashtags_blob,
                    'hashtag_name': hashtag_name,
                    'voter_registration_blob': voter_registration_blob,
                    'filter': story['filter'],
                    'number_of_qualitities': story['number_of_qualities'],
                    'expiring_at': story['expiring_at'],
                    'location_blob': location_blob,
                    'location_name': location_name,
                    'location_coordinates': location_coordinates,
                    'reel_mentions_blob': reel_mentions_blob
                }})


# api-endpoint
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


que = list(chunks(records, 10))
pp.pprint(records)
pp.pprint('it begins')
for record_list in que:
    pp.pprint(len(record_list))

api_key = "keyiHeRvc2XH57s2N"
API_ENDPOINT = 'https://api.airtable.com/v0/appBbhGoVwwockVVP/story_table?api_key=keyiHeRvc2XH57s2N'

if len(records) == 1:
    data = {
        "records": records
    }
else:
    data = {
        records[0]
    }


# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = {"fields": {'story_id': '121123123'}})

pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)
