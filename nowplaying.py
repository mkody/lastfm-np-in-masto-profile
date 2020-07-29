# Based on https://github.com/hugovk/lastfm-tools/blob/master/nowplaying.py
import os
import time
import pylast

from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()
SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".lastfm_session_key")

mastodon = Mastodon(
    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
    api_base_url=os.getenv('MASTODON_HOST')
)

network = pylast.LastFMNetwork(os.getenv('LASTFM_KEY'), os.getenv('LASTFM_SECRET'))

if not os.path.exists(SESSION_KEY_FILE):
    skg = pylast.SessionKeyGenerator(network)
    url = skg.get_web_auth_url()

    print(f"Please authorize the scrobbler to scrobble to your account: {url}\n")
    import webbrowser

    webbrowser.open(url)

    while True:
        try:
            session_key = skg.get_web_auth_session_key(url)
            fp = open(SESSION_KEY_FILE, "w")
            fp.write(session_key)
            fp.close()
            break
        except pylast.WSError:
            time.sleep(1)
else:
    session_key = open(SESSION_KEY_FILE).read()

network.session_key = session_key
user = network.get_user(os.getenv('LASTFM_USER'))
print("Tuned in to %s" % os.getenv('LASTFM_USER'))
print('---')

playing_track = '~'

while True:
    try:
        new_track = user.get_now_playing()
        if new_track != playing_track:
            playing_track = new_track

            fields = mastodon.account_verify_credentials()['source']['fields']
            new_fields = []

            for f in fields:
                if (f['name'] == 'Now Playing' or f['name'] == os.getenv('MASTODON_NOTPLAYING_NAME')):
                    if playing_track is None:
                        f['name'] = os.getenv('MASTODON_NOTPLAYING_NAME')
                        f['value'] = os.getenv('MASTODON_NOTPLAYING_VALUE')
                    else:
                        f['name'] = 'Now Playing'
                        f['value'] = str(playing_track)

                new_fields.append([f['name'], f['value']])

            print(new_fields)
            mastodon.account_update_credentials(fields=new_fields)
    except Exception as e:
        print("Error: %s" % repr(e))

    time.sleep(15)
